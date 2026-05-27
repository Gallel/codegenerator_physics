"""Global charts built from the aggregated metric CSVs. Run after a full
benchmark so the CSVs exist. Each function makes one figure; main() runs them
all and drops the PNGs into output/metrics/plots/.

Usage:  python -m src.metrics.plots   (or)   python src/metrics/plots.py
"""
import csv
import json
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display in the sandbox / headless runs.
import matplotlib.pyplot as plt

from src.settings import OUTPUT_DIR, CORPUS_DIR, MAX_ITERATIONS
from src.metrics.stats import mean_ci, spearman

METRICS_DIR = OUTPUT_DIR / "metrics"
PLOTS_DIR = METRICS_DIR / "plots"

DPI = 150


def _read_csv(name):
    path = METRICS_DIR / name
    if not path.exists():
        print("[WARN] missing " + name + ", skipping the charts that need it")
        return None
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(raw):
    # CSV cells are strings; empty means "no value".
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _truthy(raw):
    return str(raw).strip().lower() in ("true", "1", "yes")


def _problem_meta():
    # domain + difficulty per problem id, read from the corpus.
    meta = {}
    for f in sorted(CORPUS_DIR.glob("problem_*/metadata.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        meta[m.get("id", f.parent.name)] = {
            "domain": m.get("domain", "unknown"),
            "difficulty": m.get("difficulty", "unknown"),
        }
    return meta


def _save(fig, filename):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    path = PLOTS_DIR / filename
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("[INFO] wrote " + str(path))


def _grouped_mean(rows, keyFn, valueFn):
    # mean of valueFn over rows, grouped by keyFn; skips None values.
    buckets = {}
    for r in rows:
        v = valueFn(r)
        if v is None:
            continue
        buckets.setdefault(keyFn(r), []).append(v)
    return {k: (sum(vs) / len(vs)) for k, vs in buckets.items()}


# Branch order/labels for the ablation.
BRANCH_ORDER = ["single", "ontology"]
BRANCH_LABEL = {"single": "single", "ontology": "ontology"}
BRANCH_COLOR = {"single": "#C44E52", "ontology": "#55A868"}


def _filter_branch(rows, branch):
    # Keep rows of one branch. Rows without a branch column count as ontology
    # (backward compatible with single-branch CSVs).
    return [r for r in rows if (r.get("branch") or "ontology") == branch]


def _branches_present(rows):
    return [b for b in BRANCH_ORDER
            if any((r.get("branch") or "ontology") == b for r in rows)]


# ---------------------------------------------------------------------------
# 1. Pass@1 vs Pass@5, global.
# ---------------------------------------------------------------------------
def plot_passk_global(passk):
    branches = _branches_present(passk)
    if not branches:
        return
    metrics = ["pass_at_1", "pass_at_5"]
    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.35
    xs = range(len(metrics))
    for i, b in enumerate(branches):
        rows = _filter_branch(passk, b)
        means = []
        for m in metrics:
            vals = [_num(r[m]) for r in rows if _num(r[m]) is not None]
            means.append(sum(vals) / len(vals) if vals else 0.0)
        offs = [x + (i - (len(branches) - 1) / 2) * width for x in xs]
        bars = ax.bar(offs, means, width, label=BRANCH_LABEL.get(b, b),
                      color=BRANCH_COLOR.get(b))
        for bar, mv in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, mv + 0.02, "%.2f" % mv,
                    ha="center", fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(["Pass@1", "Pass@5"])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("rate")
    ax.set_title("Pass@k by branch (ablation)")
    ax.legend()
    _save(fig, "01_passk_global.png")


# ---------------------------------------------------------------------------
# 2. Pass@1 by domain.
# ---------------------------------------------------------------------------
def plot_passk_by_domain(passk, meta):
    branches = _branches_present(passk)
    if not branches:
        return
    # mean Pass@1 per (domain, branch) and the n of each domain.
    byDB, domN = {}, {}
    for r in passk:
        dom = meta.get(r["problem_id"], {}).get("domain", "?")
        b = r.get("branch") or "ontology"
        byDB.setdefault((dom, b), []).append(_num(r["pass_at_1"]))
        if b == "ontology":
            domN[dom] = domN.get(dom, 0) + 1
    # order domains by the ontology-branch mean (most informative on top)
    def dom_mean(dom, b):
        vals = [v for v in byDB.get((dom, b), []) if v is not None]
        return (sum(vals) / len(vals)) if vals else None
    domains = sorted(domN, key=lambda d: (dom_mean(d, "ontology") or 0))
    labels = ["%s (n=%d)" % (d, domN[d]) for d in domains]
    ypos = range(len(domains))
    height = 0.8 / max(1, len(branches))
    fig, ax = plt.subplots(figsize=(8, max(4, len(domains) * 0.5)))
    for i, b in enumerate(branches):
        vals = [dom_mean(d, b) or 0.0 for d in domains]
        offs = [y + (i - (len(branches) - 1) / 2) * height for y in ypos]
        ax.barh(offs, vals, height, label=BRANCH_LABEL.get(b, b), color=BRANCH_COLOR.get(b))
    ax.set_yticks(list(ypos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("mean Pass@1")
    ax.set_title("Pass@1 by physics domain (single vs ontology)")
    ax.legend(loc="lower right", fontsize=8)
    _save(fig, "02_passk_by_domain.png")


# ---------------------------------------------------------------------------
# 3. Pass@1 by difficulty.
# ---------------------------------------------------------------------------
def plot_passk_by_difficulty(passk, meta):
    passk = _filter_branch(passk, "ontology")
    order = {"easy": 0, "medium": 1, "hard": 2}
    byDiff = _grouped_mean(passk,
                           lambda r: meta.get(r["problem_id"], {}).get("difficulty", "?"),
                           lambda r: _num(r["pass_at_1"]))
    if not byDiff:
        return
    labels = sorted(byDiff.keys(), key=lambda k: order.get(k, 99))
    vals = [byDiff[k] for k in labels]
    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(labels, vals, color="#C44E52")
    for b, m in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.02, "%.2f" % m, ha="center")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("mean Pass@1")
    ax.set_title("Pass@1 by difficulty")
    _save(fig, "03_passk_by_difficulty.png")


# ---------------------------------------------------------------------------
# 4. Compile / run / pass funnel per problem (stacked status).
# ---------------------------------------------------------------------------
def plot_status_per_problem(passk):
    # Grouped stacked bars: for each problem, two adjacent stacks (single and
    # ontology) with the three advisor categories. Reading the chart left to
    # right, every pair of bars makes the ablation gain visible problem by
    # problem: how much red (not well formed) shrinks and how much green
    # (correct) grows when the ontology is added.
    branches = _branches_present(passk)
    if not branches:
        return
    # Group rows by problem_id for stable side-by-side bars.
    byProblem = {}
    for r in passk:
        byProblem.setdefault(r["problem_id"], {})[r.get("branch") or "ontology"] = r
    problemIds = sorted(byProblem.keys())
    ids = [p.replace("problem_", "") for p in problemIds]

    # Build the three category stacks per branch.
    cats = {}  # branch -> {correct: [...], compNotOk: [...], failComp: [...]}
    for b in branches:
        correct, compNotOk, failComp = [], [], []
        for pid in problemIds:
            r = byProblem[pid].get(b, {})
            ni = _num(r.get("n_samples")) or 0
            ci = _num(r.get("n_compiled")) or 0
            co = _num(r.get("n_correct")) or 0
            correct.append(co)
            compNotOk.append(ci - co)
            failComp.append(ni - ci)
        cats[b] = {"correct": correct, "compNotOk": compNotOk, "failComp": failComp}

    import numpy as np
    x = np.arange(len(ids))
    width = 0.8 / max(1, len(branches))
    fig, ax = plt.subplots(figsize=(max(8, len(ids) * 0.55), 4.5))

    # Distinct color per category; the bar position distinguishes branches.
    C_OK, C_WF, C_NF = "#55A868", "#DD8452", "#C44E52"
    branchInitial = {"single": "S", "ontology": "O"}

    for i, b in enumerate(branches):
        offs = x + (i - (len(branches) - 1) / 2) * width
        c = cats[b]
        ax.bar(offs, c["correct"], width, color=C_OK,
               label="correct" if i == 0 else None)
        ax.bar(offs, c["compNotOk"], width, bottom=c["correct"], color=C_WF,
               label="well formed, not correct" if i == 0 else None)
        ax.bar(offs, c["failComp"], width,
               bottom=[a + b_ for a, b_ in zip(c["correct"], c["compNotOk"])],
               color=C_NF, label="not well formed" if i == 0 else None)
        # Tiny 'S'/'O' marker below each bar so it's clear which is which.
        for xpos in offs:
            ax.text(xpos, -0.35, branchInitial.get(b, b[0].upper()),
                    ha="center", va="top", fontsize=7, color="#555")

    ax.set_xticks(x)
    ax.set_xticklabels(ids, rotation=90, fontsize=7)
    ax.set_ylabel("samples")
    ax.set_xlabel("problem  (S = single, O = ontology)")
    ax.set_title("Per-problem sample outcome (single vs ontology)")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_ylim(bottom=0)
    _save(fig, "04_status_per_problem.png")


# ---------------------------------------------------------------------------
# 5. CodeBLEU distribution (boxplot of per-problem means).
# ---------------------------------------------------------------------------
def plot_codebleu_distribution(codebleu):
    branches = _branches_present(codebleu)
    if not branches:
        return
    data, labels, colors = [], [], []
    for b in branches:
        vals = [_num(r["codebleu"]) for r in _filter_branch(codebleu, b)
                if _num(r["codebleu"]) is not None]
        if vals:
            data.append(vals)
            labels.append(BRANCH_LABEL.get(b, b))
            colors.append(BRANCH_COLOR.get(b))
    if not data:
        return
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.boxplot(data, vert=True, tick_labels=labels, widths=0.5)
    for i, (vals, col) in enumerate(zip(data, colors), start=1):
        ax.scatter([i] * len(vals), vals, color=col, alpha=0.6, zorder=3)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("CodeBLEU (per-problem mean)")
    ax.set_title("CodeBLEU distribution by branch")
    _save(fig, "05_codebleu_distribution.png")


# ---------------------------------------------------------------------------
# 6. CodeBLEU 4-component breakdown (mean over problems).
# ---------------------------------------------------------------------------
def plot_codebleu_components(codebleu):
    comps = ["ngram_match", "weighted_ngram_match", "syntax_match", "dataflow_match"]
    labels = ["n-gram", "weighted\nn-gram", "syntax\n(AST)", "dataflow"]
    branches = _branches_present(codebleu)
    if not branches:
        return
    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.8 / max(1, len(branches))
    xs = range(len(comps))
    for i, b in enumerate(branches):
        rows = _filter_branch(codebleu, b)
        means = []
        for c in comps:
            vs = [_num(r[c]) for r in rows if _num(r[c]) is not None]
            means.append(sum(vs) / len(vs) if vs else 0.0)
        offs = [x + (i - (len(branches) - 1) / 2) * width for x in xs]
        ax.bar(offs, means, width, label=BRANCH_LABEL.get(b, b), color=BRANCH_COLOR.get(b))
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("mean score")
    ax.set_title("CodeBLEU components by branch")
    ax.legend()
    _save(fig, "06_codebleu_components.png")


# ---------------------------------------------------------------------------
# 7. LCS rule compliance: pass fraction per rule.
# ---------------------------------------------------------------------------
def plot_lcs_rule_compliance(lcsChecks, min_n=3):
    if not lcsChecks:
        return
    byRule = {}
    for r in lcsChecks:
        rule = r["rule"]
        byRule.setdefault(rule, [0, 0])
        byRule[rule][1] += 1
        if _truthy(r["passed"]):
            byRule[rule][0] += 1
    # Drop rules applied to too few cases: a 0% or 100% based on 1 sample is
    # noise, not signal. Rare rules live in the appendix table instead.
    items = [(k, v) for k, v in byRule.items() if v[1] >= min_n]
    if not items:
        items = list(byRule.items())  # fall back if everything is rare
    items = sorted(items, key=lambda kv: kv[1][0] / kv[1][1])
    labels = ["%s (n=%d)" % (k, v[1]) for k, v in items]
    fracs = [v[0] / v[1] for _, v in items]
    fig, ax = plt.subplots(figsize=(7, max(4, len(items) * 0.3)))
    ax.barh(labels, fracs, color="#55A868")
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("fraction of applicable checks passed")
    ax.set_title("LCS compliance per rule (n>=3 applications)")
    plt.yticks(fontsize=7)
    _save(fig, "07_lcs_rule_compliance.png")


# ---------------------------------------------------------------------------
# 8. CAS lax vs strict (global mean).
# ---------------------------------------------------------------------------
def plot_cas_lax_vs_strict(cas):
    branches = _branches_present(cas)
    if not branches:
        return
    metrics = ["cas_lax", "cas_strict"]
    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.35
    xs = range(len(metrics))
    for i, b in enumerate(branches):
        rows = _filter_branch(cas, b)
        means = []
        for m in metrics:
            vals = [_num(r[m]) for r in rows if _num(r[m]) is not None]
            means.append(sum(vals) / len(vals) if vals else 0.0)
        offs = [x + (i - (len(branches) - 1) / 2) * width for x in xs]
        bars = ax.bar(offs, means, width, label=BRANCH_LABEL.get(b, b), color=BRANCH_COLOR.get(b))
        for bar, mv in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, mv + 0.02, "%.2f" % mv, ha="center", fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(["CAS-lax", "CAS-strict"])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("mean")
    ax.set_title("CAS by branch")
    ax.legend()
    _save(fig, "08_cas_lax_vs_strict.png")


# ---------------------------------------------------------------------------
# 9. Time per layer (boxplot over all samples).
# ---------------------------------------------------------------------------
def plot_efficiency_time_per_layer(layers):
    if not layers:
        return
    branches = _branches_present(layers)
    # Collect layer -> {branch: [times]}
    perLayer = {}
    for r in layers:
        t = _num(r["total_s"])
        if t is None:
            continue
        b = r.get("branch") or "ontology"
        perLayer.setdefault(r["layer"], {}).setdefault(b, []).append(t)
    if not perLayer:
        return
    # Order layers by overall median time.
    def layer_median(d):
        allv = [t for vs in d.values() for t in vs]
        return statistics.median(allv) if allv else 0.0
    layerNames = sorted(perLayer, key=lambda k: layer_median(perLayer[k]))

    fig, ax = plt.subplots(figsize=(8, max(4, len(layerNames) * 0.5)))
    width = 0.8 / max(1, len(branches))
    ypos = range(len(layerNames))
    for i, b in enumerate(branches):
        data, positions = [], []
        for j, lname in enumerate(layerNames):
            vals = perLayer[lname].get(b)
            if vals:
                data.append(vals)
                positions.append(j + (i - (len(branches) - 1) / 2) * width)
        if not data:
            continue
        bp = ax.boxplot(data, positions=positions, widths=width * 0.9,
                        vert=False, patch_artist=True)
        for box in bp["boxes"]:
            box.set_facecolor(BRANCH_COLOR.get(b, "#888888"))
            box.set_alpha(0.7)
    ax.set_yticks(list(ypos))
    ax.set_yticklabels(layerNames, fontsize=8)
    ax.set_xlabel("seconds (total per run)")
    ax.set_title("Time per pipeline layer by branch")
    handles = [plt.Rectangle((0, 0), 1, 1, color=BRANCH_COLOR.get(b), alpha=0.7) for b in branches]
    ax.legend(handles, [BRANCH_LABEL.get(b, b) for b in branches], loc="lower right", fontsize=8)
    _save(fig, "09_efficiency_time_per_layer.png")


# ---------------------------------------------------------------------------
# 10. Iterations histogram (self-correction loop).
# ---------------------------------------------------------------------------
def plot_iterations_histogram(effSummary):
    # Only the ontology branch loops; 'single' is always 1 iteration, so we
    # restrict to ontology and split validated vs. exhausted (hit MAX_ITERATIONS).
    rows = _filter_branch(effSummary, "ontology")
    if not rows:
        rows = effSummary  # backward compatible with single-branch runs
    validated, exhausted = [], []
    for r in rows:
        it = _num(r["iterations"])
        if it is None:
            continue
        if _truthy(r.get("validation_passed")):
            validated.append(it)
        else:
            exhausted.append(it)
    allIts = validated + exhausted
    if not allIts:
        return
    maxIt = int(max(allIts + [MAX_ITERATIONS]))
    edges = [b - 0.5 for b in range(1, maxIt + 2)]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist([validated, exhausted], bins=edges, stacked=True,
            color=["#55A868", "#C44E52"],
            label=["validated", "hit max (%d)" % MAX_ITERATIONS])
    ax.set_xlabel("iterations to validate (ontology branch)")
    ax.set_ylabel("number of runs")
    ax.set_xticks(list(range(1, maxIt + 1)))
    ax.set_title("Self-correction iterations until validation")
    ax.legend()
    _save(fig, "10_iterations_histogram.png")


# ---------------------------------------------------------------------------
# 11. Transversal: Pass@1 vs CodeBLEU per problem.
# ---------------------------------------------------------------------------
def plot_pass_vs_codebleu(passk, codebleu):
    passk = _filter_branch(passk, "ontology")
    codebleu = _filter_branch(codebleu, "ontology")
    cbById = {r["problem_id"]: _num(r["codebleu"]) for r in codebleu}
    xs, ys = [], []
    for r in passk:
        cb = cbById.get(r["problem_id"])
        p1 = _num(r["pass_at_1"])
        if cb is None or p1 is None:
            continue
        xs.append(cb)
        ys.append(p1)
    if not xs:
        return
    rho, n = spearman(xs, ys)
    # Pass@1 is discretized (multiples of 1/n_samples); jitter the y so
    # overlapping points are visible. Jitter is cosmetic only.
    import random
    rng = random.Random(0)
    ys_j = [y + rng.uniform(-0.02, 0.02) for y in ys]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(xs, ys_j, color="#4C72B0", alpha=0.7)
    ax.set_xlabel("CodeBLEU (structural similarity)")
    ax.set_ylabel("Pass@1 (correctness, jittered)")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.08, 1.08)
    title = "Correctness vs similarity to human reference"
    if rho is not None:
        title += "  (Spearman rho=%.2f, n=%d)" % (rho, n)
    ax.set_title(title, fontsize=11)
    _save(fig, "11_pass_vs_codebleu.png")


def plot_ablation_summary(passk, codebleu, lcsSummary, cas):
    # Headline figure: one grouped bar per metric, single vs ontology, with 95% CI error
    # bars so the reader sees the uncertainty (n is small).
    def branch_stat(rows, col):
        m = {}
        for b in _branches_present(rows):
            vals = [_num(r[col]) for r in _filter_branch(rows, b)]
            mean, half, _ = mean_ci(vals)
            m[b] = (mean if mean is not None else 0.0, half if half is not None else 0.0)
        return m

    series = [
        ("Pass@1", branch_stat(passk, "pass_at_1")),
        ("CodeBLEU", branch_stat(codebleu, "codebleu")),
        ("LCS", branch_stat(lcsSummary or [], "lcs")),
        ("CAS-strict", branch_stat(cas or [], "cas_strict")),
    ]
    branches = _branches_present(passk)
    if not branches:
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    width = 0.8 / max(1, len(branches))
    xs = range(len(series))
    for i, b in enumerate(branches):
        vals = [m.get(b, (0.0, 0.0))[0] for _, m in series]
        errs = [m.get(b, (0.0, 0.0))[1] for _, m in series]
        offs = [x + (i - (len(branches) - 1) / 2) * width for x in xs]
        bars = ax.bar(offs, vals, width, yerr=errs, capsize=3,
                      label=BRANCH_LABEL.get(b, b), color=BRANCH_COLOR.get(b))
        for bar, mv in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, mv + 0.03, "%.2f" % mv, ha="center", fontsize=8)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([name for name, _ in series])
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("mean (95% CI)")
    ax.set_title("Ablation: single vs ontology")
    ax.legend()
    _save(fig, "12_ablation_summary.png")


