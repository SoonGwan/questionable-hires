# Missing verification evidence: actionable delivery candidate — 2026-09-14

Previous source `ccca07e`. [Checkpoint 08](BUNDLE-CONTRACT-08-REVIEW.md) retains a
Hostage final command with only status lines, no native six-test output or diff,
despite the answer claiming six passes. The existing delivery guidance already
forbids that conclusion, but leaves the next action abstract. Historical output,
metadata and scores remain unchanged.

Replace the generic stopping paragraph with a conditional path: inspect an existing
report attributable to the command/inputs; observe an ongoing execution rather than
duplicate it; without usable evidence rerun only a missing safely repeatable check
within authority; otherwise report unverified. Capture native counts/results and
the test's own exit. A later run remains new evidence, not reconstructed original
output. Do not repeat deployment/side-effectful workflows to recover a transcript.
No mandatory new harness, universal rerun, report file or runtime helper is added.

`tests/test_verification_recovery_controls.py` exercises the actual retained six-test
form suite in disposable project-local copies. A native redirected report contains
six passes and can be read with original inputs unchanged. Removing only final
pending cleanup leaves that report green but changes the source fingerprint. A
separate bounded run of the same tests fails all six with intended True-is-not-False
assertions, while the original report and retained fixture remain untouched.
This illustrates why report attribution/current inputs matter; it is an author
control, **not proof of model adoption** or an automatic verifier implementation.

Skill structure validation passes. Post-edit model behavior, false-pass avoidance
and token/time effect remain unmeasured. The entry grows for a demonstrated failure
path; do not claim lower prompt cost. A focused behavioral check must distinguish
attributable reports, missing evidence and ongoing/unsafe-to-repeat execution rather
than reward merely repeating every test or adding output artifacts everywhere.

Local checks: the new native evidence control passes (one test, 0.219s); the
existing failure-preserving final-batch control passes (one test covering five
scenarios, 1.514s). Catalog/local links and featured EN/KO synchronization pass.
Runtime assets are unchanged. The previous full 509-test run belongs to `ccca07e`,
not a new whole-suite or model measurement of this instruction edit.

Subsequent [handoff screen 01](HOSTAGE-EVIDENCE-01-REVIEW.md) supports attributable
report reuse and exact-input restoration. Its absent-report case issues a new
test command but again lacks the original native output. Model-visible versus
logged output is unresolved; do not treat later replay as original verification.
