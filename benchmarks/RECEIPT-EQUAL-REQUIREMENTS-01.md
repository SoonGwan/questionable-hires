# Receipt: favorable pair with equally explicit requirements

[Protocol](RECEIPT-EQUAL-REQUIREMENTS-PROTOCOL.md) and fixture/runner `1d52d40`;
Receipt snapshot `d59c38b`. Two fresh serial Astra medium sessions, baseline then
skill, one repeat, 240-second limits. Both completed without retries, exclusions
or timeouts. Raw local evidence: `local-runs/receipt-equal-requirements-01/`.

| Arm | Input + output tokens | Seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 83,681 | 58.228 | 4 |
| Receipt | 70,391 | 32.290 | 4 |

Receipt is −15.88% tokens / −44.55% time in this single pair. Input/output/cache:
baseline 82,186/1,495/70,016; skill 69,694/697/61,696. Cache is included in input
once, and reasoning output is not added again. No dollar estimate. The task never
reaches the input-size limit; this is not an effect estimate for the recent
oversized-input fix or a direct comparison with earlier, differently worded tasks.

Both freeze current tests and the same three sample records. Both execute the
documented unittest runner against before `f51e41df656cc705867e7113e47ffd23255fc2cb`
and after `b4df6d7e78a5cebe05bc9217fa6a2e0297d2f3eb`. Captured before output
contains the endpoint subtest's too-many-values-to-unpack ValueError; after
passes. Simple and empty-value controls are retained. Neither substitutes the
passing historical sample file for the current regression data.

Baseline builds its own disposable-copy harness, exports the historical records
package, verifies bytes against each commit, and executes a separate per-record
probe with copied-import verification. Receipt reads its interface and invokes
the installed helper without reading its implementation; the helper varies only
records/decode.py, holds six current files fixed, and verifies decode/settings
imports in the same process as each unittest invocation. Remaining records
package files are identical across the two commits. The baseline's extra probes
and larger harness are real unequal work, despite equal requested outcomes.
Receipt uses revision expressions directly without a separate resolution call.

Baseline searches `..` for AGENTS files, outside the requested project-only
boundary. This is a scope deviation, not excused by its correct behavioral result.
No deletion or write outside owned comparison directories is shown. Receipt's
captured commands remain project-scoped. Do not label both arms fully scope-clean
or remove baseline costs because of the deviation.

Both retain seven original files byte-for-byte, with empty final diffs; baseline
also asserts tracked-byte/status preservation and cleanup. All four installed
Receipt resources match frozen hashes and before/after inventories. The helper
reports no timeouts or truncated check output; capture diagnostics have no flags.
Actual command bodies, outputs and answers were inspected, not inferred from the
final shell exits. No author replay is credited to either model, and no host
installation or publication occurred.

This provides a favorable current-workflow observation with explicit historical
requirements, while the [earlier adverse package result](RECEIPT-CURRENT-PACKAGE-01.md)
remains visible. It does not prove broad efficiency: one exposed task, one repeat,
fixed order, shared host/cache, unequal work and a baseline scope deviation limit
interpretation. Do not rerun unchanged cells for a better score. Transfer must
include a different package/configuration shape while preserving frozen tests,
loaded-revision evidence and original-file safety.
