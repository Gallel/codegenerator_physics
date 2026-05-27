import json
import shutil
from typing import TypedDict, List, Set, Dict, Any
from pathlib import Path
from langgraph.graph import StateGraph, END

from src.code_generator import build_domain_summary_for_domain, build_prompts, call_llm_to_generate_code, DEFAULT_PROGRAM_NAME
from src.dsl_parser import map_dsl_to_ontology
from src.validator import run_validation, describe_error
from src.java_emitter import parse_dsl_to_java
from src.settings import PHYSICS_OWL, GENERATED_FILES_DIR, TESTER_SRC_DIR, MAX_ITERATIONS
from src.problem_extractor import extract_problem_goals
from src.utils import load_ontology
from src.metrics import get_collector, Timer
from src.metrics.efficiency import (
    LAYER_EXTRACT, LAYER_GENERATE, LAYER_VALIDATE, LAYER_REASONER, LAYER_EMIT,
)

class GraphState(TypedDict):
    task: str
    problem_representation: dict
    dsl_content: str
    errors: List[str]
    iterations: int
    validation_passed: bool
    program_name: str
    java_file: str
    output_dir: Path
    # Ablation controls. mode is "ontology" (full system, default) or "single"
    # (one LLM pass, no validation/loop). first_dsl, when set, seeds the first
    # generation so both branches start from the same LLM output (paired).
    mode: str
    first_dsl: str

def extract_problem_node(state: GraphState):
    print("\n[NODE] extract_problem_node")
    # If a shared representation was injected (so both ablation branches use the
    # exact same extracted steps, no per-branch bias), reuse it and skip the LLM.
    seededRep = state.get("problem_representation")
    if seededRep:
        print("  -> Reusing shared problem representation (no extraction call).")
        return state
    with Timer(get_collector(), LAYER_EXTRACT):
        try:
            rep = extract_problem_goals(state["task"])
            state["problem_representation"] = rep
            out_dir = state.get("output_dir")
            if out_dir:
                out_dir.mkdir(parents=True, exist_ok=True)
                with open(out_dir / "problem_representation.json", "w", encoding="utf-8") as f:
                    json.dump(rep, f, indent=2)
            print("  -> Extracted Problem Semantics: \n" + json.dumps(rep, indent=2))
        except Exception as e:
            print("  -> Error extracting problem semantics: " + str(e))
            state["problem_representation"] = {}
    return state

def _build_correction_message(errors):
    """Turn the previous validation errors into actionable feedback.

    Two error families reach here and they need different advice:
      - structural DSL errors (scope / referential integrity / syntax),
        produced by _check_referential_integrity. The fix is mechanical, so we
        spell it out: declare the variable in the module 'inputs' and pass it
        through 'args' on the call.
      - physical inconsistencies, produced by the ontology reasoner. Those are
        about the physics, so we keep that framing.
    """
    structural, physical = [], []
    for e in errors:
        text = str(e)
        if ("Scope Error" in text or "Syntactic Error" in text
                or "not defined" in text or "null operands" in text
                or "output_var" in text or "results_to_print" in text):
            structural.append(text)
        else:
            physical.append(text)

    parts = ["\n\nThe previous DSL did not pass validation. Fix the following and regenerate the full JSON DSL."]

    if structural:
        parts.append("\n\nSTRUCTURAL ERRORS (DSL scope / references). For EACH one:")
        parts.append("\n- If a variable is used inside a module, it MUST appear in that module's"
                     " 'inputs' list AND be supplied in the 'args' of the module_call.")
        parts.append("\n- If a variable is genuinely unused (e.g. a zero term that cancels),"
                     " remove it from the operation entirely instead of leaving it undeclared.")
        parts.append("\n- Do not change the physics; only fix the variable declarations/wiring.")
        parts.append("\nErrors:\n" + "\n".join(structural))

    if physical:
        parts.append("\n\nPHYSICAL INCONSISTENCIES found by the reasoner. Revise the formulas/units"
                     " so the physics is consistent:\n" + "\n".join(physical))

    return "".join(parts)


