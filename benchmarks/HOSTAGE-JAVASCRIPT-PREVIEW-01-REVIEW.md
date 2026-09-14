# Preview transfer: faster observed time, more tokens, retained-test blind spot

2026-09-14. [Protocol](HOSTAGE-JAVASCRIPT-PREVIEW-01-PROTOCOL.md), launch
`4a064bc`, resource `f0b29dd`. [Original evidence](results/hostage-javascript-preview-01/run.json).
One authored transfer task, fresh serial Astra medium cells, n=1 per arm. Both
complete, no timeouts/exclusions/retries. This is not an independent user repo.

| Observation | Baseline | Skill |
|---|---:|---:|
| Total tokens, cached input included | 109,445 | 125,009 |
| Process wall seconds | 214.251 | 146.851 |
| Output tokens | 3,686 | 4,243 |
| Completed shell calls | 4 | 7 |
| Final captured native passes | 33/33 | 54/54 |
| Authored regression lines / bytes | 243 / 9,762 | 270 / 11,606 |
| Copied support lines / bytes | 0 / 0 | 165 / 6,362 |

**+14.22% tokens / −31.46% time** within this pair. More test names do not establish
better coverage. Extra work differs, shared host/cache and n=1 limit inference,
and a post-review native probe exposes a skill-test blind spot below. Do not
promote this as a general speedup or an accepted overall efficiency gain.

## Original model work

Both correct implementations assign a new per-instance request token before
fetch, set loading while preserving value, run fetch and decode for every caller,
then gate success/error state on ownership. Baseline uses a private object token;
skill uses a private Symbol token. Both preserve return/rejection identities,
original tests and requirements. Neither invents cancellation or deduplication.

Baseline authors deferred/bounded/harness, immediate outcome observers and
after-test release of both callback phases before bounded drain. Its state helper
checks status and exact value/error references. Tests cover 16 overlapping phase/
outcome/newest-state combinations with identical keys; four sync/async phase
failures, eight real abort combinations, displayed-value recovery and isolation.
It subsequently adds an abort-ignoring callback/uncancelled controller check.
Original native runs capture 32 passes then 33 passes, full names and summaries.

Skill reads the complete usage header with application files, copies the module
exactly and uses withControlledCalls; application-specific begin/entry/finish
functions remain. Tests add distinct-key combinations (32 overlap cases), idle/
ready failure origins and null/undefined reasons, two-phase actual abort checks,
abort-ignoring callbacks, argument counts, state fields and instance isolation.
Its first native run has **50/52 passes, two failures**: a default error parameter
in its own state assertion helper turns explicit `undefined` into expected null.
It repairs the helper using a rest argument, then adds two checks and captures
54/54 passes. The application and copied helper were not responsible for that
initial assertion error. Preserve the failed run; final green does not erase it.

Both use bounded waits and owned task/callback/listener cleanup. Native results
have full names/counts and test-specific exits. Skill mkdir/cp's empty output is
legitimate; baseline's initial no-match AGENTS search exit 1 is not a test failure.
No observed scope or native-output capture exception. Final test runtimes are
59.110916ms baseline and 64.438083ms skill, not model task times.

## Separate reconciliation and fault controls

[Initial author replay](results/hostage-javascript-preview-01/author-replay.json)
reconciles original usage/sanitized events, frozen installed resources, exact
reviewed inventories, unchanged originals and exact copied module. All retained
sources remain unchanged. Eighteen disposable-copy native runs, 15-second process
deadlines, preserve test/support sources. Every variant discovers 33/54 tests,
with zero cancellations/skips/process timeouts:

| Variant | Baseline pass/fail | Skill pass/fail |
|---|---:|---:|
| Final | 33/0 | 54/0 |
| Original | 4/29 | 6/48 |
| Stale success replacing state | 22/11 | 38/16 |
| Stale error replacing state | 19/14 | 32/22 |
| Reused token | 10/23 | 16/38 |
| Wrong decode signal | 1/32 | 5/49 |
| Lost displayed value | 11/22 | 13/41 |
| Global owner across instances | 32/1 | 53/1 |
| Skipped stale decode | 27/6 | 46/8 |

All initial controls meet expected outcomes. This did not end review.

## Post-review counterexample: mutate state in place

Skill overlap tests save `const protectedState = loader.state` and later compare
only object identity after stale completion. They do not snapshot its fields.
An unchanged object reference cannot prove unchanged contents.

A separate [in-place probe](results/hostage-javascript-preview-01/author-in-place.json)
replaces guarded success publication with unconditional
`Object.assign(this.state, {status:'ready', value, error:null})`. This violates
the explicit latest-owner contract without replacing the state object. Neither
retained test source nor original artifact was changed. Four additional native
runs show final implementations still pass; the faulty variant produces:

- Baseline: **22 pass / 11 fail**, detecting stale overwrite.
- Skill: **54 pass / 0 fail**, missing the same substantive defect.

No process timeout, skipped test or cancellation explains the escape. This is a
post-review counterexample, not a rewritten preregistered score or evidence that
the skill's final application implementation is wrong. It demonstrates weaker
retained regression protection for this failure mode despite more test cases.

## Decision

The helper transfers to two-stage work and the observed run is faster, but total
tokens increase and regression protection has a demonstrated hole. Keep all
evidence and original metrics; no featured update. Next improvement should target
state-content assertions across pending operations, preserving exact payload/
reason references rather than deep-cloning or relying on container identity.
Validate a correction against this counterexample before any new performance
claim. The all-eight real-use and efficiency objective remains unmet.
