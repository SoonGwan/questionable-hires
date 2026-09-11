# Receipt: current-fix evidence collection

Development check of Receipt `8a08ecf`, not confirmation data or an eight-skill
performance claim. Two new synthetic current-parser tasks share a contract and
implementation; one already contains the URL regression, the other needs it added.
This deliberately tests one workflow in two evidence states, not broad task diversity.
The author-only fixture test establishes original failure and fixed success with
identical assertions, including preservation of empty values and invalid-input
behavior. Evaluated sessions receive only the neutral task and project files.

Freeze this protocol and fixtures before running four fresh Astra medium sessions:
two cases, baseline/skill, one repeat, serial, seed 20260911, timeout 240 seconds.
Use run.py's shuffled schedule with arms baseline then skill and generated case
order missing then existing. No retries, exclusions, dependency installation or
external services. Preserve failures, original logs, total input (cache included)
plus output tokens, process wall time, diffs and installed resource identities.

Evaluate the frozen case criteria from actual command evidence and artifacts.
Check red/green uses the same URL assertion and original implementation really
fails for the reported defect; an import/setup failure is not reproduction.
Record repeated checks, history lookup and whether final collection preserves each
check's status. A consolidated step is optional and not a task-success criterion.
Command count alone is not performance, and baseline/skill are not a causal test
of this edit against the previous Receipt revision. Keep adverse observations.
