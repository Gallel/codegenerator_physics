import re
import json
import logging
from pathlib import Path
from collections import namedtuple
from typing import Dict, Set

from owlready2 import sync_reasoner_pellet, Thing, World, AllDifferent

from src.settings import (
    OUTPUT_DIR, PROGRAM_OWL, PHYSICS_DOMAIN_OWL,
    MATH_OWL, PROGRAM_TRACE_OWL, PHYSICS_BRIDGE_OWL, PHYSICS_RULES_OWL,
)
from src.utils import load_ontology

log = logging.getLogger(__name__)

DummyInst = namedtuple("DummyInst", ["name"])

def strip_owl_prefix(instName):
    prefixes = ["phys_", "Res_", "mission_", "Measurement_"]
    for p in prefixes:
        if instName.startswith(p):
            candidate = instName[len(p):]
            candidate = re.sub(r'_\d+$', '', candidate)
            return candidate
    return instName

def _get_label_or_name(entity):
    if entity is None: return "<?>"
    try:
        if hasattr(entity, "label") and entity.label: return str(entity.label[0])
    except Exception as e:
        log.debug("Could not read label of %r: %s", entity, e)
    return str(getattr(entity, "name", repr(entity)))

def summarize_instance_properties(inst):
    try:
        props = list(inst.get_properties())
    except Exception as e:
        log.debug("Could not list properties of %r: %s", inst, e)
        return ""
    parts = []
    for prop in props:
        pname = getattr(prop, "python_name", prop.name)
        if pname in ("hasQuantityType", "hasUnit"):
            labels = [_get_label_or_name(v) for v in (prop[inst] or [])]
            if labels: parts.append(pname.replace("has", "") + " = " + ", ".join(labels))
    return "; ".join(parts)

def _friendly_error_label(label):
    if "QuantityIncompatibility" in label:
        return "Choque de Magnitudes"
    if "UnitIncompatibility" in label:
        return "Choque de Unidades"
    if "InvalidTrigonometry" in label:
        return "Error en función trigonométrica"
    if "DimensionMismatch" in label:
        return "Error de Dimensionamiento"
    return "Error Detectado"


def describe_error(label, inst):
    var = strip_owl_prefix(inst.name)

    # Quantity/unit clash: "no puedes sumar fuerza con tiempo".
    if "Incompatibility" in label:
        try:
            l = inst.hasLeftOperand[0]
            r = inst.hasRightOperand[0]
            qL = l.hasQuantityType[0].name if l.hasQuantityType else "algo sin tipo"
            qR = r.hasQuantityType[0].name if r.hasQuantityType else "algo sin tipo"
            return ("En '" + str(var) + "' se mezclan magnitudes que no encajan: "
                    + qL + " con " + qR + ". No se pueden operar entre sí.")
        except Exception as e:
            log.debug("No pude leer los operandos de %s: %s", inst.name, e)
        return "En '" + str(var) + "' se mezclan magnitudes incompatibles."

    # Trig of a non-angle.
    if "Trigonometry" in label:
        found = "una magnitud que no es un ángulo"
        try:
            if getattr(inst, "hasOperand", None):
                op = inst.hasOperand[0]
                if op.hasQuantityType:
                    found = op.hasQuantityType[0].name
        except Exception as e:
            log.debug("No pude leer el operando trig de %s: %s", inst.name, e)
        return ("En '" + str(var) + "' se aplica una función trigonométrica a "
                + found + ", pero su argumento debería ser un ángulo.")

    if "DimensionMismatch" in label:
        # If it is a power of a length, the exponent is almost always the bug
        # (e.g. raising a length to 4 instead of squaring it). Give a concrete,
        # generic hint without naming any specific formula.
        try:
            exp = inst.hasRightOperand[0]
            expVal = exp.hasNumericValue[0] if exp.hasNumericValue else None
            base = inst.hasLeftOperand[0]
            baseQty = base.hasQuantityType[0].name if base.hasQuantityType else ""
            if "Length" in baseQty:
                return ("En '" + str(var) + "' se eleva una longitud al exponente "
                        + str(expVal) + ", lo que no produce una magnitud física conocida. "
                        "Una longitud al cuadrado da un área y al cubo un volumen; "
                        "revisa el exponente (no confundas un divisor de la fórmula con la potencia).")
        except Exception as e:
            log.debug("No pude leer la potencia de %s: %s", inst.name, e)
        return "En '" + str(var) + "' las dimensiones de la operación no cuadran."

    return "Se detectó un problema físico en '" + str(var) + "'."

