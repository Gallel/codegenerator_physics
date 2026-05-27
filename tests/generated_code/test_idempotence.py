"""Idempotence (B7): emitting the same DSL twice produces identical Java."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from src.dsl_parser import map_dsl_to_ontology
from src.java_emitter import parse_dsl_to_java

from tests.conftest import (
    SYNTHETIC_DSL_DIR,
    _list_dsls,
    fixture_ids,
)


SYNTHETIC_DSLS = _list_dsls(SYNTHETIC_DSL_DIR)


@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_emitter_is_idempotent(dsl_path: Path, tmp_path: Path):
    out_a = tmp_path / "a"; out_a.mkdir()
    out_b = tmp_path / "b"; out_b.mkdir()

    staged_a = out_a / dsl_path.name
    staged_b = out_b / dsl_path.name
    shutil.copy2(dsl_path, staged_a)
    shutil.copy2(dsl_path, staged_b)

    map_dsl_to_ontology(staged_a, out_a / f"{dsl_path.stem}.owl")
    map_dsl_to_ontology(staged_b, out_b / f"{dsl_path.stem}.owl")

    java_a = Path(parse_dsl_to_java(staged_a)).read_text(encoding="utf-8")
    java_b = Path(parse_dsl_to_java(staged_b)).read_text(encoding="utf-8")

    assert java_a == java_b, (
        f"Emitter is not idempotent for {dsl_path.name}; "
        f"this would break snapshot-based regression tests."
    )
