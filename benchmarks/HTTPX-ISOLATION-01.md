# HTTPX isolation routing: one development pair

Con Artist `5c697e5` uses the supplied isolation helper on a real repository task.
This is an adoption observation with favorable single-pair costs, not proof of
equivalent-work speedup or broad skill superiority.

## Setup

- HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, 125 tracked files.
- Existing local Python 3.9.6 environment; preflight: 36 tests passed.
- GPT-6 Astra, medium; one WSGI cleanup audit, baseline and explicit skill,
  one repeat each, serial order skill then baseline. No control or automatic arm.
- Entrypoint `5c697e5`; helper/reference unchanged at `941ea50`.
- Requested outcome: audit existing cleanup-test sensitivity with isolated
  mutations; propose and verify a focused test if coverage is missing; preserve
  original files. No dependency installation.
- Local ignored artifacts: `benchmarks/local-runs/httpx-isolation-01`.

| Arm | Total tokens, cached input included | Process seconds |
| --- | ---: | ---: |
| Baseline | 190,847 | 116.925 |
| Skill | 182,169 | 79.038 |
| Skill relative difference | -4.5% | -32.4% |

## Reviewed behavior

Both find partial, indirect protection: disabling cleanup causes existing tests
to fail through warnings from `wsgiref.validate` iterator finalization. Failure
attribution is garbage-collection-sensitive: baseline sees 2 failures, skill 1.
Neither mistakes that indirect detection for comprehensive coverage.

Skill invokes the existing helper twice instead of writing copy/import/process
bookkeeping. The first fault disables the close callback: correct 12 pass,
faulty 1 fail / 11 pass. The second retrieves `close` from `iter(result)` instead
of the original application iterable: existing tests pass on both variants.
A focused probe retains an iterable owning a `BytesIO`, consumes one chunk,
then checks actual resource closure after stream-context exit. It passes on
correct behavior and fails on the second fault. Six helper checks total.
The model still reads the entire helper source; interface-only consumption is
not established. The probe specification is in the execution trace, not a
retained project report.

Baseline writes its own isolated audit and retained report, logs and patches.
Its second fault suppresses cleanup only before stream exhaustion, which also
survives the existing 12 tests. Two proposed parameterized checks cover explicit
`Response.close()` and context exit, including exactly-once callback behavior.
Both pass on correct behavior and fail on each faulty variant. The original
capture, retained test, report and logs were reviewed; these are not new author
replay results.

These are different faults and different verification/delivery depths. Baseline
does additional proposed-test execution and reporting; skill checks a real
owned resource but only one closing path. Therefore the cost difference cannot
isolate helper savings or establish equal coverage.

## Integrity and limits

Both runs completed without timeout or recorded patch rejection. Post-run
`audit_httpx.py` confirms all 125 original files preserved and the four frozen
skill resources matching; runner before/after resource diagnostics are empty.
Final hashes do not rule out restored transient edits or outside writes.

Baseline's empty-output flag is a successful setup command that copies files and
writes artifacts without printing; it is not missing pytest evidence. Skill has
no capture flags. Clean diagnostics cannot guarantee complete capture generally.

One task and one repeat, shared host/cache, explicit invocation, different fault
selection and no held-out confirmation: retain this as development evidence.
Do not replace the original unfavorable benchmark chart. The all-eight-skills
performance objective remains unmet.
