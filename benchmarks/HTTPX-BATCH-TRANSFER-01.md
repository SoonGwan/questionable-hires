# Single-fault control after batch addition: adverse token cost

One existing HTTPX exception-propagation task, two fresh Astra medium sessions,
one repeat, serial skill then baseline. Frozen skill snapshot `54328b1`; source
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Preflight: 36 tests pass. Ignored raw
artifacts: `local-runs/httpx-batch-transfer-01`. This is a development control,
not a held-out task or a direct test of multi-fault batch adoption.

| Arm | Tokens including cached input | Process seconds |
| --- | ---: | ---: |
| Baseline | 79,016 | 48.340 |
| Skill | 150,818 | 45.815 |
| Skill difference | +90.9% | -5.2% |

Both change only the default `raise_app_exceptions` from true to false in isolated
copies. Correct tests: 24 pass. Mutant tests: 4 fail / 20 pass, with the intended
`DID NOT RAISE RuntimeError` in before/after-response cases on asyncio and Trio.
Both correctly stop without proposing unnecessary tests or additional faults.
Original commands and outputs were inspected; no separate author replay is
claimed for these two sessions.

Skill uses the single-audit helper, not batch mode. It reads the whole reference
(including the irrelevant batch section), searches helper source and performs
six shell commands. Baseline combines its inspection and inline audit into three
shell commands. It writes isolated copies, logs and a mutation diff, with separate
import checks before each pytest invocation (four child processes, versus the
helper's two). Baseline lacks explicit per-child deadlines; skill's helper bounds
them. These differences matter even though the targeted behavioral outcomes match.

The helper removes child-process plumbing but does not establish cheaper model
execution. More context-bearing interaction rounds and reference reading are
observed overhead candidates, not a measured causal decomposition. Do not infer
that the batch feature itself caused the token increase: the earlier exception
pair used 116,279 skill tokens / 44.661 seconds with different surrounding behavior
and no controlled ablation.

Both complete without timeout or recorded patch rejection. Capture flags are
empty. `audit_httpx.py` verifies all 125 original files and all four installed and
frozen skill resources; runner resource diagnostics show no changed paths. Final
hashes cannot prove absence of transient edits or outside writes. The last skill
search exits 1 because no disposable-copy paths remain, not because pytest failed.

Retain this adverse result. Batch work removal remains an author-level result;
this control only establishes that the model does not force it onto a single-fault
task. The next efficiency candidate should address unnecessary context/interaction
overhead, not add more machinery or rerun unchanged tasks hoping for lower numbers.
No all-skill improvement, pricing claim or replacement superiority chart is justified.
