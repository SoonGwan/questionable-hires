# Auth design transfer: justified recommendation, no efficiency win

Snapshot/protocol 98a9c79, Landlord entrypoint 925758f, HTTPX pinned at
26d48e0634e6ee9cdc0533996db289ce4b430177. One new task, Astra medium, serial skill
then baseline, one repeat, seed 20260912, 360-second deadline. Four selected preflight
nodes produce six passing parametrized tests. Existing preinstalled interpreter;
no new dependencies. No retries, exclusions or skill edits during the model runs.
Private originals: `local-runs/httpx-auth-design-01/`.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| baseline | 145,788 | 67.868 | 6 |
| skill | 157,215 | 85.430 | 8 |

Skill costs **7.8% more tokens / 25.9% more time**. Cached input is already included.
Single shared-host samples and unequal verification preclude causal/general claims.

Both recommend retaining the three entrypoints based on real client dispatch,
multi-request response feedback, sync/async body loading, specialized I/O/lock
overrides and documented extension contracts. Both recognize FunctionAuth as the
existing simple-callback option and explain why it does not replace Digest flows.
Skill additionally grounds maintenance cost in a concrete token-cache/lock change.

Baseline runs both auth test files: 88 pass in 0.20 seconds. Skill constructs a
selection from client auth tests: 11 pass, 69 deselected in 0.07 seconds. Both
recognize that buffered mock responses obscure streaming-body responsibilities
and construct in-memory actual-adapter probes. Skill captures positive sync/async
streamed request/response checks and four adapter-bypass failures (RequestNotRead
and ResponseNotRead). Baseline's positive probe command exits 0 but its original
captured output is empty despite a print in the command. Its claimed probe result
therefore lacks a captured output chain; no author replay is credited.

Skill rereads tests/client/test_auth.py lines 690–780 after having read 620–805,
and lists test names before selecting the 11 tests. That command also reads model
body-loading implementations and checks repository status: not all of its work is
test-selection overhead. The 0.13-second pytest difference does not establish
whole-session savings. This is a concrete reason to reconsider over-selecting
already-cheap relevant test groups, not to run unrelated broad suites or discard
the decision-changing streaming probe.

All 125 original files per arm match the pinned checkout; both skill resource
hashes match the frozen commit and installed before/after manifests. No original
edits, captured out-of-scope commands or rejected patches. No malformed JSON/event
errors; baseline has the one missing probe-output flag described above. Example
URLs are locally constructed Requests/Responses, not network calls. Passing current
tests does not establish every supported Python/runtime combination.

All 157 repository tests pass (17.999 seconds), including isolated new-profile
scheduling; repository validation passes. After evaluation, a new Landlord candidate
adds cost-aware selection: use a known lightweight relevant group when execution
is needed, narrowing for meaningful runtime/setup/side-effect/isolation reasons.
Distinct evidence remains required. That edit is unmeasured; this report describes
925758f, not the subsequent candidate. Do not rerun this exposed task to chase wins.
