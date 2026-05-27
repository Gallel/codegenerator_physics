import csv
import json
import math
from pathlib import Path

from src.metrics.pass_at_k import _to_float

SPEED_OF_LIGHT = 2.998e8  # m/s, sanity bound on velocities.
REL_TOL = 0.02  # 2% tolerance for the relational checks (rounded references).


def _is(*substrings, exclude=()):
    # applies_fn for per-goal rules: fires when the goal name contains any of
    # the substrings and none of the excluded ones.
    def fn(domain, goal, value):
        if any(x in goal for x in exclude):
            return False
        return any(s in goal for s in substrings)
    return fn


def _finite(value):
    return value is not None and not math.isnan(value) and not math.isinf(value)


# ---------------------------------------------------------------------------
# Type 1: per-goal rules. (rule_id, applies(domain, goal, value), check(value))
# ---------------------------------------------------------------------------
_GOAL_RULES = [
    # Non-negative magnitudes.
    ("period_positive", _is("period"), lambda v: v > 0),
    ("frequency_positive", _is("frequency"), lambda v: v > 0),
    ("mass_positive", _is("mass"), lambda v: v > 0),
    ("density_positive", _is("density"), lambda v: v > 0),
    ("volume_positive", _is("volume"), lambda v: v > 0),
    ("time_positive", _is("time", "_time"), lambda v: v > 0),
    ("height_nonneg", _is("height", exclude=("time",)), lambda v: v >= 0),
    ("distance_nonneg", _is("distance", "_covered"), lambda v: v >= 0),
    ("kinetic_energy_nonneg", _is("kinetic_energy"), lambda v: v >= 0),
    ("potential_energy_nonneg", _is("potential_energy"), lambda v: v >= 0),
    ("centripetal_accel_positive", _is("centripetal_acceleration"), lambda v: v > 0),
    ("surface_gravity_positive", _is("surface_gravity", "gravity"), lambda v: v > 0),
    ("escape_velocity_positive", _is("escape_velocity"), lambda v: v > 0),
    ("energy_consumed_nonneg", _is("energy_consumed"), lambda v: v >= 0),
    # Force magnitude is positive (generic: covers engine/average/advance/...).
    ("force_positive", _is("force"), lambda v: v > 0),
    # Acceleration can be negative (braking), so we only require it to be finite.
    ("acceleration_finite", _is("acceleration", exclude=("centripetal",)), lambda v: _finite(v)),
    # Sanity bound on any velocity.
    ("velocity_below_c", _is("velocity"), lambda v: abs(v) < SPEED_OF_LIGHT),
    # Mechanical energy near the surface (work_energy) is Ec+Ep >= 0.
    ("surface_mech_energy_nonneg",
     lambda domain, goal, value: domain == "work_energy" and "mechanical_energy" in goal,
     lambda v: v >= 0),
    # Orbital mechanical energy of a bound orbit is negative.
    ("orbital_mech_energy_negative",
     lambda domain, goal, value: domain == "gravitation" and "mechanical_energy" in goal,
     lambda v: v < 0),
    ("orbital_energy_required_positive",
     lambda domain, goal, value: domain == "gravitation" and "energy_required" in goal,
     lambda v: v > 0),
]


# ---------------------------------------------------------------------------
# Type 2: relational rules between several goals of the same program.
# Each: (rule_id, needs(list of goal substrings), check(values_dict)).
# The rule only applies if all needed goals are present and finite.
# ---------------------------------------------------------------------------

def _close(a, b, tol=REL_TOL):
    if a is None or b is None:
        return False
    if b == 0.0:
        return abs(a) <= tol
    return abs(a - b) / abs(b) <= tol


def _find(values, *substrings, exclude=()):
    # Return the value of the first goal whose name matches.
    for g, v in values.items():
        if any(x in g for x in exclude):
            continue
        if all(s in g for s in substrings):
            return v
    return None


def _check_mech_energy_sum(values):
    ec = _find(values, "kinetic_energy")
    ep = _find(values, "potential_energy")
    em = _find(values, "mechanical_energy")
    if None in (ec, ep, em):
        return None  # not applicable
    return _close(em, ec + ep)


