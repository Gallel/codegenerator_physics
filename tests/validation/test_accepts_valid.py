"""For every fixture in tests/fixtures/valid_dsls/, run_validation must
produce zero errors. These fixtures are the structural counterparts of the
invalid ones: same shape, but with consistent quantities/units.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from src.dsl_parser import map_dsl_to_ontology
from src.validator import run_validation

from tests.conftest import (
    VALID_DSL_DIR,
    _list_dsls,
    fixture_ids,
)


VALID_DSLS = _list_dsls(VALID_DSL_DIR)


@pytest.mark.parametrize("dsl_path", VALID_DSLS, ids=fixture_ids(VALID_DSLS))
def test_valid_dsl_is_accepted(dsl_path: Path, dsl_workdir: Path):
    staged = dsl_workdir / dsl_path.name
    shutil.copy2(dsl_path, staged)

    owl_path = dsl_workdir / f"{dsl_path.stem}.owl"
    map_dsl_to_ontology(staged, owl_path)

    errors = run_validation(staged, dsl_workdir, owl_path)
    assert errors == [], (
        f"{dsl_path.name} should have validated cleanly; got errors: "
        f"{[lbl for lbl, _ in errors]}"
    )
