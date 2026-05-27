import csv
import json
import math
import re
import shutil
import subprocess
import time
from pathlib import Path

from src.metrics.efficiency import get_collector, LAYER_COMPILE, LAYER_RUN

REL_TOLERANCE = 0.02  # 2%

# Leading signed number, plain or scientific notation. The corpus solutions
# use dot decimals and e-notation, so this is enough.
_NUM_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def parse_reference_number(text):
    # "3066.15 m/s" -> 3066.15 ; "-2.45e22 J" -> -2.45e22 ; takes the first number.
    if text is None:
        return None
    m = _NUM_RE.search(str(text).strip())
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def values_match(generated, reference, rel_tol=REL_TOLERANCE):
    # Relative tolerance + strict sign.
    if generated is None or reference is None:
        return False
    if (generated < 0) != (reference < 0):
        return False
    if reference == 0.0:
        return abs(generated) <= rel_tol
    return abs(generated - reference) / abs(reference) <= rel_tol


def _normalize_name(name):
    # Lowercase, drop separators, so 'kinetic_energy' ~ 'KineticEnergy' ~ 'kineticenergy'.
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def _to_float(raw):
    try:
        return float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def _compile_java(java_file, work_dir, collector):
    work_dir.mkdir(parents=True, exist_ok=True)
    javac = shutil.which("javac")
    if javac is None:
        return None, "javac not found on PATH"
    t0 = time.perf_counter()
    proc = subprocess.run(
        [javac, "-d", str(work_dir), str(java_file)],
        capture_output=True, text=True, timeout=60,
    )
    if collector is not None:
        collector.record(LAYER_COMPILE, time.perf_counter() - t0)
    if proc.returncode != 0:
        return None, "compile error: " + proc.stderr.strip()
    return work_dir, None


def _run_java(class_name, work_dir, collector):
    java = shutil.which("java")
    if java is None:
        return None, "java not found on PATH"
    t0 = time.perf_counter()
    proc = subprocess.run(
        [java, "-cp", str(work_dir), class_name],
        capture_output=True, text=True, timeout=60,
    )
    if collector is not None:
        collector.record(LAYER_RUN, time.perf_counter() - t0)
    if proc.returncode != 0:
        return None, "runtime error: " + proc.stderr.strip()
    return proc.stdout, None


def _parse_program_output(stdout):
    # The program prints a JSON object with a 'results' map. Be lenient and
    # grab the first {...} block.
    if not stdout:
        return None
    start = stdout.find("{")
    end = stdout.rfind("}")
    if start < 0 or end < 0:
        return None
    try:
        data = json.loads(stdout[start:end + 1])
    except json.JSONDecodeError:
        return None
    return data.get("results", {})


def evaluate(java_file, class_name, expected_goals, reference_solution, work_dir):
    # Run one program and check all its goals against the reference.
    collector = get_collector()
    result = {"compiled": False, "ran": False, "passed": False, "error": None, "goals": {}}

    classpathDir, err = _compile_java(Path(java_file), Path(work_dir), collector)
    if err:
        result["error"] = err
        return result
    result["compiled"] = True

    stdout, err = _run_java(class_name, classpathDir, collector)
    if err:
        result["error"] = err
        return result
    result["ran"] = True

    produced = _parse_program_output(stdout)
    if produced is None:
        result["error"] = "could not parse program output as JSON"
        return result
    result["produced"] = produced

    # Index the produced values both by normalized name and as a plain list,
    # so we can match a goal by name first and fall back to matching by value.
    producedByName = {}
    producedValues = []
    for k, v in produced.items():
        val = _to_float(v)
        producedByName[_normalize_name(k)] = val
        producedValues.append(val)

    allOk = True
    for goal in expected_goals:
        refVal = parse_reference_number(reference_solution.get(goal))

        # 1) try the LLM's own name (normalized).
        genVal = producedByName.get(_normalize_name(goal))
        how = "name"

        # 2) fall back to matching by value: any produced number that matches.
        if not values_match(genVal, refVal):
            byValue = next((v for v in producedValues if values_match(v, refVal)), None)
            if byValue is not None:
                genVal = byValue
                how = "value"

        ok = values_match(genVal, refVal)
        result["goals"][goal] = {
            "reference": refVal, "generated": genVal, "match": ok,
            "matched_by": how if ok else None,
        }
        if not ok:
            allOk = False

    result["passed"] = allOk and len(expected_goals) > 0
    return result


