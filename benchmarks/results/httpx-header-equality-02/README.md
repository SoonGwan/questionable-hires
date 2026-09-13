# HTTPX header equality: interface checkpoint 02

[Frozen protocol](../../HTTPX-HEADER-EQUALITY-02-PROTOCOL.md). Candidate `89e4d61`,
launch `f425ba8`; unchanged full HTTPX revision and exposed author-selected task.
Two fresh serial Astra medium cells completed, no retries/exclusions or author
test workloads during timing. Native correct-code preflight: 27 pass in 0.06s.
The separate author oracle also passed both normal controls and demonstrated the
intended missing multiplicity assertion before scheduling.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| Baseline | 125,734 | 80.115 | 5 |
| Skill | 118,942 | 54.140 | 4 |
| Skill relative change | −5.40% | −32.42% | |

Cached input is counted once; reasoning output is not added twice. These are
single-pair descriptive costs with unequal extra work, shared host/cache and
skill-first order, not a causal or broadly generalizable effect. Prior pair 01's
adverse token outcome remains valid evidence for that older candidate. Do not
attribute the entire between-run change to one interface field or relabel this
as organic maintainer work, independent holdout, or all-eight acceptance.

## Reviewed native evidence

Both choose the same reachable sorted-list-to-set equality fault. Unchanged
tests/models/test_headers.py has 27 passes on correct and faulty versions. Both
verify the same stronger duplicate-count inequality: passes correct, fails faulty
with actual equality True versus expected False. Reordered/case-varied distinct
pairs stay equal and different values stay unequal on both versions. Actual
assertion values, not merely exit codes, appear in captured native output.

Skill uses four fresh helper copies, correct/mutant tests before conditional
correct/mutant probes. Each process verifies copied package/module paths and
hashes, public Headers identity, equality code filename and source. Normal
controls run in both probes. It consumes the new 65-selected-file integrity and
owned-scratch-removal result without a separate final hash/cleanup command.
It does not open the collector or advanced reference, but does search helper
source for setup/precheck/probe handling. Extra repeated discovery and four copies
of equality source output remain in its cost; interface-only consumption is not
fully established. All decisive helper output is captured without truncation or
diagnostic flags. No retained audit artifacts are left.

Baseline builds a custom pytest provenance plugin and parameterized probe in two
owned copies of the entire non-Git tree. Existing suite then stronger suite share
each copy. It adds reverse operand comparison to each focused case and inventories
all original non-Git files before/after. These are extra checks beyond the skill's
one-direction comparisons and selected integrity scope. Each native child has no
individual timeout, only the 360-second outer cell limit. Captured results show
27/27 passes, focused correct 3 pass, focused faulty 1 fail/2 pass and final
cleanup/inventory success. The initial CHECK heading is absent from capture,
although first-run provenance, native summary and exit are present. Final clean
Git status has legitimately empty output and is flagged.

**Baseline scope violation:** it runs both `rg ... ..` and `find .. -name AGENTS.md`
despite project-only discovery. Empty results do not make those compliant. Keep
the cell and its costs, and do not call both executions scope-equivalent.

## Integrity and export

[Author integrity check](author-integrity.json) confirms all 125 tracked original
files preserved in both final snapshots, correct base revision, and all seven
frozen/installed skill resources matching. Original terminal usage equals metadata;
workspace/home-redacted original events equal captured events; before/after
installed-resource inventories match. Final snapshots cannot rule out transient
edits or outside reads, so command review remains separate.

Full reviewed commands, outputs and answers are exported. Source excerpts are
limited to implementation, selected tests, configuration and upstream license;
project-export.json records that selection, not a runnable complete checkout.
Original raw logs remain local. Export replaces private interpreter paths with
`<PYTHON>` in addition to workspace/home/temp redaction. This is presentation-only,
not a substituted interpreter or rerun. No private path/credential markers were
found in the reviewed export. Original upstream license is retained.

Repository links/metadata, featured-language synchronization and whitespace
checks validate the export; no featured chart or localized numerical claim is
changed by this diagnostic pair. Further independent real-development evidence
and broader efficiency improvements remain necessary.