_KINEMATIC_PATTERNS = [
    ("LengthQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)", "Velocidad constante (v = d/t)"),
    ("VelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AccelerationQuantity)", "Aceleración media (a = v/t)"),
]

_DYNAMIC_PATTERNS = [
    ("MassQuantity), hasQuantityType(?a, AccelerationQuantity) -> hasQuantityType(?res, ForceQuantity)", "Segunda Ley de Newton (F = m*a)"),
    ("ForceQuantity), hasQuantityType(?d, LengthQuantity) -> hasQuantityType(?res, EnergyQuantity)", "Trabajo Mecánico (W = F*d)"),
    ("MassQuantity), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, MomentumQuantity)", "Momenta Lineal (p = m*v)"),
]

_FLUID_PATTERNS = [
    ("LengthQuantity), hasQuantityType(?l2, LengthQuantity) -> hasQuantityType(?res, AreaQuantity)", "Área (A = L * L)"),
    ("AreaQuantity), hasQuantityType(?l, LengthQuantity) -> hasQuantityType(?res, VolumeQuantity)", "Volumen (V = A * L)"),
    ("MassQuantity), hasQuantityType(?v, VolumeQuantity) -> hasQuantityType(?res, DensityQuantity)", "Densidad (rho = m / V)"),
    ("ForceQuantity), hasQuantityType(?a, AreaQuantity) -> hasQuantityType(?res, PressureQuantity)", "Presión (P = F / A)"),
]


def get_formula_description(ruleText):
    clean = re.sub(r'[^\s\(\?,]*[#\.]', '', ruleText)

    # arithmetic sum/sub (both share the same antecedent shape)
    if "AdditionExpression(?e)" in clean and "hasQuantityType(?l, ?q), hasQuantityType(?r, ?q)" in clean:
        return "Suma de Magnitudes Homogéneas"
    if "SubtractionExpression(?e)" in clean and "hasQuantityType(?l, ?q), hasQuantityType(?r, ?q)" in clean:
        return "Resta de Magnitudes Homogéneas"

    # trig / log: just look at the head class
    if "SineExpression(?e)" in clean: return "Relación Trigonométrica (Seno)"
    if "LogarithmExpression(?e)" in clean: return "Función Logarítmica"
    if "NaturalLogarithmExpression(?e)" in clean: return "Logaritmo Natural"

    # error rule
    if "QuantityIncompatibilityError" in clean and "DifferentFrom" in clean:
        return "Validación Semántica: Bloqueo de suma/resta heterogénea"

    # physical inferences (kinematic, dynamic, fluids)
    for pattern, desc in _KINEMATIC_PATTERNS + _DYNAMIC_PATTERNS + _FLUID_PATTERNS:
        if pattern in clean:
            return desc

    # fallback when none of the above hits
    if "LengthQuantity)" in clean and "VelocityQuantity)" in clean:
        return "Cálculo Cinemático de Velocidad"
    return "Inferencia Física Estándar (" + clean[:40] + "...)"

def check_manual_compatibility(world, errors):
    AddExprCls = world.search_one(iri="*#AdditionExpression")
    SubExprCls = world.search_one(iri="*#SubtractionExpression")
    for opCls in [AddExprCls, SubExprCls]:
        if not opCls: continue
        for inst in opCls.instances():
            try:
                l = inst.hasLeftOperand[0]
                r = inst.hasRightOperand[0]
                ql = l.hasQuantityType[0]
                qr = r.hasQuantityType[0]
                if ql != qr:
                    IncompCls = world.search_one(iri="*#QuantityIncompatibilityError")
                    if IncompCls:
                        errors.append(("QuantityIncompatibilityError", inst))
                        print("[INFO] Quantity incompatibility in " + inst.name + ": " + ql.name + " != " + qr.name)
                try:
                    ul = l.hasUnit[0]
                    ur = r.hasUnit[0]
                    if ul != ur:
                        UnitIncompCls = world.search_one(iri="*#UnitIncompatibilityError")
                        if UnitIncompCls:
                             errors.append(("UnitIncompatibilityError", inst))
                             print("[INFO] Unit incompatibility in " + inst.name + ": " + ul.name + " != " + ur.name)
                except Exception as e:
                    log.debug("No unit info for %s: %s", inst.name, e)
            except Exception as e:
                log.debug("Skipped %s during compatibility check: %s", getattr(inst, "name", inst), e)

