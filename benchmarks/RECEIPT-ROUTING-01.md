# Receipt: historical detail only when needed

Revision `e00c751` reduces the common entrypoint and moves already-present-fix
comparison mechanics into `references/existing-fix.md`. Description, character
and invocation metadata are unchanged. The common path retains the actual test
boundary, identical assertion/inputs, documented runner, independent exit status,
required checks, scope and evidence limits. History mode still freezes current
assertions rather than comparing each revision's different tests.

Two fresh Astra-medium skill sessions, serial, one per existing development task.
No baseline rerun or retry. Raw evidence: ignored `local-runs/receipt-routing-01`
and `local-runs/receipt-routing-02`.

| Task/sample | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Age boundary, previous combined screen | 101,463 | 35.923 |
| Age boundary, routed Receipt | 99,558 | 34.956 |
| Changed-test history, previous `4d9b380` | 85,406 | 38.228 |
| Changed-test history, routed Receipt | 68,978 | 65.039 |

The two current samples sum to 168,536 tokens / 99.995 seconds, versus 186,869 /
74.151 for those earlier samples: about 9.8% fewer tokens but 34.9% more time.
These separated single samples do not establish causality or stable efficiency.
The general fix's token/time differences are small. The history comparison saves
tokens but is substantially slower. Do not call the structural change a combined
performance win or replace a whole-team screen with these sums.

The general fix does not load the historical reference. It adds age 18 to the
existing test, observes that assertion fail, changes only `>` to `>=`, then runs
the same three assertions successfully. Its only intended original-file changes
are eligibility and regression test. One rejected patch remains in stderr, as in
the preceding combined-screen sample; the rejected target is not established.

The history task reads both entrypoint and reference together. It freezes
`HEAD:test_totals.py` once and uses it against implementations `39d21b3` and
`168c05d`, in project-local disposable copies. Exactly-5000 fails before and
passes after; 4999/5001 remain correct. Both original files remain byte-identical,
and disposable copies are cleaned up. No production change or outside service.

The captured history output lacks the initial frozen-test hash/before-revision
heading even though it contains both assertion outcomes and exit statuses. The
author independently replayed the reviewed original command after both sessions:
the complete output records frozen test SHA256
`80425a4e3fced1af98f603d2a766c7ccb0c94ec0e56a4c2e798e762375b09c80`, both actual
revisions, before exit 1 for the boundary assertion and after exit 0. This replay
is separate evidence, not retroactively attributed to the initial capture.

All three installed Receipt resources match their committed blobs in both cells.
The full local suite passes 98 tests, including package-resource preservation;
eight metadata/link sets and Receipt validation pass. These mechanical checks
are not model scores. `FAST-REGRESSION-04` predates this Receipt revision, so the
new combined candidate has not received another full-team screen.

Disposition: retain as a targeted progressive-disclosure candidate with successful
mode selection, not a proven broad speedup. More instruction compression is not
automatically better. Do not repeatedly rerun these unchanged tasks or remove
the frozen-assertion invariant merely to lower costs.
