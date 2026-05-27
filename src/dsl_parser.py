import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from owlready2 import default_world, get_ontology

from src.settings import PROGRAM_OWL, PHYSICS_OWL
from src.utils import load_ontology

log = logging.getLogger(__name__)

def _get_individual_by_name_or_iri(onto, identifier):
    if not identifier: return None
    ind = onto.search_one(iri=identifier)
    if ind: return ind
    fragment = identifier.split("#")[-1]
    ind = getattr(onto, fragment, None)
    return ind

def find_physics_class(physics_onto, physics_ns, name, ns_iri):
    cls = getattr(physics_ns, name, None) or physics_onto.world.search_one(iri="*#" + name)
    # fallback for old fixtures
    if name.endswith("Operation") and not cls:
        altName = name.replace("Operation", "Expression")
        cls = getattr(physics_ns, altName, None) or physics_onto.world.search_one(iri="*#" + altName)
    return cls

def create_literal_measurement(value, MeasurementClass, program_onto, literal_counter):
    name = "lit_" + str(literal_counter[0])
    m = MeasurementClass(name, namespace=program_onto)
    try:
        m.hasNumericValue = [float(value)]
    except (TypeError, ValueError) as e:
        log.debug("Could not coerce literal %r to float: %s", value, e)
    literal_counter[0] += 1
    return m

def process_operation(op_spec, context_map, definitions, program_onto, classes, counters):
    op_type = op_spec.get("type")
    
    if op_type == "module_call":
        mod_id = op_spec.get("module")
        mod_def = next((d for d in definitions if d["id"] == mod_id), None)
        if not mod_def: return
        local_map = {}
        args = op_spec.get("args", {}) or {}
        for input_spec in mod_def.get("inputs", []):
            input_name = input_spec["name"] if isinstance(input_spec, dict) else input_spec
            parent_var_name = args.get(input_name)
            if parent_var_name and parent_var_name in context_map:
                local_map[input_name] = context_map[parent_var_name]
        for sub_op in mod_def.get("operations", []):
            process_operation(sub_op, local_map, definitions, program_onto, classes, counters)
        res_key = op_spec.get("result")
        mod_res_internal = mod_def.get("output_var")
        if not mod_res_internal and mod_def.get("operations"):
            mod_res_internal = mod_def["operations"][-1].get("result")
        if mod_res_internal and mod_res_internal in local_map:
            context_map[res_key] = local_map[mod_res_internal]
        return

    res_name = op_spec.get("result")
    if not res_name: return

    MeasurementClass = classes['MeasurementClass']
    hasResultMeasurement = classes['hasResultMeasurement']

    if op_type == "assignment":
        left_m = context_map.get(op_spec.get("left"))
        right_m = context_map.get(op_spec.get("right"))
        AssignmentOperationClass = classes['AssignmentOperationClass']
        if left_m and right_m and AssignmentOperationClass:
            op_ind = AssignmentOperationClass(f"Assign_{counters['op'][0]}", namespace=program_onto)
            if classes['hasLeftOperand']: op_ind.hasLeftOperand = [left_m]
            if classes['hasRightOperand']: op_ind.hasRightOperand = [right_m]
            if hasResultMeasurement: op_ind.hasResultMeasurement = [left_m]
            counters['op'][0] += 1

    elif op_type in ["binary", "binary_literal"]:
        operator = op_spec.get("operator")
        left_m = context_map.get(op_spec.get("left") or op_spec.get("left_var"))
        right_m = context_map.get(op_spec.get("right"))
        
        if op_type == "binary_literal":
            right_m = create_literal_measurement(op_spec.get("literal"), MeasurementClass, program_onto, counters['lit'])
        elif right_m is None and op_spec.get("right"):
            try:
                right_m = create_literal_measurement(float(op_spec.get("right")), MeasurementClass, program_onto, counters['lit'])
            except (TypeError, ValueError) as e:
                log.debug("Right operand %r is not a literal nor a known var: %s", op_spec.get("right"), e)
        
        if not left_m or not right_m: return
        
        op_classes = {
            "+": classes['AdditionOperationClass'], "-": classes['SubtractionOperationClass'],
            "*": classes['MultiplicationOperationClass'], "/": classes['DivisionOperationClass'],
            "^": classes['PowerExpressionClass']
        }
        op_class = op_classes.get(operator)
        if op_class:
            op_ind = op_class(f"Op_{counters['op'][0]}_{res_name}", namespace=program_onto)
            if classes['hasLeftOperand']: op_ind.hasLeftOperand = [left_m]
            if classes['hasRightOperand']: op_ind.hasRightOperand = [right_m]
            res_m = MeasurementClass(f"Res_{res_name}_{counters['op'][0]}", namespace=program_onto)
            if hasResultMeasurement: op_ind.hasResultMeasurement = [res_m]
            context_map[res_name] = res_m
            counters['op'][0] += 1

    elif op_type == "unary":
        func = op_spec.get("function")
        operand_m = context_map.get(op_spec.get("operand"))
        if not operand_m: return
        
        op_classes = {
            "sqrt": classes['SqrtExpressionClass'], "sin": classes['SineExpressionClass'], 
            "cos": classes['CosineExpressionClass'], "derivative": classes['DerivativeExpressionClass'],
            "integral": classes['IntegralExpressionClass'],
            "log": classes['LogarithmExpressionClass'],
            "ln": classes['NaturalLogarithmExpressionClass']
        }
        op_class = op_classes.get(func)
        if op_class:
            op_ind = op_class(f"Op_{counters['op'][0]}_{res_name}", namespace=program_onto)
            if classes['hasOperand']: op_ind.hasOperand = [operand_m]
            res_m = MeasurementClass(f"Res_{res_name}_{counters['op'][0]}", namespace=program_onto)
            if hasResultMeasurement: op_ind.hasResultMeasurement = [res_m]
            context_map[res_name] = res_m
            counters['op'][0] += 1


