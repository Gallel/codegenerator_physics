"""Result tables for the thesis, in three formats per table:

  - .csv   : import into Word as an editable native table.
  - .html  : self-contained, styled; paste into web or a document.
  - .png   : quick visual check without opening Word or a browser.

Reads the aggregated metric CSVs (produced by the metric aggregators) and the
corpus metadata. Run after a benchmark:  python -m src.metrics.tables
"""
import csv
import math
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.settings import OUTPUT_DIR, CORPUS_DIR
from src.metrics.stats import wilson_interval, mean_ci
import json

METRICS_DIR = OUTPUT_DIR / "metrics"
TABLES_DIR = METRICS_DIR / "tables"

BRANCH_ORDER = ["single", "ontology"]
BRANCH_LABEL = {"single": "single", "ontology": "ontology"}

# OpenAI pricing per 1K tokens (USD). Defaults are placeholders; override in
# .env to match the model actually used in the experiment. Tokens stay the
# robust metric; the cost is a derived convenience figure that ages quickly.
PRICE_INPUT_PER_1K  = float(os.getenv("PRICE_INPUT_PER_1K",  "0.005"))
PRICE_OUTPUT_PER_1K = float(os.getenv("PRICE_OUTPUT_PER_1K", "0.015"))


# --------------------------------------------------------------------------
# IO helpers
# --------------------------------------------------------------------------
def _read_csv(name):
    path = METRICS_DIR / name
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(raw):
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _filter_branch(rows, branch):
    return [r for r in rows if (r.get("branch") or "ontology") == branch]


def _branches_present(rows):
    return [b for b in BRANCH_ORDER
            if any((r.get("branch") or "ontology") == b for r in rows)]


