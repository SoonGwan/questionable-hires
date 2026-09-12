# Inspect the automatic two-fault audit

One fresh baseline and one automatic-selection session; same exposed task and
frozen criteria, not a holdout. Auto uses **24.92% more tokens / 5.97% less time**.
Both demonstrate the requested faults. Auto selects Con Artist but never invokes
its helper; the later same-process guidance was not installed in this experiment.

| Evidence | Baseline | All eight skills available |
| --- | --- | --- |
| Answer | [Read](two-write-faults--baseline--1/answer.md) | [Read](two-write-faults--auto--1/answer.md) |
| Commands and captured output | [Read](two-write-faults--baseline--1/commands.json) | [Read](two-write-faults--auto--1/commands.json) |
| Original event structure, sanitized | [Read](two-write-faults--baseline--1/events.jsonl) | [Read](two-write-faults--auto--1/events.jsonl) |
| Usage and resource identities | [Read](two-write-faults--baseline--1/metadata.json) | [Read](two-write-faults--auto--1/metadata.json) |
| Final source | [Read](two-write-faults--baseline--1/project/service.py) | [Read](two-write-faults--auto--1/project/service.py) |

See the [full review](../../PROBE-ADOPTION-01.md),
[frozen protocol](../../PROBE-ADOPTION-PROTOCOL.md),
[task and criteria](../../probe-adoption-cases.json), and [run manifest](run.json).

Both large harness outputs lack an initial prefix in the original capture.
Those omissions are preserved, not repaired from the answer or author replay.
Visible assertions and outcomes support the statuses specified in the review,
not every detail of the missing prefix. Auto runs separate import-check processes;
baseline tests more initial store states. This is not an equivalent-work causal
efficiency result. Empty diffs and unchanged files are retained.

Exported with `benchmarks/export.py`. Beyond its workspace, home and temporary-path
redaction, the six owner/group entries in the baseline directory listing were
replaced by `<USER>` / `<GROUP>` in both events and commands. No command, status,
usage value or behavioral output was changed. `source-sha256.json` identifies
the original local source artifacts, not hashes of the edited public files.
Both answers, commands, source files, metadata, manifest and stderr were reviewed;
the evidence scanner reported no findings. This is not a guarantee that a generic
scanner can discover all private data. No original private log is required to
inspect the exported evidence; no new model run was performed for this export.
