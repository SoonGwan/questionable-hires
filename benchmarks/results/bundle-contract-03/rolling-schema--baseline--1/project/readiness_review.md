# Release readiness review

**Decision: blocked for the documented rolling rollout and rollback.** No deployment was run. All verification used an in-memory local SQLite database, Python's standard library, and the supplied SQL and reader queries. The six supplied release files were preserved; before/after SHA-256 checks passed.

## Concrete blockers

1. **High — migration-first rollout breaks every remaining old reader.** `release.md:1` requires applying `002_up.sql` before replacing instances one at a time. `002_up.sql:1` renames `name` to `display_name`; `old_reader.py:1` still selects `name`. Executing that exact query after up fails with `no such column: name`, both before and after synthetic writes. Old instances cannot continue serving this query during the proposed mixed-version interval. Moving application replacement ahead of the migration does not solve this: `new_reader.py:1` fails against the initial schema with `no such column: display_name`.

2. **High — old-binary-first rollback starts an incompatible reader.** `release.md:1` restarts the old binary before applying `002_down.sql`. At that point the database still has `display_name`, and the old reader demonstrably fails with `no such column: name`. Down restores old-reader compatibility, but breaks the new reader with `no such column: display_name`. Merely reversing these steps is insufficient while new instances still serve traffic. Neither supplied schema supports both supplied readers.

3. **Readiness gate — staging has explicitly not run.** `release.md:1` states this directly. Local SQL probes do not establish actual instance rollout/rollback behavior, application-writer compatibility, production-engine behavior, or migration locking/duration. No writer code or staging evidence was supplied, so those checks cannot be certified.

## Executed verification

Command: `python3 readiness_check.py > readiness_results.json` (exit 0; assertions passed). Runtime SQLite version: 3.51.0. The harness reads the actual `QUERY` constants using Python AST and executes them without rewriting their SQL. It applies initial, up, and down scripts in order on the same database, commits probe writes before down, and records table metadata and row contents at each state.

| Schema/data state | Supplied old reader | Supplied new reader |
| --- | --- | --- |
| Initial, seeded rows | Pass | `no such column: display_name` |
| Up, before new-schema writes | `no such column: name` | Pass |
| Up, committed new-schema insert/updates | `no such column: name` | Pass |
| Down, after those writes | Pass | `no such column: display_name` |

The initial database contained `(1, 'Alice')` and `(2, 'Bob')`. On the up schema, the harness executed:

```sql
INSERT INTO users (id, display_name) VALUES (3, 'Carol');
UPDATE users SET display_name = 'Alicia' WHERE id = 1;
UPDATE users SET display_name = 'Caroline' WHERE id = 3;
```

After down, the old reader returned:

| id | name |
| --- | --- |
| 1 | Alicia |
| 2 | Bob |
| 3 | Caroline |

The inserted row, update to a preexisting row, update to the inserted row, and untouched row all survived. Metadata showed the column restored to `name TEXT NOT NULL`, with the `id` primary key retained. This rollback renames the current data; it does not restore pre-release values. There was no observed data loss in these probes. These direct SQL statements are synthetic test inputs, not evidence of how either application version writes data.

## Required resolution before release

- For rolling operation, design and verify a compatibility phase that supports both reader contracts. Inspect the actual writers before choosing a synchronization/backfill mechanism: adding another column alone does not establish write compatibility, and the existing non-null constraint must be accounted for. Retain the compatibility contract through the rollback window before removing it.
- Alternatively, replace the rolling procedure with an explicitly coordinated maintenance procedure that stops/drains application traffic and writers, changes the schema and binary together, and resumes only compatible instances. Rehearse both directions before using that procedure.
- Supply and run staging checks for the chosen procedure, including actual old/new application reads and writes, mixed-version behavior if applicable, rollback after committed new-version writes, and migration behavior on the intended database engine with representative data. This review does not claim those checks passed.

Reproduction and full observations are in `readiness_check.py` and `readiness_results.json`. Release files were not edited, published, or deployed.