def main():
    meta = _problem_meta()
    passk = _read_csv("passk_summary.csv")
    codebleu = _read_csv("codebleu_summary.csv")
    lcsSummary = _read_csv("lcs_summary.csv")
    lcsChecks = _read_csv("lcs_checks.csv")
    cas = _read_csv("cas_summary.csv")
    layers = _read_csv("efficiency_layers.csv")
    effSummary = _read_csv("efficiency_summary.csv")

    # NOTE: Pass@k global, Pass@1-by-difficulty and CAS lax/strict are now
    # reported as TABLES (see tables.py), not figures: they are a handful of
    # scalars each, better given as exact citable values. The figures kept here
    # are the ones that show distribution / contrast / per-problem structure.
    if passk:
        plot_status_per_problem(passk)            # per-problem outcome (27 bars)
        plot_passk_by_domain(passk, meta)         # single vs ontology per domain, n annotated
    if codebleu:
        plot_codebleu_distribution(codebleu)      # boxplot by branch
        plot_codebleu_components(codebleu)        # 4-component breakdown
    if lcsChecks:
        plot_lcs_rule_compliance(lcsChecks)       # filtered to rules with n>=min
    if layers:
        plot_efficiency_time_per_layer(layers)    # boxplot by branch
    if effSummary:
        plot_iterations_histogram(effSummary)     # validated vs exhausted
    if passk and codebleu:
        plot_pass_vs_codebleu(passk, codebleu)    # scatter + Spearman
    if passk:
        plot_ablation_summary(passk, codebleu or [], lcsSummary or [], cas or [])  # headline

    print("[INFO] plots written to " + str(PLOTS_DIR))


if __name__ == "__main__":
    main()
