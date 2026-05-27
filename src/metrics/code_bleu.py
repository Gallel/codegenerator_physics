import csv
import json
from pathlib import Path

# CodeBLEU compares the generated Java against a human-written reference.
# It measures structural/lexical similarity, NOT correctness (Pass@k covers
# that). The library parses source text with tree-sitter; it does not compile,
# so the file name vs class name mismatch is irrelevant here.

# Component weights (ngram, weighted-ngram, syntax/AST, dataflow). Equal split.
WEIGHTS = (0.25, 0.25, 0.25, 0.25)


def evaluate(generated_java_path, reference_java_path):
    # Lazy import so the rest of the pipeline runs even without the library.
    try:
        from codebleu import calc_codebleu
    except ImportError:
        return {"error": "codebleu library not installed", "codebleu": None}

    gen = Path(generated_java_path)
    ref = Path(reference_java_path)
    if not gen.exists():
        return {"error": "generated java not found", "codebleu": None}
    if not ref.exists():
        return {"error": "reference java not found", "codebleu": None}

    genCode = gen.read_text(encoding="utf-8")
    refCode = ref.read_text(encoding="utf-8")

    try:
        scores = calc_codebleu([refCode], [genCode], lang="java", weights=WEIGHTS)
    except Exception as e:
        return {"error": "codebleu failed: " + str(e), "codebleu": None}

    return {
        "error": None,
        "codebleu": scores.get("codebleu"),
        "ngram_match": scores.get("ngram_match_score"),
        "weighted_ngram_match": scores.get("weighted_ngram_match_score"),
        "syntax_match": scores.get("syntax_match_score"),
        "dataflow_match": scores.get("dataflow_match_score"),
    }


def save_result(problem_id, result, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = dict(result)
    rec["problem_id"] = problem_id
    path = out_dir / ("codebleu_" + problem_id + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return path


def aggregate(results_dir, out_dir=None):
    results_dir = Path(results_dir)
    out_dir = Path(out_dir) if out_dir else results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    scores = []
    for path in sorted(results_dir.rglob("codebleu_*.json")):
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        pid = rec.get("problem_id", path.stem)
        rows.append({
            "problem_id": pid,
            "branch": rec.get("branch", "ontology"),
            "codebleu": rec.get("codebleu"),
            "codebleu_std": rec.get("codebleu_std"),
            "codebleu_max_correct": rec.get("codebleu_max_correct"),
            "codebleu_min_correct": rec.get("codebleu_min_correct"),
            "n_computed": rec.get("n_computed"),
            "ngram_match": rec.get("ngram_match"),
            "weighted_ngram_match": rec.get("weighted_ngram_match"),
            "syntax_match": rec.get("syntax_match"),
            "dataflow_match": rec.get("dataflow_match"),
            "error": rec.get("error") or "",
        })
        if rec.get("codebleu") is not None:
            scores.append(rec["codebleu"])

    _write_csv(rows, ["problem_id", "branch", "codebleu", "codebleu_std",
                      "codebleu_max_correct", "codebleu_min_correct", "n_computed",
                      "ngram_match", "weighted_ngram_match",
                      "syntax_match", "dataflow_match", "error"],
               out_dir / "codebleu_summary.csv")

    computed = len(scores)
    errored = len(rows) - computed
    print("[INFO] codebleu_summary.csv: " + str(len(rows)) + " rows")
    if computed:
        mean = sum(scores) / computed
        print("[INFO] mean CodeBLEU over " + str(computed) + " computed: " + ("%.3f" % mean))
    else:
        print("[INFO] mean CodeBLEU: not available (0 computed)")
    if errored:
        print("[WARN] " + str(errored) + " problem(s) had a CodeBLEU error (see 'error' column)")


def _write_csv(rows, fieldnames, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
