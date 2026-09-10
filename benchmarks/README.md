# Same ticket. Three coworkers.

Latest skill revision check: [Exorcist transfer comparison — 27 sessions, all conditions 9/9](REPORT-EXORCIST-TRANSFER.md). No comparative quality gain was observed.

This suite runs actual Codex sessions in fresh synthetic Git repositories. The model can inspect files, run commands, and implement changes when the task asks for them. It is not a single-shot code-generation comparison.

## Arms

- **baseline:** the task, with no project skill installed.
- **control:** the same task plus “Keep the change focused, investigate relevant evidence, and verify your conclusions with appropriate checks.”
- **skill:** the same task with exactly its corresponding Questionable Hires skill installed and explicitly invoked.

All arms use the same model, reasoning effort, tool sandbox, starting files, and history. Every cell gets a new process, repository, and conversation. The runner ignores user configuration and disables personal skill files it discovers. Runtime system instructions still apply. Inspect traces for unexpected skills or tools before accepting a run; this setup does not claim to erase the host's built-in knowledge.

## Reproduce

Requires an authenticated Codex CLI with access to GPT-6 Astra, Python 3.8+, and Git. Model runs consume your account's usage. Start with a single task:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/pilot --case boundary-fix --jobs 3
```

Run the full matrix with repeated independent samples:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/full --repeats 3 --jobs 3
```

The default is one repetition, three arms, medium reasoning, and a 240-second per-cell timeout. Use `--case`, `--arms`, `--timeout`, and `--effort` to narrow a run. Output directories must be new; an existing experiment is never overwritten.

For a separately preregistered task set, pass `--cases-file path/to/cases.json` (the same schema as `cases.json`). For version comparisons, `--skills-root path/to/frozen/skills` evaluates a separate skill snapshot without replacing working or installed skills. The manifest records the task-file digest and skill entrypoint digests; each skill cell also records the entrypoint actually copied. Snapshot digests cover `SKILL.md`, not supporting resources. Use distinct output directories, keep model/effort/tasks fixed, and interleave version runs in a predeclared order to reduce time-of-run confounding. These options do not themselves implement a paired-version experiment or prove behavioral improvement.

For automatic selection with all eight skills installed, use `--arms auto`. This supplies the task without explicitly naming a skill; inspect command traces to see which files the model actually loads. Use `--suite clean --arms skill` for the additional clean and limiting cases. Actual recorded results are in [the report](REPORT.md).

## Evidence

Each cell retains the final answer, tool-event log, diff, actual usage reported by Codex, elapsed wall time, fixture commit, skill digest, and completion status. Workspaces remain in temporary directories for inspection. A process completing is not a correctness score. Missing usage and timeouts remain visible.

Review against each case's criteria in `cases.json`, which is never copied into the model's workspace. Run behavior checks against resulting code where applicable. Verify that mutations were isolated, review-only tasks left production files unchanged, and claims match executed commands.

Raw logs stay in ignored `local-runs/`. Before promoting evidence into `results/` or `examples/`, inspect it for private paths, credentials, and unrelated data. The runner replaces its workspace and home prefix in text logs, but that is not a complete secrets scanner.

## What this suite cannot establish

These small synthetic tasks establish smoke-test behavior, not broad real-repository effectiveness. One repetition cannot establish reliability or statistical superiority. Include clean cases, missing-evidence cases, larger tasks, and repeated samples before drawing general conclusions. Cost is not inferred from token counts without a documented applicable pricing model.

Inspired by [Ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md), especially its controls for conversational verbosity and global-skill contamination. Our cases and instructions are original.

## Repeated comparison (September 11)

The new 72-cell experiment is defined in the [preregistered plan](PLAN-2026-09-11.md). It is separate from the September 10 smoke runs. The runner now shuffles a recorded schedule with a fixed seed, caps concurrency at three, retains original local stdout/stderr and final snapshots, and stops scheduling after an explicit account limit. No cell retries are performed.

Rebuild the published metrics and light/dark graphs from sanitized raw evidence:

```sh
python3 benchmarks/aggregate.py benchmarks/results/astra-repeat-2026-09-11 \
  --reviews benchmarks/results/astra-repeat-2026-09-11/reviews.json \
  --output benchmarks/results/astra-repeat-2026-09-11/analysis
python3 benchmarks/audit.py benchmarks/results/astra-repeat-2026-09-11
```

`aggregate.json` includes per-cell input/cached/output/total tokens, wall time, implementation-only line churn, per-task raw mean/sample SD/min/max, complete-block coverage, zero-baseline exclusions, and separate quality counts. Every task gets equal weight after its arm means are normalized to its baseline mean. Timeout measurements remain in all-attempt summaries, but incomplete three-arm blocks cannot contribute to the completed-resource chart. Missing usage is null, not zero. Review verdicts are author judgments backed by cited commands and independent source checks; they are not inferred from token counts or prose length.

The SVGs use only the Montage semantic palette documented in `assets/README.md`. Use the explicit dark file for renderers without theme support. The chart's range bars show variation across task ratios, not a confidence interval. Changed LOC means added plus deleted physical text lines, not net file size; it is limited to the two implementation tasks and is not a quality score. No subscription usage is presented as dollar billing.

To regenerate the trace audit, add `--traces` to `benchmarks/audit.py`. Optional raster verification requires Playwright and its Chromium installation:

```sh
python3 benchmarks/render_charts.py \
  benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-light.svg \
  benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-dark.svg \
  --output benchmarks/results/astra-repeat-2026-09-11/analysis
```
