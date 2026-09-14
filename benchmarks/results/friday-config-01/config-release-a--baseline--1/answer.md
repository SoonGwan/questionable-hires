I’ll read the release plan and applicable project instructions, then exercise the versioned options functions and compare each active pairing’s returned values with the service contract. I’ll preserve all supplied files and keep any scratch local.


The contract requires `timeout_ms=7500`, `attempts=4`, and no mutation of caller-owned config mappings at every active pairing. The manifest restores the bridge config before the old consumer returns during rollback. I’ll now verify all seven active pairings by calling the supplied functions.


No local compatibility failures were found. All seven active pairings satisfy the contract; there is no earliest incompatible step.

Followed `AGENTS.md`, `ops/AGENTS.md`, and `services/worker/AGENTS.md`, including manifest order and config immutability checks.

| Step | Active consumer/config pairing | Returned `(timeout_ms, attempts)` |
|---|---|---|
| 1 — original | old / legacy | `(7500, 4)` |
| 2 — mixed rollout | old / bridge | `(7500, 4)` |
| 2 — mixed rollout | new / bridge | `(7500, 4)` |
| 3 — old retired, config pruned | new / current | `(7500, 4)` |
| 4 — rollback overlap | new / bridge | `(7500, 4)` |
| 4 — rollback overlap | old / bridge | `(7500, 4)` |
| 5 — rollback complete | old / legacy | `(7500, 4)` |

Every call returned the exact expected dictionary with integer values and left its caller-owned config mapping unchanged.

Commands executed:

- `pwd; rg --files --hidden -g '!\.git/**' -g 'AGENTS.md' -g 'current.json' -g '*.py' -g '*.md' -g '*.json'`
- Two `python3 -` heredocs read instructions, inventoried files, and inspected supplied sources/configs.
- A `python3 -B -` heredoc loaded both actual modules using `runpy.run_path`, called `options()` for each manifest pairing, checked exact values and immutability, and compared before/after SHA-256 file inventories. Exit status: `0`; files unchanged: `True`.

Final rollback recovers the original configuration, and **every listed intermediate state also passes**. Minimal mitigation: no changes are needed for this manifest; preserve its bridge-config ordering whenever old consumers are active.

Production reloading, network timing, and process orchestration evidence are unavailable. These results establish compatibility of the listed local states, but cannot prove production transitions follow that order.

No supplied files were changed, no scratch was created, and no services, network access, or dependency installation were used.
