# HTTPX cookie storage design transfer 01

Prospective, authored real-source transfer task; not an organic ticket or blind
holdout. The author knows the source contract. No performance target is a scoring
rule. Freeze before model execution; retain both scheduled cells, including
failures, missing captures and adverse costs. Do not rerun to seek a preferred score.

- Source: HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, unchanged full checkout.
- Resource: Landlord at `e267919`; runner profile `cookie-design`.
- Astra medium, baseline and skill once each, serial, seeded order from runner;
  360 seconds per cell. Shared host/cache; no causal speedup or generalization claim.
- Exact model-visible task and installed hashes are retained in the run manifest.
- Proposal: replace Cookies/CookieJar with a name-only string dictionary.
  Review only; runtime checks explicitly required for scoped duplicates and a
  single-cookie control. Preserve original files and avoid network/install/edit.

Review evidence separately: source-backed recommendation and actual consumers;
domain/path and duplicate compatibility; executed native checks and normal
control; nearest viable alternative; scope and original-file integrity. Existing
tests or a bounded probe both qualify. Extra work and evidence capture differences
must be disclosed before comparing total input-plus-output tokens and wall time.

Author preflight (not model evidence): imported the pinned checkout with its
preinstalled Python, created three `session` cookies at example.com `/a`, `/b`
and example.org `/a`, values A/B/C. Actual request headers matched `session=A`,
`session=B`, `session=C`; example.net received no cookie. A name-only dictionary
collapsed three records to one: intentional assertion failed with
`actual=1, expected=3`. Single-cookie mapping control passed. No network or source
edits. The runner additionally requires unchanged native cookie tests to pass
before scheduling. The author probe is not placed in model workspaces.

Do not replace landing-page images with this pair alone, or label old benchmarks
with this resource revision. Export complete captures, selected licensed source,
resource provenance and both outcomes before considering any narrower claim.
