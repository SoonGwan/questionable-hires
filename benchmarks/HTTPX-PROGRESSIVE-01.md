# Progressive reference check: routing works, overhead remains

One skill-only development session on the existing HTTPX default-exception task,
snapshot `4bbac5a`, Astra medium. Preflight: 36 pass. Raw ignored artifacts:
`local-runs/httpx-progressive-01`. No new baseline or repeat; this checks reading
behavior after the reference split, not independent confirmation of superiority.

The model reads the common reference and does not read the advanced reference
(its filename appears in discovery). However, it reads the entire helper source
in two ranges and executes seven shell commands, versus six in the preceding
skill cell. It also reads the contribution guide. There is no demonstrated
reduction in interaction count or implementation inspection.

The audit remains correct: only the constructor exception default is mutated;
normal tests pass 24/24; the mutant fails four before/after-response propagation
checks across asyncio and Trio with `DID NOT RAISE RuntimeError`. It stops without
a stronger probe or batch execution. The original command output was reviewed;
no new author replay is attributed to this session.

| Observation | Total tokens, cache included | Process seconds |
| --- | ---: | ---: |
| Current skill | 125,527 | 43.119 |
| Preceding skill (`54328b1`) | 150,818 | 45.815 |
| Earlier paired baseline | 79,016 | 48.340 |

Current costs are about 16.8% fewer tokens / 5.9% less time than the preceding
skill, but about 58.9% more tokens than the earlier baseline. These are separated
single observations with different reading behavior on a shared host/cache;
neither the favorable difference nor the adverse magnitude is a causal estimate
of the documentation change. Do not count a shorter reference as equivalent to
lower total model input or fewer interactions.

All 125 upstream files and five installed/frozen skill resources match the audit.
No timeout, patch rejection or capture flags. The final command exits 1 on an
empty disposable-path search, not a test failure; `.agents/` remains installed.
Final snapshots do not prove absence of transient changes or outside operations.

Disposition: optional-reference routing is observed, overall efficiency is not
accepted. Repeated wording tweaks on this exposed task have not established
baseline parity. Preserve the adverse pair and stop using this task to chase
favorable numbers; subsequent work needs a substantive workflow change and
broader task coverage while keeping development batches below ten tasks.