def _check_orbit_v_T(values):
    # v should be consistent with 2*pi*r / T, but we don't have r here;
    # instead check both are positive and finite and that v*T (a length) is
    # within a plausible planetary range (> Earth radius, < 1 AU).
    v = _find(values, "orbital_velocity")
    t = _find(values, "orbital_period")
    if None in (v, t):
        return None
    if not (_finite(v) and _finite(t)) or v <= 0 or t <= 0:
        return False
    circumference = v * t  # = 2*pi*r
    return 1.0e6 < circumference < 1.0e12  # ~ between 160 km and 1 AU radius


def _check_monthly_is_30_daily(values):
    daily = _find(values, "daily_energy")
    monthly = _find(values, "monthly_energy")
    if None in (daily, monthly):
        return None
    return _close(monthly, 30.0 * daily)


def _check_kwh_joule(values):
    kwh = _find(values, "energy_consumed_kwh")
    j = _find(values, "energy_consumed_j")
    if None in (kwh, j):
        return None
    return _close(j, kwh * 3.6e6)


_RELATIONAL_RULES = [
    ("mechanical_energy_equals_sum", _check_mech_energy_sum),
    ("orbital_v_period_consistency", _check_orbit_v_T),
    ("monthly_energy_is_30_daily", _check_monthly_is_30_daily),
    ("energy_kwh_joule_consistency", _check_kwh_joule),
]


def evaluate(produced, domain):
    """Apply the rule catalogue to one program's produced values.

    `produced` is a dict goal-name -> raw value. Returns the per-rule outcome
    and the LCS score (passed / applicable). Covers both per-goal rules and
    relational rules between goals.
    """
    checks = []
    valuesByGoal = {str(k).lower(): _to_float(v) for k, v in (produced or {}).items()}

    # Type 1: per-goal.
    for ruleId, applies, check in _GOAL_RULES:
        for goal, value in valuesByGoal.items():
            if value is None or not applies(domain, goal, value):
                continue
            ok = _finite(value) and bool(check(value))
            checks.append({"rule": ruleId, "goal": goal, "value": value, "passed": ok})

    # Type 2: relational. Applies only when its goals are present.
    for ruleId, check in _RELATIONAL_RULES:
        outcome = check(valuesByGoal)
        if outcome is None:
            continue
        checks.append({"rule": ruleId, "goal": "(relational)", "value": None, "passed": bool(outcome)})

    applicable = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    score = (passed / applicable) if applicable else None

    return {
        "domain": domain,
        "applicable": applicable,
        "passed": passed,
        "lcs": score,
        "checks": checks,
    }


def save_result(problem_id, result, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = dict(result)
    rec["problem_id"] = problem_id
    path = out_dir / ("lcs_" + problem_id + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return path


def aggregate(results_dir, out_dir=None):
    results_dir = Path(results_dir)
    out_dir = Path(out_dir) if out_dir else results_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    checkRows = []
    summaryRows = []
    scores = []
    for path in sorted(results_dir.rglob("lcs_*.json")):
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        pid = rec.get("problem_id", path.stem)
        for c in rec.get("checks", []):
            checkRows.append({
                "problem_id": pid, "rule": c["rule"], "goal": c["goal"],
                "value": c["value"], "passed": c["passed"],
            })
        summaryRows.append({
            "problem_id": pid,
            "branch": rec.get("branch", "ontology"),
            "domain": rec.get("domain"),
            "applicable": rec.get("applicable"),
            "passed": rec.get("passed"),
            "lcs": rec.get("lcs"),
            "lcs_std": rec.get("lcs_std"),
            "lcs_max_correct": rec.get("lcs_max_correct"),
            "lcs_min_correct": rec.get("lcs_min_correct"),
        })
        if rec.get("lcs") is not None:
            scores.append(rec["lcs"])

    _write_csv(checkRows, ["problem_id", "rule", "goal", "value", "passed"],
               out_dir / "lcs_checks.csv")
    _write_csv(summaryRows, ["problem_id", "branch", "domain", "applicable", "passed", "lcs", "lcs_std",
                             "lcs_max_correct", "lcs_min_correct"],
               out_dir / "lcs_summary.csv")

    meanLcs = (sum(scores) / len(scores)) if scores else 0.0
    print("[INFO] lcs_checks.csv: " + str(len(checkRows)) + " rows")
    print("[INFO] lcs_summary.csv: " + str(len(summaryRows)) + " rows")
    print("[INFO] mean LCS (problems with applicable rules): " + ("%.3f" % meanLcs))


def _write_csv(rows, fieldnames, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
