# Historical assertion-contract scan: known cases, not a new performance claim

At repository revision `d22d328`, the retained Python files under
`benchmarks/results` were checked using [scan_test_contracts.py](scan_test_contracts.py).
[Raw scan](test-contract-scan-01.json): **533 files parsed, zero parse errors,
six async/synchronous unittest-method collision candidates, 98 unresolved classes**.
Files are read as source; none of the archived modules is imported or executed.

The six candidates belong to two already-qualified experiments:

- Four copies of `CatalogCase.fail` in
  [native integration](results/mother-native-project-01/README.md). Its original
  report already discloses the author-supplied support collision. Added subclasses
  repair dispatch in both unguarded arms and guarded baseline; the scanner reports
  the base definition regardless of those repairs. Guarded skill's reported scalar
  mismatch used an actual assertion path. Do not count four definitions as four
  newly discovered model failures or silently rescore the experiment.
- Two generated `fail` helpers in
  [account-panel QA](results/mother-panel-01/README.md). The preserved post-run
  replay already records their broken diagnostic paths and the name-only repair.

No previously undisclosed collision is established by this scan. This finding
does **not** certify all earlier evidence: the 98 unresolved classes include
production classes as well as test classes with imported project bases. They are
not 98 defects. The checker understands ordinary unittest aliases and top-level
local inheritance only; it does not resolve nested/dynamic classes, imported
project bases, rebinding, decorators, monkeypatches, or synchronous signature
collisions. Embedded source in JSON command logs is not part of this `.py` scan.
Warnings and candidate counts are not a mutation score or a test outcome.

## Future review use

```sh
python3 -B benchmarks/scan_test_contracts.py PATH_TO_PROJECT
```

The optional `--output NEW.json` preserves the candidate report and refuses
existing files. A nonexistent root is an error, not a zero-finding success.
Inspect candidates and actual failure-path evidence before interpreting them;
keep model observations, author replays, repairs and their costs distinct.
This is a review aid, not a new skill loaded into evaluated model sessions.

Four focused tests pass (0.003s): aliases/local inheritance, valid non-test
transport helper exclusion, unresolved imported base reporting, parse gaps,
non-execution, symlink-file exclusion and missing-root rejection. No skill
instructions, frozen fixture, original output, score or featured chart changed.
Full repository suite: **377 tests pass (52.668s)**; catalog/local links,
featured synchronization and whitespace checks pass.
