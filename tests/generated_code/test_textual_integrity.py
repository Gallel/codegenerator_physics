"""Static, textual contract on the emitted Java (B6).

These tests don't compile or run anything; they parse the .java output as
text and verify referential integrity at the source-code level.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import pytest

from src.dsl_parser import map_dsl_to_ontology
from src.java_emitter import parse_dsl_to_java

from tests.conftest import (
    SYNTHETIC_DSL_DIR,
    _list_dsls,
    fixture_ids,
    load_dsl,
)


SYNTHETIC_DSLS = _list_dsls(SYNTHETIC_DSL_DIR)


def _emit(dsl_path: Path, workdir: Path) -> tuple[dict, str]:
    dsl = load_dsl(dsl_path)
    staged = workdir / dsl_path.name
    shutil.copy2(dsl_path, staged)
    map_dsl_to_ontology(staged, workdir / f"{dsl_path.stem}.owl")
    java_file = Path(parse_dsl_to_java(staged))
    return dsl, java_file.read_text(encoding="utf-8")


@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_class_name_matches_metadata(dsl_path: Path, dsl_workdir: Path):
    dsl, source = _emit(dsl_path, dsl_workdir)
    class_name = dsl["metadata"]["name"]
    assert re.search(rf"public class {re.escape(class_name)}\b", source), (
        f"Class name {class_name!r} not found in emitted Java for {dsl_path.name}"
    )


@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_every_main_declaration_appears_in_main(dsl_path: Path, dsl_workdir: Path):
    dsl, source = _emit(dsl_path, dsl_workdir)
    # Restrict the search to the body of `public static void main`.
    main_match = re.search(r"public static void main\([^)]*\)\s*\{(.*?)\n\s*\}", source, re.S)
    assert main_match, "main(...) body not found"
    main_body = main_match.group(1)
    for decl in dsl.get("main_declarations", []):
        name = decl["name"]
        assert re.search(rf"\b{re.escape(name)}\b", main_body), (
            f"Declaration {name!r} not present in main() body of {dsl_path.name}"
        )


@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_every_module_definition_is_emitted(dsl_path: Path, dsl_workdir: Path):
    dsl, source = _emit(dsl_path, dsl_workdir)
    for mod in dsl.get("definitions", []):
        mod_id = mod["id"]
        assert re.search(rf"public static \w+\s+{re.escape(mod_id)}\s*\(", source), (
            f"Module {mod_id!r} from {dsl_path.name} is not declared as a Java method."
        )


@pytest.mark.parametrize("dsl_path", SYNTHETIC_DSLS, ids=fixture_ids(SYNTHETIC_DSLS))
def test_no_dangling_assignment_operator(dsl_path: Path, dsl_workdir: Path):
    """Catches `x = ;` or `x = null;` patterns where the emitter dropped a token."""
    _, source = _emit(dsl_path, dsl_workdir)
    assert "= ;" not in source, f"Empty RHS found in emitted Java for {dsl_path.name}"
    # `null` literal is not used by the current emitter; if it shows up, it's a regression.
    assert " = null;" not in source, f"Suspicious null assignment in {dsl_path.name}"
