# Existing upload suite: adverse transfer evidence

One preregistered authored development case in `hostage-transfer-cases.json`
at `04029fc`, baseline then skill, one execution each, serial GPT-6 Astra medium.
Skill instructions are from `6bd153a`. This is not held-out or broad evidence.
Logs remain under ignored `local-runs/hostage-transfer-01`.

| Arm | Total tokens, input including cache + output | Seconds |
| --- | ---: | ---: |
| baseline | 98,573 | 49.588 |
| skill | 105,630 | 67.677 |

The skill used 7.2% more tokens and 36.5% more wall time in this single pair.
Both produced identical production fixes, retained the original test methods,
preserved requirements/branding, and extended unittest with controlled overlap
and cancellation/retry tests. Neither recorded commands outside the project.
The skill reused one controlled client, while baseline wrapped the existing
client in each new test. Baseline ran the final suite twice; skill once, but
skill used more separate discovery/read commands. No overall efficiency win.

Author checks: the original fixture has one real pending-reset assertion
failure and one passing test. Independent replay of both finished projects
passed four tests each. Additional isolated mutation, using the repository's
audit helper with verified copied imports, removed only the duplicate guard:

- Baseline: correct suite passes; mutant completes with a test-local
  `asyncio.TimeoutError` at its bounded duplicate send.
- Skill: correct suite passes; mutant blocks at its duplicate send until the
  audit's three-second process timeout kills it. This is incomplete diagnostic
  evidence, not a clean assertion failure or proof of robust regression tests.

The originals were preserved by the isolated audit. The follow-up skill change
requires behavior-dependent async waits to be bounded and controlled tasks
released/cancelled in cleanup. That instruction is not yet model-validated.
Existing-suite reuse and bounded discovery occurred here, but a single sample
does not establish that the preceding instruction changes caused either.
