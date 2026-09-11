# Scoped helper invocation follow-up

Candidate `a772b0d` adds explicit project-bounded discovery and moves ordinary
helper use through the documented CLI, reserving full implementation reads
for trust review, adaptation or troubleshooting. No character, mutation or
task changes. One fresh serial Astra-medium exception task on pinned HTTPX;
preflight 36 tests pass. Logs: ignored `local-runs/httpx-routing-01`.

The new trace has neither an above-project search nor a full helper source
read. It correctly identifies the existing exception assertions, invokes the
helper with the same True-to-False default mutation, and observes 24 correct
tests pass / 4 mutant tests fail with DID NOT RAISE RuntimeError under both
async backends. No extra test is demanded. These are trace-reviewed outcomes,
not an additional independent replay in this follow-up.

The provenance audit verifies the 125 original files, pinned revision and all
four frozen and installed skill resource hashes. No rejected patches or
unremoved mutation copies are recorded. Final snapshots and command review
are not proof of absence of all transient or out-of-scope actions.

Costs: 134,523 total tokens (133,574 input including cache + 949 output),
45.807 seconds. Previous helper run: 117,162 tokens / 44.889 seconds. Despite
removing source inspection, total cost increased. The candidate used six shell
commands versus five, inspected additional test-file paths and manually selected
test support files instead of copying the tests directory. These observations
do not isolate a causal token effect, but defeat a claim that removing one
large read necessarily reduces overall cost.

Retain the scope correction. Do not call this an efficiency win, generalize
one compliant sample into guaranteed behavior, or rerun unchanged inputs to
seek a favorable result. The all-skill performance goal remains unachieved.