def save_result(problem_id, result, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = dict(result)
    rec["problem_id"] = problem_id
    path = out_dir / ("passk_" + problem_id + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return path


def pass_at_k(n, c, k):
    # Unbiased estimator from Chen et al. 2021 (Codex). With n samples and c
    # correct ones, the chance that a random pick of k contains at least one
    # correct is 1 - C(n-c, k) / C(n, k). If we can't even fail k times
    # (n - c < k) every draw hits a correct sample, so it's 1.0.
    if k > n:
        return None
    if n - c < k:
        return 1.0
    return 1.0 - (math.comb(n - c, k) / math.comb(n, k))


# Aggregation: turn all the passk_*.json into two tidy CSVs.

def aggregate(results_dir, out_dir=None):
    results_dir = Path(results_dir)
    out_dir = Path(out_dir) if out_dir else results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    goalRows = []
    summaryRows = []
    for path in sorted(results_dir.rglob("passk_*.json")):
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        pid = rec.get("problem_id", path.stem)

        # The benchmark writes a consolidated record over the n samples. Older
        # single-run records (no 'n_samples') still parse: we treat them as
        # n=1, c=1 if they passed.
        n = rec.get("n_samples", 1)
        c = rec.get("n_correct", 1 if rec.get("passed") else 0)
        p1 = rec.get("pass_at_1")
        p5 = rec.get("pass_at_5")
        if p1 is None:
            p1 = pass_at_k(n, c, 1)
        if p5 is None:
            p5 = pass_at_k(n, c, min(5, n))

        # Goal-level rows come from the representative sample (the first one
        # that passed, else the first sample) so the goals CSV stays readable.
        goals = rec.get("goals", {})
        for goal, info in goals.items():
            goalRows.append({
                "problem_id": pid, "goal": goal,
                "reference": info.get("reference"),
                "generated": info.get("generated"),
                "match": bool(info.get("match")),
            })

        summaryRows.append({
            "problem_id": pid,
            "branch": rec.get("branch", "ontology"),
            "n_samples": n,
            "n_correct": c,
            "n_compiled": rec.get("n_compiled", 1 if rec.get("compiled") else 0),
            "n_ran": rec.get("n_ran", 1 if rec.get("ran") else 0),
            "pass_at_1": round(p1, 4) if p1 is not None else "",
            "pass_at_5": round(p5, 4) if p5 is not None else "",
            "error": rec.get("error") or "",
        })

    _write_csv(goalRows, ["problem_id", "goal", "reference", "generated", "match"],
               out_dir / "passk_goals.csv")
    _write_csv(summaryRows,
               ["problem_id", "branch", "n_samples", "n_correct", "n_compiled", "n_ran",
                "pass_at_1", "pass_at_5", "error"],
               out_dir / "passk_summary.csv")

    total = len(summaryRows)
    mean1 = (sum(r["pass_at_1"] for r in summaryRows if r["pass_at_1"] != "") / total) if total else 0.0
    mean5 = (sum(r["pass_at_5"] for r in summaryRows if r["pass_at_5"] != "") / total) if total else 0.0
    print("[INFO] passk_goals.csv: " + str(len(goalRows)) + " rows")
    print("[INFO] passk_summary.csv: " + str(total) + " rows")
    print("[INFO] mean Pass@1: " + ("%.3f" % mean1) + "  mean Pass@5: " + ("%.3f" % mean5))


def _write_csv(rows, fieldnames, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