def generate_dsl_node(state: GraphState):
    print("\n[NODE] generate_dsl_node (Iteration " + str(state.get("iterations", 0) + 1) + ")")

    with Timer(get_collector(), LAYER_GENERATE):
        firstIteration = state.get("iterations", 0) == 0
        seeded = state.get("first_dsl")

        # Paired sampling: on the first iteration, reuse the shared LLM output
        # if one was injected, so the ablation branches start from the same
        # generation. Only later iterations (corrections) call the LLM again.
        if firstIteration and seeded:
            dsl_json_str = seeded
        else:
            onto = load_ontology(PHYSICS_OWL)
            domain_summary = build_domain_summary_for_domain(PHYSICS_OWL, onto=onto)
            prompts = build_prompts(state["task"], domain_summary, state.get("problem_representation", {}))

            user_prompt = prompts["user"]
            if state.get("errors"):
                user_prompt += _build_correction_message(state["errors"])

            dsl_json_str = call_llm_to_generate_code(
                system_prompt=prompts["system"],
                user_prompt=user_prompt,
                onto=onto,
                output_dir=state.get("output_dir")
            )

        prog_name = state.get("program_name", DEFAULT_PROGRAM_NAME)
        out_dir = state.get("output_dir", GENERATED_FILES_DIR)
        out_dir.mkdir(parents=True, exist_ok=True)

        output_path = out_dir / f"{prog_name}.json"
        output_path.write_text(dsl_json_str, encoding="utf-8")

        state["dsl_content"] = dsl_json_str
        state["program_name"] = prog_name
        state["iterations"] = state.get("iterations", 0) + 1

    col = get_collector()
    if col is not None:
        col.set_iterations(state["iterations"])
    return state

def _get_op_vars(op: Dict[str, Any]) -> List[str]:
    used = []
    op_type = op.get("type")
    if op_type == "assignment":
        used.append(op.get("right"))
    elif op_type in ["binary", "binary_literal"]:
        used.extend([op.get("left") or op.get("left_var"), op.get("right") or op.get("literal")])
    elif op_type in ["unary", "unary_literal"]:
        used.append(op.get("operand") or op.get("arg"))
    elif op_type == "module_call":
        args = op.get("args", {})
        if isinstance(args, dict): used.extend(args.values())
    return [u for u in used if u is not None]

def _cleanup_execution_flow(data: Dict[str, Any]):
    flow = data.get("execution_flow", [])
    if not flow: return

    results_to_print = data.get("results_to_print", [])
    used_globals_final = set(results_to_print)

    if not used_globals_final and flow:
        used_globals_final = {flow[-1].get("result") or flow[-1].get("left")}

    pruned_flow = []

    for op in reversed(flow):
        res = op.get("result") or op.get("left")
        if res in used_globals_final:
            pruned_flow.insert(0, op)
            used_globals_final.update(_get_op_vars(op))

    data["execution_flow"] = pruned_flow
    return used_globals_final

def _cleanup_modules(data: Dict[str, Any]):
    called_modules = {op.get("module") for op in data.get("execution_flow", []) if op.get("type") == "module_call"}
    remaining_definitions = []
    surviving_inputs_by_module: Dict[str, set] = {}

    for mod in data.get("definitions", []):
        if mod.get("id") not in called_modules:
            continue

        used_locals = set([mod.get("output_var")])
        pruned_ops = []
        for op in reversed(mod.get("operations", [])):
            res = op.get("result") or op.get("left")
            if res in used_locals or res == mod.get("output_var"):
                pruned_ops.insert(0, op)
                used_locals.update(_get_op_vars(op))

        mod["operations"] = pruned_ops

        actually_used_in_mod = set()
        for op in pruned_ops:
            actually_used_in_mod.update(_get_op_vars(op))

        new_inputs = [
            i for i in mod.get("inputs", [])
            if (i["name"] if isinstance(i, dict) else i) in actually_used_in_mod
        ]
        mod["inputs"] = new_inputs
        surviving_inputs_by_module[mod["id"]] = {
            (i["name"] if isinstance(i, dict) else i) for i in new_inputs
        }
        remaining_definitions.append(mod)

    data["definitions"] = remaining_definitions

    for op in data.get("execution_flow", []):
        if op.get("type") != "module_call":
            continue
        mod_id = op.get("module")
        surviving = surviving_inputs_by_module.get(mod_id)
        if surviving is None:
            continue
        args = op.get("args") or {}
        op["args"] = {k: v for k, v in args.items() if k in surviving}

