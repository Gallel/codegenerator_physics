import sys
import os
import json
import shutil
import logging
import statistics
from pathlib import Path

# Make `import src.*` work.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Pass@k only means something with stochastic sampling, so we force a higher
# temperature before importing the modules that read it. The settings module
# caches OPENAI_TEMPERATURE at import time and code_generator imports the value
# by name, so we set the env var here, before any of that runs.
N_SAMPLES = int(os.getenv("BENCHMARK_SAMPLES", "5"))
SAMPLE_TEMPERATURE = float(os.getenv("BENCHMARK_TEMPERATURE", "0.7"))
os.environ["OPENAI_TEMPERATURE"] = str(SAMPLE_TEMPERATURE)

from src.settings import OUTPUT_DIR, CORPUS_DIR, LOG_LEVEL
from src import settings
from src import code_generator
from src.graph import dsl_generation_app
from src.problem_extractor import extract_problem_goals
from src.metrics import reset_collector
from src.metrics import efficiency
from src.metrics import pass_at_k
from src.metrics import lcs
from src.metrics import cas
from src.metrics import code_bleu

# The two modules read the temperature into a module-level constant at import
# time. Override both so the loop below actually samples at 0.7.
settings.OPENAI_TEMPERATURE = SAMPLE_TEMPERATURE
code_generator.OPENAI_TEMPERATURE = SAMPLE_TEMPERATURE

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)-7s %(name)s :: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("benchmark")

METRICS_DIR = OUTPUT_DIR / "metrics"
SAMPLES_DIR = METRICS_DIR / "samples"  # raw per-sample JSONs, kept for tracing

# The two ablation branches. "single" = raw LLM, one pass, no ontology.
# "ontology" = full system (loop + reasoner). Both start from the same first
# generation (paired sampling), so the difference is attributable to the system.
BRANCHES = ("single", "ontology")


def _load_problem(problem_dir):
    pid = problem_dir.name
    description = (problem_dir / "description.txt").read_text(encoding="utf-8").strip()
    goals = json.loads((problem_dir / "expected_goals.json").read_text(encoding="utf-8"))
    solution = json.loads((problem_dir / "reference_solution.json").read_text(encoding="utf-8"))
    return pid, description, goals, solution


def _load_corpus(requested):
    problems = []
    for d in sorted(CORPUS_DIR.glob("problem_*")):
        if not d.is_dir() or not (d / "description.txt").exists():
            continue
        problems.append(_load_problem(d))
    if requested:
        wanted = set()
        for r in requested:
            wanted.add(r)
            if not r.startswith("problem_"):
                wanted.add("problem_" + r)
        problems = [p for p in problems if p[0] in wanted]
    return problems


def _invoke_graph(problem_id, description, output_folder, mode, first_dsl=None, representation=None):
    # One graph run in a given ablation mode. Resets the collector so the
    # efficiency JSON is per-(sample, branch). first_dsl, when given, seeds the
    # first generation so both branches share the same starting LLM output.
    collector = reset_collector(problem_id)
    initial_state = {
        "task": "PROBLEM NAME: " + problem_id + "\nPROBLEM DESCRIPTION: " + description,
        "dsl_content": "",
        "errors": [],
        "iterations": 0,
        "validation_passed": False,
        "program_name": problem_id,
        "java_file": "",
        "output_dir": output_folder,
        "mode": mode,
        "first_dsl": first_dsl or "",
        # Shared extracted steps so both branches use identical input (no bias).
        "problem_representation": representation or {},
    }
    try:
        final_state = dsl_generation_app.invoke(initial_state)
    except Exception as e:
        log.error("CRITICAL ERROR generating %s [%s]: %s", problem_id, mode, e)
        return None, collector
    return final_state, collector


def _evaluate_branch(problem_id, final_state, goals, solution, branch_dir):
    java_file = final_state.get("java_file") if final_state else None
    if not java_file or not Path(java_file).exists():
        return {"compiled": False, "ran": False, "passed": False,
                "error": "no java file emitted", "goals": {}}
    work_dir = branch_dir / "build"
    return pass_at_k.evaluate(java_file, problem_id, goals, solution, work_dir)


def _problem_domain(problem_id):
    meta = CORPUS_DIR / problem_id / "metadata.json"
    if meta.exists():
        return json.loads(meta.read_text(encoding="utf-8")).get("domain", "")
    return ""


