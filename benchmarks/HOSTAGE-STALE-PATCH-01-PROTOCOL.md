# Stale patch recovery 01

Freeze one newly authored page-limit task before fresh model calls. Unlike
buffer tests this has an existing four-test suite, no async helper need and an
explicit instruction to attempt a supplied stale patch before adapting it.
This is an intentional failure-recovery probe, not a random real-world sample.
Task explicitly prohibits native tests until a production edit succeeds and
preserves append-only native invocation logs; all scored obligations are visible.

Three fresh GPT-6 Astra medium sessions: baseline/original/candidate, fixed
order, serial, n=1, 240-second deadline. Original resources `3083086`, identical
roundtrip candidate from `hostage_roundtrip_candidate.py`; do not modify the
candidate to fit this task. No replacement/exclusion/retry, stop account limits.
No all-eight automatic routing claim; named skill used only in skill arms.

Preflight actual git apply must reject the supplied patch without changing
production. Native tests must expose `100 != 0` on faulty code and pass correct
and alternate valid implementations, preserving all invocation audit entries.
The models receive the existing suite and audit mechanism, not a hidden oracle.

Review original command order and outputs, rejected edit exit, successful repair,
native source hash/zero-result audit, exact skill exposure, unchanged owner files
and HEAD. Audit content supplements tool evidence, not a substitute for it; check
models do not rewrite audit/test files. Native exit must remain distinct from a
later successful command. Neither a rejected edit nor unexecuted code supports
a claim of passing tests. No requirement to batch; measure actual behavior.

After all sessions finish, independently run delivered source against unchanged
supplied tests in disposable project-local copies, and test faulty/valid code
with those tests. Label author replay separate from original execution. Retain
all observed quality/scope failures and setup/repair cost before cost comparison.
Full input including cache plus output counted once, process time, responses.
No superiority inference from one task, no confidence intervals or chart updates.
