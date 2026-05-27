# Each row in BINARY_RULES / UNARY_RULES drives one parametric test that
# fires the matching SWRL rule in an isolated world.
from __future__ import annotations

import pytest
from owlready2 import sync_reasoner_pellet


BINARY_RULES = [
    ("prop_mult_at",   "MultiplicationExpression", ["AccelerationQuantity", "TimeQuantity"],          "VelocityQuantity"),
    ("prop_mult_vt",   "MultiplicationExpression", ["VelocityQuantity",     "TimeQuantity"],          "DisplacementQuantity"),
    ("prop_v_wR",      "MultiplicationExpression", ["AngularVelocityQuantity", "LengthQuantity"],     "VelocityQuantity"),
    ("prop_at_alphaR", "MultiplicationExpression", ["AngularAccelerationQuantity", "LengthQuantity"], "AccelerationQuantity"),
    ("prop_force",     "MultiplicationExpression", ["MassQuantity", "AccelerationQuantity"],          "ForceQuantity"),
    ("prop_momentum",  "MultiplicationExpression", ["MassQuantity", "VelocityQuantity"],              "MomentumQuantity"),
    ("prop_work",      "MultiplicationExpression", ["ForceQuantity", "LengthQuantity"],               "EnergyQuantity"),
    ("prop_impulse",   "MultiplicationExpression", ["ForceQuantity", "TimeQuantity"],                 "MomentumQuantity"),
    ("prop_power",     "DivisionExpression",       ["EnergyQuantity", "TimeQuantity"],                "PowerQuantity"),
    ("prop_w",         "DivisionExpression",       ["AngleQuantity", "TimeQuantity"],                 "AngularVelocityQuantity"),
    ("prop_alpha",     "DivisionExpression",       ["AngularVelocityQuantity", "TimeQuantity"],       "AngularAccelerationQuantity"),
    ("prop_v_pm",      "DivisionExpression",       ["MomentumQuantity", "MassQuantity"],              "VelocityQuantity"),
    ("prop_friction",  "MultiplicationExpression", ["FrictionCoefficientQuantity", "ForceQuantity"], "ForceQuantity"),
    ("prop_accel_from_force", "DivisionExpression", ["ForceQuantity", "MassQuantity"],                "AccelerationQuantity"),
    ("prop_energy_from_specific", "MultiplicationExpression", ["SpecificEnergyQuantity", "MassQuantity"], "EnergyQuantity"),
    ("prop_grav_field",       "DivisionExpression",       ["GravitationalParameterQuantity", "AreaQuantity"], "AccelerationQuantity"),
    ("prop_force_from_accel", "MultiplicationExpression", ["AccelerationQuantity", "MassQuantity"],           "ForceQuantity"),
    ("prop_force_from_impulse", "DivisionExpression",     ["MomentumQuantity", "TimeQuantity"],              "ForceQuantity"),
    # Fluid statics
    ("prop_area",      "MultiplicationExpression", ["LengthQuantity", "LengthQuantity"],              "AreaQuantity"),
    ("prop_volume",    "MultiplicationExpression", ["AreaQuantity", "LengthQuantity"],                "VolumeQuantity"),
    ("prop_density",   "DivisionExpression",       ["MassQuantity", "VolumeQuantity"],                "DensityQuantity"),
    ("prop_pressure",  "DivisionExpression",       ["ForceQuantity", "AreaQuantity"],                 "PressureQuantity"),
    ("prop_force_from_pressure", "MultiplicationExpression", ["PressureQuantity", "AreaQuantity"],     "ForceQuantity"),
    # Dimensionless^dimensionless. The exponent-aware power cases live in
    # tests/ontology/test_literal_propagation.py.
    ("prop_pow_dimensionless", "PowerExpression", ["DimensionlessQuantity", "DimensionlessQuantity"], "DimensionlessQuantity"),
]

UNARY_RULES = [
    ("prop_deriv_v",   "DerivativeExpression", "LengthQuantity",   "VelocityQuantity"),
    ("prop_deriv_a",   "DerivativeExpression", "VelocityQuantity", "AccelerationQuantity"),
    ("prop_int_s",     "IntegralExpression",   "VelocityQuantity", "LengthQuantity"),
    ("prop_v_sqrt",    "SqrtExpression",       "SpecificEnergyQuantity", "VelocityQuantity"),
    ("prop_sin",       "SineExpression",       "AngleQuantity",    "DimensionlessQuantity"),
    ("prop_cos",       "CosineExpression",     "AngleQuantity",    "DimensionlessQuantity"),
    ("prop_tan",       "TangentExpression",            "AngleQuantity",        "DimensionlessQuantity"),
    ("prop_ln",        "NaturalLogarithmExpression",   "DimensionlessQuantity", "DimensionlessQuantity"),
]


def _build_binary(world, op_cls_name, qty_names, ns_iri):
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    OpCls = world.search_one(iri=f"*#{op_cls_name}")
    QL = world.search_one(iri=f"*#{qty_names[0]}")
    QR = world.search_one(iri=f"*#{qty_names[1]}")

    hasQuantityType = world.search_one(iri="*#hasQuantityType")
    hasLeftOperand = world.search_one(iri="*#hasLeftOperand")
    hasRightOperand = world.search_one(iri="*#hasRightOperand")
    hasResultMeasurement = world.search_one(iri="*#hasResultMeasurement")

    with test_ns:
        l = Measurement("l_op")
        r = Measurement("r_op")
        res = Measurement("res")
        op = OpCls("op")
        hasQuantityType[l] = [QL]
        hasQuantityType[r] = [QR]
        hasLeftOperand[op] = [l]
        hasRightOperand[op] = [r]
        hasResultMeasurement[op] = [res]
    return res, hasQuantityType