def _cleanup_global_declarations(data: Dict[str, Any]):
    final_used_globals = set()
    for op in data.get("execution_flow", []):
        final_used_globals.update(_get_op_vars(op))
    data["main_declarations"] = [d for d in data.get("main_declarations", []) if d.get("name") in final_used_globals]

def _perform_dead_code_elimination(output_path: Path):
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    used_globals_from_flow = _cleanup_execution_flow(data)
    if used_globals_from_flow is not None:
        data["main_declarations"] = [d for d in data.get("main_declarations", []) if d.get("name") in used_globals_from_flow]

    _cleanup_modules(data)
    _cleanup_global_declarations(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def _check_op_referential_integrity(op: Dict[str, Any], local_scope: Set[str], scope_name: str, integrity_errors: List[str]):
    op_type = op.get("type")

    if op_type in ["binary", "assignment"]:
        if op.get("operator") is None and op_type == "binary":
            integrity_errors.append(f"Syntactic Error in {scope_name}: Binary operation missing operator: {op}")
        if op.get("left") is None or op.get("right") is None:
            integrity_errors.append(f"Syntactic Error in {scope_name}: Operation contains null operands (left/right): {op}")
    elif op_type == "unary":
        if op.get("function") is None:
            integrity_errors.append(f"Syntactic Error in {scope_name}: Unary operation missing function: {op}")
        if op.get("operand") is None:
            integrity_errors.append(f"Syntactic Error in {scope_name}: Unary operation missing operand: {op}")

    for var in _get_op_vars(op):
        if isinstance(var, (int, float)): continue
        if str(var) not in local_scope:
            try: float(var)
            except ValueError:
                integrity_errors.append(f"Scope Error in {scope_name}: Variable '{var}' used but not defined in this scope. Ops: {op}")

    res = op.get("result") or op.get("left")
    if res: local_scope.add(res)

def _check_referential_integrity(output_path: Path) -> List[str]:
    integrity_errors = []
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    global_decls = data.get("main_declarations", data.get("declarations", []))
    defined_globals = {d.get("name") for d in global_decls if d.get("name")}
    definitions = data.get("definitions", [])
    execution_flow = data.get("execution_flow", data.get("operations", []))

    for decl in global_decls:
        if decl.get("value") is None:
            integrity_errors.append(f"Syntactic Error: Declaration '{decl.get('name')}' has a null value. All physical constants/inputs must have concrete values.")

    # Per-module scope check + check on output_var
    for mod in definitions:
        mod_id = mod.get("id", "UnknownModule")
        local_scope = set()
        for inp in mod.get("inputs", []):
            local_scope.add(inp["name"] if isinstance(inp, dict) else inp)
        for op in mod.get("operations", []):
            _check_op_referential_integrity(op, local_scope, f"Module '{mod_id}'", integrity_errors)

            # Reject dual-root sqrt inside a module (Java method = 1 return value).
            if (op.get("type") == "unary"
                and (op.get("function") or "").lower() == "sqrt"
                and op.get("solution_polarity") == "both"):
                integrity_errors.append(
                    "Module '" + mod_id + "' has a dual-root sqrt on '"
                    + str(op.get("result")) + "'. Move it to execution_flow."
                )

        out_var = mod.get("output_var")
        if out_var and out_var not in local_scope:
            integrity_errors.append(
                f"Module '{mod_id}': output_var '{out_var}' is declared but never assigned "
                f"by any operation in the module body."
            )

    # Main execution flow scope check
    current_globals = set(defined_globals)
    for op in execution_flow:
        _check_op_referential_integrity(op, current_globals, "Main Execution Flow", integrity_errors)

        # sqrt with polarity=both exposes an extra <result>_negative variable
        if (op.get("type") == "unary"
            and (op.get("function") or "").lower() == "sqrt"
            and op.get("solution_polarity") == "both"
            and op.get("result")):
            current_globals.add(op["result"] + "_negative")

    # results_to_print scope check
    results_to_print = data.get("results_to_print", []) or []
    for name in results_to_print:
        if not isinstance(name, str) or not name.strip():
            integrity_errors.append("results_to_print: invalid entry " + repr(name))
            continue
        if name not in current_globals:
            integrity_errors.append(
                "results_to_print: '" + name + "' is not declared nor produced anywhere."
            )

    return integrity_errors

def validate_dsl_node(state: GraphState):
    print("\n[NODE] validate_dsl_node")
    col = get_collector()

    # 'single' branch: one LLM pass, no ontology, no loop. We emit whatever
    # the model produced (it may not even compile, which is itself a result).
    if state.get("mode") == "single":
        print("  -> [single] skipping ontology validation (baseline branch).")
        state["errors"] = []
        state["validation_passed"] = True
        if col is not None:
            col.set_validation_passed(True)
        return state

    with Timer(col, LAYER_VALIDATE):
        prog_name = state.get("program_name", DEFAULT_PROGRAM_NAME)
        out_dir = state.get("output_dir", GENERATED_FILES_DIR)
        output_path = out_dir / f"{prog_name}.json"

        try:
            _perform_dead_code_elimination(output_path)
        except Exception as e:
            print(f"  -> Cleanup Error: {e}")

        print("  -> Mapping DSL to program ontology...")
        output_owl = out_dir / f"{prog_name}.owl"
        try:
            map_dsl_to_ontology(output_path, output_owl)
        except Exception as e:
            print(f"  -> JSON Parse Error: {e}")
            state["errors"] = [f"JSON Parse/Mapping Error: {str(e)}"]
            state["validation_passed"] = False
            return state

        print("  -> Checking Variable Referential Integrity...")
        try:
            integrity_errors = _check_referential_integrity(output_path)
            if integrity_errors:
                print(f"  -> Found {len(integrity_errors)} referential integrity errors.")
                state["errors"] = integrity_errors
                state["validation_passed"] = False
                return state
        except Exception as e:
            print(f"  -> Integrity Check Error: {e}")

        print("  -> Validating generated code with ontologies...")
        # The reasoner (Pellet) is the dominant cost inside run_validation,
        # timed here as its own layer.
        with Timer(col, LAYER_REASONER):
            raw_errors = run_validation(output_path, state.get("output_dir"), output_owl)

        if raw_errors:
            error_strings = [f"[{lbl}] {describe_error(lbl, inst)}" for lbl, inst in raw_errors]
            state["errors"] = error_strings
            state["validation_passed"] = False
            print(f"  -> Found {len(error_strings)} errors.")
        else:
            state["errors"] = []
            state["validation_passed"] = True
            print("  -> No errors found!")

    if col is not None:
        col.set_validation_passed(state.get("validation_passed", False))
    return state

def emit_java_node(state: GraphState):
    print("\n[NODE] emit_java_node")
    with Timer(get_collector(), LAYER_EMIT):
        prog_name = state.get("program_name", DEFAULT_PROGRAM_NAME)
        out_dir = state.get("output_dir", GENERATED_FILES_DIR)
        output_path = out_dir / f"{prog_name}.json"
        java_out = parse_dsl_to_java(output_path)
        state["java_file"] = str(java_out)

    if TESTER_SRC_DIR is None:
        print("  -> Skipping Java tester sync (TESTER_SRC_DIR not configured).")
    elif not state.get("validation_passed", False):
        print("  -> Skipping Java tester sync (validation did not pass).")
    else:
        try:
            TESTER_SRC_DIR.mkdir(parents=True, exist_ok=True)
            dest = TESTER_SRC_DIR / Path(java_out).name
            shutil.copy2(java_out, dest)
            print(f"  -> Merged copy to: {dest}")
        except Exception as e:
            print(f"  -> Copy Warning: {e}")

    return state

def should_continue(state: GraphState):
    if state.get("validation_passed", False):
        return "emit_java"
    if state.get("iterations", 0) >= MAX_ITERATIONS:
        print(f"\n[WARN] Maximum iterations ({MAX_ITERATIONS}) reached. Exiting with errors.")
        return "emit_java"
    return "generate_dsl"

workflow = StateGraph(GraphState)

workflow.add_node("extract_problem", extract_problem_node)
workflow.add_node("generate_dsl", generate_dsl_node)
workflow.add_node("validate_dsl", validate_dsl_node)
workflow.add_node("emit_java", emit_java_node)

workflow.set_entry_point("extract_problem")

workflow.add_edge("extract_problem", "generate_dsl")
workflow.add_edge("generate_dsl", "validate_dsl")
workflow.add_conditional_edges(
    "validate_dsl",
    should_continue,
    {
        "generate_dsl": "generate_dsl",
        "emit_java": "emit_java"
    }
)
workflow.add_edge("emit_java", END)

dsl_generation_app = workflow.compile()
