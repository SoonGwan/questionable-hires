# Current bundle review — in progress, not final results

Frozen evaluation aeb582b; see BUNDLE-CURRENT-01-PROTOCOL.md. Original logs live
privately under `local-runs/bundle-current-01/`. The runner is still executing the
same serial schedule. This document records reviewed cells, not an overall score.
No model restart, changed skill, altered criterion or author replay.

## First three reviewed cells

- Persistence baseline: original source/test preserved. Isolated missing-append
  mutation leaves the original test green; actual stored-record probe fails on
  mutant and passes after restoring the copied implementation. Temporary copy is
  removed. The captured harness command includes an initial original-test run and
  assertion, but its initial printed result is missing from otherwise nonempty
  output. Later mutant/probe outputs and final successful harness assertion/status
  are captured. Do not reconstruct the absent original-test output or equate empty
  diagnostic flags with complete capture. Four shell commands; no process deadlines
  inside the isolated child runner.
- Protected search baseline: two deterministic completion orders pass against the
  actual generation guard; no defect manufactured. Only test_search.py is added,
  original search.py unchanged. Owned tasks are cancelled/gathered, but the test's
  queue waits themselves have no explicit timeout. Four shell commands; captured
  unittest output records two passes. No extra deadline criterion is added.
- Boundary fix skill: actual age-18 assertion fails before the one-line >= fix,
  then the unchanged assertion passes in the three-test suite. Final suite,
  whitespace check and focused diff are collected with fail-fast && and exit 0;
  there is no separate redundant targeted after-run. Five shell commands. Changes
  are limited to eligibility.py and the new age-18 regression in its existing test.
  This observes Receipt's collection behavior, not a causal or bundle efficiency win.

Original captured commands for these cells stay scoped. The two diagnosis/audit
cells' input bytes match the frozen fixtures. Receipt's installed resource hashes
match frozen Git and before/after manifests agree; baseline has no installed skill.
No patch rejections, malformed JSON, empty-output flags or event errors in metadata
for these three cells, subject to the concrete missing-output limitation above.
Remaining cells and paired cost comparisons still require review.
