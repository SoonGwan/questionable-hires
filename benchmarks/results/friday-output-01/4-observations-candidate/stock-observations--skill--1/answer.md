I’m using the supplied Friday skill to review the release in memory, execute the exact SQL and readers at every phase, and print the full JSON observations without changing project files or Git state.

**Blocked by evidence.** Executed the exact supplied SQL and both literal readers at all five phases in memory.

- **First active failure: step 3.** OLD returns `[(A,7),(B,3),(C,0)]` instead of required totals `[(A,12),(B,4),(C,0)]`. NEW passes.
- **Last compatible checkpoint before failure: step 2.** Its view redefinition introduces the semantic mismatch, masked while reservations are zero.
- **Step 4 remains incompatible:** restarting OLD does not restore total-quantity semantics.
- **Step 5 restores compatibility and preserves committed data:** `(sku,quantity,reserved)` remains `[(A,12,5),(B,4,1),(C,0,0)]`.
- NEW’s step-1 `no such column: reserved` error is **inactive and nonblocking**. Every successful reader preserves ordered columns `[sku,units]`, lexical SKU order, and zero values.

Scoped mitigation: retain total-quantity semantics in `legacy_stock` before step-3 writes; NEW already computes available quantity directly. Rollback must restore that view before OLD resumes. No mitigation was applied.

The complete machine-readable JSON is printed in command output **`3615f3`**: all 10 observations, full rows/errors, reader provenance and hashes, contracts, preservation checks, and completion/truncation fields.

Files and Git state remained unchanged; no scratch, dependencies, external services, or deployment. Evidence is limited to the specified SQL-only SQLite sequence.
