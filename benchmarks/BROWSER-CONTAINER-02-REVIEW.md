# Container browser model review 02

Reviewed 2026-09-12 KST. These are local candidate-development results, not
published superiority evidence.

## Exclusion before comparison

`browser-container-paired-01` is invalid and excluded. Colima mounted the macOS
temporary workspaces as empty directories; both agents reported `/work` empty and
performed no browser QA. Commit `baf71d4` moved container workspaces below the
repository's ignored `benchmarks/local-runs` tree and added a pre-model fixture
check. The runner tests reject missing or symlinked auth files and verify workspace
translation.

## Valid paired run

`browser-container-paired-02` used revision `baf71d4`, Codex CLI 0.153.4, GPT-6
Astra medium, Node 24.20.0, the pinned Playwright image, independent fresh
workspaces and sessions, and one baseline then one skill arm.

| Measure | Baseline | Skill | Skill change |
|---|---:|---:|---:|
| Observed target defects | 2/3 | 3/3 | +1 defect |
| Elapsed seconds | 145.482 | 118.339 | -18.7% |
| Input tokens | 119,815 | 142,907 | +19.3% |
| Output tokens | 4,038 | 3,179 | -21.3% |

Both cells completed without timeout, retained unchanged dependency inventories,
and reported no error events or invalid JSONL. Baseline reproduced stale success
after newer success and stale success after clear, but omitted stale failure after
newer success. The skill reproduced all three with trusted browser input and
rendered evidence. It retained three files rather than baseline's report, runner,
JSON, and ten screenshots.

The result supports improved defect coverage, elapsed time, and output efficiency.
It does not support lower total input usage.

## Focused token iteration

Revision `dbb473b` instructed the agent to keep full evidence in files and print
only compact statuses. In `browser-container-skill-03`, command-output capture for
the post-run evidence check fell from 2,431 characters to 45. The session still
used 160,520 input tokens, 3,726 output tokens, and 139.807 seconds while retaining
3/3 defect coverage. This misses the paired baseline's input target and shows that
one-session token movement cannot be attributed to echoed evidence alone.

## Decision

Keep the coverage fix and compact-output instruction. Do not claim an input-token
win or tune further from one stochastic sample. The next evaluation should use a
preregistered set of at most ten small interaction tasks, repeated enough to show
task-level variation, and report quality outcomes beside resources rather than
optimizing tokens at the expense of defect coverage.
