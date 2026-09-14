# JavaScript lifecycle screen: adoption, less authored code, still more tokens

2026-09-14. [Frozen protocol](HOSTAGE-JAVASCRIPT-SCOPE-MODEL-01-PROTOCOL.md),
launch `330a17b`, resource `22bd929`. [Exported evidence](results/hostage-javascript-scope-model-01/run.json).
One exposed authored task, two fresh serial Astra medium sessions, n=1 per arm.
Both completed without timeout; no excluded/retried cell. No general efficiency
claim, independent confirmation, or featured-chart update.

| Observation | Baseline | Skill |
|---|---:|---:|
| Input + output tokens, cached input included | 104,047 | 115,286 |
| Process wall seconds | 99.788 | 93.105 |
| Output tokens | 2,684 | 2,367 |
| Completed shell calls | 5 | 7 |
| Original native tests passing | 7/7 | 7/7 |
| New regression file lines / bytes | 174 / 6,181 | 136 / 5,355 |
| Copied support lines / bytes | 0 / 0 | 162 / 6,124 |

Within this pair: **+10.80% total tokens, −6.70% wall time**. The new regression
file is 21.84% fewer lines / 13.36% fewer bytes; output tokens are 11.81% lower.
These are descriptive observations, not isolated causal savings. Including the
copied module, skill adds *more* test/support code. Smaller authored code is not
itself task success or proof of lower maintenance cost. Prior screen's +93.51%
tokens is historical context, not a controlled before/after treatment effect.

## Actual implementation and tests

Both implement per-instance `pending = false`, early duplicate return, set before
callback, `return await save(signal)`, and finally clear state. Only whitespace
differs. Both preserve the original tests and requirements byte-for-byte.

Baseline writes its own bounded/scenario/gate/track/cleanup support. Five new
tests cover pending at actual callback entry, signal/result identity, duplicate
completion while the first callback is blocked, independent concurrent instances,
sync/async failure identity with retry, and actual AbortController-driven callback
rejection with listener removal. Rejection handlers attach promptly and finally
releases gates before bounded task drain. Extra witnesses include two consecutive
duplicates and retrying one instance while its sibling remains pending.

Skill copies the frozen module exactly and imports **withControlledCalls**.
Each of five new tests uses owned callbacks, run registration and bounded waits;
it does not author another scenario/deadline implementation. Its short retry
function asserts actual application behavior, not generic lifecycle mechanics.
It covers all requested transitions and abort-listener cleanup. In the sync-error
case it invokes SubmitPanel outside `run()` inside `assert.doesNotThrow`, then
registers the returned task, so the helper cannot hide an API regression from a
rejected Promise to a synchronous throw. This is a useful extra witness absent
as an explicit assertion in baseline. The two runs do not perform identical
extra work; do not attribute the time delta exclusively to the helper.

Original native output captures all seven names and full pass/fail/cancel/skip
summaries for each run. Each `node --test` command has its own exit 0. Baseline
native duration is 48.047791ms; skill 55.202666ms: those are test runtime, not
model task time. Skill's one empty shell output is mkdir/cp with exit 0, not a
missing native test transcript. No observed scope or capture exception.

## Reconciliation and separate fault replay

[Author replay](results/hostage-javascript-scope-model-01/author-replay.json)
reconciles original JSONL usage against metadata, sanitized event content,
installed resources before/after and frozen Git hashes, exact reviewed file
inventories and copied asset identity. Retained projects remain unchanged.

Ten native runs in separate copies preserve all retained test/support sources:

| Variant | Baseline pass/fail | Skill pass/fail |
|---|---:|---:|
| Final implementation | 7/0 | 7/0 |
| Original implementation | 2/5 | 2/5 |
| Missing duplicate guard | 6/1 | 6/1 |
| Missing cleanup | 2/5 | 2/5 |
| Wrong signal forwarding | 4/3 | 3/4 |

All ten meet expected exits/counts, discover seven tests, cancel/skip zero and
finish within the 15-second outer deadline. Skill's missing-guard case fails by
its owned 1-second deadline because the duplicate stays blocked; it is not an
AssertionError or process hang. Baseline gets a direct value AssertionError.
Do not claim identical diagnostics. Replay is separate from original evidence.

## Decision

The wrapper demonstrably replaces authored lifecycle boilerplate and preserves
required regression coverage in this screen. It does **not** establish lower
total token cost or the all-eight performance objective. Retain as a measured
development candidate, not an efficiency headline. Both runs still rediscover
files across separate reads; skill loads a larger module and needs two extra
shell calls. A subsequent change must address that cost without dropping real
checks, followed by transfer/repeated evidence rather than favorable reruns.
