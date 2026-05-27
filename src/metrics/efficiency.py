import csv
import json
import time
from pathlib import Path

# Layer names. The plots group on these, so keep them stable.
LAYER_EXTRACT = "extract_problem"
LAYER_GENERATE = "generate_dsl"
LAYER_VALIDATE = "validate_dsl"
LAYER_REASONER = "reasoner_pellet"
LAYER_EMIT = "emit_java"
LAYER_COMPILE = "java_compile"
LAYER_RUN = "java_run"


class RunCollector:
    def __init__(self, problem_id):
        self.problemId = problem_id
        self.samples = {}            # layer -> list of seconds
        # Token usage, accumulated by layer. Both numbers are cumulative across
        # all calls of that layer in this run (the ontology branch may call
        # generate_dsl several times, each adds to the same bucket).
        self.tokens = {}             # layer -> {"prompt": int, "completion": int}
        self.iterations = 0
        self.validationPassed = False
        self._start = time.perf_counter()

    def record(self, layer, seconds):
        self.samples.setdefault(layer, []).append(seconds)

    def record_tokens(self, layer, prompt_tokens, completion_tokens):
        # Robust to None / missing fields: an LLM call that didn't return usage
        # info simply adds zero, so the totals stay coherent.
        t = self.tokens.setdefault(layer, {"prompt": 0, "completion": 0})
        t["prompt"] += int(prompt_tokens or 0)
        t["completion"] += int(completion_tokens or 0)

    def set_iterations(self, n):
        self.iterations = n

    def set_validation_passed(self, ok):
        self.validationPassed = bool(ok)

    def total_time(self):
        return time.perf_counter() - self._start

    def total_tokens(self):
        # Sum across all layers; used by the consolidated summary.
        p = sum(v["prompt"] for v in self.tokens.values())
        c = sum(v["completion"] for v in self.tokens.values())
        return p, c

    def to_records(self, branch=""):
        records = []
        layerNames = set(self.samples) | set(self.tokens)
        for layer in layerNames:
            samples = self.samples.get(layer, [])
            tokens = self.tokens.get(layer, {"prompt": 0, "completion": 0})
            n = len(samples)
            total = sum(samples)
            records.append({
                "problem_id": self.problemId,
                "branch": branch,
                "record_type": "layer",
                "layer": layer,
                "calls": n,
                "total_s": round(total, 6),
                "mean_s": round(total / n, 6) if n else 0.0,
                "min_s": round(min(samples), 6) if n else 0.0,
                "max_s": round(max(samples), 6) if n else 0.0,
                "prompt_tokens": tokens["prompt"],
                "completion_tokens": tokens["completion"],
            })
        promptTotal, completionTotal = self.total_tokens()
        records.append({
            "problem_id": self.problemId,
            "branch": branch,
            "record_type": "summary",
            "layer": "ALL",
            "iterations": self.iterations,
            "validation_passed": self.validationPassed,
            "wall_total_s": round(self.total_time(), 6),
            "prompt_tokens_total": promptTotal,
            "completion_tokens_total": completionTotal,
        })
        return records

    def save(self, out_dir, branch="", sample=None):
        # Include the sample index in the filename so the 5 samples of a problem
        # don't overwrite each other (they share problemId). The aggregator
        # picks up all of them through its recursive glob.
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = ("_s" + str(sample)) if sample is not None else ""
        path = out_dir / ("efficiency_" + self.problemId + suffix + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_records(branch=branch), f, ensure_ascii=False, indent=2)
        return path


class Timer:
    # Context manager. If the collector is None it does nothing, so the
    # pipeline still runs when metrics are off.
    def __init__(self, collector, layer):
        self.collector = collector
        self.layer = layer
        self._t0 = 0.0

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, excType, exc, tb):
        if self.collector is not None:
            self.collector.record(self.layer, time.perf_counter() - self._t0)
        return False


# The graph nodes don't share a clean state object, so we thread the timing
# through a process-global collector.
_collector = None


def reset_collector(problem_id):
    global _collector
    _collector = RunCollector(problem_id)
    return _collector


def get_collector():
    return _collector


# Aggregation: turn all the per-problem efficiency_*.json into two tidy CSVs.

def aggregate(results_dir, out_dir=None):
    results_dir = Path(results_dir)
    out_dir = Path(out_dir) if out_dir else results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    layerRows = []
    summaryRows = []
    for path in sorted(results_dir.rglob("efficiency_*.json")):
        with open(path, encoding="utf-8") as f:
            records = json.load(f)
        for r in records:
            if r.get("record_type") == "layer":
                layerRows.append(r)
            elif r.get("record_type") == "summary":
                summaryRows.append(r)

    layerFields = ["problem_id", "branch", "layer", "calls", "total_s", "mean_s", "min_s", "max_s",
                   "prompt_tokens", "completion_tokens"]
    summaryFields = ["problem_id", "branch", "iterations", "validation_passed", "wall_total_s",
                     "prompt_tokens_total", "completion_tokens_total"]

    _write_csv(layerRows, layerFields, out_dir / "efficiency_layers.csv")
    _write_csv(summaryRows, summaryFields, out_dir / "efficiency_summary.csv")

    print("[INFO] efficiency_layers.csv: " + str(len(layerRows)) + " rows")
    print("[INFO] efficiency_summary.csv: " + str(len(summaryRows)) + " rows")


def _write_csv(rows, fieldnames, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
