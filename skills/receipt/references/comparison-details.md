# Comparison compatibility and failure details

Use the [routine comparison guide](existing-fix.md) for recipes and ordinary
results. Read the relevant section here for startup compatibility, ambiguous
exits or resource/cleanup questions; this is not another required setup pass.

## Native module startup

`"invocation":"module"` runs Python `-B -m unittest` with the recipe's test
arguments. Default `bootstrap` is unchanged. Temporary copy-local startup checks
same-process imports; results include `command`, `native_exit_code` and
`provenance_ready`. Timeout/output supervision remains.

Only child-local lookup changes; descendants do not inherit the probe. Existing
system/user `sitecustomize` and enabled `usercustomize` run in order before
copied-import verification. Their actual modules are retained, not replaced with
the probe. User-site disabling remains effective. Hook errors, including early
exit, stop comparison with check 7 rather than continuing tests after a warning.

Conventional hooks are supported, not arbitrary startup rewrites. Project-local
customization, disabled site initialization, hooks depending on the exact startup
stack or replacing import machinery need native project setup. Do not remove
hooks or bypass provenance to make a comparison pass.

When using that native setup, [preservation-only support](native-preservation.md)
can replace a handwritten tree inventory without altering the startup hook.

## Exit interpretation

CLI 0 means observations collected, not a verified fix. Inspect actual test
identities, assertions, counts/skips, copied imports and each check's own output.

| Check mode | Observed exit behavior |
| --- | --- |
| Bootstrap unittest | Failure 1; empty/all-skipped 5; partial-skip success 0 |
| Module unittest | Native exit preserved; empty discovery may return 0 or 5 depending on Python; all-skipped checks can return 0 |
| Pytest | Native exits retained; otherwise-success/failure 0/1 without collection-time import verification becomes incomplete 7 |
| Missing startup provenance | Check 7; native exit retained separately; CLI 2; no next comparison |
| Import verification exceptions, including `SystemExit(0)` | Traceback retained; check 7; CLI 2; no next comparison |

An independent runner exit 7 is conservatively incomplete too. No mode proves
requested coverage. These checks do not catch `os._exit`, later early exits or
adversarial execution; inspect actual tests. A setup/import error is not the
requested defect's reproduction.

Pytest owns configuration and test collection before listed imports are checked
in that same process, before test bodies. This preserves native assertion
rewriting, custom test filenames and configuration hooks. Import failures during
native collection keep pytest's own failure code; they are not passing evidence.
Collection and plugin code can execute before verification: trusted tests only,
not a sandbox. Explicit `--assert=plain` remains plain; a collect-only result or
all-skipped run still does not establish that the requested assertions executed.

## Preservation guards

`watch` checks selected existing files/directories without copying or executing
them. It excludes new entries and arbitrary effects. `originals` records selected
hashes/modes/unchanged status; reuse those checks instead of another snapshot.

`guard_tree` is opt-in for requested whole-project preservation, only when all
source reads are authorized. It inventories Git/ignored files, directories
(including empty/root), bytes/modes and link text, not link targets. `tree_guard`
reports unchanged/counts/digest, not a full hash listing. It replaces snapshots
around native comparison, not diff review or later checks.

Added/removed/changed entries abort without restoration. There are no exclusions;
special files and oversize fail closed: 10,000 entries including root, 20 MB streamed
per inventory, separate from copying. Larger projects need another native method.

This is not a sandbox. Test paths/subprocesses can escape; snapshots are not atomic.
Tree guards exclude link targets, ownership, timestamps, ACLs/xattrs, concurrent
writes, changes restored between observations and operations outside their interval.

## Resource and process boundaries

Copying has a shared 20 MB budget. Known overflow rejects before reading; reads
stop at remaining budget + 1 byte, growth overflow aborts before tests, and final
integrity reads stop at original length + 1. Total memory is not bounded by these
limits. Directory expansion is limited to 10,000 entries. An optional tree guard
has its own 10,000-entry/20 MB streamed inventory budget, separate from copying.

Selected-input reads use nonblocking, no-follow descriptor opens and compare the
opened regular file's identity/mode with its immediately preceding observation.
An observed replacement aborts instead of following a link or waiting on a FIFO,
including during final integrity reads. This is not an atomic snapshot: parent
directory races and concurrent writes to the same inode remain outside the guarantee.

Execution defaults to 30 seconds/check (`--timeout` up to 300), retaining the last
12,000 output characters. `output_truncated` leaves omitted evidence unavailable.
Child exit has a separate five-second cleanup wait: unconfirmed exit means CLI 2,
comparison not established and no next comparison. Other errors/interruptions
propagate. Descendant termination is not guaranteed; do not retry automatically
while a prior process may remain.

Required work must finish in the foreground. After direct-runner exit, remaining
process-group members are killed and buffered output drained under the original
deadline; inherited pipes alone do not cause timeouts. Exit polling is 50 ms,
subject to scheduling. Persistent background jobs are unsupported. Tests still
own assertions/cleanup and escaped groups are not contained.

Python 3.9+/POSIX, trusted tests only. Selected-original checks and optional tree
guards do not restore changes or prevent test effects.
