# Ontology invariants. These should pass regardless of which problem is loaded.
from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.settings import PHYSICS_DOMAIN_OWL, MATH_OWL, PHYSICS_RULES_OWL


def _quantities_declared_in(world):
    PhysicalQuantity = world.search_one(iri="*#PhysicalQuantity")
    if PhysicalQuantity is None:
        return set()
    return {ind.name for ind in world.search(type=PhysicalQuantity)}


def _rules_text(world):
    return [str(r) for r in world.rules()]


def _quantities_in_any_rule(rule_strings):
    found = set()
    for rule in rule_strings:
        for match in re.finditer(r'([A-Z][A-Za-z]*Quantity)', rule):
            found.add(match.group(1))
    return found


# Unit / conversion factor invariants

def test_every_unit_has_positive_si_conversion(isolated_world):
    Unit = isolated_world.search_one(iri="*#Unit")
    assert Unit is not None, "Unit class not present in ontology."
    units = list(Unit.instances())
    assert units, "No Unit individuals declared."
    for u in units:
        factors = list(u.hasConversionFactorToSI or [])
        assert factors, f"Unit {u.name} has no hasConversionFactorToSI."
        assert factors[0] > 0, f"Unit {u.name} has non-positive SI factor: {factors[0]}"


# Constants

CONSTANT_NAMES = [
    "Pi", "StandardGravity", "UniversalGravitationalConstant", "SpeedOfLight",
    "AstronomicalUnit", "Day", "JulianYear",
    "StandardAtmosphericPressure", "StandardWaterDensity", "StandardAirDensity",
]
CELESTIAL_BODIES = ["Earth", "Moon", "Mars", "Sun", "Jupiter"]


@pytest.mark.parametrize("name", CONSTANT_NAMES)
def test_universal_constant_has_value(isolated_world, name):
    c = isolated_world.search_one(iri=f"*#{name}")
    assert c is not None, f"Constant {name} not declared in ontology."
    values = list(c.hasNumericValue or [])
    assert values, f"Constant {name} has no hasNumericValue."
    assert isinstance(values[0], (int, float)), f"Constant {name} value is not numeric: {values[0]!r}"


@pytest.mark.parametrize("body", CELESTIAL_BODIES)
def test_celestial_body_has_radius_and_mu(isolated_world, body):
    radius = isolated_world.search_one(iri=f"*#{body}_MeanRadius")
    mu = isolated_world.search_one(iri=f"*#{body}_GravitationalParameter")
    assert radius is not None, f"{body}_MeanRadius missing."
    assert mu is not None, f"{body}_GravitationalParameter missing."
    assert radius.hasNumericValue, f"{body}_MeanRadius has no value."
    assert mu.hasNumericValue, f"{body}_GravitationalParameter has no value."


# Error taxonomy

def test_error_taxonomy(isolated_world):
    PhysicsError = isolated_world.search_one(iri="*#PhysicsError")
    assert PhysicsError is not None
    expected = [
        "QuantityIncompatibilityError",
        "UnitIncompatibilityError",
        "DimensionMismatchError",
        "InvalidTrigonometryArgumentError",
    ]
    declared_subclasses = {c.name for c in PhysicsError.subclasses()}
    for err in expected:
        assert err in declared_subclasses, (
            f"{err} should be a subclass of PhysicsError "
            f"(found subclasses: {sorted(declared_subclasses)})."
        )


# Expression hierarchy

EXPRESSION_SUBCLASSES = [
    "AdditionExpression", "SubtractionExpression", "MultiplicationExpression",
    "DivisionExpression", "PowerExpression", "AssignmentOperation",
    "SqrtExpression", "SineExpression", "CosineExpression", "TangentExpression",
    "DerivativeExpression", "IntegralExpression",
    "LogarithmExpression", "NaturalLogarithmExpression",
]


@pytest.mark.parametrize("name", EXPRESSION_SUBCLASSES)
def test_expression_hierarchy(isolated_world, name):
    cls = isolated_world.search_one(iri=f"*#{name}")
    assert cls is not None, f"{name} not declared."
    Expression = isolated_world.search_one(iri="*#Expression")
    assert Expression is not None
    ancestor_names = {a.name for a in cls.ancestors() if hasattr(a, "name")}
    assert "Expression" in ancestor_names, (
        f"{name} is not in the Expression hierarchy (ancestors={sorted(ancestor_names)})."
    )