def _problem_meta():
    meta = {}
    for f in sorted(CORPUS_DIR.glob("problem_*/metadata.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        meta[m.get("id", f.parent.name)] = {
            "domain": m.get("domain", "unknown"),
            "difficulty": m.get("difficulty", "unknown"),
        }
    return meta


def _fmt(x, nd=3):
    if x is None:
        return "-"
    if isinstance(x, float):
        return ("%." + str(nd) + "f") % x
    return str(x)


# --------------------------------------------------------------------------
# Generic writers: a "table" is (title, header list, list-of-row-lists).
# --------------------------------------------------------------------------
def _write_csv(table, path):
    title, header, rows = table
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def _write_html(table, path):
    title, header, rows = table
    css = (
        "table{border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;"
        "font-size:14px;margin:8px 0}"
        "caption{font-weight:bold;text-align:left;padding:6px 0;font-size:15px}"
        "th,td{border:1px solid #bbb;padding:6px 10px;text-align:center}"
        "th{background:#f0f0f0}"
        "tr:nth-child(even) td{background:#fafafa}"
        "td:first-child,th:first-child{text-align:left}"
    )
    parts = ["<!doctype html><meta charset='utf-8'><style>" + css + "</style>",
             "<table><caption>" + _esc(title) + "</caption><thead><tr>"]
    parts += ["<th>" + _esc(h) + "</th>" for h in header]
    parts.append("</tr></thead><tbody>")
    for r in rows:
        parts.append("<tr>" + "".join("<td>" + _esc(str(c)) + "</td>" for c in r) + "</tr>")
    parts.append("</tbody></table>")
    path.write_text("".join(parts), encoding="utf-8")


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _write_png(table, path):
    title, header, rows = table
    nrows = len(rows) + 1
    ncols = len(header)
    fig, ax = plt.subplots(figsize=(min(2 + ncols * 1.6, 16), 0.5 + nrows * 0.35))
    ax.axis("off")
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left", pad=10)
    tbl = ax.table(cellText=[[str(c) for c in r] for r in rows],
                   colLabels=header, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.3)
    for (row, col), cell in tbl.get_celld().items():
        if row == 0:
            cell.set_facecolor("#f0f0f0")
            cell.set_text_props(fontweight="bold")
        if col == 0:
            cell.set_text_props(ha="left")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _emit(table, stem):
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    _write_csv(table, TABLES_DIR / (stem + ".csv"))
    _write_html(table, TABLES_DIR / (stem + ".html"))
    _write_png(table, TABLES_DIR / (stem + ".png"))
    print("[INFO] wrote " + stem + ".{csv,html,png}")


# --------------------------------------------------------------------------
# Table 1: main results per branch (with CIs).
# --------------------------------------------------------------------------
def table_main_results(passk, codebleu, lcsSummary, cas):
    header = ["Branch", "Pass@1 [95% CI]", "Pass@5 [95% CI]",
              "LCS (mean)", "CAS-lax", "CAS-strict", "CodeBLEU (mean)", "n"]
    rows = []
    for b in _branches_present(passk or []):
        pk = _filter_branch(passk, b)
        nprob = len(pk)
        succ1 = sum(1 for r in pk if (_num(r.get("pass_at_1")) or 0) >= 0.999)
        # Pass@1 mean is the average per-problem estimate; CI via Wilson on the
        # count of fully-solved problems is a readable proxy for the corpus rate.
        p1mean, _, _ = mean_ci([_num(r.get("pass_at_1")) for r in pk])
        p5mean, _, _ = mean_ci([_num(r.get("pass_at_5")) for r in pk])
        lo1, hi1 = wilson_interval(succ1, nprob) if nprob else (0, 0)
        succ5 = sum(1 for r in pk if (_num(r.get("pass_at_5")) or 0) >= 0.999)
        lo5, hi5 = wilson_interval(succ5, nprob) if nprob else (0, 0)

        lcsB = _filter_branch(lcsSummary or [], b)
        casB = _filter_branch(cas or [], b)
        cbB = _filter_branch(codebleu or [], b)
        lcsM, _, _ = mean_ci([_num(r.get("lcs")) for r in lcsB])
        laxM, _, _ = mean_ci([_num(r.get("cas_lax")) for r in casB])
        strM, _, _ = mean_ci([_num(r.get("cas_strict")) for r in casB])
        cbM, _, _ = mean_ci([_num(r.get("codebleu")) for r in cbB])

        rows.append([
            BRANCH_LABEL.get(b, b),
            "%s [%s, %s]" % (_fmt(p1mean, 2), _fmt(lo1, 2), _fmt(hi1, 2)),
            "%s [%s, %s]" % (_fmt(p5mean, 2), _fmt(lo5, 2), _fmt(hi5, 2)),
            _fmt(lcsM), _fmt(laxM), _fmt(strM), _fmt(cbM), nprob,
        ])
    return ("Table 1. Main results by branch (mean over problems; Pass@k CI = Wilson on fully-solved count).",
            header, rows)


# --------------------------------------------------------------------------
# Table 2: per-domain Pass@1, single vs ontology, with n.
# --------------------------------------------------------------------------
def table_by_domain(passk, meta):
    byDomBranch = {}
    domN = {}
    for r in passk or []:
        pid = r.get("problem_id")
        dom = meta.get(pid, {}).get("domain", "unknown")
        b = r.get("branch") or "ontology"
        byDomBranch.setdefault((dom, b), []).append(_num(r.get("pass_at_1")))
        if b == "ontology":
            domN[dom] = domN.get(dom, 0) + 1
    branches = _branches_present(passk or [])
    domains = sorted(domN, key=lambda d: domN[d], reverse=True)
    header = ["Domain", "n"] + [BRANCH_LABEL.get(b, b) for b in branches] + ["delta (ontology - single)"]
    rows = []
    for dom in domains:
        cells = [dom, domN.get(dom, 0)]
        means = {}
        for b in branches:
            vals = [v for v in byDomBranch.get((dom, b), []) if v is not None]
            means[b] = (sum(vals) / len(vals)) if vals else None
            cells.append(_fmt(means[b], 2))
        if "single" in means and "ontology" in means and None not in (means["single"], means["ontology"]):
            cells.append(_fmt(means["ontology"] - means["single"], 2))
        else:
            cells.append("-")
        rows.append(cells)
    return ("Table 2. Pass@1 by physics domain (mean per problem; n = problems in domain).",
            header, rows)


# --------------------------------------------------------------------------
# Table: per-sample outcome by branch (advisor nomenclature).
# --------------------------------------------------------------------------
def table_outcome_by_branch(passk):
    # Aggregate over the whole corpus: how many generated samples were
    #   not well formed      = did not compile        (n_samples - n_compiled)
    #   well formed, not correct = compiled but failed tests (n_compiled - n_correct)
    #   correct              = compiled and passed     (n_correct)
    # for each branch (single vs ontology).
    branches = _branches_present(passk or [])
    if not branches:
        return None
    agg = {b: {"total": 0, "compiled": 0, "correct": 0} for b in branches}
    for r in passk:
        b = r.get("branch") or "ontology"
        if b not in agg:
            continue
        agg[b]["total"] += int(_num(r.get("n_samples")) or 0)
        agg[b]["compiled"] += int(_num(r.get("n_compiled")) or 0)
        agg[b]["correct"] += int(_num(r.get("n_correct")) or 0)

    header = ["Outcome"] + [BRANCH_LABEL.get(b, b) for b in branches]
    categories = [
        ("not well formed",
         lambda a: a["total"] - a["compiled"]),
        ("well formed, not correct",
         lambda a: a["compiled"] - a["correct"]),
        ("correct",
         lambda a: a["correct"]),
    ]
    rows = []
    for name, fn_count in categories:
        cells = [name]
        for b in branches:
            a = agg[b]
            cnt = fn_count(a)
            pct = (100.0 * cnt / a["total"]) if a["total"] else 0.0
            cells.append("%d (%.1f%%)" % (cnt, pct))
        rows.append(cells)
    # total samples row for context
    totalRow = ["total samples"] + [str(agg[b]["total"]) for b in branches]
    rows.append(totalRow)
    return ("Table. Per-sample outcome by branch (whole corpus; counts and % of generated samples).",
            header, rows)


# --------------------------------------------------------------------------
# Table 3: CodeBLEU components per branch.
# --------------------------------------------------------------------------
def table_codebleu_components(codebleu):
    comps = ["ngram_match", "weighted_ngram_match", "syntax_match", "dataflow_match", "codebleu"]
    labels = ["n-gram", "weighted n-gram", "syntax (AST)", "dataflow", "CodeBLEU (total)"]
    header = ["Branch"] + labels
    rows = []
    for b in _branches_present(codebleu or []):
        cb = _filter_branch(codebleu, b)
        cells = [BRANCH_LABEL.get(b, b)]
        for c in comps:
            m, _, _ = mean_ci([_num(r.get(c)) for r in cb])
            cells.append(_fmt(m))
        rows.append(cells)
    return ("Table 3. CodeBLEU components by branch (mean over problems).", header, rows)


# --------------------------------------------------------------------------
# Appendix table: LCS rule compliance with n.
# --------------------------------------------------------------------------
def table_lcs_rules(lcsChecks, min_n=1):
    byRule = {}
    for r in lcsChecks or []:
        rule = r.get("rule")
        byRule.setdefault(rule, [0, 0])
        byRule[rule][1] += 1
        if str(r.get("passed")).strip().lower() in ("true", "1", "yes"):
            byRule[rule][0] += 1
    header = ["Rule", "n (applied)", "passed", "compliance"]
    rows = []
    for rule, (p, tot) in sorted(byRule.items(), key=lambda kv: kv[1][0] / kv[1][1] if kv[1][1] else 0):
        if tot < min_n:
            continue
        rows.append([rule, tot, p, _fmt(p / tot, 2) if tot else "-"])
    return ("Appendix Table. LCS rule compliance (n = times the rule applied).", header, rows)


# --------------------------------------------------------------------------
# Table: token efficiency by branch.
# --------------------------------------------------------------------------
def table_token_efficiency(efficiencySummary, passk, codebleu=None):
    # Combines efficiency (token totals per sample and branch, recorded by
    # RunCollector) with the quality metrics (Pass@k for correctness,
    # CodeBLEU for structural similarity to the human reference). Reports
    # efficiency along two complementary dimensions:
    #   - toward correctness: tokens spent per correct sample (TPC)
    #   - toward similarity:  CodeBLEU points earned per 1000 tokens spent
    # The two answer different questions and a system can be efficient on
    # one while being inefficient on the other (e.g. producing code that
    # looks human but doesn't run, or code that runs but reads awkwardly).
    if not efficiencySummary or not passk:
        return None

    agg = {}
    # Tokens: efficiency has one row per generated sample (per problem and
    # branch). Sum prompt and completion totals across all rows for each branch.
    for r in efficiencySummary:
        b = r.get("branch") or "ontology"
        a = agg.setdefault(b, {"prompt": 0, "completion": 0, "samples": 0,
                               "correct": 0, "codebleu_sum": 0.0, "codebleu_n": 0})
        a["prompt"]     += int(_num(r.get("prompt_tokens_total")) or 0)
        a["completion"] += int(_num(r.get("completion_tokens_total")) or 0)
        a["samples"]    += 1
    # Correctness: passk has one consolidated row per (problem, branch) with
    # n_correct already counting the samples that passed Pass@k.
    for r in passk:
        b = r.get("branch") or "ontology"
        a = agg.setdefault(b, {"prompt": 0, "completion": 0, "samples": 0,
                               "correct": 0, "codebleu_sum": 0.0, "codebleu_n": 0})
        a["correct"] += int(_num(r.get("n_correct")) or 0)
    # CodeBLEU: per-problem mean already, one row per (problem, branch). We
    # average those means again to get a corpus-level value per branch.
    for r in (codebleu or []):
        b = r.get("branch") or "ontology"
        v = _num(r.get("codebleu"))
        if v is None:
            continue
        a = agg.setdefault(b, {"prompt": 0, "completion": 0, "samples": 0,
                               "correct": 0, "codebleu_sum": 0.0, "codebleu_n": 0})
        a["codebleu_sum"] += v
        a["codebleu_n"]   += 1

    branches = [b for b in BRANCH_ORDER if b in agg]
    if not branches:
        return None

    header = ["Metric"] + [BRANCH_LABEL.get(b, b) for b in branches]
    rows = []

    def add_row(label, fmt_fn):
        cells = [label]
        for b in branches:
            cells.append(fmt_fn(agg[b]))
        rows.append(cells)

    def section(label):
        # Visual separator: text in the first column, blanks elsewhere.
        rows.append([label] + [""] * len(branches))

    # ---- shared header block (token totals + sample counts) ----
    add_row("samples",
            lambda a: "%d (%d correct)" % (a["samples"], a["correct"]))
    add_row("prompt tokens (total)",   lambda a: "%d" % a["prompt"])
    add_row("completion tokens (total)", lambda a: "%d" % a["completion"])
    add_row("tokens per sample",
            lambda a: "%.0f" % ((a["prompt"] + a["completion"]) / a["samples"])
                       if a["samples"] else "-")

    # ---- block 1: efficiency toward correctness ----
    section("--- EFFICIENCY TOWARD CORRECTNESS (Pass@k) ---")
    add_row("tokens per correct sample",
            lambda a: "%.0f" % ((a["prompt"] + a["completion"]) / a["correct"])
                       if a["correct"] else "n/a")
    add_row("estimated cost (USD)",
            lambda a: "$%.4f" % (a["prompt"] / 1000.0 * PRICE_INPUT_PER_1K +
                                 a["completion"] / 1000.0 * PRICE_OUTPUT_PER_1K))
    add_row("cost per correct sample (USD)",
            lambda a: ("$%.4f" % ((a["prompt"] / 1000.0 * PRICE_INPUT_PER_1K +
                                   a["completion"] / 1000.0 * PRICE_OUTPUT_PER_1K)
                                  / a["correct"])) if a["correct"] else "n/a")

    # ---- block 2: efficiency toward code similarity (CodeBLEU) ----
    section("--- EFFICIENCY TOWARD CODE SIMILARITY (CodeBLEU) ---")
    add_row("CodeBLEU (mean over problems)",
            lambda a: ("%.3f" % (a["codebleu_sum"] / a["codebleu_n"]))
                       if a["codebleu_n"] else "n/a")
    add_row("CodeBLEU per 1000 tokens",
            lambda a: ("%.4f" % ((a["codebleu_sum"] / a["codebleu_n"]) /
                                 ((a["prompt"] + a["completion"]) / 1000.0)))
                       if a["codebleu_n"] and (a["prompt"] + a["completion"]) else "n/a")

    # ---- ratio row (overall token cost) ----
    if "single" in agg and "ontology" in agg:
        tot_o = agg["ontology"]["prompt"] + agg["ontology"]["completion"]
        tot_s = agg["single"]["prompt"]   + agg["single"]["completion"]
        r_tokens = (tot_o / tot_s) if tot_s else None
        section("--- OVERALL ---")
        rows.append([
            "ratio ontology / single (total tokens)",
            "-",
            ("%.2fx" % r_tokens) if r_tokens else "n/a",
        ])

    caption = ("Table. Token efficiency by branch along two dimensions "
               "(USD prices: $%.4f/1K input, $%.4f/1K output)."
               % (PRICE_INPUT_PER_1K, PRICE_OUTPUT_PER_1K))
    return (caption, header, rows)


def main():
    meta = _problem_meta()
    passk = _read_csv("passk_summary.csv")
    codebleu = _read_csv("codebleu_summary.csv")
    lcsSummary = _read_csv("lcs_summary.csv")
    lcsChecks = _read_csv("lcs_checks.csv")
    cas = _read_csv("cas_summary.csv")
    effSummary = _read_csv("efficiency_summary.csv")

    if passk:
        _emit(table_main_results(passk, codebleu, lcsSummary, cas), "table1_main_results")
        _emit(table_by_domain(passk, meta), "table2_by_domain")
        outcome = table_outcome_by_branch(passk)
        if outcome:
            _emit(outcome, "table4_outcome_by_branch")
    if codebleu:
        _emit(table_codebleu_components(codebleu), "table3_codebleu_components")
    if lcsChecks:
        _emit(table_lcs_rules(lcsChecks), "tableA_lcs_rules")
    if effSummary and passk:
        tokTbl = table_token_efficiency(effSummary, passk, codebleu)
        if tokTbl:
            _emit(tokTbl, "table5_token_efficiency")

    print("[INFO] tables written to " + str(TABLES_DIR))


if __name__ == "__main__":
    main()
