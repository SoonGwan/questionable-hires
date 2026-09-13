# HTTPX decoder audit: frozen external-code transfer

Use the full unmodified HTTPX checkout at
`26d48e0634e6ee9cdc0533996db289ce4b430177` (0.28.1), with its real test support and
configuration. Two new author-selected requests in `run_httpx.py`'s decoder-audit
profile: incomplete UTF-8 finalization and CRLF split across chunks. This is actual
upstream source, not a fabricated implementation; requests and mutations are
author-selected, not independent maintainer tickets. No upstream issue/PR write.

First run the unchanged tests/test_decoders.py using the existing pinned virtual
environment, verify imports originate from the checkout and confirm it is clean.
After freezing requests, use separate disposable full copies for author oracles.
Verify normal and deliberately broken behavior, including a failing assertion
with actual/expected evidence. Keep oracles outside evaluated project contexts.

Then freeze current Con Artist resources at the committed protocol revision.
GPT-6 Astra medium; baseline and skill; one new session per task/arm (four cells),
one job, seed 20260912, 360-second cell deadline. No retry, exclusion or changed
criteria during execution. Account-limit stops leave unattempted cells visible.

Acceptance review: actual implementation used; selected fault reachable and not
equivalent or merely syntactically broken; original suite on correct/faulty code;
if survivor, stronger assertion passes correct and fails faulty for the intended
reason; required normal control observed; detecting assertion identified if killed;
original files preserved and no external writes or dependencies installed. Final
prose alone is insufficient. Record scope, capture and import-provenance limits.

Report all token usage (input including cached input + output) and process wall
times. Equal-case mean skill/baseline ratios are descriptive with n=1. Unequal
mutations, added coverage and isolation work must be disclosed. This cannot prove
all-eight resource savings or replace the frozen featured interaction benchmark.
Do not count an injected mutation as an upstream production defect. Preserve the
HTTPX BSD-3-Clause license in any exported third-party source.
