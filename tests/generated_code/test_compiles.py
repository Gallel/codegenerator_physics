"""For every synthetic DSL fixture, the emitted Java must compile (B2)."""
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
    compile_java,
    JAVA_AVAILABLE,
)


SYNTHETIC_DSLS = _list_dsls(SYNTHETIC_DSL_DIR)


@pytest.mark.skipif(not JAVA_AVAILABLE, reason="JDK not installed.")
@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_synthetic_dsl_compiles(dsl_path: Path, dsl_workdir: Path):
    # Stage the fixture next to a fresh working dir so the emitter can write
    # `<class>.java` next to the JSON.
    staged = dsl_workdir / dsl_path.name
    shutil.copy2(dsl_path, staged)

    # Build the program ontology once (validation is not asserted here; that
    # is what tests/validation does). We run it because the parser creates an
    # OWL artifact that some downstream pipelines depend on.
    map_dsl_to_ontology(staged, dsl_workdir / f"{dsl_path.stem}.owl")

    java_file = parse_dsl_to_java(staged)
    assert Path(java_file).exists(), f"Emitter did not produce a .java for {dsl_path.name}"

    result = compile_java(Path(java_file), dsl_workdir)
    assert result.returncode == 0, (
        f"javac failed for {dsl_path.name}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
