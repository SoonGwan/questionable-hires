# JavaScript SubmitPanel screen — adoption with adverse cost

Launch `3949ef6`, resource `8ca9e70`;
[frozen protocol](HOSTAGE-JAVASCRIPT-PANEL-01-PROTOCOL.md). Both scheduled cells
completed, no timeouts/exclusions. No resource/task edits or author tests occurred
during timing. Pending statements below are sequential notes superseded by the
final reconciliation, not replacement original evidence.

## Final reconciliation — 2026-09-14

Raw events/terminal usage, unchanged installed resources and reviewed complete
file inventories reconcile against launch `3949ef6`. Both original tests and
requirements remain byte-identical to the frozen fixture. Only panel.mjs changes;
both add panel.pending.test.mjs and skill additionally copies the ES-module asset
byte-for-byte. No observed scope violation or missing decisive output.

[Separate author replay](results/hostage-javascript-panel-01/author-replay.json)
runs each arm's unchanged tests against final/original/missing-guard/missing-cleanup/
wrong-signal implementations: ten 15-second-bounded native runs, seven discovered
tests each, zero cancelled/skipped tests. Both final implementations pass all
seven. Original and missing cleanup fail five pending assertions; wrong signal
fails four baseline/three skill identity assertions. Missing guard fails baseline's
explicit assertion, while skill's held duplicate reaches its one-second deadline
and fails before cleanup drains callbacks. These are distinct failure witnesses,
not ten model measurements. All expected outcomes match; retained files unchanged.

| Arm | Total tokens | Elapsed seconds | Native model test result |
| --- | ---: | ---: | --- |
| Baseline | 68,671 | 92.478 | 7 pass, 0 fail |
| Skill | 132,886 | 102.947 | 7 pass, 0 fail |

Skill costs **+93.51% tokens / +11.32% time** (cached input counted once plus
output). Same implemented semantics, different extra test witnesses and setup.
This confirms helper adoption and scoped delivery, not efficiency improvement.
One authored task/pair, shared host/cache and unequal extras prohibit causal or
general claims. No reconnect subtraction, favorable retry or altered chart.

The asset replaces entry/release mechanics but leaves enough lifecycle ownership
that both models build a custom scenario layer. Skill also splits discovery and
known-file reads across more calls. Next work must address demonstrated repeated
setup, without dropping rejection handling, abort ownership or fault-sensitive
assertions. Merely shortening the entry has not proved useful in prior screens.

## Skill

Completed: **132,886 tokens / 102.947s**, nine shell calls. Reads the correct JS
asset (not Python), but implementation is opened separately after requirements/
tests/asset. Copies the asset unchanged and adds a scenario wrapper registering
cleanup, owned task outcomes and callback settlement, including calls entering
during cleanup. Actual abort listener rejects the controlled call with signal.reason;
listener is removed in finally. No automatic Promise cancellation is invented.
Five new native tests plus two originals pass with all names and full summary
captured (55.715875ms), zero failures/cancellations/skips. Existing tests unchanged.

Required pending, duplicate, independence, identity, sync/async failure and abort/
retry checks are present. Baseline additionally tests reentrant duplicate and
normal-success retry, and checks synchronous-error reset before processing the
rejection; skill groups required checks differently and guards cleanup against
later callback entry. No observed capture/scope issue. Final asset cmp is silent
with exit zero, which is expected comparison behavior, not missing test output.

## Baseline

Completed: **68,671 tokens / 92.478s**, three shell calls. Adds per-instance pending,
an early duplicate return and finally reset. New panel.pending.test.mjs retains
five native tests alongside the two unchanged original tests. Original output
captures all seven names and a seven-pass summary, zero failures/cancellations/
skips (51.882ms). The failure-preserving `&&` command also checks diff formatting,
empty original-test diff and scoped status.

Tests use actual SubmitPanel with owned deferred callbacks, one-second application
waits, immediate outcome/rejection handling, finally settlement/draining and abort
listener cleanup. Cover initial/pending state before callback invocation, signal
and result identity, reentrant plus later duplicates, concurrent independent
instances, delayed and synchronous error identity/retry, and actual controller
abort causing callback rejection with the same reason followed by retry.
Synchronous-error test also checks immediate pending reset before promise handling.
No new cancellation policy or browser claim. No observed scope/capture issue.
Raw/resource/original-file inventory reconciliation and retained-test fault replay
remain pending until timing ends. Extra reentrant/normal-retry witnesses must be
distinguished from required work in the pair comparison.
