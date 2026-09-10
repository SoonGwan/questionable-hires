# Same ticket. Three coworkers.

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

For automatic selection with all eight skills installed, use `--arms auto`. This supplies the task without explicitly naming a skill; inspect command traces to see which files the model actually loads. Use `--suite clean --arms skill` for the additional clean and limiting cases. Actual recorded results are in [the report](REPORT.md).

## Evidence

Each cell retains the final answer, tool-event log, diff, actual usage reported by Codex, elapsed wall time, fixture commit, skill digest, and completion status. Workspaces remain in temporary directories for inspection. A process completing is not a correctness score. Missing usage and timeouts remain visible.

Review against each case's criteria in `cases.json`, which is never copied into the model's workspace. Run behavior checks against resulting code where applicable. Verify that mutations were isolated, review-only tasks left production files unchanged, and claims match executed commands.

Raw logs stay in ignored `local-runs/`. Before promoting evidence into `results/` or `examples/`, inspect it for private paths, credentials, and unrelated data. The runner replaces its workspace and home prefix in text logs, but that is not a complete secrets scanner.

## What this suite cannot establish

These small synthetic tasks establish smoke-test behavior, not broad real-repository effectiveness. One repetition cannot establish reliability or statistical superiority. Include clean cases, missing-evidence cases, larger tasks, and repeated samples before drawing general conclusions. Cost is not inferred from token counts without a documented applicable pricing model.

Inspired by [Ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md), especially its controls for conversational verbosity and global-skill contamination. Our cases and instructions are original.
