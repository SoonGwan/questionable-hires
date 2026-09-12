# Fast iteration 02: implementation checks and discovery overhead

Two fresh skill-only sessions at revision `e441eb7`, Astra medium, serial, one sample per case. Evidence remains in ignored `benchmarks/local-runs/fast-implementation-01`. These exposed development checks have no paired baseline and establish neither comparative efficiency nor general reliability.

| Case / skill | Observed behavior | Total tokens | Seconds |
| --- | --- | ---: | ---: |
| boundary-fix / Receipt | Same exact-age assertion fails before the fix and passes after; neighboring ages remain green | 101,791 | 42.947 |
| necessary-state / Hostage Negotiator | Pending state, duplicate suppression, return value, failure propagation, retry and instance isolation checked | 102,148 | 59.569 |

Total tokens are input plus output, with cached input already included. Both processes completed without timeout. Command traces and diffs were inspected, not merely final answers.

Receipt added the regression to the existing unittest file, observed assertion failure with exit 1, changed only the eligibility comparison, then ran the unchanged three-test suite with exit 0. Its separate diff check exited 0.

Hostage Negotiator changed only `form.py`: instance pending state, duplicate guard, and `try/finally` around the existing save. One inline deterministic asyncio check exited 0 and covered the required state transitions. This verifies the synthetic state boundary, not a rendered browser button. Its diff-check command was chained with a diff print, so that process exit alone is not independent proof of diff-check success.

Both sessions first guessed framework/file patterns, then made additional discovery calls. The necessary-state search missed both actual project files. This is a concrete avoidable discovery step, not a demonstrated sole cause of token cost.

Correction across all eight skills: locate relevant files from supplied paths or the actual repository listing before guessing framework-specific paths. Preserve focused inspection; this does not request reading every file. No task criteria changed. The correction remains behaviorally unverified until the next bounded regression screen; do not claim reduced tokens from instruction length alone.
