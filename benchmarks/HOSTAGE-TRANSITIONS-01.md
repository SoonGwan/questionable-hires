# Hostage Negotiator: state transitions, not a diff budget

Candidate `6bbbbeb` retains the character and supporting-change acceptance
test, connects state ownership to completion/recovery (including applicable
cancellation), and asks for missing checks rather than duplicate harnesses.
No new helper, mandatory document or framework was added.

One fresh `necessary-state` skill session under ignored
`local-runs/hostage-transitions-01` completed with 85,493 total tokens
(84,178 input including cache, 1,315 output) in 56.662 seconds.
The prior `fast-regression-02` sample used 102,734 tokens in 51.819 seconds:
16.8% fewer tokens, 9.3% more wall time. These are temporally separated
single samples, not a paired causal estimate or general performance win.

The agent changed only `form.py`: initialized pending, rejected duplicate
submissions, preserved the save result and cleared pending with `finally`.
Its executed assertions covered initial/pending states, one save during
overlap, success, original exception propagation, retry and cancellation.
The prior sample did not explicitly test cancellation, though its implementation
also used `finally`. This establishes broader checked behavior in this sample,
not a newly fixed cancellation defect or repeatable skill advantage.

Scope failure retained: `find .. -name AGENTS.md -print` searched above the
explicit project boundary. No claim of full task/scope success is made.
The follow-up instruction keeps discovery, including instruction-file searches,
inside an explicitly restricted root. That correction is not yet model-tested.

The initial framework-specific file search happened before loading the skill;
post-load instructions cannot reliably prevent such pre-load overhead.
Do not attribute that overhead to the skill's body or disguise it by excluding
tokens. Existing-test reuse was not exercised because this fixture has no tests.
