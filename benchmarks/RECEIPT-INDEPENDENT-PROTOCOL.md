# Receipt: independent checks must continue after a failure

One new development workflow case. A real renderer regression is fixable, while
an independently owned missing packaging input keeps another actual checker red.
The example checker must still execute after that failure. The neutral request
explicitly requires all checks and preserves packaging ownership. This tests the
explicit-status branch of Receipt's collection guidance, not universal fail-fast
chaining. Author fixture verifies real checker statuses 1/1/1 before and 0/1/0
after a correct scoped fix, with unchanged check/packaging files. Do not provide
this oracle to model sessions.

Freeze entrypoint abb4b93, runner fd8d578 and this protocol/fixture commit. Two fresh
Astra medium sessions, baseline/skill, one repeat, serial, seed 20260911, 240-second
limit via run.py shuffled schedule. No retries, exclusions, installation or source
candidate edits during execution. Capture all original outputs, statuses, diffs,
resource identities, input-plus-output tokens and process wall time.

Judge actual execution of each required checker after the fix, not a wrapper's
last exit alone. A known packaging failure is expected task evidence, not a failed
model cell; creating a fake NOTICE or skipping the example is a task failure.
Record evidence collection style without mandating one tool call or shell recipe.
One sample and shared host/cache do not establish causal or broad performance.
