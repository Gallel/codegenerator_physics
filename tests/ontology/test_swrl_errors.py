from __future__ import annotations
# err_* SWRL rules: each pattern is checked with a positive and a negative case.

import pytest
from owlready2 import sync_reasoner_pellet, AllDisjoint


QUANTITY_INCOMP = [
    ("force_plus_time",   "AdditionExpression",    ["ForceQuantity", "TimeQuantity"],     True,  "QuantityIncompatibilityError"),
    ("mass_minus_length", "SubtractionExpression", ["MassQuantity", "LengthQuantity"],    True,  "QuantityIncompatibilityError"),
    ("force_plus_force",  "AdditionExpression",    ["ForceQuantity", "ForceQuantity"],    False, "QuantityIncompatibilityError"),
    ("mass_minus_mass",   "SubtractionExpression", ["MassQuantity", "MassQuantity"],      False, "QuantityIncompatibilityError"),
]

TRIG_OF_ANGLE = [
    ("sin_of_mass",   "SineExpression",    "MassQuantity",  True,  "InvalidTrigonometryArgumentError"),
    ("sin_of_angle",  "SineExpression",    "AngleQuantity", False, "InvalidTrigonometryArgumentError"),
    ("cos_of_mass",   "CosineExpression",  "MassQuantity",  True,  "InvalidTrigonometryArgumentError"),
    ("cos_of_angle",  "CosineExpression",  "AngleQuantity", False, "InvalidTrigonometryArgumentError"),
    ("tan_of_mass",   "TangentExpression", "MassQuantity",  True,  "InvalidTrigonometryArgumentError"),
    ("tan_of_angle",  "TangentExpression", "AngleQuantity", False, "InvalidTrigonometryArgumentError"),
]


def _build_binary_with_disjointness(world, op_cls_name, qty_names, ns_iri):
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    OpCls = world.search_one(iri=f"*#{op_cls_name}")
    QL = world.search_one(iri=f"*#{qty_names[0]}")
    QR = world.search_one(iri=f"*#{qty_names[1]}")

    hasQty = world.search_one(iri="*#hasQuantityType")
    hasL = world.search_one(iri="*#hasLeftOperand")
    hasR = world.search_one(iri="*#hasRightOperand")

    with test_ns:
        if QL != QR:
            AllDisjoint([QL, QR])
        l = Measurement("l"); hasQty[l] = [QL]
        r = Measurement("r"); hasQty[r] = [QR]
        op = OpCls("op")
        hasL[op] = [l]; hasR[op] = [r]
    return op


def _build_trig(world, op_cls_name, qty_name, ns_iri):
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    OpCls = world.search_one(iri=f"*#{op_cls_name}")
    QIn = world.search_one(iri=f"*#{qty_name}")
    AngleQ = world.search_one(iri="*#AngleQuantity")

    hasQty = world.search_one(iri="*#hasQuantityType")
    hasOp = world.search_one(iri="*#hasOperand")

    with test_ns:
        if QIn != AngleQ:
            AllDisjoint([QIn, AngleQ])
        operand = Measurement("op_in"); hasQty[operand] = [QIn]
        op = OpCls("op")
        hasOp[op] = [operand]
    return op


@pytest.mark.parametrize(
    "label, op_cls, qtys, should_trigger, err_cls", QUANTITY_INCOMP,
    ids=[c[0] for c in QUANTITY_INCOMP],
)
def test_quantity_incompatibility(isolated_world, label, op_cls, qtys, should_trigger, err_cls):
    op = _build_binary_with_disjointness(
        isolated_world, op_cls, qtys, f"http://test.org/swrl_err/{label}"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)

    ErrCls = isolated_world.search_one(iri=f"*#{err_cls}")
    assert ErrCls is not None
    triggered = op in list(ErrCls.instances())
    if should_trigger:
        assert triggered, f"{err_cls} should have fired on {label} but did not."
    else:
        assert not triggered, f"{err_cls} should NOT fire on {label} but did."


@pytest.mark.parametrize(
    "label, op_cls, qty, should_trigger, err_cls", TRIG_OF_ANGLE,
    ids=[c[0] for c in TRIG_OF_ANGLE],
)
def test_trig_of_angle(isolated_world, label, op_cls, qty, should_trigger, err_cls):
    op = _build_trig(
        isolated_world, op_cls, qty, f"http://test.org/swrl_err/{label}"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)

    ErrCls = isolated_world.search_one(iri=f"*#{err_cls}")
    assert ErrCls is not None
    triggered = op in list(ErrCls.instances())
    if should_trigger:
        assert triggered, f"{err_cls} should have fired on {label} but did not."
    else:
        assert not triggered, f"{err_cls} should NOT have fired on {label}."
