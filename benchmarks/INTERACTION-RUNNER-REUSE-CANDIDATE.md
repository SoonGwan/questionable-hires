# Interaction runner reuse: unmeasured candidate

The completed [bundle 02](BUNDLE-CURRENT-02-REVIEW.md) includes two Mother-in-law
sessions that wrote self-spawning subprocess wrappers into their QA files:
`search-order--skill--1/project/test_search_qa.py` and
`search-protected--skill--1/project/qa_search.py`. Both use a five-second parent
deadline around a worker. The broken-search file also bounds its controlled
event/task waits. Original execution output is missing for both commands;
separate author replay is not original model evidence.

The earlier entrypoint required a process deadline if cancellation can be ignored,
but did not distinguish an existing runner boundary from a new test-file wrapper.
The candidate now explicitly prefers a sufficient existing runner timeout and
retains process containment where cancellation-resistant operations require it.
This does not assert that the observed wrappers were unnecessary: their available
runner guarantees were not established. It creates a cheaper valid route when
those guarantees are already present, without inventing one for other projects.

No timeout is removed from existing artifacts. No historical result is rescored.
This wording change has no measured token, time or behavioral improvement yet.

Next behavioral evaluation should supply a real existing runner with an explicit
whole-test/cleanup deadline and cover both a cooperative controlled response and
a cancellation-resistant operation. Check actual runner use, decisive output,
timeout classification and absence of redundant wrappers; do not require exact
phrasing or treat fewer lines as success. Compare whole-task costs only after
equivalent relevant coverage is established. Retain unsuccessful attempts.

## Author-side deadline check

`python3 -m unittest discover -s tests -p test_probe_runner.py -v` passes
14 tests on the local POSIX host. The added check runs the same direct async
program with cooperative cleanup and with cleanup that never finishes and
suppresses cancellation. No self-spawning wrapper is embedded in that program.
The existing Exorcist runner returns success with the cooperative cleanup marker;
with stubborn cleanup it retains the entered-cleanup marker, reports timeout and
child status −9, and confirms child reaping within the test's two-second bound.
The runner deadline is 0.5 seconds; its separate reaping allowance still applies.

This establishes a concrete reusable boundary, not a guarantee about arbitrary
project runners, escaped process groups, or operating-system termination delays.
`cleanup_complete` means the runner reaped its child, not that application cleanup
finished: the stubborn case explicitly lacks the finished-cleanup marker. This
does not make Exorcist a dependency of Mother-in-law or measure model adoption,
interaction correctness, token savings, or end-to-end speed.