def check_manual_trigonometry(world, errors):
    TrigClasses = [
        world.search_one(iri="*#SineExpression"),
        world.search_one(iri="*#CosineExpression"),
        world.search_one(iri="*#TangentExpression"),
    ]
    AngleQty = world.search_one(iri="*#AngleQuantity")
    TrigErrCls = world.search_one(iri="*#InvalidTrigonometryArgumentError")
    for trigCls in TrigClasses:
        if not trigCls: continue
        for inst in trigCls.instances():
            try:
                op = inst.hasOperand[0]
                q = op.hasQuantityType[0]
                if AngleQty is not None and q != AngleQty and TrigErrCls is not None:
                    errors.append(("InvalidTrigonometryArgumentError", inst))
                    print("[INFO] Invalid trig arg in " + inst.name + ": " + q.name + " is not AngleQuantity")
            except Exception as e:
                log.debug("Skipped %s during trig check: %s", getattr(inst, "name", inst), e)

def check_invalid_power(world, errors):
    """Flag Length raised to a power that is not a recognized physical magnitude.

    The dimension propagator only types Length^2 -> Area and Length^3 -> Volume.
    A bare Length^4 (e.g. confusing the '4' of pi*d^2/4 with the exponent) leaves
    the result untyped, so downstream rules never fire and the error slips through
    silently. Here we catch any Length base with an integer exponent other than
    2 or 3 (or a non-integer / non-positive exponent) as a dimension mismatch, so
    the self-correction loop regenerates. Generic: no problem-specific values.
    """
    PowExprCls = world.search_one(iri="*#PowerExpression")
    LengthQ = world.search_one(iri="*#LengthQuantity")
    DimErrCls = world.search_one(iri="*#DimensionMismatchError")
    if PowExprCls is None or LengthQ is None or DimErrCls is None:
        return
    for inst in PowExprCls.instances():
        try:
            base = inst.hasLeftOperand[0]
            exp = inst.hasRightOperand[0]
            baseQty = base.hasQuantityType[0]
        except Exception:
            continue
        if baseQty != LengthQ:
            continue
        expVal = None
        try:
            expVal = exp.hasNumericValue[0]
        except Exception:
            pass
        bad = False
        if expVal is None:
            bad = True
        else:
            try:
                n = int(expVal)
                if n != expVal or n not in (2, 3):
                    bad = True
            except (TypeError, ValueError):
                bad = True
        if bad:
            errors.append(("DimensionMismatchError", inst))
            print("[INFO] Invalid Length power in " + inst.name +
                  ": exponent " + str(expVal) + " does not yield a known magnitude.")


def extract_physics_errors_from_reasoner(world, errors):
    try:
        PhysicsErrorCls = world.search_one(iri="*#PhysicsError")
        if PhysicsErrorCls:
            for cls in [PhysicsErrorCls] + list(PhysicsErrorCls.subclasses()):
                for individual in cls.instances():
                    errors.append((cls.name, individual))
                    log.debug("Reasoner found error %s of type %s", individual.name, cls.name)
    except Exception as e:
        print("[ERROR] Failed to enumerate PhysicsError instances: " + str(e))

def extract_fallback_errors(world, errors):
    for individual in world.individuals():
        for cls in individual.is_a:
            if hasattr(cls, "name") and "Error" in cls.name:
                pair = (cls.name, individual)
                if pair not in errors:
                    errors.append(pair)
                    log.debug("Reasoner found error (fallback) %s of type %s", individual.name, cls.name)


def _first_value(propValues):
    if not propValues:
        return None
    try:
        return list(propValues)[0]
    except Exception:
        return None


def _set_quantity_if_new(resMeasurement, qtyCls, ruleName, logName):
    if qtyCls is None or resMeasurement is None:
        return
    current = list(resMeasurement.hasQuantityType or [])
    if qtyCls in current:
        return
    resMeasurement.hasQuantityType.append(qtyCls)
    print("[INFO] Python rule " + ruleName + " applied on " + logName + " -> " + qtyCls.name)