def _build_unary(world, op_cls_name, qty_name, ns_iri):
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    OpCls = world.search_one(iri=f"*#{op_cls_name}")
    QIn = world.search_one(iri=f"*#{qty_name}")

    hasQuantityType = world.search_one(iri="*#hasQuantityType")
    hasOperand = world.search_one(iri="*#hasOperand")
    hasResultMeasurement = world.search_one(iri="*#hasResultMeasurement")

    with test_ns:
        operand = Measurement("op_in")
        res = Measurement("res")
        op = OpCls("op")
        hasQuantityType[operand] = [QIn]
        hasOperand[op] = [operand]
        hasResultMeasurement[op] = [res]
    return res, hasQuantityType


@pytest.mark.parametrize(
    "rule_id, op_cls, qtys, expected", BINARY_RULES,
    ids=[r[0] for r in BINARY_RULES],
)
def test_binary_rule_propagates(isolated_world, rule_id, op_cls, qtys, expected):
    res, hasQty = _build_binary(
        isolated_world, op_cls, qtys,
        f"http://test.org/swrl_prop/{rule_id}",
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)

    expected_cls = isolated_world.search_one(iri=f"*#{expected}")
    assert expected_cls is not None, f"Expected class {expected} missing in ontology."
    assert expected_cls in hasQty[res], (
        f"Rule {rule_id}: expected {expected} on result, got {[q.name for q in hasQty[res]]}"
    )


@pytest.mark.parametrize(
    "rule_id, op_cls, qty, expected", UNARY_RULES,
    ids=[r[0] for r in UNARY_RULES],
)
def test_unary_rule_propagates(isolated_world, rule_id, op_cls, qty, expected):
    res, hasQty = _build_unary(
        isolated_world, op_cls, qty,
        f"http://test.org/swrl_prop/{rule_id}",
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)

    expected_cls = isolated_world.search_one(iri=f"*#{expected}")
    assert expected_cls is not None, f"Expected class {expected} missing in ontology."
    assert expected_cls in hasQty[res], (
        f"Rule {rule_id}: expected {expected} on result, got {[q.name for q in hasQty[res]]}"
    )


def test_cascade_acceleration_time_time_yields_displacement(isolated_world):
    """a * t = Velocity (prop_mult_at), then Velocity * t = Displacement (prop_mult_vt)."""
    test_ns = isolated_world.get_ontology("http://test.org/swrl_prop/cascade_at2")
    Measurement = isolated_world.search_one(iri="*#Measurement")
    Mul = isolated_world.search_one(iri="*#MultiplicationExpression")
    AccelQ = isolated_world.search_one(iri="*#AccelerationQuantity")
    TimeQ = isolated_world.search_one(iri="*#TimeQuantity")
    DispQ = isolated_world.search_one(iri="*#DisplacementQuantity")

    hasQty = isolated_world.search_one(iri="*#hasQuantityType")
    hasL = isolated_world.search_one(iri="*#hasLeftOperand")
    hasR = isolated_world.search_one(iri="*#hasRightOperand")
    hasRes = isolated_world.search_one(iri="*#hasResultMeasurement")

    with test_ns:
        a = Measurement("a"); hasQty[a] = [AccelQ]
        t = Measurement("t"); hasQty[t] = [TimeQ]
        m1 = Mul("m1"); res1 = Measurement("res_at")
        hasL[m1] = [a]; hasR[m1] = [t]; hasRes[m1] = [res1]
        m2 = Mul("m2"); res2 = Measurement("res_att")
        hasL[m2] = [res1]; hasR[m2] = [t]; hasRes[m2] = [res2]

    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    assert DispQ in hasQty[res2], (
        f"Expected DisplacementQuantity, got {[q.name for q in hasQty[res2]]}"
    )



def test_assignment_propagates_quantity(isolated_world):
    """prop_assign: a := b copies b's quantity type onto a."""
    test_ns = isolated_world.get_ontology("http://test.org/swrl_prop/assign")
    Measurement = isolated_world.search_one(iri="*#Measurement")
    Assign = isolated_world.search_one(iri="*#AssignmentOperation")
    VelQ = isolated_world.search_one(iri="*#VelocityQuantity")

    hasQty = isolated_world.search_one(iri="*#hasQuantityType")
    hasL = isolated_world.search_one(iri="*#hasLeftOperand")
    hasR = isolated_world.search_one(iri="*#hasRightOperand")
    hasRes = isolated_world.search_one(iri="*#hasResultMeasurement")

    with test_ns:
        src = Measurement("src"); hasQty[src] = [VelQ]
        dst = Measurement("dst")
        op = Assign("assign_op")
        hasL[op] = [dst]; hasR[op] = [src]; hasRes[op] = [dst]

    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    assert VelQ in hasQty[dst], (
        f"Assignment should have propagated VelocityQuantity from src to dst, "
        f"got {[q.name for q in hasQty[dst]]}"
    )
