# Friday: reusable transition mechanics, not an efficiency win

Added an optional SQLite in-memory matrix helper at `580ac16`, then clarified
interface-only routing and the Python API at `4ac4ffe`. Character and release
review scope are unchanged. The helper reuses actual migration files and reader
queries across explicit phases, rejects external database access and mutating
checks, stops after migration failure, and marks truncated rows/incomplete runs.
It does not simulate production or certify deployment readiness.

One unchanged exposed development task (`rolling-schema`), Astra medium, serial
fresh sessions, one sample per candidate and one baseline. Raw local evidence:
ignored `local-runs/friday-matrix-01` and `local-runs/friday-matrix-02`.

| Sample | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Baseline | 63,825 | 36.096 |
| Helper candidate `580ac16` | 73,540 | 40.370 |
| Interface routing `4ac4ffe` | 67,823 | 45.183 |

The first candidate costs 15.2% more tokens and 11.8% more time than baseline.
The routing follow-up uses 7.8% fewer tokens than that candidate but takes 11.9%
longer. Against baseline it still uses 6.3% more tokens and 25.2% more time.
These single exposed samples establish neither causality nor a performance win.

All three identify migration-first old-reader failure, old-binary-first rollback
failure, and a compatible expand/contract alternative without approving staging.
Both skills additionally exercise post-up inserted/updated values through down,
identify the first incompatible state, and distinguish coordinated downtime from
rolling compatibility. Baseline checks readers at three schema states without
post-up writes: verification depth is not identical.

The first skill reads the entire helper source and invokes its Python function;
the captured matrix shows all reader errors and surviving changed/new rows.
The follow-up does not read the helper/reference or invoke it: it writes a native
SQLite loop and asserts surviving values instead. Its lower tokens therefore
cannot be credited to helper execution. Both remain in the project boundary.
The fixture does not specify a production engine; SQLite is local illustrative
evidence only, not verified production equivalence.

Author inspection confirms all six original files unchanged, empty source diffs,
and all four installed Friday resources byte-identical to their respective Git
snapshots. Command outputs capture the actual checks; no deployment occurred.

Local helper tests cover incompatible rename/rollback with new data, compatible
additive migration, original SQL preservation, read-only authorization including
statement-cache bypass prevention, ATTACH/VACUUM/extension rejection, partial
migration stop, recursive-query deadline, explicit row truncation, unsafe paths,
CLI blob output, and UTF-8 byte budgets. A post-run mechanical correction forces
SQLite temporary storage into memory and counts SQL/recipe limits in UTF-8 bytes;
that correction is locally tested, not another model sample.

Keep this optional mechanism experimental. Do not force it on tiny tasks, call
the latest files a combined all-skill improvement, or rerun this unchanged task
until a favorable score appears. A meaningful next workload must actually contain
repeated SQLite transitions and compatible/non-rolling controls. Freeze its
requirements before execution and retain the fixed nine-task regression screen.
