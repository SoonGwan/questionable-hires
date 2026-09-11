# Cancellation waits are not process deadlines

Screen 06's actual `probe_search.py` contains asyncio wait timeouts, including
cleanup, but no hard process deadline. The previous entrypoint advised avoiding
wrappers when waits were already bounded. That phrasing could obscure the fact
that a timed-out asyncio wait still waits for cancellation completion.

Candidate `4df3eff` distinguishes these mechanisms and retains conditional use:
if the exercised task can suppress cancellation, use the existing process runner
unless another process deadline already contains it. No helper changes, mandatory
wrapper for every experiment, or claim of faster ordinary execution.

Added a behavioral regression with a 0.02-second asyncio wait and a task that
suppresses cancellation. The existing 0.3-second process runner terminates it,
records timeout and actual exit -9, and captures suppression output.

Separately, author replay used the exact retained screen-06 probe: normal execution
through the existing wrapper passed in 0.049 seconds. A child-local replacement of
`Search.run` that never dispatches and suppresses cancellation left the same probe
waiting; the 1.5-second process deadline killed it in 1.507 seconds, exit -9,
with suppression output captured. No retained production file was edited. This
author experiment validates the diagnosed containment gap and helper behavior,
not model adoption or a change to the original benchmark's execution.

Nine process-runner tests and the full 134-test suite pass (13.107 seconds for
the latter). Skill/repository validators pass. The current entrypoint postdates
screen 06 and has not had a model check. This is a bounded-failure correction;
it does not satisfy the user's broader performance objective by itself.
