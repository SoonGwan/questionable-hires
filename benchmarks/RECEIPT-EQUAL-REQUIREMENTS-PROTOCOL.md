# Receipt with equally explicit historical-verification requirements

This screen diagnoses current workflow costs, not a claimed effect of the recent
oversized-input rejection fix. The normal fixture never reaches that limit.
It uses one exposed package task from `receipt-package-cases.json`, with source,
history and criteria unchanged. `receipt_equal_work_cases.py` changes only the
task ID and visible request to explicitly require historical execution with
frozen current tests/data. It names no helper or preferred implementation method.

The [previous current-package pair](RECEIPT-CURRENT-PACKAGE-01.md) had unequal
verification: baseline did not execute historical code. Do not directly subtract
that pair's costs from this new pair or call the difference an optimization.
Equal requested outcomes still do not ensure identical actual work.

Freeze both task sources and this protocol at one commit before running. Export
the full Receipt tree at `d59c38b`, recording file modes and SHA-256 hashes.
Record the generated JSON digest, model and CLI versions before execution.
Run exactly two fresh serial Astra medium sessions: baseline, then skill;
one repeat, 240-second deadline, seed 20260911. Use `run.py --cases-file
<generated.json> --case receipt-explicit-history --jobs 1 --repeats 1
--model gpt-6-astra --effort medium --timeout 240 --seed 20260911`, fresh output
directories, baseline/skill arms respectively, and frozen `--skills-root` for
the skill condition. No retries or exclusions; stop scheduling on account limit
or incomplete orchestration. Keep the task within the existing under-ten limit.

Both arms must execute the current regression and data against actual before and
after implementations, identify loaded revisions, observe the separator defect
before and a passing after check, retain simple/empty-value controls, and preserve
original files. Setup failures, old passing sample data, prose claims or missing
captured output cannot establish those outcomes. Inspect actual commands,
outputs, imports, diffs, source bytes and installed resource hashes. Any author
replay is separate evidence, not a repair of the model's result.

Author preflight constructs the same Git fixture and verifies the comparison:
fixed current tests/data fail before with too many values to unpack and pass
after, with copied package imports verified. A separate old-source/old-data copy
passes, demonstrating why historical data is not equivalent verification. The
fixture test passes and original source/test/data bytes and Git status remain
unchanged. This is not model execution or performance evidence.

Retain total input-plus-output tokens (cache counted once), process time, missing
evidence, redundant preparation and additional checks. A single exposed task,
fixed order and shared host/cache cannot establish broad or causal superiority.
Use the actual traces to identify a supported next improvement; do not keep
repeating the pair for favorable scores or relax historical-verification criteria.
