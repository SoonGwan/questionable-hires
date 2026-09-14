# JavaScript SubmitPanel screen — review in progress

Launch `3949ef6`, resource `8ca9e70`;
[frozen protocol](HOSTAGE-JAVASCRIPT-PANEL-01-PROTOCOL.md). No aggregate before
both scheduled cells finish and original evidence is reviewed. Author replay
waits until timing finishes; no resource/task edits or author tests during timing.

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
