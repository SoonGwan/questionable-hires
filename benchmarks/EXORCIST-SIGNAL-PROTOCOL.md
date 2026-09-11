# Conditional containment: lost and retained synchronous signals

Two new cases differ only in clear/notify order. Same neutral request and documented
immediate callback contract. Author test runs actual worker code: lost signal emits
callback completion then reaches a one-second child-process timeout; retained signal
emits callback completion and done. No author oracle is installed for model sessions.

Freeze this commit, candidate ca2e179 and runner fd8d578. Astra medium baseline/skill,
one repeat, serial, seed 20260911, 240-second limit, no retries/exclusions. Preserve
original outputs, candidate resource identities and every outcome. No skill changes
during model execution. Required JSON artifact is part of both neutral requests.

Assess actual observations, explanation of signal state, retained evidence and
production uncertainty. Record helper choice, existing process deadlines and
console duplication separately. Do not mark a normal bounded probe incorrect just
because it has a deadline: this is a routing-efficiency observation, not a ban on
defensive timeouts. The lost-signal probe must have process containment; daemonizing
a hanging thread alone does not provide a complete process deadline.

Report input-plus-output tokens (cached input already included) and process wall
time. Two one-repeat cases on shared host/cache do not prove broad or causal gains.
Do not rerun exposed cases just to obtain favorable samples.
