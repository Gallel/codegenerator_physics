"""For every fixture in tests/fixtures/invalid_dsls/, run_validation must
return at least one error and that error must mention the expected class.

Each fixture carries an `expected_error` field at the top level (a marker
string, not a real ontology class) that we check against the error labels
returned by the validator. This keeps the assertion declarative and lets us
add new invalid fixtures without modifying the test code.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from src.dsl_parser import map_dsl_to_ontology
from src.validator import run_validation

from tests.conftest import (
    INVALID_DSL_DIR,
    _list_dsls,
    fixture_ids,
    load_dsl,
)


INVALID_DSLS = _list_dsls(INVALID_DSL_DIR)


def _strip_marker_field(dsl_path: Path, workdir: Path) -> tuple[Path, str]:
    """Copy the fixture into workdir, strip the meta `expected_error` field
    (the rest of the pipeline doesn't expect it) and return the staged path
    plus the expected_error marker."""
    raw = load_dsl(dsl_path)
    expected = raw.pop("expected_error", "")
    staged = workdir / dsl_path.name
    staged.write_text(json.dumps(raw), encoding="utf-8")
    return staged, expected


@pytest.mark.parametrize("dsl_path", INVALID_DSLS, ids=fixture_ids(INVALID_DSLS))
def test_invalid_dsl_is_rejected(dsl_path: Path, dsl_workdir: Path):
    staged, expected_marker = _strip_marker_field(dsl_path, dsl_workdir)
    assert expected_marker, (
        f"{dsl_path.name} is missing the `expected_error` field; please tag it."
    )

    owl_path = dsl_workdir / f"{dsl_path.stem}.owl"
    map_dsl_to_ontology(staged, owl_path)

    errors = run_validation(staged, dsl_workdir, owl_path)
    assert errors, f"{dsl_path.name} should have produced at least one error."

    labels = [str(label) for label, _ in errors]
    assert any(expected_marker in lbl for lbl in labels), (
        f"{dsl_path.name}: expected marker {expected_marker!r} in any of {labels}"
    )
