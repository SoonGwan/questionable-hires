# Mother-in-law: choose deliverable and coverage before execution

The [all-eight contract gate](results/bundle-contract-03/README.md) exposes
duplicated helper-plus-project-test execution in both QA skill cells. Protected
search costs +58.38% tokens / −3.91% time; broken search +29.42% / +4.69%.
Required retained tests are legitimate work, not scope creep or removable checks.

Inspection establishes a routing mismatch: helper `normal` runs queries
**sequentially**, not with normal-order overlapping responses. The default second
case overlaps with reversed completion. Neither default case checks an existing
displayed result during loading or older completion while newer is pending.
The measured retained suites cover these additional obligations. A preliminary
helper execution therefore cannot discharge the requested entire project test.

## Candidate change

Only the skill entrypoint changes; helper implementation, description, UI metadata
and automatic selection remain intact. Choose the requested deliverable first:

- For a retained project regression, create/extend that test and execute directly,
  reusing existing coverage. Do not first run equivalent disposable helper cases.
- For captured observations fitting the actual helper contract, retain direct
  helper use. Unsupported checkpoints require project checks from the outset.
- Explicitly distinguish saved JSON/installed-skill commands from a standalone
  project regression. Do not change production code to fit a helper or eliminate
  required retention/pending checks to make a score look better.

This follows skill-creator's preserve-user-intent and decision-changing guidance
principles. It does not force a new harness when adequate project tests exist,
ban justified diagnosis, or claim native code is always cheaper. Scope remains
interaction QA including browser routing, not just the measured Python example.

## Actual author validation

`test_helper_success_does_not_certify_loading_retention` supplies a concrete
guarded component that clears its previous result while loading. Both default
helper cases pass, proving their green status is insufficient for that additional
contract. A native pending-state assertion passes the healthy guarded component
and fails the clearing variant with `None != 'existing result'`. Both checks
actually execute async code; bounded waits and cleanup leave their owned tasks
done. This test documents the current helper boundary, not a permanent prohibition
on a later explicitly designed helper extension.

Focused suite: **14 tests pass (0.257 seconds)**. Skill/catalog validation and
featured synchronization checks pass. These author checks verify the coverage
counterexample and unchanged helper behavior, **not model routing or token savings**.
Full repository suite: **359 tests pass (50.407 seconds)**; skill resources stayed
unchanged throughout the run, including packaging validation.

Next behavioral confirmation needs a separate realistic project-test request,
then original-output review of coverage, delivery, duplicate execution and costs.
The old exposed gate is not rerun for a better score; its original resources and
unfavorable costs stay frozen. The all-eight real-development goal remains unmet.
