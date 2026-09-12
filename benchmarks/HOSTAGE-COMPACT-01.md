# Compact hostage regression

Protocol snapshot 777f1df, entrypoint 6c5e452. One original skill session completed
in 51.673 seconds with 85,716 tokens (84,514 input including cache + 1,202 output).
No retries, exclusions or candidate changes. Raw records remain under ignored
local-runs/hostage-compact-01. No fresh baseline was run.

Historical discovery skill used 105,775 tokens / 47.746 seconds: this run uses
18.96% fewer tokens but 8.22% more time. That prior run additionally captured an
initial test failure and repaired an unavailable-interpreter command. This run does
neither, so the difference is not a causal compression estimate. It remains more
expensive than that report's historical baseline (80,561 / 45.585).

Seven completed shell calls: initial scoped discovery, separate entrypoint/status,
implementation/test read, another listing plus empty instruction search (exit 1),
requirements/branding read, final tests, focused diff/check. Discovery is still
fragmented. The documented interpreter is selected after reading requirements;
all four final tests are actually captured as passing. No before test run is claimed.

Production guard/try-finally matches the earlier implementation. Existing test
method ASTs and requirements/branding bytes are preserved. Two installed resources
match frozen Git SHA-256 and unchanged before/after manifests. Captured commands
stay scoped; metadata has no empty-output, malformed JSON, event-error or rejected
patch flags. These flags do not establish exhaustive capture.

Generated tests retain controlled overlap and cancellation/retry checks with local
deadlines at the initial signals, duplicate call and active task completion. Retry
after release and cleanup are not independently time-bounded; do not claim arbitrary
async faults cannot hang. No parallel test framework or production refactor is added.

After timed execution, the existing exact duplicate-guard audit ran in isolated
copies, verifying copied imports. Correct suite passes four tests. Removing only
the guard produces an asyncio.TimeoutError at the bounded duplicate call, completes
four tests in 1.036 seconds and exits 1 without the three-second process timeout.
This separate author check establishes bounded detection of that fault, not model
execution or universal termination. The audit JSON was captured in memory and
reported as statuses plus the relevant ending traceback; no new raw audit artifact
was written. Reproduce with the existing audit.py, hostage-duplicate-audit.json and
this run's retained project path, timeout 3.

The compact entrypoint retains useful behavior on this exposed fixture, but does
not achieve overall efficiency. Keep the adverse history; another rerun or scope-
specific instruction is not warranted solely by this result.
