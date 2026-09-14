# Con Artist short-guide screen 01 — 2026-09-14

Launch `da333ab`, resources `8e3bdc4`; [frozen protocol](CON-ARTIST-CORE-GUIDE-MODEL-01-PROTOCOL.md).
One scheduled exposed persistence task completed in **73,679 tokens / 35.540s**,
three recorded shell calls, no timeout or retry. Timing finished at 11:21:05 UTC
before author replay or edits. All usage is known, input includes cached input
once plus output. Every original attempt is retained in the [export](results/con-artist-core-guide-model-01/run.json).

## Audit observations supported; guide adoption unverified

The recorded commands show filename discovery, reading SKILL.md, then one audit
CLI call. **There is no recorded project-source, core-guide or advanced-guide
read.** There is also no recorded helper implementation read. Do not infer that
the shorter guide was read or caused the lower cost. The model's final statement
about the original assertion is correct against the preserved source, but its
source-inspection path is not evidenced by the captured commands. Capture
diagnostics report no empty commands; that does not prove completeness of all
reads/events. Whether reads were omitted or absent remains unresolved.

Actual audit output captures all four phases:

| Observation | Correct code | Missing append |
| --- | --- | --- |
| Actual existing unittest | One test passes, exit 0 | Same test passes, exit 0 |
| Same stronger assertion | Existing and new records retained, exit 0 | Only existing record remains, intended AssertionError, exit 1 |

Each child reports copied service/test paths and hashes, with a same-process
precheck that `test_save.__globals__['save'] is service.save`. The stronger probe
uses that actual test-global binding too. No timeout or output truncation is
reported. The helper reports both original files' bytes/modes preserved and owned
scratch removed. No new retained artifact or original modification is present.
This supports the lost-write audit, not every possible call/fixture binding.

## Reconciliation and independent execution layer

[Author replay](results/con-artist-core-guide-model-01/author-replay.json) reconciles
raw terminal usage/events, installed frozen resource bytes/modes, and the complete
unchanged two-file project inventory. It extracts the **actual captured JSON recipe**
with shell parsing, then executes that unchanged recipe using frozen helper files
in a disposable project-local copy under a 40-second process bound. All four
expected phase exits, native counts, binding reports, intended stored-record
assertion and integrity flags match. Originals and retained project stay unchanged.
This additional execution does not establish missing original reads or guide adoption.

Versus checkpoint 08 skill's 102,509 tokens / 38.544s, this record is descriptively
**28.12% fewer tokens / 7.79% less time**. It is **not an accepted guide-efficiency
win**: n=1 exposed authored task, shared host/cache, different recorded reads and
assertion implementation prevent causal attribution. Do not compare this favorable
single cell to claim all-eight superiority, promote it to featured, or retry the
same task to seek a desired percentage.

Next useful check is a frozen transfer task with a different real binding/layout,
requiring actual source discovery and fault-specific verification. Preserve this
record even if a later trace provides fuller reads. No runtime or skill changes
were made during this screen/review; local replay is not hosted CI/release proof.