def propagate_literal_dependent_rules(world):
    DivExpr = world.search_one(iri="*#DivisionExpression")
    MulExpr = world.search_one(iri="*#MultiplicationExpression")
    PowExpr = world.search_one(iri="*#PowerExpression")

    FreqQ           = world.search_one(iri="*#FrequencyQuantity")
    TimeQ           = world.search_one(iri="*#TimeQuantity")
    EnergyQ         = world.search_one(iri="*#EnergyQuantity")
    AccelQ          = world.search_one(iri="*#AccelerationQuantity")
    HeightQ         = world.search_one(iri="*#HeightQuantity")
    LengthQ         = world.search_one(iri="*#LengthQuantity")
    AreaQ           = world.search_one(iri="*#AreaQuantity")
    VolumeQ         = world.search_one(iri="*#VolumeQuantity")
    VelocityQ       = world.search_one(iri="*#VelocityQuantity")
    SpecificEnergyQ = world.search_one(iri="*#SpecificEnergyQuantity")
    TimeSquaredQ    = world.search_one(iri="*#TimeSquaredQuantity")

    if DivExpr is not None:
        for inst in list(DivExpr.instances()):
            try:
                l = _first_value(inst.hasLeftOperand)
                r = _first_value(inst.hasRightOperand)
                res = _first_value(inst.hasResultMeasurement)
            except Exception:
                continue
            if l is None or r is None or res is None:
                continue

            lVal = _first_value(getattr(l, "hasNumericValue", None))
            rQty = _first_value(getattr(r, "hasQuantityType", None))
            lQty = _first_value(getattr(l, "hasQuantityType", None))

            if lVal == 1.0 and rQty == TimeQ:
                _set_quantity_if_new(res, FreqQ, "prop_freq", inst.name)
            elif lVal == 1.0 and rQty == FreqQ:
                _set_quantity_if_new(res, TimeQ, "prop_period", inst.name)

            if lQty == EnergyQ and rQty == AccelQ:
                _set_quantity_if_new(res, HeightQ, "prop_h_attained", inst.name)

    if MulExpr is not None:
        for inst in list(MulExpr.instances()):
            try:
                l = _first_value(inst.hasLeftOperand)
                r = _first_value(inst.hasRightOperand)
                res = _first_value(inst.hasResultMeasurement)
            except Exception:
                continue
            if l is None or r is None or res is None:
                continue

            lVal = _first_value(getattr(l, "hasNumericValue", None))
            rVal = _first_value(getattr(r, "hasNumericValue", None))
            lQty = _first_value(getattr(l, "hasQuantityType", None))
            rQty = _first_value(getattr(r, "hasQuantityType", None))

            if lVal == 0.5 and rQty == EnergyQ:
                _set_quantity_if_new(res, EnergyQ, "prop_ke", inst.name)
            elif rVal == 0.5 and lQty == EnergyQ:
                _set_quantity_if_new(res, EnergyQ, "prop_ke", inst.name)

    # TODO: handle non-integer exponents (e.g. v ** 1.5 in some scaling laws).
    if PowExpr is not None:
        for inst in list(PowExpr.instances()):
            try:
                base = _first_value(inst.hasLeftOperand)
                exp = _first_value(inst.hasRightOperand)
                res = _first_value(inst.hasResultMeasurement)
            except Exception:
                continue
            if base is None or exp is None or res is None:
                continue

            baseQty = _first_value(getattr(base, "hasQuantityType", None))
            expVal = _first_value(getattr(exp, "hasNumericValue", None))
            if expVal is None:
                continue
            try:
                n = int(expVal)
            except (TypeError, ValueError):
                continue
            if n != expVal:
                continue

            if baseQty == LengthQ and n == 2:
                _set_quantity_if_new(res, AreaQ, "prop_pow_length_2", inst.name)
            elif baseQty == LengthQ and n == 3:
                _set_quantity_if_new(res, VolumeQ, "prop_pow_length_3", inst.name)
            elif baseQty == VelocityQ and n == 2:
                _set_quantity_if_new(res, SpecificEnergyQ, "prop_pow_velocity_2", inst.name)
            elif baseQty == TimeQ and n == 2:
                _set_quantity_if_new(res, TimeSquaredQ, "prop_pow_time_2", inst.name)


def _qty_names(measurement):
    """Return the list of quantity-type names attached to a Measurement."""
    if measurement is None:
        return []
    out = []
    for q in (getattr(measurement, "hasQuantityType", None) or []):
        name = getattr(q, "name", None)
        if name:
            out.append(name)
    return out


def _measurement_value(measurement):
    if measurement is None:
        return None
    vals = list(getattr(measurement, "hasNumericValue", None) or [])
    return vals[0] if vals else None


