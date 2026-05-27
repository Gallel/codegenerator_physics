"""For every synthetic DSL fixture, the emitted Java must:
  * compile and run without raising (B3),
  * emit valid JSON to stdout (B4),
  * include exactly the keys listed in `results_to_print` (B5).
"""
from __future__ import annotations

import json
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
    run_java,
    load_dsl,
    JAVA_AVAILABLE,
)


SYNTHETIC_DSLS = _list_dsls(SYNTHETIC_DSL_DIR)


@pytest.mark.skipif(not JAVA_AVAILABLE, reason="JDK not installed.")
@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_synthetic_dsl_runs_and_emits_valid_json(dsl_path: Path, dsl_workdir: Path):
    dsl = load_dsl(dsl_path)
    staged = dsl_workdir / dsl_path.name
    shutil.copy2(dsl_path, staged)

    map_dsl_to_ontology(staged, dsl_workdir / f"{dsl_path.stem}.owl")
    java_file = Path(parse_dsl_to_java(staged))

    compile_result = compile_java(java_file, dsl_workdir)
    assert compile_result.returncode == 0, (
        f"javac failed for {dsl_path.name}: {compile_result.stderr}"
    )

    class_name = dsl["metadata"]["name"]
    run_result = run_java(class_name, dsl_workdir)
    assert run_result.returncode == 0, (
        f"java {class_name} failed (returncode={run_result.returncode}).\n"
        f"--- stdout ---\n{run_result.stdout}\n--- stderr ---\n{run_result.stderr}"
    )

    # B4: stdout is a JSON document
    parsed = json.loads(run_result.stdout)
    assert "results" in parsed, f"Output missing 'results' key: {run_result.stdout!r}"

    # B5: every results_to_print key is present in output
    expected_keys = set(dsl.get("results_to_print", []))
    actual_keys = set(parsed["results"].keys())
    assert expected_keys.issubset(actual_keys), (
        f"Expected results_to_print keys {expected_keys}, got {actual_keys}"
    )