def _mean_std(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return None, None
    mean = sum(vals) / len(vals)
    std = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    return mean, std


def _max_min_correct(values, passed_flags):
    # max and min of `values`, but only over the samples whose Pass@k passed.
    # Per the director: report best/worst among the runs that were correct.
    picked = [v for v, ok in zip(values, passed_flags)
              if ok and v is not None]
    if not picked:
        return None, None
    return max(picked), min(picked)


def _pick_representative(passk_results):
    for i, r in enumerate(passk_results):
        if r.get("passed"):
            return i
    for i, r in enumerate(passk_results):
        if r.get("compiled"):
            return i
    return 0


def _all_metrics_for_branch(problem_id, final_state, goals, solution, domain, refJava, branch_dir):
    # Run the four metrics on one branch's emitted program. Returns the four
    # per-sample result dicts.
    passk = _evaluate_branch(problem_id, final_state, goals, solution, branch_dir)
    matchedValues = {g: info.get("generated") for g, info in passk.get("goals", {}).items()}
    lcsRes = lcs.evaluate(matchedValues, domain)
    casRes = cas.evaluate(passk.get("goals", {}))
    genJava = final_state.get("java_file") if final_state else None
    if genJava and refJava.exists():
        cbRes = code_bleu.evaluate(genJava, refJava)
    else:
        cbRes = {"codebleu": None, "error": "missing generated or reference java"}
    return passk, lcsRes, casRes, cbRes


def _consolidate(problem_id, branch, samples, domain):
    # samples: list of (passk, lcs, cas, cb) tuples over the N samples of one
    # branch. Writes one consolidated record per metric, tagged with the branch.
    passkS = [s[0] for s in samples]
    lcsS = [s[1] for s in samples]
    casS = [s[2] for s in samples]
    cbS = [s[3] for s in samples]

    n = len(samples)
    c = sum(1 for r in passkS if r.get("passed"))
    passedFlags = [bool(r.get("passed")) for r in passkS]
    rep = _pick_representative(passkS)
    suffix = problem_id + "__" + branch  # unique file name per branch

    passkC = dict(passkS[rep])
    passkC.update({
        "branch": branch,
        "n_samples": n,
        "n_correct": c,
        "n_compiled": sum(1 for r in passkS if r.get("compiled")),
        "n_ran": sum(1 for r in passkS if r.get("ran")),
        "pass_at_1": pass_at_k.pass_at_k(n, c, 1),
        "pass_at_5": pass_at_k.pass_at_k(n, c, min(5, n)),
    })
    passkC["problem_id"] = problem_id
    pass_at_k.save_result(suffix, passkC, METRICS_DIR)

    lcsMean, lcsStd = _mean_std([r.get("lcs") for r in lcsS])
    lcsMaxOk, lcsMinOk = _max_min_correct([r.get("lcs") for r in lcsS], passedFlags)
    lcsC = dict(lcsS[rep])
    lcsC.update({"branch": branch, "lcs": lcsMean, "lcs_std": lcsStd,
                 "lcs_max_correct": lcsMaxOk, "lcs_min_correct": lcsMinOk,
                 "problem_id": problem_id})
    lcs.save_result(suffix, lcsC, METRICS_DIR)

    laxMean, laxStd = _mean_std([r.get("cas_lax") for r in casS])
    strictMean, strictStd = _mean_std([r.get("cas_strict") for r in casS])
    laxMaxOk, laxMinOk = _max_min_correct([r.get("cas_lax") for r in casS], passedFlags)
    strictMaxOk, strictMinOk = _max_min_correct([r.get("cas_strict") for r in casS], passedFlags)
    casC = dict(casS[rep])
    casC.update({"branch": branch, "cas_lax": laxMean, "cas_lax_std": laxStd,
                 "cas_lax_max_correct": laxMaxOk, "cas_lax_min_correct": laxMinOk,
                 "cas_strict": strictMean, "cas_strict_std": strictStd,
                 "cas_strict_max_correct": strictMaxOk, "cas_strict_min_correct": strictMinOk,
                 "problem_id": problem_id})
    cas.save_result(suffix, casC, METRICS_DIR)

    cbMean, cbStd = _mean_std([r.get("codebleu") for r in cbS])
    cbMaxOk, cbMinOk = _max_min_correct([r.get("codebleu") for r in cbS], passedFlags)
    cbC = dict(cbS[rep])
    cbC.update({"branch": branch, "codebleu": cbMean, "codebleu_std": cbStd,
                "codebleu_max_correct": cbMaxOk, "codebleu_min_correct": cbMinOk,
                "n_computed": sum(1 for r in cbS if r.get("codebleu") is not None),
                "problem_id": problem_id})
    for comp in ("ngram_match", "weighted_ngram_match", "syntax_match", "dataflow_match"):
        m, _ = _mean_std([r.get(comp) for r in cbS])
        cbC[comp] = m
    code_bleu.save_result(suffix, cbC, METRICS_DIR)

    return passkC["pass_at_1"], c, cbMean


def _run_problem(problem_id, description, goals, solution):
    problem_dir = OUTPUT_DIR / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)
    domain = _problem_domain(problem_id)
    refJava = CORPUS_DIR / problem_id / "reference.java"

    # Per branch, collect the N sample-tuples.
    perBranch = {b: [] for b in BRANCHES}

    task_text = "PROBLEM NAME: " + problem_id + "\nPROBLEM DESCRIPTION: " + description

    for s in range(N_SAMPLES):
        sample_dir = problem_dir / ("sample_" + str(s))

        # --- shared extraction: extract the problem steps ONCE for this sample
        # and feed the SAME representation to both branches. Tokens consumed
        # here will be attributed to BOTH branches further down (each branch
        # pays the cost it would pay if run alone). ---
        sharedCol = reset_collector(problem_id + "_shared")
        try:
            sharedRep = extract_problem_goals(task_text)
        except Exception as e:
            log.error("extraction failed for %s sample %d: %s", problem_id, s, e)
            sharedRep = {}
        sharedExtractTokens = dict(sharedCol.tokens.get("extract_problem",
                                                       {"prompt": 0, "completion": 0}))

        # --- shared first generation: one LLM pass in 'single' mode, seeded with
        # the shared representation. This run IS the 'single' branch. ---
        singleDir = sample_dir / "single"
        singleDir.mkdir(parents=True, exist_ok=True)
        singleState, singleCol = _invoke_graph(
            problem_id, description, singleDir, "single", representation=sharedRep)
        # Add the shared extraction cost to the single branch (it would have
        # paid it on its own).
        singleCol.record_tokens("extract_problem",
                                sharedExtractTokens["prompt"],
                                sharedExtractTokens["completion"])
        # Remember the cost of the first (shared) generate_dsl call; this is
        # the one that gets seeded into the ontology branch and that the
        # ontology run won't call again. Attribute it to ontology below.
        sharedGenTokens = dict(singleCol.tokens.get("generate_dsl",
                                                   {"prompt": 0, "completion": 0}))
        singleCol.save(SAMPLES_DIR / problem_id / "single", branch="single", sample=s)
        firstDsl = singleState.get("dsl_content") if singleState else ""

        singleMetrics = _all_metrics_for_branch(
            problem_id, singleState, goals, solution, domain, refJava, singleDir)
        perBranch["single"].append(singleMetrics)
        _save_sample_raw(problem_id, "single", s, singleMetrics)

        # --- ontology branch: full system seeded with the SAME first generation. ---
        ontoDir = sample_dir / "ontology"
        ontoDir.mkdir(parents=True, exist_ok=True)
        ontoState, ontoCol = _invoke_graph(
            problem_id, description, ontoDir, "ontology",
            first_dsl=firstDsl, representation=sharedRep)
        # Charge the ontology branch with what it would have paid if it ran
        # alone: the shared extraction + the shared first generation.
        ontoCol.record_tokens("extract_problem",
                              sharedExtractTokens["prompt"],
                              sharedExtractTokens["completion"])
        ontoCol.record_tokens("generate_dsl",
                              sharedGenTokens["prompt"],
                              sharedGenTokens["completion"])
        ontoCol.save(SAMPLES_DIR / problem_id / "ontology", branch="ontology", sample=s)

        ontoMetrics = _all_metrics_for_branch(
            problem_id, ontoState, goals, solution, domain, refJava, ontoDir)
        perBranch["ontology"].append(ontoMetrics)
        _save_sample_raw(problem_id, "ontology", s, ontoMetrics)

    # Consolidate each branch separately.
    for branch in BRANCHES:
        p1, c, cb = _consolidate(problem_id, branch, perBranch[branch], domain)
        log.info("  [%s | %s] pass@1=%.2f (%d/%d correct)  codebleu=%s",
                 problem_id, branch, p1, c, N_SAMPLES,
                 ("%.3f" % cb) if cb is not None else "n/a")


