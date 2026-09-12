# Receipt package comparison: favorable single development pair

Frozen task `227f65c`, Receipt reference `48ec1c3`, helper `048fb21`.
One fresh GPT-6 Astra medium session per arm, serial, no retry/exclusion/timeout.
Raw evidence: ignored `local-runs/receipt-package-01`. No full-team rerun.

| Arm | Input including cache + output tokens | Process seconds |
| --- | ---: | ---: |
| No skill | 80,126 | 31.064 |
| Receipt | 68,515 | 28.750 |

Receipt uses 14.5% fewer tokens and 7.4% less wall time in this pair. This is a
single author-created development comparison, not a stable or broad speedup.
The task is derived from the previously tested package-helper scenario, not a
held-out set. Its data changes alongside the implementation: old historical data
passes without exercising the reported defect. Local fixture checks establish
old/old pass, current/current pass, and old implementation/current data fail.

## Evidence and unequal verification scope

Both models correctly identify first-separator splitting and verify the current
implementation with the documented unittest runner. Neither changes original
files, installs dependencies or contacts external services in the captured trace.

Baseline runs the current regression and three additional in-memory inputs
(repeated separators and empty values). It reads the commit diff but does not
execute the old implementation. Thus it verifies current behavior but does not
satisfy the predeclared failing-before criterion. The user prompt says to verify
the committed fix, not explicitly to perform a historical execution; Receipt
itself supplies that stronger method. This is not evidence that baseline's final
behavioral conclusion is wrong, nor an equal-work microbenchmark.

Receipt reads its entrypoint and compact reference, adapts the helper recipe to
the package, and invokes it once without reading its source. Five fixed files
include package initializers, settings, the current test and current JSON data;
only `records/decode.py` varies. Copied imports include both decoder and settings.

- Before `f51e41df656cc705867e7113e47ffd23255fc2cb`: test exit 1, caused by
  `ValueError: too many values to unpack` on the multi-separator endpoint. This
  is the actual decoder defect, not an import/setup failure or `AssertionError`.
- After `b4df6d7e78a5cebe05bc9217fa6a2e0297d2f3eb`: test exit 0. The same data
  checks simple, empty and multi-separator values successfully.
- Frozen data SHA256:
  `adff01dc975cf4e449241dd646c4fdc85493a993e349437206b9cf8b09b0e4e5`.

The original captured JSON includes resolved revisions, all fixed-file hashes,
both complete test outputs and import provenance. Receipt's final answer correctly
limits evidence to the three examples. Its shorthand documented-command wording
does not describe the literal helper bootstrap (`runpy` plus provenance checks).

Author inspection confirms all seven original files remain byte-identical in
both workspaces, all four installed Receipt resources match `48ec1c3`, and no
comparison copies remain. No rejected patch or missing-output diagnostic. One
Receipt discovery command exits 1 because `rg` finds no AGENTS.md; its preceding
diff is present, and it is not treated as failed reproduction. Preservation checks
do not certify all transient side effects. No author replay replaced model output.

## Disposition

The compact reference and helper transfer successfully to this package/data case,
with lower observed resource use and stronger historical evidence in this pair.
Retain as a promising candidate, not a proven all-skill performance result. The
adverse token result in [RECEIPT-HELPER-01](RECEIPT-HELPER-01.md) remains valid.
This comparison cannot isolate reference compression from task/model variation.
The complete local suite passes 108 tests; those mechanics are not model scores.
