# Frame parsing: fewer calls, higher measured cost

[Frozen protocol](../../RECEIPT-FRAME-01-PROTOCOL.md), revision `7af8ed3`,
[run manifest](run.json), [all metadata](summary.json). One new authored task,
one baseline and one Receipt session, serial, baseline first. Both completed;
no retries, exclusions, candidate changes or author tests during model timing.
This is development evidence, not a real-repository holdout or all-eight proof.

| Arm | Input + output tokens | Process seconds | Shell calls | Before / after |
| --- | ---: | ---: | ---: | --- |
| Baseline | 67,271 | 28.239 | 6 | 3 pass + 2 intended failures / 5 pass |
| Receipt | 69,969 | 31.010 | 3 | 3 pass + 2 intended failures / 5 pass |

Receipt records **+4.01% tokens / +9.81% time** despite half as many shell calls.
Cached input is already in input tokens; reasoning tokens are not added again.
No confidence interval, causality, dollar estimate or broad efficiency claim
follows from this shared-host n=1 pair. The adverse result is retained.

## Actual work and evidence

- [Baseline commands](fragmented-frame-buffer--baseline--1/commands.json): file
  inventory; source/requirements/tests read; before suite; project instructions
  and status/diff; after suite; final whitespace/diff/status check. AGENTS.md is
  explicitly read after the before suite but before editing. The suite uses the
  required runner and produces the two intended payload-list assertion failures.
- [Receipt commands](fragmented-frame-buffer--skill--1/commands.json): batches
  inventory, entrypoint, source/requirements and status; then reads project
  instructions/tests and runs before suite; after editing batches the unchanged
  suite, whitespace/diff/status checks in one fail-fast command. No optional
  references or helper implementation are read, no extra after probe executes.
- Both original event logs contain the decisive missing `[b'hello']` and
  `[b'world', b'last']` assertions before the production patch and all five
  passing outcomes afterward. There are no setup failures or missing-output
  flags, rejected patches or observed command repairs. Original and redacted
  event objects agree under the runner's documented path substitutions (20
  baseline events, 14 skill events).
- Both final projects change only `packet.py`; all three other supplied files
  match the fixture bytes. Baseline postpones header deletion until completeness;
  Receipt slices the payload after its header and removes the complete frame
  together. Both retain incomplete data and the requested API. Neither changes
  the supplied tests. No external service/install/out-of-project search is
  observed. Skill inventory before/after is identical; baseline inventory empty.
- Final answers accurately describe captured before/after outcomes and focused
  diffs. No author replay of model solutions is used as execution evidence.

The five supplied tests establish the requested regression/control witnesses,
not exhaustive correctness for every possible stream. The model code review
supports the retained suffix logic; it is distinct from tested input coverage.
The author preflight witness belongs to fixture validation, not these solutions.

## Consequence for development

Final-check batching is adopted here and removes a separate after/diff round,
but call count is not total token/time cost. Repeating this exposed task for a
better number is not the next step. Investigate instruction-loading overhead
and task applicability on separate work; do not add more generic batching rules
or count a narrower verification workload as a gain. Keep featured images and
localized landing-page scores attached to their original experiments.

Exported `source-sha256.json` files identify original artifacts, not redacted
export bytes. Full commands, final projects, diffs and metadata remain available
for both attempts, including this unfavorable result.
