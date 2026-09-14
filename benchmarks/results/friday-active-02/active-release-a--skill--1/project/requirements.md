Scope is local SQLite SQL compatibility and value recovery only.
The deployment is a documented maintenance-window strategy, not a rolling release:
old processes are drained before up.sql; only the listed active readers run at each
checkpoint. release.json is the exact proposed order, including rollback. Do not
silently reorder it. Each phase executes files in order, then its SQL, then the
listed readers. All phases share the same database. Empty file/SQL lists mean no
change, not a fresh database. Reader names map to literal QUERY constants in the
named Python files; these files are declarations, not application writer code.
Each reader returns id and its version's label column, ordered by id. Before new
writes, values must be [(1, 'Ada'), (2, 'keep')]; afterward they must remain
[(1, '새 이름'), (2, 'keep'), (3, 'inserted')] through rollback. All three record
identities must survive. No queued/external effects are in this local SQL contract.
Actual application writers, locking, maintenance orchestration and staging are not
supplied and cannot be certified. An acceptable local plan is not deployment approval.
