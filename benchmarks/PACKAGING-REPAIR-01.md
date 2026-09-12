# Real packaging repair: favorable single pair, unequal coverage

Protocol/resources frozen at `64b1774`; actual project source export `a701093`.
One fresh baseline then Hostage Negotiator session, Astra medium, serial,
seed 20260911, 240-second timeout. No retries or exclusions. Original artifacts:
`local-runs/packaging-repair-01/`. Candidate entrypoint remains `6c5e452`.

| Arm | Input + output tokens | Wall seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 109,315 | 89.315 | 7 |
| Skill | 96,434 | 83.390 | 8 |

Skill uses 11.78% fewer tokens and 6.63% less time in this pair. Input/output:
106,976/2,339 versus 94,173/2,261. Cached input 90,496/77,824 is included once;
reasoning output is not added again. More shell calls did not imply more tokens.
This is not a causal improvement estimate or whole-bundle acceptance.

Both wrap only work after exclusive destination creation in cleanup handling,
remove the owned partial directory and re-raise the original failure even if
cleanup fails. Existing destinations fail before cleanup. Successful build path,
return value and CLI source remain compatible. Both retain the original two tests
unchanged by AST comparison and finish with six passing tests in captured output.
Neither initial failing test run is defect-before evidence: both already patched
production code and then repaired macOS canonical-path assumptions in new tests.

Coverage differs. Baseline checks early and final-copy failure, retry, error
identity, cleanup failure, existing directory/file/symlink preservation, plus
actual CLI success and refusal. Skill exercises OSError, RuntimeError and
KeyboardInterrupt across two copy operations, an additional final catalog failure,
retry, cleanup failure and existing directory/file preservation. It does not add
the baseline's CLI/symlink checks. Both cover the original bundle resources and
bundled Receipt execution through existing tests. No arbitrary concurrent-path
replacement or guaranteed recovery from filesystem cleanup failure is proven.

Each retained project changes only scripts/build.py and tests/test_build.py;
the other 32 supplied files are byte-identical. Both installed Hostage resources
match frozen Git SHA-256 and before/after manifests. Skill has one empty-output
diagnostic: an AGENTS search exits 1 and its chained status command is unrun.
This is not a missing test receipt; final suite output is present. Preserve the
failed discovery call rather than hiding it. No author replay is credited as model
execution, and neither generated implementation has been merged into main source.

The newly authorized self-selected target supplies useful real repository work.
Keep this favorable result alongside adverse Hostage tasks; do not repeat it for a
better score. Both arms' path-assertion repair is a concrete workflow issue to
investigate, not justification for adding a benchmark-specific answer to the skill.

Subsequent implementation note: `436e409` independently integrates the repair
and focused regression tests into the repository. Later commits add source-link
rejection. These author changes do not alter the frozen model artifacts or count
as work performed by either measured session. A [worked follow-up](../examples/packaging-repair.md)
distinguishes the old task from checking today's already-fixed source.
