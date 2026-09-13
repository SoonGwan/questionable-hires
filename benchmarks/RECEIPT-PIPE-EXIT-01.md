# Receipt inherited-pipe completion — 2026-09-14

Runtime fix `a869f62`, following the independently verified Exorcist case.
This is native helper behavior, not a model performance result.

## Reproduced failure

The real Receipt integration fixture compares committed `eligible(n) > 18` with
`eligible(n) >= 18`, using the same current native boundary test. The test module
also starts an owned local sleeping subprocess that inherits the output pipe.
The runner exits after its real assertion failure, but the old wrapper waits on
the descendant's pipe until its two-second deadline. Receipt records the timeout
and stops before the after check.

The new regression fails against the prior implementation with the actual missing
`after` result (one test / 2.288s). It is not a mocked timeout or fabricated model
failure. Sleeping subprocesses remain in the invocation's owned process group.

## Change and observed behavior

The selector checks direct-runner exit at 50 ms polling intervals, subject to
scheduling. Once it exits, remaining group members are killed and buffered output
is drained under the original deadline. Final cleanup also handles descendants
that closed output. This shortens background lifetime; tests whose required
background work must survive the runner are unsupported. Existing timeout and
unconfirmed-cleanup rules remain; escaped process groups are not contained.

The unchanged regression now observes **both** checks: before exit 1 with native
AssertionError, after exit 0, neither timed out. Both retain copied-import identity
and the one-test summary. Exact original file inventory/bytes remain unchanged;
owned comparison copies are removed. Five targeted tests pass in 1.683s, covering
this path, genuine hangs, bounded incomplete cleanup, interruption propagation and
large-output handling. Metadata validation passes.

No before/after model-token comparison or general speed percentage is claimed.
The old comparison aborted and the new one completes more work, so their total
times would not represent equal completed work. Subsequent full local suite:
**429 tests pass in 147.545s**, macOS/Python 3.9.6, no failures or skips reported.
The tested executable/test bytes are those committed as `a869f62`; no executable
edits or model benchmarks occurred during execution. No historical benchmark or
featured chart is rewritten. This is not hosted CI or model-performance proof.

Reproduce the native regression:

```sh
PYTHONPATH=tests python3 -B -m unittest \
  test_receipt_helper.ReceiptHelperTests.test_finished_native_checks_do_not_wait_on_inherited_descendant_pipe
```

Con Artist has a related capture loop but is not modified or claimed repaired by
this change. Its own execution/acceptance contract needs separate verification.
