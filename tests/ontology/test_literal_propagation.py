from __future__ import annotations
# Covers the rules that owlready can't express because they depend on a
# numeric literal (1/T, 0.5*E, L^2, ...).

import pytest
from owlready2 import sync_reasoner_pellet

from src.validator import propagate_literal_dependent_rules


def _build_division(world, ns_iri, l_value, l_quantity_name, r_quantity_name):
    """Create a DivisionExpression (l / r) in `world` and return res, hasQty."""
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    Div = world.search_one(iri="*#DivisionExpression")

    hasQty = world.search_one(iri="*#hasQuantityType")
    hasNumVal = world.search_one(iri="*#hasNumericValue")
    hasL = world.search_one(iri="*#hasLeftOperand")
    hasR = world.search_one(iri="*#hasRightOperand")
    hasRes = world.search_one(iri="*#hasResultMeasurement")

    LQ = world.search_one(iri=f"*#{l_quantity_name}") if l_quantity_name else None
    RQ = world.search_one(iri=f"*#{r_quantity_name}") if r_quantity_name else None

    with test_ns:
        l = Measurement("l_op")
        if l_value is not None:
            hasNumVal[l] = [l_value]
        if LQ is not None:
            hasQty[l] = [LQ]
        r = Measurement("r_op")
        if RQ is not None:
            hasQty[r] = [RQ]
        res = Measurement("res")
        op = Div("div_op")
        hasL[op] = [l]; hasR[op] = [r]; hasRes[op] = [res]
    return res, hasQty


def _build_multiplication(world, ns_iri, l_value, l_quantity_name, r_value, r_quantity_name):
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    Mul = world.search_one(iri="*#MultiplicationExpression")

    hasQty = world.search_one(iri="*#hasQuantityType")
    hasNumVal = world.search_one(iri="*#hasNumericValue")
    hasL = world.search_one(iri="*#hasLeftOperand")
    hasR = world.search_one(iri="*#hasRightOperand")
    hasRes = world.search_one(iri="*#hasResultMeasurement")

    LQ = world.search_one(iri=f"*#{l_quantity_name}") if l_quantity_name else None
    RQ = world.search_one(iri=f"*#{r_quantity_name}") if r_quantity_name else None

    with test_ns:
        l = Measurement("l_op")
        if l_value is not None:
            hasNumVal[l] = [l_value]
        if LQ is not None:
            hasQty[l] = [LQ]
        r = Measurement("r_op")
        if r_value is not None:
            hasNumVal[r] = [r_value]
        if RQ is not None:
            hasQty[r] = [RQ]
        res = Measurement("res")
        op = Mul("mul_op")
        hasL[op] = [l]; hasR[op] = [r]; hasRes[op] = [res]
    return res, hasQty


