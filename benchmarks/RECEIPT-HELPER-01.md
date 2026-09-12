# Receipt helper: adopted, but not a token-efficiency win

Candidate helper/reference `048fb21`, run from clean repository HEAD `19a78e8`.
One fresh GPT-6 Astra medium skill session, serial, on the existing
`receipt-changed-tests` development task. No baseline rerun, retries, exclusions
or new full-team screen. Raw evidence is retained under ignored
`local-runs/receipt-helper-01/receipt-changed-tests--skill--1`.

| Historical sample | Input including cache + output tokens | Process seconds |
| --- | ---: | ---: |
| Frozen-assertion instructions `4d9b380` | 85,406 | 38.228 |
| Progressive routing `e00c751` | 68,978 | 65.039 |
| Optional helper `048fb21` | 86,814 | 32.841 |

The new sample uses 25.9% more tokens and 49.5% less time than the immediately
preceding routed sample. Against the earlier frozen-assertion sample, tokens
increase 1.6% and time falls 14.1%. These temporally separated single samples
cannot establish causality or repeatable savings. No all-skill improvement claim.

## Observed behavior

The model reads the entrypoint and historical reference, inspects the two-file
commit and current assertions, then invokes the installed helper once. It does
not read the helper source or recreate the snapshot machinery. The captured JSON
contains both resolved revisions, the fixed-test hash, copied-import verification,
and complete before/after test outputs without truncation:

- Before `39d21b3a81796dfedc6743db8c9ef476c95230bb`: test exit 1, specifically
  `assertTrue(accepts_total(5000))` fails. The neighboring-input test passes.
- After `168c05d753cf1dd3606221e2fefd4ed4230d1fce`: test exit 0, both tests pass.
- Both use current test SHA256
  `80425a4e3fced1af98f603d2a766c7ccb0c94ec0e56a4c2e798e762375b09c80`.

The model reports the actual behavior and limits, and checks tracked-file status.
Author inspection independently confirms both original files remain byte-identical
to fixture inputs, all four installed Receipt resources match committed `048fb21`
blobs, and no `.receipt-*` copies remain. This does not certify every possible
transient side effect. Capture diagnostics show no invalid JSON, empty completed
command output, timeout or rejected patch. This is evidence from the original
session, not an author replay substituted for missing output.

The helper internally uses a provenance-checking bootstrap and `runpy` for the
unittest invocation; the final answer's shorthand `python3 -m unittest` describes
the test runner, not the literal top-level shell command.

## Limits and next decision

The helper example uses this exposed task's filenames and revision shape. This
checks adoption and mechanics, not transfer to an unseen repository. It must not
be presented as held-out evidence. The helper removes repeated generated plumbing,
but the extra reference also adds reading/context cost; this run alone does not
isolate that cost from model variation. Retain the optional helper as a functional
candidate, not a demonstrated token optimization. Next changes should simplify
its decision/interface burden without losing frozen tests or provenance, followed
by a different small history comparison before another whole-team screen.

The preceding implementation's 105 local tests validate package/helper mechanics,
not model performance. The broad objective remains unmet.
