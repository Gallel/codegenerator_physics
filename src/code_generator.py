import json
import os
import time
from pathlib import Path
from typing import Dict
from openai import OpenAI
from owlready2 import get_ontology

from src.settings import (
    PHYSICS_OWL,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
)
from src.utils import load_ontology
from src.metrics import get_collector
from src.metrics.efficiency import LAYER_GENERATE

DEFAULT_PROGRAM_NAME = "PhysicsProgram"

# Small pause before each LLM call to avoid bursting into OpenAI 429s.
# Override via env var LLM_CALL_DELAY (seconds).
LLM_CALL_DELAY = float(os.getenv("LLM_CALL_DELAY", "3.0"))


def _collect_unit_quantity_table(onto):
    unitToCat = {}
    qtyToCats = {}

    for ind in onto.individuals():
        types = [t.name for t in ind.is_a if hasattr(t, "name")]
        isUnit = any("Unit" in t for t in types)
        isQty = any(t in ("PhysicalQuantity", "PhysicalQuantityType") for t in types)

        if isUnit:
            try:
                cats = list(getattr(ind, "hasUnitCategory", None) or [])
            except Exception:
                cats = []
            if cats:
                unitToCat[ind.name] = cats[0]

        if isQty:
            try:
                allowed = list(getattr(ind, "hasAllowedUnitCategory", None) or [])
            except Exception:
                allowed = []
            if allowed:
                qtyToCats[ind.name] = sorted(set(allowed))

    return unitToCat, qtyToCats


def build_domain_summary_for_domain(ontology_path, onto=None):
    if onto is None:
        onto = load_ontology(ontology_path)

    lines = ["DOMAIN VOCABULARY\n", "CLASSES:"]
    for cls in onto.classes():
        lines.append("- " + cls.name + " (iri: " + cls.iri + ")")
    lines.append("")

    lines.append("KEY INDIVIDUALS (Constants, Quantities & Units):")
    hasNumericValue = getattr(onto, "hasNumericValue", None)
    hasUnit = getattr(onto, "hasUnit", None)
    hasConversionFactorToSI = getattr(onto, "hasConversionFactorToSI", None)

    for ind in onto.individuals():
        hasVal = hasNumericValue and hasNumericValue[ind]
        isQty = any(t.name in ["PhysicalQuantityType", "PhysicalQuantity"] for t in ind.is_a if hasattr(t, "name"))
        isUnit = any("Unit" in t.name for t in ind.is_a if hasattr(t, "name"))

        if hasVal or isQty or isUnit:
            types = [t.name for t in ind.is_a if hasattr(t, "name")][:2]
            valStr = (" [value=" + str(hasNumericValue[ind][0]) + "]") if hasVal else ""
            unitStr = (" [unit=" + hasUnit[ind][0].name + "]") if hasUnit and hasUnit[ind] else ""
            convStr = (" [factor_to_SI=" + str(hasConversionFactorToSI[ind][0]) + "]") if isUnit and hasConversionFactorToSI and hasConversionFactorToSI[ind] else ""
            lines.append("- " + ind.name + " (iri: " + ind.iri + ") " + valStr + unitStr + convStr + " [types=" + str(types) + "]")
    lines.append("")

    unitToCat, qtyToCats = _collect_unit_quantity_table(onto)
    if unitToCat and qtyToCats:
        lines.append("UNIT-QUANTITY COMPATIBILITY (CRITICAL): the unit of every declaration")
        lines.append("must belong to a category that the declaration's quantity accepts.")
        lines.append("Mismatches are rejected by the validator.")
        lines.append("")
        lines.append("Unit categories:")
        for u in sorted(unitToCat):
            lines.append("  - " + u + " -> " + unitToCat[u])
        lines.append("")
        lines.append("Allowed categories per quantity:")
        for q in sorted(qtyToCats):
            lines.append("  - " + q + " -> " + str(qtyToCats[q]))
        lines.append("Quantities not listed here (e.g. DimensionlessQuantity) are unconstrained.")
        lines.append("")

    lines.append("KEY PROPERTIES: hasQuantityType, hasUnit, hasNumericValue, hasLeftOperand, hasRightOperand, hasOperand, hasResultMeasurement\n")

    CodeGenerationProfile = getattr(onto, "CodeGenerationProfile", None)
    hasProfileText = getattr(onto, "hasProfileText", None)

    if CodeGenerationProfile and hasProfileText:
        profiles = list(CodeGenerationProfile.instances())
        if profiles:
            lines.append("CODE GENERATION GUIDELINES:")
            for prof in profiles:
                texts = hasProfileText[prof]
                for t in texts:
                    lines.append("\n- Profile " + prof.name + ":\n" + t)
            lines.append("")

    return "\n".join(lines)


def build_prompts(task_description, domain_summary, problem_representation = None):
    system = SYSTEM_PROMPT
    reprStr = json.dumps(problem_representation, indent=2) if problem_representation else "{}"
    user = USER_PROMPT_TEMPLATE.format(
        task_description=task_description,
        problem_representation=reprStr,
        domain_summary=domain_summary
    )
    return {"system": system, "user": user}


