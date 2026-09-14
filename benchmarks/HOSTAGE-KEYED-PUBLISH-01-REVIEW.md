# Keyed publication transfer screen — reviewed, no efficiency win

[Protocol](HOSTAGE-KEYED-PUBLISH-01-PROTOCOL.md), launch `a1a258c`; skill/collector
`7dd4b56`, asset `d9e7711`. Both fresh scheduled sessions complete without timeout,
account-limit events, exclusions or author retries. No resource/task edits or
author tests during model timing.

| Arm | Tokens including cached input | Seconds | Shell calls |
| --- | --- | --- | --- |
| Baseline | 104,309 | 92.624 | 4 |
| Skill | 130,644 | 99.704 | 8 |

**+25.25% tokens / +7.64% time** is adverse. One newly authored but exposed task,
n=1, shared host/cache and unequal work do not establish causal or general gains.
Do not compare this to previous incomplete Form runs as a corrected speedup.

## Implementation and tests

Both produce identical Publisher code: instance-owned set keyed by exact ID,
duplicate early return before state mutation, and finally removal after awaiting
the original callback. Existing files/tests remain byte-identical except Publisher;
no global lock, queue, automatic retry or external effects.

Both retain seven new tests exercising actual Publisher, adding to two originals.
Required duplicate/noninterference, cross-key/instance concurrency, arguments and
result/exception identity, success/failure/synchronous-failure retry and cancellation
cleanup/retry are covered. Owned tasks and behavior waits are bounded.

Baseline uses custom gates, checks additional Unicode/whitespace normalization
witnesses concurrently and repeats regressions after its full suite command.
Skill copies exact ControlledCall bytes and uses real entry/response handles,
including keyword payload identity and cancellation. This confirms transfer of the
asset beyond a zero-argument form; it does not prove lower setup cost. Entry,
reference and asset reads are separate calls, in addition to discovery/source reads.

## Original verification evidence and limits

Baseline captures the original two-test pass. Its final command chains full-suite
and regression runs with `&&`; output contains only the seven-test regression
pass (0.036s) and diff/status. The full nine-test native section is absent despite
the final nine-pass claim. Later execution is indirect evidence, not a full log.

Skill separates final Git checks from a standalone unittest command. That command
has native exit 0 and `Ran 9 tests ... OK` (0.050s), supporting its total-pass claim.
However only the last full verbose header and a preceding `ok` survive in original
output. The existing header-count diagnostic flags this as partial/nonstandard.
Do not claim full individual-result capture or that the new wording caused the
better test-status delivery. Neither original command has a missing summary under
the new heuristic; this demonstrates why that diagnostic is not a completeness
validator. Empty copy output is legitimate.

## Separate native replay and integrity

[Exports](results/hostage-keyed-publish-01/) retain all attempts, commands, answers,
metadata and sources. [Author replay](results/hostage-keyed-publish-01/author-replay.json)
uses unchanged retained tests in isolated copies with 20-second process bounds.
Both final implementations pass all nine tests (baseline 0.042s, skill 0.048s)
with full native headers. Original implementation fails each duplicate assertion.
Global-busy variants error at bounded cross-key entry waits. Missing cleanup
causes baseline's five result-identity failures and skill's four bounded retry
timeouts. These are real control failures, not all actual/expected assertions.
All eight expected outcomes match; copied originals/tests remain unchanged.

Raw terminal usage, sanitized events, frozen installed resources and reviewed
inventory reconcile for both cells; no observed scope violation. Separate replay
does not replace absent original output or prove its cause. Featured/historical
data remains unchanged.

Next: reduce the small asset's discovery/reference burden without hiding cleanup
or callback contracts. More test-support reuse alone has not demonstrated savings;
preserve this adverse transfer result when evaluating a future interface change.
