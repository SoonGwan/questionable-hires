I’ll use the friday skill to check the documented rollout and rollback states, execute the supplied reader queries, and inspect data survival after rollback. I’ll preserve the release files and keep all work inside this project.


**Blocked by evidence.** The documented rollout and rollback both expose active readers to incompatible schemas.

Executed the exact supplied reader queries in SQLite 3.51.0 against all relevant states:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up, before writes | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down, after writes | Pass | Missing `display_name` |

- **Rollout blocker:** Applying `002_up.sql` first immediately breaks every old instance by renaming `name`. Rolling replacement prolongs this incompatibility. The last compatible serving state is before the migration.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` breaks its reads. Running down while new instances still serve breaks their reads instead. Reordering alone cannot support mixed versions.

For rolling deployment, use an expand/migrate/contract transition that preserves both reader contracts and synchronizes writes until old consumers are retired. Alternatively, use a coordinated maintenance window: stop consumers, migrate and replace binaries, then resume; rollback must likewise stop consumers before reversing the schema and restoring old binaries.

**Data recovery check:** Before down, I inserted `(3, 'New user')` and updated ID 1 to `'Updated 이름'` through `display_name`. After down, both values and the untouched ID 2 survived under `name`. This rename reversal preserved tested data; it did not restore the original pre-update value.

Application writers were not supplied; these were representative SQL writes, not application-writer verification. Runtime/configuration compatibility remains unknown, and staging explicitly has not run this release.

All checks completed and assertions passed. Release files and existing user changes were preserved. No deployment or external services were used.
