"""End-to-end smoke test of the LangGraph pipeline.

We mock both LLM calls (problem_extractor + code_generator) with recorded
JSON payloads so the test is deterministic, free, and offline. The point is
to verify the *contract* of the orchestrator, not numeric correctness:

* When the recorded DSL passes validation, the graph reaches `emit_java` and
  produces a .java file.
* `validation_passed=True` is reflected in the final state.
* The .java compiles (when a JDK is available).

If you want to swap the recorded DSL for a different one, just replace
RECORDED_DSL below; everything else is generic.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import (
    SYNTHETIC_DSL_DIR,
    compile_java,
    JAVA_AVAILABLE,
)


# Pick a small, well-known fixture as the recorded LLM output.
RECORDED_DSL_PATH = SYNTHETIC_DSL_DIR / "binary_div.json"

RECORDED_PROBLEM_REPRESENTATION = {
    "knowns": [
        {"name": "dist", "value": 100.0, "quantity_type": "DisplacementQuantity",
         "description": "distance traveled"},
        {"name": "time", "value": 10.0, "quantity_type": "TimeQuantity",
         "description": "duration"},
    ],
    "goals": [
        {"target_quantity": "VelocityQuantity", "condition": "average velocity",
         "description": "compute v"}
    ],
    "solution_strategy": ["Step 1: v = dist / time"],
}


def test_pipeline_smoke_with_mocked_llm(tmp_path: Path):
    """Run dsl_generation_app end-to-end with both LLM endpoints mocked."""
    # Import inside the test so we can patch the underlying functions before
    # the graph captures their references.
    import src.problem_extractor as problem_extractor_module
    import src.code_generator as code_generator_module

    recorded_dsl_text = RECORDED_DSL_PATH.read_text(encoding="utf-8")

    with patch.object(
        problem_extractor_module, "extract_problem_goals",
        return_value=RECORDED_PROBLEM_REPRESENTATION,
    ), patch.object(
        code_generator_module, "call_llm_to_generate_code",
        return_value=recorded_dsl_text,
    ):
        # Re-import the graph so it picks up the patched call_llm if needed.
        from src.graph import dsl_generation_app

        out_dir = tmp_path / "out"
        out_dir.mkdir()

        initial_state = {
            "task": "PROBLEM NAME: BinaryDiv\nPROBLEM DESCRIPTION: distance/time",
            "dsl_content": "",
            "errors": [],
            "iterations": 0,
            "validation_passed": False,
            "program_name": "BinaryDiv",
            "java_file": "",
            "output_dir": out_dir,
        }
        final = dsl_generation_app.invoke(initial_state)

    assert final["validation_passed"] is True, (
        f"Pipeline should have validated the recorded DSL; errors: {final.get('errors')}"
    )
    java_path = Path(final["java_file"])
    assert java_path.exists(), "emit_java did not produce a .java file."

    if JAVA_AVAILABLE:
        compile_result = compile_java(java_path, out_dir)
        assert compile_result.returncode == 0, (
            f"Recorded DSL produced .java that does not compile.\n"
            f"stderr:\n{compile_result.stderr}"
        )
