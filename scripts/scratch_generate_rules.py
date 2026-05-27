from owlready2 import *
import os

onto_path.append('resources')

domain_onto = get_ontology('http://example.org/physics/physics-domain').load()
math_onto = get_ontology('http://example.org/physics/physics-math').load()
physics_ns = math_onto.get_namespace('http://example.org/physics#')

rule_onto = get_ontology('http://example.org/physics/physics-rules')

with rule_onto:
    # --- ERROR CLASSES ---
    if "PhysicsError" not in [c.name for c in rule_onto.classes()]:
        class PhysicsError(Thing): pass
        class DimensionalInconsistencyError(PhysicsError): pass
        class UnitIncompatibilityError(PhysicsError): pass
        class QuantityIncompatibilityError(PhysicsError): pass
        class DimensionMismatchError(PhysicsError): pass
        class InvalidTrigonometryArgumentError(PhysicsError): pass
    else:
        PhysicsError = rule_onto.PhysicsError
        QuantityIncompatibilityError = rule_onto.QuantityIncompatibilityError

    def add_rule(name, rule_str):
        r = Imp()
        r.set_as_rule(rule_str, namespaces=[math_onto, domain_onto, rule_onto, physics_ns])
        return r

    # 1. CORE ARITHMETIC (Generic propagation)
    add_rule("prop_add", "AdditionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?l, ?q), hasQuantityType(?r, ?q) -> hasQuantityType(?res, ?q)")
    add_rule("prop_sub", "SubtractionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?l, ?q), hasQuantityType(?r, ?q) -> hasQuantityType(?res, ?q)")
    
    # 2. SCALARS & TRIG
    add_rule("prop_mult_scalar_l", "MultiplicationExpression(?e), hasLeftOperand(?e, ?s), hasRightOperand(?e, ?q), hasResultMeasurement(?e, ?res), hasQuantityType(?s, DimensionlessQuantity), hasQuantityType(?q, ?t) -> hasQuantityType(?res, ?t)")
    add_rule("prop_mult_scalar_r", "MultiplicationExpression(?e), hasLeftOperand(?e, ?q), hasRightOperand(?e, ?s), hasResultMeasurement(?e, ?res), hasQuantityType(?s, DimensionlessQuantity), hasQuantityType(?q, ?t) -> hasQuantityType(?res, ?t)")
    add_rule("prop_div_scalar", "DivisionExpression(?e), hasLeftOperand(?e, ?q), hasRightOperand(?e, ?s), hasResultMeasurement(?e, ?res), hasQuantityType(?s, DimensionlessQuantity), hasQuantityType(?q, ?t) -> hasQuantityType(?res, ?t)")
    add_rule("prop_sin", "SineExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
    add_rule("prop_cos", "CosineExpression(?e), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, DimensionlessQuantity)")
    
    # Angle from arc/radius
    add_rule("prop_theta_sR", "DivisionExpression(?e), hasLeftOperand(?e, ?s), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?s, LengthQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, AngleQuantity)")


    # 3. KINEMATICS (Linear)
    add_rule("prop_v_st", "DivisionExpression(?e), hasLeftOperand(?e, ?s), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?s, LengthQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_a_vt", "DivisionExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
    add_rule("prop_s_vt", "MultiplicationExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, LengthQuantity)")
    add_rule("prop_v_at", "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AccelerationQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_as_spec", "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?s), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AccelerationQuantity), hasQuantityType(?s, LengthQuantity) -> hasQuantityType(?res, SpecificEnergyQuantity)")
    add_rule("prop_v2_spec", "PowerExpression(?e), hasLeftOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, SpecificEnergyQuantity)")
    
    # Frequency & Period
    add_rule("prop_f_t", "DivisionExpression(?e), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, FrequencyQuantity)")
    add_rule("prop_t_f", "DivisionExpression(?e), hasRightOperand(?e, ?f), hasResultMeasurement(?e, ?res), hasQuantityType(?f, FrequencyQuantity) -> hasQuantityType(?res, TimeQuantity)")

    # 4. KINEMATICS (Circular/Angular)
    add_rule("prop_w_thetat", "DivisionExpression(?e), hasLeftOperand(?e, ?th), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?th, AngleQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularVelocityQuantity)")
    add_rule("prop_alpha_wt", "DivisionExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?w, AngularVelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularAccelerationQuantity)")
    add_rule("prop_theta_wt", "MultiplicationExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?w, AngularVelocityQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngleQuantity)")
    add_rule("prop_w_alphat", "MultiplicationExpression(?e), hasLeftOperand(?e, ?a), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?a, AngularAccelerationQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularVelocityQuantity)")
    add_rule("prop_w_t", "DivisionExpression(?e), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, AngularVelocityQuantity)")
    
    # MCU Bridge
    add_rule("prop_v_wR", "MultiplicationExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?w, AngularVelocityQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_w_f", "MultiplicationExpression(?e), hasLeftOperand(?e, ?f), hasQuantityType(?f, FrequencyQuantity), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, AngularVelocityQuantity)")
    add_rule("prop_ac_v2r", "DivisionExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
    add_rule("prop_ac_vw", "MultiplicationExpression(?e), hasLeftOperand(?e, ?v), hasRightOperand(?e, ?w), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity), hasQuantityType(?w, AngularVelocityQuantity) -> hasQuantityType(?res, AccelerationQuantity)")

    # 5. DYNAMICS, ENERGY & MOMENTUM
    add_rule("prop_f_ma", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m), hasRightOperand(?e, ?a), hasResultMeasurement(?e, ?res), hasQuantityType(?m, MassQuantity), hasQuantityType(?a, AccelerationQuantity) -> hasQuantityType(?res, ForceQuantity)")
    add_rule("prop_p_mv", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m), hasRightOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?m, MassQuantity), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, MomentumQuantity)")
    add_rule("prop_v_rt", "DivisionExpression(?e), hasLeftOperand(?e, ?r), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?r, LengthQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_ek_p2m", "DivisionExpression(?e), hasLeftOperand(?e, ?p), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?p, MomentumQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, EnergyQuantity)") # Simplified cascade trigger for p^2/2m
    add_rule("prop_spec_e_ratio", "DivisionExpression(?e), hasLeftOperand(?e, ?en), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?en, EnergyQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, SpecificEnergyQuantity)")
    add_rule("prop_e_from_spec", "MultiplicationExpression(?e), hasLeftOperand(?e, ?se), hasRightOperand(?e, ?m), hasResultMeasurement(?e, ?res), hasQuantityType(?se, SpecificEnergyQuantity), hasQuantityType(?m, MassQuantity) -> hasQuantityType(?res, EnergyQuantity)")
    add_rule("prop_i_ft", "MultiplicationExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, MomentumQuantity)")
    add_rule("prop_w_fd", "MultiplicationExpression(?e), hasLeftOperand(?e, ?f), hasRightOperand(?e, ?d), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity), hasQuantityType(?d, LengthQuantity) -> hasQuantityType(?res, EnergyQuantity)")
    add_rule("prop_p_wt", "DivisionExpression(?e), hasLeftOperand(?e, ?w), hasRightOperand(?e, ?t), hasResultMeasurement(?e, ?res), hasQuantityType(?w, EnergyQuantity), hasQuantityType(?t, TimeQuantity) -> hasQuantityType(?res, PowerQuantity)")
    
    # Work Integral
    add_rule("prop_w_integral", "IntegralExpression(?e), hasOperand(?e, ?f), hasResultMeasurement(?e, ?res), hasQuantityType(?f, ForceQuantity) -> hasQuantityType(?res, EnergyQuantity)")
    
    # CALCULUS
    add_rule("prop_deriv_v", "DerivativeExpression(?e), hasOperand(?e, ?s), hasResultMeasurement(?e, ?res), hasQuantityType(?s, LengthQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_deriv_a", "DerivativeExpression(?e), hasOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, AccelerationQuantity)")
    add_rule("prop_deriv_p", "DerivativeExpression(?e), hasOperand(?e, ?w), hasResultMeasurement(?e, ?res), hasQuantityType(?w, EnergyQuantity) -> hasQuantityType(?res, PowerQuantity)")
    add_rule("prop_integ_s", "IntegralExpression(?e), hasOperand(?e, ?v), hasResultMeasurement(?e, ?res), hasQuantityType(?v, VelocityQuantity) -> hasQuantityType(?res, LengthQuantity)")
    
    # 7. GRAVITATION
    # F_grav = G * m1 * m2 / r^2. Simplification: m * m / r^2 -> Force if we imply G's dimensions.
    # In practice, we can map (m * m / r^2) * DimensionlessG -> Force.
    add_rule("prop_f_grav", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m1), hasQuantityType(?m1, MassQuantity), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, ForceQuantity)") # Simplified trigger
    
    # mu = G * M
    add_rule("prop_mu_gm", "MultiplicationExpression(?e), hasLeftOperand(?e, ?m), hasQuantityType(?m, MassQuantity), hasResultMeasurement(?e, ?res) -> hasQuantityType(?res, GravitationalParameterQuantity)")
    
    # g = GM/r^2
    add_rule("prop_g_field", "DivisionExpression(?e), hasLeftOperand(?e, ?mu), hasResultMeasurement(?e, ?res), hasQuantityType(?mu, GravitationalParameterQuantity) -> hasQuantityType(?res, AccelerationQuantity)") # Simplified trigger for mu/r^2


    add_rule("prop_v_circ_sqrt", "SqrtExpression(?e), hasOperand(?e, ?op), hasResultMeasurement(?e, ?res), hasQuantityType(?op, SpecificEnergyQuantity) -> hasQuantityType(?res, VelocityQuantity)")
    add_rule("prop_e_spec", "DivisionExpression(?e), hasLeftOperand(?e, ?mu), hasRightOperand(?e, ?r), hasResultMeasurement(?e, ?res), hasQuantityType(?mu, GravitationalParameterQuantity), hasQuantityType(?r, LengthQuantity) -> hasQuantityType(?res, SpecificEnergyQuantity)")

    # 8. ERROR DETECTION (Negative Rules)
    add_rule("err_add_quant", "AdditionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasQuantityType(?l, ?q1), hasQuantityType(?r, ?q2), differentFrom(?q1, ?q2) -> QuantityIncompatibilityError(?e)")
    add_rule("err_sub_quant", "SubtractionExpression(?e), hasLeftOperand(?e, ?l), hasRightOperand(?e, ?r), hasQuantityType(?l, ?q1), hasQuantityType(?r, ?q2), differentFrom(?q1, ?q2) -> QuantityIncompatibilityError(?e)")
    add_rule("err_trig_quant", "SineExpression(?e), hasOperand(?e, ?op), hasQuantityType(?op, ?q), differentFrom(?q, AngleQuantity) -> InvalidTrigonometryArgumentError(?e)")



rule_onto.save(file=os.path.join('resources', 'physics-rules.owl'))
print("physics-rules.owl updated with all requested Bachillerato formulas.")
