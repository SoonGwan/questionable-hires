# Mutation audit inherited-pipe completion — 2026-09-14

Runtime fix `ea28d0e`. Native integration evidence only; no model efficiency claim.

A test module starts an owned sleeping descendant with an inherited output pipe.
The real native runner finishes, but the old helper waits out its two-second limit
and marks correct-code execution incomplete. Both weak and sensitive test variants
reproduce this: two subtest failures in 4.053s against the previous implementation.

The fixed runner polls direct-child exit every 50 ms, subject to scheduling,
starts group cleanup on exit and drains buffered output under the original
deadline. Final cleanup also stops same-group descendants that closed output.
Background lifetime is shorter: checks must finish required work in the foreground.
Escaped groups are not contained. Five-second unconfirmed-child cleanup and
interruption propagation remain unchanged.

The unchanged regression verifies weak correct/mutant tests both pass, while the
same stronger probe passes correct code and rejects the mutant with AssertionError.
Sensitive tests pass correct code and reject the mutant without extra probes.
None time out; copied-import evidence, selected original preservation and owned
scratch cleanup remain. Five focused tests pass in 0.877s, including true timeout,
closed-output deadlines, cleanup/interruption and multibyte capture. Full-suite
follow-up at `ea28d0e`: **430 tests pass in 145.613s** on macOS/Python 3.9.6,
no failures/skips reported. No executable edits or model runs occurred during
the suite. This is local checkout coverage, not hosted/platform-matrix evidence.
Different completed work makes these timings
unsuitable for a speedup claim. No historical or featured result is rewritten.

```sh
PYTHONPATH=tests python3 -B -m unittest \
  test_mutation_helper.MutationHelperTests.test_finished_checks_with_inherited_pipe_preserve_survival_and_detection
```

This separately verifies Con Artist; the prior [Receipt](RECEIPT-PIPE-EXIT-01.md)
and [Exorcist](EXORCIST-PIPE-EXIT-01.md) fixes have different acceptance contracts.