# Expression class -> the operator/function symbol used in the trace, so the
# reconstructed chain reads like the original DSL.
_EXPR_SYMBOL = {
    "AdditionExpression": "+", "SubtractionExpression": "-",
    "MultiplicationExpression": "*", "DivisionExpression": "/",
    "PowerExpression": "^", "AssignmentOperation": ":=",
    "SqrtExpression": "sqrt", "SineExpression": "sin",
    "CosineExpression": "cos", "TangentExpression": "tan",
    "LogarithmExpression": "log", "NaturalLogarithmExpression": "ln",
    "DerivativeExpression": "derivative", "IntegralExpression": "integral",
}


def build_inference_trace(world):
    """Reconstruct the inference chain for the program currently in `world`.

    For every Expression node it records the operands (name, quantity, value)
    and the quantity inferred on the result Measurement. This is the per-problem
    trace used to reconstruct what the reasoner actually propagated, as opposed
    to listing the full rule catalogue.
    """
    Expression = world.search_one(iri="*#Expression")
    steps = []
    if Expression is None:
        return steps

    for cls in Expression.descendants():
        cls_name = getattr(cls, "name", None)
        if not cls_name or cls_name not in _EXPR_SYMBOL:
            continue
        for inst in cls.instances():
            left = list(getattr(inst, "hasLeftOperand", None) or [])
            right = list(getattr(inst, "hasRightOperand", None) or [])
            operand = list(getattr(inst, "hasOperand", None) or [])
            result = list(getattr(inst, "hasResultMeasurement", None) or [])

            def descr(m):
                return {
                    "name": getattr(m, "name", None),
                    "quantities": _qty_names(m),
                    "value": _measurement_value(m),
                }

            step = {
                "expression": inst.name,
                "operation": cls_name,
                "symbol": _EXPR_SYMBOL[cls_name],
                "operands": [],
                "result": descr(result[0]) if result else None,
            }
            for m in left + right + operand:
                step["operands"].append(descr(m))
            steps.append(step)

    return steps


def validate_dsl_semantics(customOwlPath = None):
    owlToLoad = customOwlPath if customOwlPath else PROGRAM_OWL
    world = World()

    world.get_ontology(str(PHYSICS_DOMAIN_OWL.resolve())).load()
    world.get_ontology(str(MATH_OWL.resolve())).load()
    world.get_ontology(str(PROGRAM_TRACE_OWL.resolve())).load()
    world.get_ontology(str(PHYSICS_BRIDGE_OWL.resolve())).load()
    if PHYSICS_RULES_OWL.exists():
        world.get_ontology(str(PHYSICS_RULES_OWL.resolve())).load()

    if owlToLoad.exists():
        world.get_ontology(str(owlToLoad.resolve())).load()

    # TODO: Pellet has a JVM warm-up cost of ~2s per call. Reuse the JVM
    # across iterations or batch DSLs.
    print("[INFO] Running Pellet reasoner in fresh world...")
    with world:
        PhysicalQuantityCls = world.search_one(iri="*#PhysicalQuantity") or Thing
        allQuantities = list(world.search(type=PhysicalQuantityCls))
        if len(allQuantities) > 1:
            AllDifferent(allQuantities)
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

    propagate_literal_dependent_rules(world)

    errors = []
    check_manual_compatibility(world, errors)
    check_manual_trigonometry(world, errors)
    check_invalid_power(world, errors)
    extract_physics_errors_from_reasoner(world, errors)
    extract_fallback_errors(world, errors)

    rules = []
    for r in world.rules():
        rules.append(str(r))

    trace = build_inference_trace(world)

    return errors, rules, trace

def check_dsl_purity(dsl):
    errors = []
    whitelist = {"0", "0.0", "1", "1.0", "2", "2.0", "0.5", "PI", "E"}

    definitions = dsl.get("definitions", [])
    for definition in definitions:
        defId = definition.get("id", "unknown")
        for op in definition.get("operations", []):
            for field in ["left", "right", "operand"]:
                val = op.get(field)
                if val is None: continue

                strVal = str(val).strip()
                try:
                    float(strVal)
                    if strVal not in whitelist:
                        errors.append("Purity check failed in module " + defId + ": literal '" + strVal + "' is not allowed, use an input variable.")
                except ValueError:
                    pass
    return errors


# Unit/quantity compatibility tables read from the OWL ontology.
# Populated lazily on first use.

_UNIT_CATEGORY_CACHE: Dict[str, str] = {}
_QUANTITY_CATEGORIES_CACHE: Dict[str, Set[str]] = {}
_TABLES_LOADED = False


