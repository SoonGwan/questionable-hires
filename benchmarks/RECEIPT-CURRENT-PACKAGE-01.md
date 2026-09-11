# Current Receipt package: correct historical comparison, higher session cost

Protocol snapshot `4bf18cf`; unchanged exposed package task, one fresh baseline
and skill session, Astra medium, serial, seed 20260911, 240-second timeout.
No retries or exclusions. Entrypoint `abb4b93`, helper `302066c`, reference
`48ec1c3`. Raw local artifacts: `local-runs/receipt-current-package-01/`.

| Arm | Input + output tokens | Process seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 63,704 | 22.510 | 3 |
| Skill | 107,643 | 42.765 | 6 |

Skill costs **68.97% more tokens and 89.98% more time** in this single pair.
Cached input is included once. Baseline input/output: 63,341/363; skill:
106,773/870. Cached input respectively 57,984 and 90,752. This is not a causal
estimate or a whole-bundle result.

Baseline inspects the actual committed splitter change and runs the documented
current suite (one test covering three records). It does not execute historical
code. Its current-fix conclusion is correct; it misses the stronger frozen-before
criterion, not an explicit demand in the ordinary user prompt.

Skill reads the reference and invokes the optional helper without reading its
source. It holds six current files fixed and varies only `records/decode.py`.
Captured helper output identifies before `f51e41df656cc705867e7113e47ffd23255fc2cb`
and after `b4df6d7e78a5cebe05bc9217fa6a2e0297d2f3eb`. The endpoint record raises
`ValueError: too many values to unpack (expected 2)` before (exit 1); the same
suite passes after (exit 0). Both outputs verify copied imports for
`records.decode` and `records.settings`; neither times out or truncates output.
The final answer accurately describes those observations and limited coverage.

Both retained projects preserve all seven supplied files byte-for-byte; both
change diffs are empty. All four installed skill resources are unchanged across
execution and match the frozen Git snapshot by SHA-256. Capture diagnostics are
clear. Skill's final scratch-file search exits 1 with no matches, not a test
failure. No author replay is credited as model execution.

The historical comparison is useful additional work, but does not establish the
requested efficiency. Skill also separates discovery, settings/revision lookup,
helper execution and final inspection across calls. This observation does not
isolate how much overhead any individual instruction caused. With only one
varying file, the helper's multi-file local savings cannot offset or explain
model-session costs. Preserve the earlier favorable `RECEIPT-PACKAGE-01.md` as
well as this adverse result; do not select the favorable pair or rerun for a
better score. Further candidate changes need a concrete workflow improvement,
not another assertion that the model should be faster.
