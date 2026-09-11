# Correct-probe reuse: local paired check

Freeze before execution: previous helper `5f68ac7`, candidate helper `91fdde3`,
example files/recipe `e7fb780`. No model calls or changes during the check.

Use `examples/con-artist-batch` in disposable directories. Run two cases:

1. The unchanged two-fault recipe, with identical stronger probes.
2. The same recipe with `assert len(store) == 2` appended to the second probe.
   This remains a valid assertion but differs in code, so it must execute anew.

Three repetitions per case/version, serially. Alternate previous/candidate order
by case index plus repetition index. Use the same Python interpreter/environment
and helper defaults. Load each helper from its pinned Git source before timing.
Time only `audit_batch`, including an identical execution-count wrapper in both
versions. Fixture copying and verification are outside timing.

Require both audits observed; correct tests/probes exit 0, mutant tests exit 0,
mutant probes exit 1 with the appropriate missing/duplicate-record AssertionError.
Resolve observation references before checking output; reused results must point
directly to actual observations, not other references. No timeouts/truncation,
source byte/mode changes or surviving disposable directories are allowed.

Record each elapsed time, child-execution count and serialized JSON byte count.
Expected execution counts: identical probes 7 → 6; different probes 7 → 7.
Keep adverse timing/output results; no retries or exclusions. Report all rows and
arithmetic means. Three repetitions on a shared host/cache are descriptive only;
JSON bytes are not tokens, and helper timing is not whole-task/model latency.
