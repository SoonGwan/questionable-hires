# Compressed Con Artist: one real-repository check

One WSGI cleanup audit on the pinned HTTPX checkout, using Con Artist `b7a768d`, runner revision `0fa1486`, Astra medium, serial, 360-second cap. The historical 27-cell comparison remains interrupted; this is a separately recorded single skill-only development check, not its continuation or a baseline comparison.

Preflight: the 36 existing WSGI/ASGI tests passed. The agent completed in 103.956 seconds using 155,133 input-plus-output tokens (cached input already included).

The mutation leaves cleanup working after full consumption but skips the response iterable's close callback on early close. Existing WSGI tests pass on both correct and faulty implementations (12/12 each). The proposed test holds a strong reference to a partially consumed generator, exits the HTTPX streaming response context, and checks its underlying resource is closed without draining the remaining body. It passes correct code and fails the mutant at `resource.closed`, even though `response.is_closed` is true. Holding the generator reference prevents garbage collection from substituting for the missing explicit cleanup.

The author inspected the commands, mutation and proposed test. An independent replay from the retained mutated copy produced 12 passing original tests and one failing proposed test at the same assertion. Correct-code execution was observed in the original trace, not independently replayed here. Import checks resolve to the copied repository. The provenance audit confirms the upstream revision, frozen skill hash, no recorded patch rejection and all 125 original tracked files preserved. The agent's count of 127 includes its two injected skill files.

Local retained evidence: `local-runs/httpx-compressed-01`, including the manifest, commands in `events.jsonl`, final project snapshot and `.cleanup-audit/mutation.diff` plus proposed test. These full-checkout artifacts have not been exported for publication; retain HTTPX's BSD license if subsequently exporting them.

Important scope limitation: an inspection command searched for ancestor `AGENTS.md` files outside the project. No outside write is shown, but this violates a literal project-only read boundary. Therefore this run is behavioral evidence, not an unqualified all-constraints success. Final snapshots also cannot establish absence of all transient changes. The existing skill's narrow fault-selection and effect-level verification transferred to this real codebase, but no general reliability or performance win is established by one run.

The bounded runner now accepts case, arms, repeats and a pinned skill revision; its original defaults retain the historical 27-cell schedule. Three new schedule tests verify a one-cell selection, original matrix membership/determinism and invalid repeats; all 42 local tests pass.