# Shared enums for the operation schema.
_FUNCTION_ENUM = ["sqrt", "sin", "cos", "tan", "ln", "log", "derivative", "integral", None]
_OPERATOR_ENUM = ["+", "-", "*", "/", "^", None]
_OP_TYPE_ENUM  = ["binary", "unary", "assignment", "module_call"]
_VAR_TYPE_ENUM = ["double", "int"]
_POLARITY_ENUM = ["positive", "negative", "both", None]


def _operation_schema():
    return {
        "type": "object",
        "properties": {
            "type":              {"type": "string", "enum": _OP_TYPE_ENUM},
            "operator":          {"type": ["string", "null"], "enum": _OPERATOR_ENUM},
            "function":          {"type": ["string", "null"], "enum": _FUNCTION_ENUM},
            "left":              {"type": ["string", "number", "null"]},
            "right":             {"type": ["string", "number", "null"]},
            "operand":           {"type": ["string", "number", "null"]},
            "result":            {"type": "string"},
            "module":            {"type": ["string", "null"]},
            "solution_polarity": {"type": ["string", "null"], "enum": _POLARITY_ENUM},
            "args": {
                "type": ["object", "null"],
                "additionalProperties": {"type": ["string", "number"]},
            },
        },
        "required": [
            "type", "operator", "function", "left", "right", "operand",
            "result", "module", "solution_polarity", "args",
        ],
        "additionalProperties": False,
    }


def call_llm_to_generate_code(system_prompt, user_prompt, onto = None, output_dir = None):
    # max_retries lets the SDK ride out transient 429s with backoff instead of
    # failing the whole run; override LLM_CALL_DELAY to space requests further.
    client = OpenAI(max_retries=8)

    if onto is None:
        onto = load_ontology(PHYSICS_OWL)

    qtyEnums = [ind.name for ind in onto.individuals() if any(t.name in ['PhysicalQuantityType', 'PhysicalQuantity'] or 'PhysicalQuantity' in t.name for t in ind.is_a if hasattr(t, 'name'))]
    unitEnums = [ind.name for ind in onto.individuals() if any('Unit' in t.name for t in ind.is_a if hasattr(t, 'name'))]

    # Dump prompts to disk for debugging
    if output_dir:
        (output_dir / "debug_system_prompt.txt").write_text(system_prompt, encoding="utf-8")
        (output_dir / "debug_user_prompt.txt").write_text(user_prompt, encoding="utf-8")
    else:
        Path("output/debug_system_prompt.txt").write_text(system_prompt, encoding="utf-8")
        Path("output/debug_user_prompt.txt").write_text(user_prompt, encoding="utf-8")
    # End of dump

    opSchema = _operation_schema()

    dslSchema = {
        "name": "physics_program",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
                "main_declarations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "value": {"type": ["number", "null"]},
                            "type": {"type": "string", "enum": _VAR_TYPE_ENUM, "default": "double"},
                            "semantics": {
                                "type": "object",
                                "properties": {
                                    "quantity": {"type": "string", "enum": qtyEnums},
                                    "unit": {"type": "string", "enum": unitEnums},
                                },
                                "required": ["quantity", "unit"],
                                "additionalProperties": False,
                            },
                        },
                        "required": ["name", "value", "type", "semantics"],
                        "additionalProperties": False,
                    },
                },
                "definitions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "description": {"type": "string"},
                            "inputs": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "type": {"type": "string", "enum": _VAR_TYPE_ENUM, "default": "double"},
                                    },
                                    "required": ["name", "type"],
                                    "additionalProperties": False,
                                },
                            },
                            "operations": {
                                "type": "array",
                                "items": opSchema,
                            },
                            "output_var": {"type": ["string", "null"]},
                            "return_type": {"type": "string", "enum": _VAR_TYPE_ENUM, "default": "double"},
                        },
                        "required": ["id", "description", "inputs", "operations", "output_var", "return_type"],
                        "additionalProperties": False,
                    },
                },
                "execution_flow": {
                    "type": "array",
                    "items": opSchema,
                },
                "results_to_print": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["metadata", "main_declarations", "definitions", "execution_flow", "results_to_print"],
            "additionalProperties": False,
        },
    }

    if LLM_CALL_DELAY > 0:
        time.sleep(LLM_CALL_DELAY)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": dslSchema,
        },
        temperature=OPENAI_TEMPERATURE,
    )

    # Record token usage for this call, if a collector is active. The shared
    # first generation in the paired-sampling design is later attributed to
    # both branches by run_benchmark; this only records the actual API call.
    col = get_collector()
    if col is not None and getattr(response, "usage", None) is not None:
        col.record_tokens(
            LAYER_GENERATE,
            getattr(response.usage, "prompt_tokens", 0),
            getattr(response.usage, "completion_tokens", 0),
        )

    return response.choices[0].message.content.strip()
