# TFM — Ontology-driven physics DSL with self-correcting code generation

This is the code for my master's thesis. The idea: you give the system a
physics word problem in plain English, an LLM turns it into an intermediate
representation (a JSON DSL), a logic reasoner (Pellet over SWRL rules)
checks that the physics is consistent, and from there it emits a Java
program that solves the problem. If the reasoner finds inconsistencies,
the errors are fed back to the LLM and it regenerates, up to
`MAX_ITERATIONS` times.

The corpus is 27 problems from Spanish university-entrance exams
(PAU/EvAU/EAU/EBAU) translated into English, each with a reference
solution verified by hand.

## Pipeline

```
problem in plain text
        │
        ▼
  extract_problem      ─►  algebraic steps (LLM, structured output)
        │
        ▼
  generate_dsl         ─►  DSL in JSON (LLM, JSON schema)
        │
        ▼
  validate_dsl
   ├─ referential integrity (syntactic)
   ├─ units vs quantities (declarations)
   ├─ dimensional propagation (powers, products…)
   └─ Pellet over physics-rules.owl (SWRL)
        │
        ├─ OK         ─►  emit_java  ─►  Java program
        └─ errors     ─►  back to generate_dsl with feedback
```

## Layout

```
src/
  graph.py             # LangGraph orchestrator
  problem_extractor.py # first LLM call (extraction)
  code_generator.py    # second LLM call (DSL)
  dsl_parser.py        # DSL JSON -> program ontology
  validator.py         # Pellet + manual checks (scope, powers, etc.)
  java_emitter.py      # DSL JSON -> Java
  settings.py          # config + .env + prompt loading
  utils.py             # ontology cache
  metrics/             # Pass@k, LCS, CAS, CodeBLEU, efficiency, plots, tables

prompts/   # extraction.txt, system.txt, user_template.txt
resources/ # OWLs: domain, math, rules, bridge
corpus/    # 27 problems: description, metadata, expected_goals,
           # reference_solution, reference.java
scripts/   # maintenance (rebuild ontologies, etc.)
tests/     # layered tests (ontology, validation, generated_code, contracts)

run_benchmark.py  # runs the whole corpus with n samples and two branches (A/C)
__main__.py       # runs a single problem or the corpus in simple mode
```

## Setup

Python 3.10+ and a JDK are required (for Pellet and for compiling the
emitted Java in the tests). I develop on Windows with the Microsoft JDK.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env   # then edit .env with your API key
```

Most-used `.env` variables:

| Variable             | Default                      | Notes |
|----------------------|------------------------------|-------|
| `OPENAI_API_KEY`     | —                            | required |
| `OPENAI_MODEL`       | `gpt-5.4-2026-03-05`         | any chat model your account can use |
| `OPENAI_TEMPERATURE` | `0.1`                        | run_benchmark bumps it to 0.7 for Pass@k |
| `MAX_ITERATIONS`     | `5`                          | self-correction loop cap |
| `LLM_CALL_DELAY`     | `3.0`                        | seconds between calls (to avoid 429) |

## How to run it

### A single problem (simple mode)

```powershell
python __main__.py problem_001
```

Creates `output/problem_001/` with the representation, the DSL, the
program OWL, the validation report and the `.java`. Pass multiple ids
and they run in series. With no arguments it processes the whole corpus
but **wipes `output/`** first (full run).

### Full benchmark (five metrics, two branches)

```powershell
python run_benchmark.py            # all 27 problems
python run_benchmark.py problem_005 problem_018   # subset
```

For each problem and sample it runs **two branches**:

- **`single`**: one LLM pass, no validation, no loop. The baseline.
- **`ontology`**: the full system, starting from the **same** first
  LLM generation as the `single` branch (paired sampling).

By default it draws **5 samples** at temperature 0.7 (override with
`BENCHMARK_SAMPLES` and `BENCHMARK_TEMPERATURE`).

When it finishes it aggregates all metrics. Tables and figures are
generated separately:

```powershell
python -m src.metrics.tables   # CSV + HTML + PNG
python -m src.metrics.plots    # PNG
```

Everything lands in `output/metrics/`. Tables under `tables/` and
figures under `plots/`.

### Metrics

| Metric      | What it measures |
|-------------|------------------|
| Pass@1/@5   | functional correctness (numbers match the reference within 2%) |
| LCS         | logical consistency (physical rules on sign, range and relations) |
| CAS         | contextual alignment (coverage of the requested goals) |
| CodeBLEU    | structural similarity to the human reference solution |
| Efficiency  | time per pipeline layer and iterations of the self-correction loop |

The consolidated CSVs include mean, std, and max/min restricted to the
samples that passed Pass@k (this last one at my advisor's request).

## Tests

```powershell
python -m pytest tests/ -q
```

The suite runs in layers, each with its own contract:

- `tests/ontology/` — SWRL propagation and error rules. If you add a SWRL
  rule, append its row to `BINARY_RULES`/`UNARY_RULES` in
  `test_swrl_propagation.py`. A guard test complains if you forget.
- `tests/generated_code/` — for every fixture DSL, the emitted `.java`
  must compile, run, return valid JSON, and contain every variable in
  `results_to_print`. Skipped if no JDK is on the PATH.
- `tests/validation/` — invalid DSLs must produce the expected error
  type; valid ones must produce zero errors.
- `tests/contracts/` — end-to-end smoke test of the graph with both LLM
  endpoints mocked.

For a fast loop the cheap buckets are `validation/` and `generated_code/`;
the `ontology/` ones invoke Pellet and are the slow ones.

## Things worth knowing

A few notes I've learned the hard way:

- Prompts live under `prompts/*.txt` and are loaded by `settings.py` at
  import time. If you change a prompt, be aware it invalidates the
  comparability of any earlier results; you have to rerun the corpus
  cleanly so everything was generated with the same prompt.
- Pellet is invoked through `owlready2.sync_reasoner_pellet`, which
  shells out to a bundled JAR. State leaks across `World`s unless you
  use a fresh one, which is why the reasoning tests use the
  `isolated_world` fixture.
- `src/utils.py:load_ontology` caches OWLs by absolute path: each one
  is parsed once per process. The real bottleneck is not the parse, it's
  Pellet booting the JVM (~1s per iteration).
- OpenAI tends to rate-limit me (429) if I push too hard.
  `LLM_CALL_DELAY=3` and `max_retries=8` on the client (already wired)
  ride it out reasonably. If your tier is low, raise it with
  `set LLM_CALL_DELAY=5` before launching.
- The Java emitter has been the single biggest source of "silly
  failures" that went unnoticed for weeks (integer literals overflowing
  `int`, `int`-typed values that came as 2.0, etc.). Worth reading the
  unit tests of the number formatter if you touch it.
- `corpus/problem_xxx/reference.java` is the human-written solution that
  CodeBLEU compares against. I wrote each one by hand and verified it
  against `reference_solution.json`. If you add a new problem, don't
  forget the reference or CodeBLEU will be empty for it.

## License and authorship

TFM (UOC). Carles Gallel, 2026.
