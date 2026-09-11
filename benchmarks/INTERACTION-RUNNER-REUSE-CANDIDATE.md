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
