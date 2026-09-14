I’m using the friday skill to check the documented rollout and rollback states, execute the supplied reader queries, and inspect data survival after rollback. I’ll keep the review inside this project and preserve release files.

**Blocked by evidence.** The documented rollout and rollback both expose incompatible readers.

Executed the supplied reader queries in SQLite memory; all migration phases completed:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up migration | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down migration | Pass | Missing `display_name` |

- **Rollout blocker:** Applying `002_up.sql` first immediately breaks active old instances by renaming `name`. The last compatible service state is before that migration. Replacing instances gradually cannot bridge this schema change.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` leaves it querying the missing `name` column. Running down while new instances serve would instead break their queries.

For the intended rolling strategy, use an expand/migrate/contract transition with both column contracts supported and synchronized until old consumers and the rollback window are retired. Alternatively, an explicitly coordinated outage could stop all consumers, change the schema, then start only the matching version.

**Data recovery:** Before down, I updated row 1 and inserted row 3 through `display_name`. After down, the old reader returned all three rows:

```text
1  Updated by new schema
2  Unchanged
3  New schema insert
```

The tested down migration preserves current values and inserted rows; it does **not** restore the original value of row 1.

Application writers were not supplied; these were representative SQL writes, not application-writer verification. Runtime/configuration compatibility remains unknown. Staging explicitly has not run, so staging readiness is unverified.

Release files and existing user changes were preserved. No deployment or external services were used.