def parse_dsl_to_program_ontology(json_file: Path, physics_onto, output_path: Path = None) -> Optional[object]:
    ns_iri = "http://example.org/physics#"
    physics_ns = physics_onto.world.get_namespace(ns_iri)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    declarations = data.get("main_declarations", data.get("declarations", []))
    definitions = data.get("definitions", [])
    execution_flow = data.get("execution_flow", data.get("operations", []))

    classes = {
        'MeasurementClass': find_physics_class(physics_onto, physics_ns, "Measurement", ns_iri),
        'hasQuantityType': find_physics_class(physics_onto, physics_ns, "hasQuantityType", ns_iri),
        'hasUnit': find_physics_class(physics_onto, physics_ns, "hasUnit", ns_iri),
        'hasNumericValue': find_physics_class(physics_onto, physics_ns, "hasNumericValue", ns_iri),
        'AssignmentOperationClass': find_physics_class(physics_onto, physics_ns, "AssignmentOperation", ns_iri),
        'AdditionOperationClass': find_physics_class(physics_onto, physics_ns, "AdditionExpression", ns_iri),
        'SubtractionOperationClass': find_physics_class(physics_onto, physics_ns, "SubtractionExpression", ns_iri),
        'MultiplicationOperationClass': find_physics_class(physics_onto, physics_ns, "MultiplicationExpression", ns_iri),
        'DivisionOperationClass': find_physics_class(physics_onto, physics_ns, "DivisionExpression", ns_iri),
        'hasLeftOperand': find_physics_class(physics_onto, physics_ns, "hasLeftOperand", ns_iri),
        'hasRightOperand': find_physics_class(physics_onto, physics_ns, "hasRightOperand", ns_iri),
        'hasOperand': find_physics_class(physics_onto, physics_ns, "hasOperand", ns_iri),
        'hasResultMeasurement': find_physics_class(physics_onto, physics_ns, "hasResultMeasurement", ns_iri),
        'SqrtExpressionClass': find_physics_class(physics_onto, physics_ns, "SqrtExpression", ns_iri),
        'SineExpressionClass': find_physics_class(physics_onto, physics_ns, "SineExpression", ns_iri),
        'CosineExpressionClass': find_physics_class(physics_onto, physics_ns, "CosineExpression", ns_iri),
        'DerivativeExpressionClass': find_physics_class(physics_onto, physics_ns, "DerivativeExpression", ns_iri),
        'IntegralExpressionClass': find_physics_class(physics_onto, physics_ns, "IntegralExpression", ns_iri),
        'PowerExpressionClass': find_physics_class(physics_onto, physics_ns, "PowerExpression", ns_iri),
        'LogarithmExpressionClass': find_physics_class(physics_onto, physics_ns, "LogarithmExpression", ns_iri),
        'NaturalLogarithmExpressionClass': find_physics_class(physics_onto, physics_ns, "NaturalLogarithmExpression", ns_iri)
    }

    old_onto = default_world.get_ontology("http://example.org/program")
    if old_onto:
        old_onto.destroy()
        
    program_onto = get_ontology("http://example.org/program")

    measurement_prefix = "phys_"
    name_to_measurement = {}
    counters = {'lit': [1], 'op': [1]}

    with program_onto:
        for decl in declarations:
            m = classes['MeasurementClass'](f"{measurement_prefix}{decl['name']}")
            if classes['hasNumericValue'] and decl.get("value") is not None:
                m.hasNumericValue = [float(decl["value"])]
            
            sem = decl.get("semantics", {})
            if sem:
                qty = _get_individual_by_name_or_iri(physics_onto, sem.get("quantity"))
                if qty and classes['hasQuantityType']: classes['hasQuantityType'][m] = [qty]
                unit = _get_individual_by_name_or_iri(physics_onto, sem.get("unit"))
                if unit and classes['hasUnit']: classes['hasUnit'][m] = [unit]
            
            name_to_measurement[decl["name"]] = m

        for op in execution_flow:
            process_operation(op, name_to_measurement, definitions, program_onto, classes, counters)

    savePath = output_path if output_path else PROGRAM_OWL
    program_onto.save(file=str(savePath.resolve()));
    print("[INFO] Finished processing modular DSL. Saved to: " + str(savePath))
    return program_onto

def map_dsl_to_ontology(dsl_path: Path, output_owl_path: Path = None):
    physics_onto = load_ontology(PHYSICS_OWL)
    return parse_dsl_to_program_ontology(dsl_path, physics_onto, output_owl_path)
