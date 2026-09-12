# Real transport design review: no efficiency advantage

One task, one skill and one baseline execution, serial Astra medium; skill first
under the fixed schedule. Landlord frozen at `cb43845`, HTTPX at
`26d48e0634e6ee9cdc0533996db289ce4b430177`. No retry or excluded result.
The separate Python 3.9 environment uses `httpx-design-requirements.txt`; its
additional chardet 5.2.0 pin comes from upstream requirements. Existing audit
environment is unchanged. Both lifecycle preflight tests pass.

| Arm | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| skill | 194,663 | 86.177 |
| baseline | 148,202 | 85.133 |

Skill costs 31.3% more tokens and 1.2% more time in this single pair. Shared
host/cache and differing test selections prevent a causal generalization.
The synthetic Landlord improvement does not transfer to an efficiency win here.

Both reviews preserve the sync/async lifecycle and extension contracts, request
body buffering, result-based handler dispatch and Python support constraints.
Both identify the stale base-class example: tuple URLs fail and response streams
have no `.read()` method. Both demonstrate those issues and three async handler
forms through local probes. Skill executes 15 focused tests; baseline 19. Those
counts reflect different selections, not a proportional quality score. Neither
edits source or proposes removing necessary runtime contracts.

Provenance audit confirms all 125 original files, source revision, both frozen
Landlord resources and installed resource copies. Traces and findings were
reviewed; no independent replay of every probe was performed for this report.
MockTransport probes do not contact example.org despite URLs in test inputs.

Scope limitation: baseline searches its temporary project's parent directory
for AGENTS.md, outside the explicit boundary. The skill's recorded searches
remain in-project, but it guesses nonexistent `tests/transports/test_mock.py`
and `tests/test_dispatch.py`, including repeating the latter after a failed
read. This wastes exploration and is a concrete next correction candidate.
Some combined commands mask a missing-file exit; subsequent output was reviewed
instead of treating shell completion as proof of every read/check.

Local evidence: ignored `local-runs/httpx-design-01`, including dependencies,
full snapshots and traces. This is a real-repository development task, not
held-out confirmation. No task success or resource metric alone establishes
overall superiority. Preserve HTTPX licensing if exporting source artifacts.
