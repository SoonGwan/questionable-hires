# Capture persistence check — 2026-09-14

Source inspected: `b2993d2`; installed executable reports `codex-cli 0.153.4`.
The executable is a standalone Mach-O binary, not locally available CLI source.

## Boundaries

[Official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
describes `--json` as the emitted event stream and `--ephemeral` as avoiding
persisted session rollout files. It does not establish why a particular command's
leading output is absent or that emitted events equal all model-visible output.
The existing handoff absent-report gap remains unresolved; no skill instruction
change, model retry, restored original transcript, or performance claim follows.

Local `run.py` collects stdout/stderr with `Popen.communicate` and exports a
path-redacted copy. Its existing real-child multiline preservation control passes.
There is no evidence here that the exporter removed the absent-report prefix.

## Separate implemented fix

Previously, resource inspection and Git diff collection preceded saving the
received CLI streams. A post-execution Git error therefore discarded those streams
from the result directory even after the child had finished. Save both original
streams and redacted counterparts immediately after timing, before post-processing.
Still propagate the error; missing metadata is not a completed scored cell.
This does not recover output never emitted by the CLI, survive an orchestrator
crash during execution, guarantee disk writes, or preserve raw bytes before Python
text-mode decoding/newline normalization.

The new real-child control emits JSON and Korean stderr, preserves the disposable
fixture's Git data under `saved-git`, and puts an invalid `.git` pointer in its
place to prevent ancestor-repository discovery. Native post-run Git add fails.
Before the fix, the original stream file is absent; afterwards all four stream
files retain the expected text while the Git exception still propagates and no
metadata is manufactured. An initial fixture revision omitted the invalid pointer
and accidentally discovered the parent repository; its temporary intent-to-add
entries were explicitly cleared. That initial run is not the regression evidence.

Validation: `python3 -B -m unittest discover -s tests -p test_benchmark_runner.py -v`
passes **25 tests / 2.549s**. Featured synchronization and `git diff --check` pass.
These are local collector controls, not new model measurements. Historical
results, graphs, scores, installed skills and user configuration are unchanged.
