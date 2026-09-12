# Con Artist gets a reusable Python audit tool

The character, tagline and audit contract remain unchanged. This iteration moves recurring copy/mutate/run/import-check mechanics into `skills/con-artist/scripts/audit.py`, with an optional routed reference. Other languages and unsupported layouts retain the existing workflow. The helper is not a sandbox or an automatic semantic grader.

Twelve local helper tests exercise surviving/killed mutations, the same stronger check on correct/faulty code, invalid baseline/proposal, external imports, syntax failure classification, exact replacement validation, unsafe paths/symlinks, timeout cleanup, fresh filesystem per check, stdin recipes and malformed recipe types. Bundle tests verify script/reference contents ship with the skill.

## Actual agent checks

Two fresh Astra-medium sessions, one unchanged `persistence-test` case each, serial, no retries. Both used the helper, demonstrated the original test surviving a missing append, and showed a stronger stored-contents assertion pass correct code/fail the mutant. Both final diffs are empty and the actual command traces were reviewed.

| Candidate | Total tokens | Seconds | Observed orchestration |
| --- | ---: | ---: | --- |
| `1c4c41a`, local `con-artist-tool-01` | 91,086 | 40.353 | Reads helper source; writes temporary recipe through a Python wrapper |
| `8c56744`, local `con-artist-tool-02` | 86,935 | 36.547 | Calls helper directly with stdin JSON; no temporary recipe/wrapper or source read |

The second candidate adds stdin support and a smaller CLI-focused reference in response to the first trace. Input includes cached input once; totals add output. Both adverse and favorable observations remain retained under ignored `local-runs/`.

This is not a proven token win. The prior no-helper sample at `b7a768d` used 67,931 tokens and 39.295 seconds; the recent paired baseline used 80,188 tokens and 44.416 seconds. Tool adoption reduced generated output in these samples but increased total context cost relative to both, while the second sample's wall time was lower. Temporal/cache variation prevents causal speedup claims. A reusable mechanism is implemented and behaviorally checked, but its value on larger/repeated audits still needs evaluation.

The helper intentionally reports observations rather than declaring every nonzero mutant exit a kill. Correct-code failures stop it; selected inputs are integrity-checked without restoration, and only generated scratch copies are cleaned up. Full logs can be truncated with explicit flags. Arbitrary trusted tests can still perform outside side effects; callers must preserve the user's scope. Do not claim this implements security isolation or protects unselected originals.
