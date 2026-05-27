from owlready2 import *
import os

def rebuild():
    onto_path.append('resources')

    # 1. Base Structure (physics-math)
    math_onto = get_ontology("http://example.org/physics/physics-math")
    math_base_iri = "http://example.org/physics#"
    phys = math_onto.get_namespace(math_base_iri)

    with math_onto:
        class PhysicalQuantity(Thing): namespace = phys
        class Unit(Thing): namespace = phys
        class Expression(Thing): namespace = phys
        class Measurement(Expression): namespace = phys
        class BinaryExpression(Expression): namespace = phys
        class UnaryExpression(Expression): namespace = phys

        class hasLeftOperand(ObjectProperty): namespace = phys
        class hasRightOperand(ObjectProperty): namespace = phys
        class hasOperand(ObjectProperty): namespace = phys
        class hasUnit(ObjectProperty): namespace = phys
        class hasQuantityType(ObjectProperty): namespace = phys
        class hasResultMeasurement(ObjectProperty): namespace = phys
        class hasNumericValue(DatatypeProperty): namespace = phys
        class hasSymbol(DatatypeProperty): namespace = phys
        class hasConversionFactorToSI(DatatypeProperty): namespace = phys
        class hasUnitCategory(DatatypeProperty): namespace = phys
        class hasAllowedUnitCategory(DatatypeProperty): namespace = phys

        # Arithmetic
        class AdditionExpression(BinaryExpression): namespace = phys
        class SubtractionExpression(BinaryExpression): namespace = phys
        class MultiplicationExpression(BinaryExpression): namespace = phys
        class DivisionExpression(BinaryExpression): namespace = phys
        class PowerExpression(BinaryExpression): namespace = phys
        class AssignmentOperation(BinaryExpression): namespace = phys

        class SqrtExpression(UnaryExpression): namespace = phys
        class SineExpression(UnaryExpression): namespace = phys
        class CosineExpression(UnaryExpression): namespace = phys
        class TangentExpression(UnaryExpression): namespace = phys
        class LogarithmExpression(UnaryExpression): namespace = phys
        class NaturalLogarithmExpression(UnaryExpression): namespace = phys

        # Calculus
        class DerivativeExpression(UnaryExpression): namespace = phys
        class IntegralExpression(UnaryExpression): namespace = phys

    math_onto.save("resources/physics-math.owl")

    # 2. Domain (physics-domain)
    domain_onto = get_ontology("http://example.org/physics/physics-domain")
    domain_onto.imported_ontologies.append(math_onto)
    phys_domain = domain_onto.get_namespace("http://example.org/physics/physics-domain#")

    with domain_onto:
        def add_qty(name, allowed_categories=()):
            q = PhysicalQuantity(name, namespace=phys_domain)
            if allowed_categories:
                q.hasAllowedUnitCategory = list(allowed_categories)
            return q

        MassQty             = add_qty("MassQuantity",                   ("mass",))
        LengthQty           = add_qty("LengthQuantity",                 ("length",))
        PositionQty         = add_qty("PositionQuantity",               ("length",))
        AltitudeQty         = add_qty("AltitudeQuantity",               ("length",))
        DisplacementQty     = add_qty("DisplacementQuantity",           ("length",))
        HeightQty           = add_qty("HeightQuantity",                 ("length",))
        TimeQty             = add_qty("TimeQuantity",                   ("time",))
        VelQty              = add_qty("VelocityQuantity",               ("length",))
        AccelQty            = add_qty("AccelerationQuantity",           ("length",))
        ForceQty            = add_qty("ForceQuantity",                  ("force",))
        MomentumQty         = add_qty("MomentumQuantity",               ("length", "mass"))
        EnergyQty           = add_qty("EnergyQuantity",                 ("energy",))
        PowerQty            = add_qty("PowerQuantity",                  ("power",))
        AngleQty            = add_qty("AngleQuantity",                  ("angle",))
        AngularVelQty       = add_qty("AngularVelocityQuantity",        ("angle",))
        AngularAccelQty     = add_qty("AngularAccelerationQuantity",    ("angle",))
        FrequencyQty        = add_qty("FrequencyQuantity",              ("frequency",))
        SpecificEnergyQty   = add_qty("SpecificEnergyQuantity",         ("energy", "length"))
        GravParamQty        = add_qty("GravitationalParameterQuantity", ("length",))
        AreaQty             = add_qty("AreaQuantity",                   ("area",))
        VolumeQty           = add_qty("VolumeQuantity",                 ("volume",))
        DensityQty          = add_qty("DensityQuantity",                ("density",))
        PressureQty         = add_qty("PressureQuantity",               ("pressure",))
        # Auxiliary magnitude for the result of t^2 (used in ½·a·t²).
        TimeSquaredQty      = add_qty("TimeSquaredQuantity",            ("time_squared",))
        FrictionCoeffQty    = add_qty("FrictionCoefficientQuantity",    ())
        DimQty              = add_qty("DimensionlessQuantity",          ())

        AllDifferent([
            MassQty, LengthQty, PositionQty, AltitudeQty, DisplacementQty, HeightQty, TimeQty, VelQty, AccelQty, ForceQty, MomentumQty, EnergyQty,
            PowerQty, AngleQty, AngularVelQty, AngularAccelQty, FrequencyQty,
            SpecificEnergyQty, GravParamQty,
            AreaQty, VolumeQty, DensityQty, PressureQty,
            TimeSquaredQty, FrictionCoeffQty,
            DimQty
        ])

        def add_unit(name, factor, category):
            u = Unit(name, namespace=phys_domain)
            u.hasConversionFactorToSI = [factor]
            u.hasUnitCategory = [category]
            return u

        Meter     = add_unit("Meter",     1.0,         "length")
        Kilometer = add_unit("Kilometer", 1000.0,      "length")
        Second    = add_unit("Second",    1.0,         "time")
        Minute    = add_unit("Minute",    60.0,        "time")
        Hour      = add_unit("Hour",      3600.0,      "time")
        Kilogram  = add_unit("Kilogram",  1.0,         "mass")
        Gram      = add_unit("Gram",      0.001,       "mass")
        Newton    = add_unit("Newton",    1.0,         "force")
        Joule     = add_unit("Joule",     1.0,         "energy")
        Watt      = add_unit("Watt",      1.0,         "power")
        Radian    = add_unit("Radian",    1.0,         "angle")
        Degree    = add_unit("Degree",    0.0174532925,"angle")
        Hertz     = add_unit("Hertz",     1.0,         "frequency")
        SquareMeter           = add_unit("SquareMeter",            1.0,      "area")
        CubicMeter            = add_unit("CubicMeter",             1.0,      "volume")
        Liter                 = add_unit("Liter",                  0.001,    "volume")
        KilogramPerCubicMeter = add_unit("KilogramPerCubicMeter",  1.0,      "density")
        Pascal                = add_unit("Pascal",                 1.0,      "pressure")
        Bar                   = add_unit("Bar",                    1.0e5,    "pressure")
        Atmosphere            = add_unit("Atmosphere",             101325.0, "pressure")
        SecondSquared         = add_unit("SecondSquared",          1.0,      "time_squared")

        def add_c(name, qty, val, symbol=None, unit=None):
            c = Measurement(name, namespace=phys)
            c.hasQuantityType = [qty]
            c.hasNumericValue = [val]
            if symbol: c.hasSymbol = [symbol]
            if unit: c.hasUnit = [unit]
            return c

        # Universal Constants
        add_c("Pi", DimQty, 3.141592653589793, "pi")
        add_c("StandardGravity", AccelQty, 9.80665, "g", unit=Meter)
        G_val = 6.67430e-11
        G_type = PhysicalQuantity("UniversalGravitationalConstantType", namespace=phys_domain)
        add_c("UniversalGravitationalConstant", G_type, G_val, "G")
        add_c("SpeedOfLight", VelQty, 299792458.0, "c", unit=Meter)
        add_c("AstronomicalUnit", LengthQty, 149597870700.0, "AU", unit=Meter)
        add_c("Day", TimeQty, 86400.0, "day", unit=Second)
        add_c("JulianYear", TimeQty, 31557600.0, "yr", unit=Second)
        add_c("StandardAtmosphericPressure", PressureQty, 101325.0,    "P_atm",    unit=Pascal)
        add_c("StandardWaterDensity",        DensityQty,  1000.0,      "rho_water", unit=KilogramPerCubicMeter)
        add_c("StandardAirDensity",          DensityQty,  1.225,       "rho_air",   unit=KilogramPerCubicMeter)

        # Celestial Bodies
        add_c("Earth_Mass", MassQty, 5.97217e24, "M_earth", unit=Kilogram)
        add_c("Earth_MeanRadius", LengthQty, 6371000.0, "R_earth", unit=Meter)
        add_c("Earth_EquatorialRadius", LengthQty, 6378136.6, "R_eq_earth", unit=Meter)
        add_c("Earth_GravitationalParameter", GravParamQty, 3.986004418e14, "mu_earth")
        add_c("Mars_MeanRadius", LengthQty, 3389500.0, "R_mars", unit=Meter)
        add_c("Mars_GravitationalParameter", GravParamQty, 4.282837e13, "mu_mars")
        add_c("Sun_MeanRadius", LengthQty, 695700000.0, "R_sun", unit=Meter)
        add_c("Sun_GravitationalParameter", GravParamQty, 1.32712440018e20, "mu_sun")
        add_c("Moon_MeanRadius", LengthQty, 1737400.0, "R_moon", unit=Meter)
        add_c("Moon_GravitationalParameter", GravParamQty, 4.902800066e12, "mu_moon")
        add_c("Jupiter_MeanRadius", LengthQty, 69911000.0, "R_jup", unit=Meter)
        add_c("Jupiter_GravitationalParameter", GravParamQty, 1.26686534e17, "mu_jup")

    domain_onto.save("resources/physics-domain.owl")

    # 3. Rules (physics-rules)
    rules_onto = get_ontology("http://example.org/physics/physics-rules")
    rules_onto.imported_ontologies.append(domain_onto)

    with rules_onto:
        class PhysicsError(Thing): namespace = phys
        class QuantityIncompatibilityError(PhysicsError): namespace = phys
        class UnitIncompatibilityError(PhysicsError): namespace = phys
        class InvalidTrigonometryArgumentError(PhysicsError): namespace = phys
        class DimensionMismatchError(PhysicsError): namespace = phys

        def r(name, text):
            imp = Imp()
            imp.namespace = rules_onto
            imp.set_as_rule(text, namespaces=[math_onto, domain_onto, phys, phys_domain])
            return imp

        # Basic Dimensional Arithmetic
        r("prop_add", "AdditionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?l, ?q), hasQuantityType(?r, ?q) -> hasQuantityType(?res, ?q)")
        r("prop_sub", "SubtractionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?l, ?q), hasQuantityType(?r, ?q) -> hasQuantityType(?res, ?q)")

        # Assignment
        r("prop_assign", "AssignmentOperation(?e), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?r, ?q) -> hasQuantityType(?res, ?q)")

        # Relational Positions (Strict)
        r("prop_alt_disp_add", "AdditionExpression(?e), hasLeftOperand(?e, ?p), hasRightOperand(?e, ?d), hasResultMeasurement(?e, ?res), hasQuantityType(?p, AltitudeQuantity), hasQuantityType(?d, DisplacementQuantity) -> hasQuantityType(?res, AltitudeQuantity)")
        r("prop_disp_disp_add", "AdditionExpression(?e), hasLeftOperand(?e, ?d1), hasRightOperand(?e, ?d2), hasResultMeasurement(?e, ?res), hasQuantityType(?d1, DisplacementQuantity), hasQuantityType(?d2, DisplacementQuantity) -> hasQuantityType(?res, DisplacementQuantity)")
        r("prop_alt_alt_sub", "SubtractionExpression(?e), hasLeftOperand(?e, ?p1), hasRightOperand(?e, ?p2), hasResultMeasurement(?e, ?res), hasQuantityType(?p1, AltitudeQuantity), hasQuantityType(?p2, AltitudeQuantity) -> hasQuantityType(?res, DisplacementQuantity)")

        # Kinematics
        r("prop_vel", "DivisionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?l, DisplacementQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)")
        r("prop_acc", "DivisionExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
        r("prop_mult_vt", "MultiplicationExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, DisplacementQuantity)")
        r("prop_mult_at", "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AccelerationQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)")

        # Circular Motion
        r("prop_w", "DivisionExpression(?e), hasLeftOperand(?e, ?theta), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?theta, AngleQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularVelocityQuantity)")
        r("prop_alpha", "DivisionExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?w, AngularVelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularAccelerationQuantity)")
        r("prop_v_wR", "MultiplicationExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?w, AngularVelocityQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, VelocityQuantity)")
        r("prop_at_alphaR", "MultiplicationExpression(?e), hasLeftOperand(?e, ?alpha), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?alpha, AngularAccelerationQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, AccelerationQuantity)")

        # Dynamics & Energy
        r("prop_force", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m), hasRightOperand(?e, ?a), hasResultMeasurement(?e, ?res), hasQuantityType(?m, MassQuantity), hasQuantityType(?a, AccelerationQuantity) -> hasQuantityType(?res, ForceQuantity)")
        r("prop_momentum", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m), hasRightOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?m, MassQuantity), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, MomentumQuantity)")
        r("prop_work", "MultiplicationExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?d), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?d, LengthQuantity) -> hasQuantityType(?res, EnergyQuantity)")
        r("prop_power", "DivisionExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?w, EnergyQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, PowerQuantity)")
        r("prop_impulse", "MultiplicationExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, MomentumQuantity)")
        r("prop_friction", "MultiplicationExpression(?e), hasLeftOperand(?e, ?mu), hasRightOperand(?e, ?n), hasResultMeasurement(?e, ?res), hasQuantityType(?mu, FrictionCoefficientQuantity), hasQuantityType(?n, ForceQuantity) -> hasQuantityType(?res, ForceQuantity)")
        r("prop_accel_from_force", "DivisionExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
        r("prop_force_from_impulse", "DivisionExpression(?e), hasLeftOperand(?e, ?p), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?p, MomentumQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, ForceQuantity)")

        # Astro & Gravitation
        r("prop_mu", "MultiplicationExpression(?e), hasLeftOperand(?e, ?G), hasRightOperand(?e, ?M), hasResultMeasurement(?e, ?res), hasQuantityType(?G, UniversalGravitationalConstantType), hasQuantityType(?M, MassQuantity) -> hasQuantityType(?res, GravitationalParameterQuantity)")
        r("prop_eps_pot", "DivisionExpression(?e), hasLeftOperand(?e, ?neg_mu), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?neg_mu, GravitationalParameterQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, SpecificEnergyQuantity)")
        r("prop_v_sqrt", "SqrtExpression(?e), hasOperand(?e, ?mu_r), hasResultMeasurement(?e, ?res), hasQuantityType(?mu_r, SpecificEnergyQuantity) -> hasQuantityType(?res, VelocityQuantity)")
        r("prop_v_pm", "DivisionExpression(?e), hasLeftOperand(?e, ?p), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?p, MomentumQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, VelocityQuantity)")
        r("prop_energy_from_specific", "MultiplicationExpression(?e), hasLeftOperand(?e, ?eps), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?eps, SpecificEnergyQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, EnergyQuantity)")
        r("prop_grav_field", "DivisionExpression(?e), hasLeftOperand(?e, ?mu), hasRightOperand(?e, ?r2), hasResultMeasurement(?e, ?res), hasQuantityType(?mu, GravitationalParameterQuantity), hasQuantityType(?r2, AreaQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
        r("prop_force_from_accel", "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AccelerationQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, ForceQuantity)")

        # Calculus
        r("prop_deriv_v", "DerivativeExpression(?e), hasOperand(?e, ?s), hasResultMeasurement(?e, ?res), hasQuantityType(?s, LengthQuantity) -> hasQuantityType(?res, VelocityQuantity)")
        r("prop_deriv_a", "DerivativeExpression(?e), hasOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
        r("prop_int_s", "IntegralExpression(?e), hasOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, LengthQuantity)")

        # Transcendent
        r("prop_log", "LogarithmExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
        r("prop_ln",  "NaturalLogarithmExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
        r("prop_sin", "SineExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
        r("prop_cos", "CosineExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
        r("prop_tan", "TangentExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")

        # Power (only the dimensionless case; the rest goes through Python).
        r("prop_pow_dimensionless", "PowerExpression(?e), hasLeftOperand(?e, ?b), hasRightOperand(?e, ?x), hasResultMeasurement(?e, ?res), hasQuantityType(?b, DimensionlessQuantity), hasQuantityType(?x, DimensionlessQuantity) -> hasQuantityType(?res, DimensionlessQuantity)")

        # Fluid statics
        r("prop_area",     "MultiplicationExpression(?e), hasLeftOperand(?e, ?l1), hasRightOperand(?e, ?l2), hasResultMeasurement(?e, ?res), hasQuantityType(?l1, LengthQuantity), hasQuantityType(?l2, LengthQuantity) -> hasQuantityType(?res, AreaQuantity)")
        r("prop_volume",   "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?l), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AreaQuantity), hasQuantityType(?l, LengthQuantity) -> hasQuantityType(?res, VolumeQuantity)")
        r("prop_density",  "DivisionExpression(?e), hasLeftOperand(?e, ?m), hasRightOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?m, MassQuantity), hasQuantityType(?v, VolumeQuantity) -> hasQuantityType(?res, DensityQuantity)")
        r("prop_pressure", "DivisionExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?a), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?a, AreaQuantity) -> hasQuantityType(?res, PressureQuantity)")
        r("prop_force_from_pressure", "MultiplicationExpression(?e), hasLeftOperand(?e, ?p), hasRightOperand(?e, ?a), hasResultMeasurement(?e, ?res), hasQuantityType(?p, PressureQuantity), hasQuantityType(?a, AreaQuantity) -> hasQuantityType(?res, ForceQuantity)")

        # Error Checking
        r("err_add_q", "AdditionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasQuantityType(?l, ?q1), hasQuantityType(?r, ?q2), differentFrom(?q1, ?q2) -> QuantityIncompatibilityError(?e)")
        r("err_sub_q", "SubtractionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasQuantityType(?l, ?q1), hasQuantityType(?r, ?q2), differentFrom(?q1, ?q2) -> QuantityIncompatibilityError(?e)")
        r("err_unit_incomp", "BinaryExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasUnit(?l, ?u1), hasUnit(?r, ?u2), differentFrom(?u1, ?u2) -> UnitIncompatibilityError(?e)")
        r("err_sin_angle", "SineExpression(?e), hasOperand(?e, ?op), hasQuantityType(?op, ?q), differentFrom(?q, AngleQuantity) -> InvalidTrigonometryArgumentError(?e)")
        r("err_cos_angle", "CosineExpression(?e), hasOperand(?e, ?op), hasQuantityType(?op, ?q), differentFrom(?q, AngleQuantity) -> InvalidTrigonometryArgumentError(?e)")
        r("err_tan_angle", "TangentExpression(?e), hasOperand(?e, ?op), hasQuantityType(?op, ?q), differentFrom(?q, AngleQuantity) -> InvalidTrigonometryArgumentError(?e)")

    rules_onto.save("resources/physics-rules.owl")

if __name__ == "__main__":
    rebuild()
