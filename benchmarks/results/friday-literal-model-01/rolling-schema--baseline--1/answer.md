I’ll inspect the release files, run the supplied readers against the initial, upgraded, and rolled-back schemas, and check what happens to representative new-schema data during rollback. I’ll keep release files unchanged and won’t deploy anything.

**Blocked for the documented rollout and rollback.** Executed both supplied reader queries using SQLite 3.51.0 against the actual migration scripts.

| Schema state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Fails: missing `display_name` |
| After up | Fails: missing `name` | Pass |
| Up, after insert/update | Fails: missing `name` | Pass |
| After down | Pass | Fails: missing `display_name` |

Concrete blockers:

- **Rollout:** Migration-first immediately breaks old instances. The renamed column cannot support the documented mixed-version rollout.
- **Rollback:** Restarting the old binary before running down breaks its reads until the schema is reverted. Any new instances still serving after down would also fail.
- **Staging verification is absent:** `release.md` explicitly says staging has not run this release.

Rollback data check passed: before down, I committed an update to existing row 1 and inserted row 3 using `display_name`. After down, the old reader returned:

```text
1 | Updated after up
2 | Unchanged name
3 | Inserted after up
```

All tested IDs and values survived under `name`; integrity check passed. These were synthetic SQL writes, **not evidence of application-writer compatibility**; no application writers were supplied.

Before proceeding, provide a schema transition compatible with overlapping versions, or revise the procedure for a coordinated maintenance window. Validate the chosen rollout and rollback in staging with actual application readers and writers.

No deployment, installation, or external access occurred. All six release files were verified unchanged.
