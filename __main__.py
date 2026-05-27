import sys
import os
import shutil
import logging
from pathlib import Path

# Make `import src.*` work when invoked as either `python __main__.py` or `python -m tfm`.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.settings import OUTPUT_DIR, CORPUS_DIR, PROBLEMS_DIR, LOG_LEVEL
from src.graph import dsl_generation_app
from src.metrics import reset_collector
from src.metrics.efficiency import aggregate as aggregate_efficiency

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)-7s %(name)s :: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("tfm")

METRICS_DIR = OUTPUT_DIR / "metrics"


def run_problem(problem_id, task_description, output_folder):
    log.info("==== Processing problem: %s ====", problem_id)

    # Start a fresh efficiency collector for this run. The graph nodes time
    # themselves into it; we save it afterwards.
    collector = reset_collector(problem_id)

    initial_state = {
        "task": task_description,
        "dsl_content": "",
        "errors": [],
        "iterations": 0,
        "validation_passed": False,
        "program_name": problem_id,
        "java_file": "",
        "output_dir": output_folder,
    }

    try:
        final_state = dsl_generation_app.invoke(initial_state)
    except Exception as e:
        log.error("CRITICAL ERROR processing %s: %s", problem_id, e)
        collector.save(METRICS_DIR)
        return

    collector.save(METRICS_DIR)

    if final_state.get("validation_passed"):
        log.info("Success! [%s] generated and validated -> %s",
                 problem_id, final_state.get("java_file"))
    else:
        log.warning("Failed! [%s] reached max iterations.", problem_id)
        for e in final_state.get("errors") or []:
            log.warning("  - %s", e)


def _load_corpus_problems():
    """Return a list of (problem_id, description) read from corpus/."""
    problems = []
    for d in sorted(CORPUS_DIR.glob("problem_*")):
        if not d.is_dir():
            continue
        desc_file = d / "description.txt"
        if not desc_file.exists():
            log.warning("Skipping %s: no description.txt", d.name)
            continue
        description = desc_file.read_text(encoding="utf-8").strip()
        problems.append((d.name, description))
    return problems


def _load_legacy_problems():
    """Fallback: flat .txt files in problems/ (old behaviour)."""
    problems = []
    for p_file in sorted(PROBLEMS_DIR.glob("*.txt")):
        raw_name = p_file.stem
        clean_name = raw_name.split("_", 1)[1] if "_" in raw_name else raw_name
        description = p_file.read_text(encoding="utf-8").strip()
        problems.append((clean_name, description))
    return problems


def _filter_problems(problems, requested):
    """Keep only the problems whose id matches one of the requested names.

    A request matches if it equals the id exactly ('problem_001') or just the
    numeric/short part ('001'), so both forms work on the command line.
    """
    if not requested:
        return problems
    wanted = set()
    for r in requested:
        wanted.add(r)
        if not r.startswith("problem_"):
            wanted.add("problem_" + r)
    selected = [(pid, desc) for pid, desc in problems if pid in wanted]
    missing = wanted - {pid for pid, _ in problems} - {r for r in requested}
    found_ids = {pid for pid, _ in selected}
    not_found = [r for r in requested
                 if r not in found_ids and ("problem_" + r) not in found_ids]
    if not_found:
        log.warning("Requested problems not found in corpus: %s", ", ".join(not_found))
    return selected


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    requested = [a for a in argv if not a.startswith("-")]

    # When running specific problems we must NOT wipe the whole output dir,
    # otherwise the metrics of other runs are lost. Only clean on a full run.
    full_run = not requested
    if full_run:
        log.info("Cleaning output directory: %s", OUTPUT_DIR)
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    # Prefer the corpus; fall back to the legacy problems/ folder.
    if CORPUS_DIR.exists():
        problems = _load_corpus_problems()
        log.info("Loaded %d problems from corpus: %s", len(problems), CORPUS_DIR)
    elif PROBLEMS_DIR.exists():
        problems = _load_legacy_problems()
        log.info("Loaded %d problems from legacy folder: %s", len(problems), PROBLEMS_DIR)
    else:
        log.error("No corpus/ nor problems/ directory found.")
        return

    problems = _filter_problems(problems, requested)

    if not problems:
        if requested:
            log.error("None of the requested problems were found: %s", ", ".join(requested))
        else:
            log.warning("No problems to solve.")
        return

    if requested:
        log.info("Running %d selected problem(s): %s",
                 len(problems), ", ".join(pid for pid, _ in problems))

    for problem_id, description in problems:
        problem_output_dir = OUTPUT_DIR / problem_id
        problem_output_dir.mkdir(parents=True, exist_ok=True)
        full_task = "PROBLEM NAME: " + problem_id + "\nPROBLEM DESCRIPTION: " + description
        run_problem(problem_id, full_task, problem_output_dir)

    # Aggregate all per-problem efficiency JSONs into the two tidy CSVs.
    log.info("Aggregating efficiency metrics...")
    aggregate_efficiency(METRICS_DIR, METRICS_DIR)

    log.info("All problems processed. Results in '%s', metrics in '%s'.", OUTPUT_DIR, METRICS_DIR)


if __name__ == "__main__":
    main()
