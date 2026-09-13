I’ll use the mother-in-law skill to check the catalog sequences against `requirements.md`, retain the execution JSON, and leave existing files unchanged.

Found a recovery defect: successful retry updates `result` but leaves the previous error visible.

| Sequence | Expected | Observed |
|---|---|---|
| Normal success | Current result, no error | Passed both checkpoints |
| Current failure → successful retry | Error displayed, then cleared with retry result | Failure displayed correctly; retry showed `new result` but retained `controlled failure` |
| Newer success → older success | Newer result preserved | Passed |
| Newer success → older failure | Newer result preserved, no error | Passed |

Deterministic local async component checks completed; exit code **1** indicates the recovery failure. Actual execution JSON: [catalog-qa-execution.json](project/catalog-qa-execution.json).

Run from the project root; waits default to 5 seconds. Use a fresh output filename on subsequent runs:

```sh
python3 -B .agents/skills/mother-in-law/scripts/sequence_probe.py --root . --source lookup.py --class-name Lookup --error-state error --output catalog-qa-reproduction.json
```

Limits: controlled component responses only; no browser or backend testing. No existing files modified, dependencies installed, external services used, or fixes applied.
