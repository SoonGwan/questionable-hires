I’ll use the Friday skill to review the supplied rollout and rollback, execute the exact SQL and readers locally, and print the full JSON observation record without modifying project files or Git state.

The proposal changes OLD’s view to available stock in step 2, but zero reservations hide that semantic change. I’ll check the full results after step 3’s writes and through both rollback phases, including whether quantities and reservations remain committed.

**Blocked by evidence.** Executed all supplied SQL and both literal readers at all five phases in memory.

- **First active failure: step 3**, starting with the reservation update. OLD returns `[(A,7),(B,3),(C,0)]`, but requires `[(A,12),(B,4),(C,0)]`. NEW passes.
- **Last compatible checkpoint before failure: step 2.** Its view redefinition introduces the semantic defect, masked by zero reservations.
- **Step 4 remains incompatible:** restarting OLD does not restore its view.
- **Step 5 restores compatibility and preserves committed data:** ordered `(sku,quantity,reserved)` rows remain `[(A,12,5),(B,4,1),(C,0,0)]`.
- NEW’s step-1 `no such column: reserved` error is **inactive and nonblocking**. All successful results retain ordered columns `[sku,units]` and zero-valued C.

Scoped mitigation: retain total-quantity semantics in `legacy_stock` throughout coexistence; NEW already calculates available stock directly. Restoring the view before restarting OLD addresses the rollback gap alone. Neither change was applied.

The complete machine-readable JSON is in command output **`7bf84d`**, including full observations, actual error, reader provenance, contract comparisons, and `complete: true`, `truncated: false`.

Files and Git state were preserved; no scratch, dependencies, external services, or deployment. Evidence is limited to the authored SQL-only SQLite scope.