def _save_sample_raw(problem_id, branch, s, metrics):
    passk, lcsRes, casRes, cbRes = metrics
    d = SAMPLES_DIR / problem_id / branch
    d.mkdir(parents=True, exist_ok=True)
    bundle = {"sample": s, "branch": branch,
              "passk": passk, "lcs": lcsRes, "cas": casRes, "codebleu": cbRes}
    path = d / ("sample_metrics_" + str(s) + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    requested = [a for a in argv if not a.startswith("-")]

    full_run = not requested
    if full_run:
        log.info("Cleaning output directory: %s", OUTPUT_DIR)
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    problems = _load_corpus(requested)
    if not problems:
        log.error("No problems to run (corpus: %s, requested: %s)", CORPUS_DIR, requested)
        return

    log.info("Running benchmark on %d problem(s), %d samples each at temp %.2f, branches: %s.",
             len(problems), N_SAMPLES, SAMPLE_TEMPERATURE, ", ".join(BRANCHES))

    for problem_id, description, goals, solution in problems:
        log.info("==== %s ====", problem_id)
        _run_problem(problem_id, description, goals, solution)

    log.info("Aggregating metrics...")
    efficiency.aggregate(SAMPLES_DIR, METRICS_DIR)
    pass_at_k.aggregate(METRICS_DIR, METRICS_DIR)
    lcs.aggregate(METRICS_DIR, METRICS_DIR)
    cas.aggregate(METRICS_DIR, METRICS_DIR)
    code_bleu.aggregate(METRICS_DIR, METRICS_DIR)

    log.info("Done. Results in '%s', metrics in '%s'.", OUTPUT_DIR, METRICS_DIR)


if __name__ == "__main__":
    main()
