# Optional component retention checks — 2026-09-14

Gate 05's protected-search skill test printed the older-completed/newer-pending
display but did not assert it. The existing disposable component probe explicitly
excluded retention and normal overlap; its native counterexample test showed
that clearing the display during loading could pass the default checks.

The new `--retain-while-pending` option makes this particular documented product
contract reusable without a handwritten disposable harness. It does **not** replace
standalone project-test delivery, fix past generated tests, or impose retention on
products permitting clearing/intermediate display. Default probe behavior remains.

Two additional cases seed a result through the actual component method, start
two controlled requests and complete them in normal/reverse order. Checkpoints
cover seed completion, both pending entries, each completion and final ownership.
No direct production-state assignments. Failed checkpoints retain phase, query,
actual and expected values before later calls can mask the problem. A seed
callback exception remains an unexpected error even if subsequent calls succeed.

Native tests first reproduced the absent API (`TypeError`), then passed after
implementation. Three behavioral controls distinguish guarded Search (passes),
loading-clear fault (pending-entry failure) and stale-overwrite fault (completion
failure). CLI subprocess tests separately show default success for loading-clear
versus opt-in exit 1 with actual null/expected `seed result`; guarded code exits 0.
Both preserve original source bytes. All **17 probe tests passed in 0.586s**.

This is local capability evidence, not new model behavior or savings. No model
benchmark was launched for this change; the preceding Necromancer timeout remains
preserved. Limits: direct payload state, zero-argument constructor, distinct
overlapping query keys, cooperative async waits and success-path retention only.
No production network, browser, writer, error-retention or general concurrency
claim. Existing installed-probe tests still cover the default interface separately.
