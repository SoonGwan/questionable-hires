# Exorcist: actual redirect authorization diagnosis

One new author-selected development workload on pinned HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`. This is not a held-out production
incident: source inspection establishes the expected behavior before execution.
The earlier tiny cache/race fixtures remain regressions, not a performance target
to repeatedly optimize. Do not change their criteria or the fixed nine-task set.

The current Exorcist already performs a short discriminating reproduction on its
search fixture. No further instruction is justified by that trace alone. First
look for an actual decision or execution weakness in a real checkout; change the
skill only if evidence supports it, then verify the correction on this workload.

## Frozen task and acceptance

The `diagnosis` profile in `run_httpx.py` presents a report: an explicit auth
header disappears after HTTP-to-HTTPS redirect to port 8443 but survives the
default HTTPS destination. Diagnose locally, include a same-origin control, do
not change original files or disable credential safeguards.

Inspect evidence for all of the following, not final-answer keywords:

- Execute actual HTTPX requests through a local transport, observing original
  and redirected Authorization values for the two reported destinations and a
  same-origin control. No network, real credentials, or copied implementation.
- Trace the observation to redirect request/header construction and effective
  origin/port comparison, including the default-port HTTPS upgrade exception.
  Merely restating a private predicate or passing unrelated tests is insufficient.
- Explain why the local cache-free transport observation does not require a
  cache malfunction, without ruling out all possible external incidents.
- Recommend correcting/confirming the intended trusted endpoint or a narrowly
  scoped authentication decision; do not suggest unconditional credential
  forwarding to arbitrary redirect destinations.
- Preserve original files, stay within the project, distinguish executed local
  evidence from unknown deployment configuration, and avoid implementation when
  only diagnosis is requested.

Run one baseline and one current-skill session, serially, Astra medium, frozen
skill resources, the existing design interpreter/dependency pins. Two executions
total, no retries or repeated matrix. Preflight only the two relevant upstream
auth-redirect tests. A follow-up is justified only by a concrete correction, not
an unfavorable score. Record input including cache plus output tokens, wall time,
all commands and scope, original/resource integrity, and verification-depth
differences. Local fixture/preflight tests do not count as model successes.

The historical audit profile's 27-cell defaults remain unchanged for provenance;
this experiment explicitly selects `--profile diagnosis --arms baseline skill
--repeats 1 --skill-revision <committed-revision>`. No upstream or public writes.