def _load_compatibility_tables_from_ontology():
    global _TABLES_LOADED
    if _TABLES_LOADED:
        return

    onto = load_ontology(PHYSICS_DOMAIN_OWL)
    Unit = onto.world.search_one(iri="*#Unit")
    PhysicalQuantity = onto.world.search_one(iri="*#PhysicalQuantity")

    if Unit is not None:
        for u in Unit.instances():
            cats = list(u.hasUnitCategory or [])
            if cats:
                _UNIT_CATEGORY_CACHE[u.name] = cats[0]

    if PhysicalQuantity is not None:
        for q in PhysicalQuantity.instances():
            allowed = list(q.hasAllowedUnitCategory or [])
            if allowed:
                _QUANTITY_CATEGORIES_CACHE[q.name] = set(allowed)

    if not _UNIT_CATEGORY_CACHE or not _QUANTITY_CATEGORIES_CACHE:
        raise Exception("[ERROR] Compatibility tables empty. Run `python scripts/rebuild_all_ontologies.py` to regenerate the OWL.")

    _TABLES_LOADED = True


def _local_name(value):
    if value is None:
        return ""
    s = str(value)
    if "#" in s:
        s = s.split("#")[-1]
    return s.strip()


def check_declaration_unit_compatibility(dsl):
    _load_compatibility_tables_from_ontology()

    errors = []
    decls = dsl.get("main_declarations", dsl.get("declarations", []))
    for decl in decls:
        sem = decl.get("semantics") or {}
        qty = _local_name(sem.get("quantity"))
        unit = _local_name(sem.get("unit"))
        if not qty or not unit:
            continue

        allowed = _QUANTITY_CATEGORIES_CACHE.get(qty)
        if allowed is None:
            continue
        if not allowed:
            continue

        unitCat = _UNIT_CATEGORY_CACHE.get(unit)
        if unitCat is None:
            errors.append("[" + str(decl.get("name", "?")) + "] unknown unit: " + unit)
            continue
        if unitCat not in allowed:
            declName = str(decl.get("name", "?"))
            errors.append("Bad declaration " + declName + ": unit " + unit + " is " + unitCat + ", not in " + str(sorted(allowed)) + ".")
    return errors

def run_validation(json_path, custom_output_dir = None, custom_owl_path = None):
    # Load DSL
    with open(json_path, 'r', encoding='utf-8') as f:
        dslContent = json.load(f)

    purityErrors = check_dsl_purity(dslContent)
    declUnitErrors = check_declaration_unit_compatibility(dslContent)
    # End of load DSL

    # Run reasoner
    errors, rules, trace = validate_dsl_semantics(custom_owl_path)
    baseOut = custom_output_dir if custom_output_dir else OUTPUT_DIR
    reportFile = baseOut / ("result_" + json_path.stem + ".txt")
    traceFile = baseOut / ("trace_" + json_path.stem + ".json")
    # End of run reasoner

    # Write the per-problem inference trace (the actual propagation chain).
    with open(traceFile, "w", encoding="utf-8") as f:
        json.dump({"program": json_path.stem, "steps": trace}, f, ensure_ascii=False, indent=2)

    staticErrors = list(purityErrors) + list(declUnitErrors)

    # Write a short human-readable report. The full inference chain lives in
    # the trace JSON; here we only keep the status, the errors and a pointer.
    with open(reportFile, "w", encoding="utf-8") as f:
        f.write("VALIDATION REPORT: " + json_path.name + "\n")
        f.write("=" * 52 + "\n\n")

        if not errors and not staticErrors:
            f.write("STATUS: OK - no physical inconsistencies found.\n")
            print("[INFO] Validation OK: " + json_path.name)
        else:
            total = len(errors) + len(staticErrors)
            f.write("STATUS: FAILED - " + str(total) + " semantic error(s).\n\n")
            f.write("ERRORS:\n")
            for label, inst in errors:
                f.write("  * " + describe_error(label, inst) + "\n")
            for sErr in staticErrors:
                f.write("  * " + sErr + "\n")

            for sErr in staticErrors:
                errors.append((sErr, DummyInst(name="DSL_STRUCTURE")))

            print("[WARN] Validation FAILED: " + json_path.name + " -> " + str(total) + " errors")

        f.write("\nInference chain: " + str(len(trace)) + " step(s). See " + traceFile.name + " for the full trace.\n")

    return errors