def test_prop_freq_one_over_time(isolated_world):
    """1.0 / Time -> FrequencyQuantity."""
    res, hasQty = _build_division(
        isolated_world, "http://test.org/lit/freq", 1.0, None, "TimeQuantity"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    FreqQ = isolated_world.search_one(iri="*#FrequencyQuantity")
    assert FreqQ in hasQty[res], (
        f"prop_freq did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_period_one_over_frequency(isolated_world):
    """1.0 / Frequency -> TimeQuantity."""
    res, hasQty = _build_division(
        isolated_world, "http://test.org/lit/period", 1.0, None, "FrequencyQuantity"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    TimeQ = isolated_world.search_one(iri="*#TimeQuantity")
    assert TimeQ in hasQty[res], (
        f"prop_period did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_h_attained_energy_over_acceleration(isolated_world):
    """Energy / Acceleration -> HeightQuantity (v² / 2g pattern)."""
    res, hasQty = _build_division(
        isolated_world, "http://test.org/lit/h", None, "EnergyQuantity", "AccelerationQuantity"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    HeightQ = isolated_world.search_one(iri="*#HeightQuantity")
    assert HeightQ in hasQty[res], (
        f"prop_h_attained did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_ke_half_times_energy_left(isolated_world):
    """0.5 * Energy -> EnergyQuantity (literal on the left)."""
    res, hasQty = _build_multiplication(
        isolated_world, "http://test.org/lit/ke_l",
        0.5, None, None, "EnergyQuantity"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    EnergyQ = isolated_world.search_one(iri="*#EnergyQuantity")
    assert EnergyQ in hasQty[res], (
        f"prop_ke (0.5 left) did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_ke_energy_times_half_right(isolated_world):
    """Energy * 0.5 -> EnergyQuantity (literal on the right)."""
    res, hasQty = _build_multiplication(
        isolated_world, "http://test.org/lit/ke_r",
        None, "EnergyQuantity", 0.5, None
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    EnergyQ = isolated_world.search_one(iri="*#EnergyQuantity")
    assert EnergyQ in hasQty[res], (
        f"prop_ke (0.5 right) did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def _build_power(world, ns_iri, base_quantity_name, exponent_value):
    """Create a PowerExpression (base^exp) where exp is a numeric literal."""
    test_ns = world.get_ontology(ns_iri)
    Measurement = world.search_one(iri="*#Measurement")
    Pow = world.search_one(iri="*#PowerExpression")

    hasQty = world.search_one(iri="*#hasQuantityType")
    hasNumVal = world.search_one(iri="*#hasNumericValue")
    hasL = world.search_one(iri="*#hasLeftOperand")
    hasR = world.search_one(iri="*#hasRightOperand")
    hasRes = world.search_one(iri="*#hasResultMeasurement")

    BaseQ = world.search_one(iri=f"*#{base_quantity_name}") if base_quantity_name else None

    with test_ns:
        base = Measurement("base_op")
        if BaseQ is not None:
            hasQty[base] = [BaseQ]
        exp = Measurement("exp_op")
        hasNumVal[exp] = [exponent_value]
        res = Measurement("res")
        op = Pow("pow_op")
        hasL[op] = [base]; hasR[op] = [exp]; hasRes[op] = [res]
    return res, hasQty


def test_prop_pow_length_2_yields_area(isolated_world):
    """Length^2 -> AreaQuantity."""
    res, hasQty = _build_power(
        isolated_world, "http://test.org/lit/pow_l2", "LengthQuantity", 2
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    AreaQ = isolated_world.search_one(iri="*#AreaQuantity")
    assert AreaQ in hasQty[res], (
        f"prop_pow_length_2 did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_pow_length_3_yields_volume(isolated_world):
    """Length^3 -> VolumeQuantity."""
    res, hasQty = _build_power(
        isolated_world, "http://test.org/lit/pow_l3", "LengthQuantity", 3
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    VolumeQ = isolated_world.search_one(iri="*#VolumeQuantity")
    assert VolumeQ in hasQty[res], (
        f"prop_pow_length_3 did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_pow_velocity_2_yields_specific_energy(isolated_world):
    """Velocity^2 -> SpecificEnergyQuantity (closes the loop with prop_v_sqrt)."""
    res, hasQty = _build_power(
        isolated_world, "http://test.org/lit/pow_v2", "VelocityQuantity", 2
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    SpecificEnergyQ = isolated_world.search_one(iri="*#SpecificEnergyQuantity")
    assert SpecificEnergyQ in hasQty[res], (
        f"prop_pow_velocity_2 did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_pow_time_2_yields_time_squared(isolated_world):
    """Time^2 -> TimeSquaredQuantity (auxiliary magnitude for ½·a·t²)."""
    res, hasQty = _build_power(
        isolated_world, "http://test.org/lit/pow_t2", "TimeQuantity", 2
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    TimeSquaredQ = isolated_world.search_one(iri="*#TimeSquaredQuantity")
    assert TimeSquaredQ in hasQty[res], (
        f"prop_pow_time_2 did not fire: result quantities are "
        f"{[q.name for q in hasQty[res]]}"
    )


def test_prop_pow_non_integer_exponent_does_not_fire(isolated_world):
    """Length^2.5 must NOT propagate as Area (only integer exponents covered)."""
    res, hasQty = _build_power(
        isolated_world, "http://test.org/lit/pow_l25", "LengthQuantity", 2.5
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)

    AreaQ = isolated_world.search_one(iri="*#AreaQuantity")
    assert AreaQ not in (hasQty[res] or []), (
        "prop_pow_length_2 fired on a non-integer exponent (2.5); it should not."
    )


def test_propagation_is_idempotent(isolated_world):
    """Calling propagate_literal_dependent_rules twice must not duplicate types."""
    res, hasQty = _build_division(
        isolated_world, "http://test.org/lit/idem", 1.0, None, "TimeQuantity"
    )
    sync_reasoner_pellet(isolated_world, infer_property_values=True)
    propagate_literal_dependent_rules(isolated_world)
    propagate_literal_dependent_rules(isolated_world)

    FreqQ = isolated_world.search_one(iri="*#FrequencyQuantity")
    assert qtys.count(FreqQ) == 1, (
        f"Expected FrequencyQuantity exactly once, got {len(qtys)} occurrences: "
        f"{[q.name for q in qtys]}"
    )
