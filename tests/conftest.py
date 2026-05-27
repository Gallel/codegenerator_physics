"""Shared fixtures for the test suite."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import owlready2
from owlready2 import World

from src.settings import (
    PHYSICS_DOMAIN_OWL,
    MATH_OWL,
    PROGRAM_TRACE_OWL,
    PHYSICS_BRIDGE_OWL,
    PHYSICS_RULES_OWL,
)

# Register resources/ so owlready resolves owl:imports locally instead of
# trying to download them from example.org.
_RESOURCES_DIR = str(MATH_OWL.resolve().parent)
if _RESOURCES_DIR not in owlready2.onto_path:
    owlready2.onto_path.append(_RESOURCES_DIR)


TESTS_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = TESTS_DIR / "fixtures"
SYNTHETIC_DSL_DIR = FIXTURES_DIR / "synthetic_dsls"
INVALID_DSL_DIR = FIXTURES_DIR / "invalid_dsls"
VALID_DSL_DIR = FIXTURES_DIR / "valid_dsls"


def _list_dsls(folder):
    if not folder.exists():
        return []
    return sorted(folder.glob("*.json"))


def fixture_ids(paths):
    return [p.stem for p in paths]


def _load_full_world():
    world = World()
    # Load in dependency order: math is imported by domain, domain by rules.
    world.get_ontology(str(MATH_OWL.resolve())).load()
    world.get_ontology(str(PHYSICS_DOMAIN_OWL.resolve())).load()
    world.get_ontology(str(PROGRAM_TRACE_OWL.resolve())).load()
    world.get_ontology(str(PHYSICS_BRIDGE_OWL.resolve())).load()
    if PHYSICS_RULES_OWL.exists():
        world.get_ontology(str(PHYSICS_RULES_OWL.resolve())).load()
    return world


# Function-scoped: Pellet inferences pollute the World between tests.
@pytest.fixture()
def isolated_world():
    return _load_full_world()


# Java toolchain detection
def _which(tool):
    return shutil.which(tool)


JAVAC_PATH = _which("javac")
JAVA_PATH = _which("java")
JAVA_AVAILABLE = JAVAC_PATH is not None and JAVA_PATH is not None


def require_java():
    if not JAVA_AVAILABLE:
        pytest.skip("JDK not available (no `javac`/`java` on PATH).")


def compile_java(java_file, work_dir):
    require_java()
    return subprocess.run(
        [JAVAC_PATH, "-d", str(work_dir), str(java_file)],
        capture_output=True, text=True, timeout=30,
    )


def run_java(class_name, work_dir):
    require_java()
    return subprocess.run(
        [JAVA_PATH, "-cp", str(work_dir), class_name],
        capture_output=True, text=True, timeout=30,
    )


def load_dsl(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture()
def dsl_workdir(tmp_path):
    return tmp_path
