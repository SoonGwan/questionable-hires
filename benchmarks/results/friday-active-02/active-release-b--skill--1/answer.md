I’ll use the friday skill to check the documented rollout and rollback in disposable in-memory SQLite databases, preserving all supplied files and reporting the observed reader contracts and failures.

**Blocked by evidence:** the local SQL plan fails at phase 4, `rollback starts`. It activates the old reader before `down.sql` restores its required `name` column.

Executed `python3 -B - <<'PY' … PY` using Python’s native `sqlite3`, SQLite **3.51.0**, and one disposable `:memory:` database. The script executed files, writes and literal reader queries in `release.json` order, checking exact column names and rows.

Observed row sets:

- **Original:** `[(1, 'Ada'), (2, 'keep')]`
- **After writes:** `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]`

| Phase | Active reader | Observed columns and results |
|---|---|---|
| 1. initial | Old | `['id', 'name']`; original rows — pass |
| 2. up after old drained | New | `['id', 'label']`; original rows — pass |
| 3. new writes | New | `['id', 'label']`; after-write rows — pass |
| 4. rollback starts | Old | **`OperationalError: no such column: name`** |
| 5. rollback finishes | Old | `['id', 'name']`; after-write rows — pass |

All supplied SQL statements succeeded, including the Unicode update and insert. Execution continued after the reader failure solely to assess recovery in the supplied order. After `down.sql`, the updated record, untouched record and inserted record all survived with their exact values and identities.

Diagnostic probes also observed incompatible **inactive** readers: the new reader failed before migration and after rollback; the old reader failed during phases 2–3. Those are not blockers under the documented maintenance window. Phase 4 is different because the incompatible old reader is explicitly active.

Phase 3 is the last compatible checkpoint before the failure. No irreversible data loss was observed; phase 4’s data remained recoverable. The smallest ordering correction would keep readers drained during rollback and complete `down.sql` before activating the old reader. That revised order was neither applied nor tested.

Production application writers, locking, maintenance orchestration and staging remain unknown, as specified in `requirements.md`. This review is not deployment approval.

All 13 non-Git project files were verified unchanged by SHA-256 comparison. No scratch files, dependencies, service calls or deployments were used.
