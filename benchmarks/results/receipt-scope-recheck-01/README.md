# Receipt scope recheck: scoped once, efficiency remains unproven

[Protocol](../../RECEIPT-SCOPE-RECHECK-01-PROTOCOL.md), [manifest](run.json),
candidate/runner `b7ae490`, unchanged invoice fixture `340d7f3`. One fresh
skill-only Astra medium session on an exposed authored case, 240-second limit.
Completed in 53.747 seconds, no retry, exclusion or timeout. No author test suite
or other benchmark was launched concurrently. Input/output/cached input:
129,585/1,023/112,384; input plus output **130,608 tokens**, cache included once.
No fresh baseline: these are raw costs, not an efficiency comparison.

## Behavior review

[All captured commands](receipt-invoice-history--skill--1/commands.json).
The seven shell calls stay inside the project. No parent-directory search or
ancestor-file sweep appears, unlike the [previous invoice transfer](../receipt-invoice-01/README.md).
The model reads the revised skill/reference and reuses the installed helper
without inspecting its source. This is one observed scope pass, not proof of
consistent compliance or causality from the wording change.

The helper runs the unchanged current four-test suite against before
`cd977e157a823954db7e382d5d60fe258e5498fe` and after
`ad875f211bc29230a9558a23c38c26713f396035`. Both ties fail before with actual
`1.00`/`-1.00` versus expected `1.01`/`-1.01`; all four tests pass after.
Sum-before-rounding and empty controls pass on both revisions. Nine current
fixed inputs, including nested test support/data and company configuration,
are hashed; four imports are verified in the test processes. Each suite runs
once, output is not truncated, and copies are cleaned.

Remaining inefficiency is visible: the model lists nonexistent root `fixtures`
(exit 2), then finds `checks/fixtures` from the support code and reads the helper's
`--help` despite already having its invocation recipe. It also repeats a
project-local instruction-file search and uses semicolon chains. The captured
helper result supplies decisive statuses, but discovery/status-handling guidance
is not consistently adopted. Do not equate fewer scope violations with lower
token use or delete these failed/unnecessary calls from cost accounting.

Author inspection confirms all 11 original fixture files retain their bytes;
the final diff is empty and installed-resource inventories are unchanged.
Capture diagnostics have no flags; decisive outputs and all command paths were
manually reviewed. Export scanning finds no private-path or credential shapes.
Raw artifacts remain under `benchmarks/local-runs/receipt-scope-recheck-01/run/`;
exported source hashes refer to original artifacts. Preflight: 41 Receipt tests
pass before the model run, with metadata/catalog/localization checks passing.

Keep the explicit scope boundary. Whole-task efficiency and reliable transfer
remain unmet, and adding a separate rule for each bad path is not justified.
Further work should reduce repeated preparation while preserving required
evidence; this one recheck is not promoted to a featured chart or broad claim.
