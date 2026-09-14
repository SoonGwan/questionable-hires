# URL-auth history: direct instruction transfer — 2026-09-15

Freeze before model calls. Original Necromancer: `488515f`; candidate: `f1c30e3`.
Only `SKILL.md` differs (+224 bytes preserving extracted Python compiler context).
No no-skill arm: this directly compares two skill revisions, not skill superiority.
New authored ticket on the same real HTTPX checkout, not the exposed redirect task.
Source `26d48e0634e6ee9cdc0533996db289ce4b430177`, 125 files, full 1,499-ancestor
history. Earlier source/experiments remain unchanged.

## Exact shared task

Substitute the same existing interpreter for `<PREINSTALLED_PYTHON>` in both cells.

> Review the proposal to remove URL-userinfo authentication fallback from
> BaseClient._build_request_auth: delete the username/password assignment and its
> following if block, leaving the explicit/client authentication selection and
> final return Auth() unchanged. Is this a behavior-preserving removal of obsolete
> compatibility code? Establish current necessity and locally evidenced history.
>
> Compare current and proposed behavior through an actual Client with MockTransport
> and trust_env=False. Record the outgoing Authorization header for each of these
> five cases, using only these synthetic credentials:
> (1) https://url-user:url-pass@example.invalid/path, no client/request auth;
> (2) that URL with client auth=("client-user", "client-pass"), request auth omitted;
> (3) that URL/client with request auth=("request-user", "request-pass");
> (4) that URL/client with request auth=None explicitly;
> (5) https://example.invalid/path with that client auth and request auth=None.
> Explain the differences between omitted auth and explicit None; do not infer
> server-side acceptance from locally observed headers. Do not use real credentials.
>
> Inspect the relevant local history and an earlier implementation. Distinguish
> code movement/line attribution from behavioral introduction, and support any
> claimed earlier presence with actual ancestor code. First-ever origin or intent
> is not required and must not be invented. Use only ancestors of pinned HEAD,
> not later branch tips or external issue pages. Recommend retain, simplify or
> remove based on the supported behavior you observed, with current and historical
> evidence. This is a compatibility review, not an authorization to change policy.
>
> Preserve original project files and installed resources. No network, dependency
> installs, fetching, commits or publishing. In-memory substitutions or owned
> disposable copies are permitted; do not force a particular technique. Use
> <PREINSTALLED_PYTHON> with -B; pytest additionally with -p no:cacheprovider. Any
> scratch must stay inside the project and be removed before finishing. Captured
> output is sufficient; do not create a separate report/harness unless needed.

## Preflight and frozen criteria

[Author preflight](httpx-auth-history-01-preflight.json), generated with
`preflight_httpx_auth_history.py`: an existing native test passes, ten current/
proposed observations match expected headers, and an actual contradictory
assertion reports missing versus expected URL-derived auth. The mutation removes
exactly the two proposed statements and preserves compiler flags/annotations.
Both URL-only and explicit-None-with-URL behavior change; explicit client/request
credentials and the no-userinfo control are preserved. Earlier client middleware
code demonstrates the fallback predates a later move. All 125 files stay unchanged;
no bytecode or scratch remains. Preflight code/results are not model inputs.

All five cases and history obligations are model-visible. Score actual current/
proposed Client observations, independent precedence interpretation, supported
history, scope and evidence. Alternative correct probe techniques are valid;
do not require extraction or use of any helper. A compilation failure is retained
in costs, not a scored application defect. Distinguish original evidence from
author checks; do not repair missing model output through author replay.

## Fixed execution

Two fresh serial GPT-6 Astra / medium sessions, **candidate then original**, one
per condition, 360 seconds each, persisted original sessions. Full source copies,
no global installation. Snapshot all four skill resources at their exact revisions
and verify only the entry differs. Store manifests before execution. No favorable
retries/exclusions or model substitution; stop on an actual account limit.

Compare whole input (cache included) plus output tokens, wall time, required work
and original setup failures. The instruction is unproven until actual behavior
is reviewed; fewer setup failures alone does not establish lower overall cost.
Shared host/cache, fixed order and n=1 prevent causal/general claims. Keep adverse
outcomes and previous benchmarks; no featured promotion from this pair.
