"""Project config. Loads .env and resolves all the paths the rest of the
modules use. Prompts live under prompts/ but inline fallbacks are kept."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

RESOURCES_DIR = BASE_DIR / "resources"
OUTPUT_DIR    = BASE_DIR / "output"
PROBLEMS_DIR  = BASE_DIR / "problems"
CORPUS_DIR    = BASE_DIR / "corpus"
PROMPTS_DIR   = BASE_DIR / "prompts"
GENERATED_FILES_DIR = OUTPUT_DIR

PHYSICS_DOMAIN_OWL   = RESOURCES_DIR / "physics-domain.owl"
MATH_OWL             = RESOURCES_DIR / "physics-math.owl"
PROGRAM_TRACE_OWL    = RESOURCES_DIR / "program-trace.owl"
PHYSICS_BRIDGE_OWL   = RESOURCES_DIR / "physics-program-bridge.owl"
PHYSICS_RULES_OWL    = RESOURCES_DIR / "physics-rules.owl"
PROGRAM_OWL          = OUTPUT_DIR / "Main.owl"

# LLM config (override via .env)
OPENAI_MODEL       = os.getenv("OPENAI_MODEL", "gpt-5.4-2026-03-05")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
MAX_ITERATIONS     = int(os.getenv("MAX_ITERATIONS", "5"))
LOG_LEVEL          = os.getenv("LOG_LEVEL", "INFO").upper()

# Optional sibling Java tester project
_tester_env = os.getenv("TESTER_SRC_DIR", "").strip()
if _tester_env:
    TESTER_SRC_DIR = Path(_tester_env)
else:
    _legacy_tester = BASE_DIR.parent / "TFMClassTester" / "src"
    TESTER_SRC_DIR = _legacy_tester if _legacy_tester.exists() else None

PHYSICS_OWL = PHYSICS_DOMAIN_OWL


# Prompt loading

_FALLBACK_EXTRACTION = """
You are an expert Physics Problem Analyzer.
Reply with a STRICT JSON object: knowns, goals, solution_strategy.
Do NOT solve numerically. Do NOT wrap in markdown.
""".strip()

_FALLBACK_SYSTEM = """
You are an expert ontology-driven semantic logic designer specializing in Top-Down Physics Design.
Generate a JSON DSL with metadata, main_declarations, definitions, execution_flow, results_to_print.
Every name in results_to_print must already exist (declared or produced).
""".strip()

_FALLBACK_USER_TEMPLATE = """
Task description:
{task_description}

EXTRACTED PROBLEM REPRESENTATION:
{problem_representation}

DOMAIN VOCABULARY:
{domain_summary}

No markdown, only raw JSON.
""".strip()


def _load_prompt(filename, fallback):
    path = PROMPTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return fallback


EXTRACTION_PROMPT    = _load_prompt("extraction.txt",    _FALLBACK_EXTRACTION)
SYSTEM_PROMPT        = _load_prompt("system.txt",        _FALLBACK_SYSTEM)
USER_PROMPT_TEMPLATE = _load_prompt("user_template.txt", _FALLBACK_USER_TEMPLATE)
