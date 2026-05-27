import csv
import json
from pathlib import Path

# CAS measures whether the program covers the goals the statement asks for.
# It reuses the matching that Pass@k already computed for each expected goal.
# A goal is "covered" if Pass@k matched it at all, either by a recognizable
# name (matched_by == "name") or by value (matched_by == "value", e.g. the LLM
# produced the right number under an opaque name like 'K' for kinetic_energy).
#
# CAS-lax    = goals covered (by name or value) / total goals.
# CAS-strict = goals covered AND with a correct value / total goals.
#
# The name-vs-value split is reported separately, so we can also say how
# descriptively the model named its variables.


def evaluate(passk_goals):
    """Compute CAS from the per-goal info produced by Pass@k.

    `passk_goals` is the dict result["goals"] from pass_at_k.evaluate:
        { goal: {"reference":..., "generated":..., "match":bool, "matched_by":...} }
    """
    total = len(passk_goals)
    covered = 0      # matched at all (by name or value)
    byName = 0       # of those, reported under a recognizable name
    byValueOnly = 0  # of those, only identifiable by value
    strict = 0       # covered AND correct value

    perGoal = {}
    for goal, info in passk_goals.items():
        matchedBy = info.get("matched_by")
        correct = bool(info.get("match"))
        reportedByName = matchedBy == "name"
        isCovered = matchedBy in ("name", "value")
        if isCovered:
            covered += 1
            if reportedByName:
                byName += 1
            else:
                byValueOnly += 1
            if correct:
                strict += 1
        perGoal[goal] = {
            "matched_by": matchedBy,
            "correct": correct,
            "covered": isCovered,
            "reported_by_name": reportedByName,
        }

    casLax = (covered / total) if total else None
    casStrict = (strict / total) if total else None

    return {
        "total_goals": total,
        "covered": covered,
        "reported_by_name": byName,
        "value_only": byValueOnly,
        "reported_and_correct": strict,
        "cas_lax": casLax,
        "cas_strict": casStrict,
        "goals": perGoal,
    }


def save_result(problem_id, result, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = dict(result)
    rec["problem_id"] = problem_id
    path = out_dir / ("cas_" + problem_id + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return path


def aggregate(results_dir, out_dir=None):
    results_dir = Path(results_dir)
    out_dir = Path(out_dir) if out_dir else results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    goalRows = []
    summaryRows = []
    laxScores = []
    strictScores = []
    for path in sorted(results_dir.rglob("cas_*.json")):
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        pid = rec.get("problem_id", path.stem)
        for goal, info in rec.get("goals", {}).items():
            goalRows.append({
                "problem_id": pid, "goal": goal,
                "matched_by": info.get("matched_by"),
                "covered": info.get("covered"),
                "reported_by_name": info.get("reported_by_name"),
                "correct": info.get("correct"),
            })
        summaryRows.append({
            "problem_id": pid,
            "branch": rec.get("branch", "ontology"),
            "total_goals": rec.get("total_goals"),
            "covered": rec.get("covered"),
            "reported_by_name": rec.get("reported_by_name"),
            "value_only": rec.get("value_only"),
            "reported_and_correct": rec.get("reported_and_correct"),
            "cas_lax": rec.get("cas_lax"),
            "cas_lax_std": rec.get("cas_lax_std"),
            "cas_lax_max_correct": rec.get("cas_lax_max_correct"),
            "cas_lax_min_correct": rec.get("cas_lax_min_correct"),
            "cas_strict": rec.get("cas_strict"),
            "cas_strict_std": rec.get("cas_strict_std"),
            "cas_strict_max_correct": rec.get("cas_strict_max_correct"),
            "cas_strict_min_correct": rec.get("cas_strict_min_correct"),
        })
        if rec.get("cas_lax") is not None:
            laxScores.append(rec["cas_lax"])
        if rec.get("cas_strict") is not None:
            strictScores.append(rec["cas_strict"])

    _write_csv(goalRows, ["problem_id", "goal", "matched_by", "covered", "reported_by_name", "correct"],
               out_dir / "cas_goals.csv")
    _write_csv(summaryRows, ["problem_id", "branch", "total_goals", "covered", "reported_by_name", "value_only",
                             "reported_and_correct", "cas_lax", "cas_lax_std",
                             "cas_lax_max_correct", "cas_lax_min_correct",
                             "cas_strict", "cas_strict_std",
                             "cas_strict_max_correct", "cas_strict_min_correct"],
               out_dir / "cas_summary.csv")

    meanLax = (sum(laxScores) / len(laxScores)) if laxScores else 0.0
    meanStrict = (sum(strictScores) / len(strictScores)) if strictScores else 0.0
    print("[INFO] cas_goals.csv: " + str(len(goalRows)) + " rows")
    print("[INFO] cas_summary.csv: " + str(len(summaryRows)) + " rows")
    print("[INFO] mean CAS-lax: " + ("%.3f" % meanLax) + "  mean CAS-strict: " + ("%.3f" % meanStrict))


def _write_csv(rows, fieldnames, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
