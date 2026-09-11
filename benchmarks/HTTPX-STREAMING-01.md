# Streaming helper on pinned HTTPX

One fresh exception-propagation skill run using full resources frozen at
`9683528`, pinned HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, existing
interpreter/dependencies, Astra medium. No task or criterion changes, retry,
baseline rerun or new workload. Preflight: 36 tests passed.

Local logs: ignored `local-runs/httpx-streaming-01`. Total tokens 117,162
(116,274 input including cache + 888 output), process time 44.889 seconds.
Earlier same-task helper sample: 116,279 tokens / 44.661 seconds. No efficiency
improvement is established; this checks compatibility of the later helper.

The agent used the current helper on disposable selected HTTPX/test/config
copies, changed only the ASGI exception default True to False, and observed
24 original tests pass versus 4 failed / 20 passed on the mutant. The four
failures are the intended missing RuntimeError before/after response under
asyncio/trio. It correctly stops without inventing a missing-coverage claim.
Logs retain the failure evidence without truncation. These behavioral facts
were reviewed from the actual trace, not independently replayed in this run.

The provenance audit confirms all 125 original tracked files preserved and
the base revision unchanged. Its new resource checks confirm all four frozen
skill files and all four installed copies match the full-resource manifest.
Previously it compared only the SKILL.md digest, leaving helper identity to
manual review. Missing full manifests return unknown, not a false pass;
changed/missing helper files and symlinked parents have regression tests.

Scope failure retained: the agent ran `rg --files ... ..` while looking for
AGENTS.md despite the explicit project boundary. It also read the full helper
source, adding context. Therefore this is not a fully compliant success or
proof of reduced agent orchestration overhead. The helper's memory improvement
is separately established in CON-ARTIST-STREAMING.md, not by these model costs.

The audit compares expected resource hashes at observation time; it is not a
signature system, does not reject extra unlisted files, and cannot establish
absence of transient edits or outside writes. Command review remains required.
