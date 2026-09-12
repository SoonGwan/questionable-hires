# Browser model screen: launch blocked in both arms

[Protocol](BROWSER-MODEL-01-PROTOCOL.md), runner revision `a1f2af4`.
Both scheduled model sessions completed, but neither reached browser interaction.
Original private evidence is in `benchmarks/local-runs/browser-model-01/`.
No outer-session retries, exclusions, installs or permission changes were made.

| Arm | Input + output tokens | Model-process seconds | Browser behavior |
| --- | ---: | ---: | --- |
| Baseline | 160,692 | 153.349 | Unverified: Chrome launch aborted |
| Skill | 215,600 | 150.966 | Unverified: Chrome launch aborted |

Skill used **34.17% more tokens / 1.55% less time**. Cached input is already
included; reasoning output is not added again. Unequal fallback work and repeated
launch failures make this unsuitable as an interaction-efficiency comparison.
Both launches report SIGABRT and cleanup EPERM. This differs from author-side
launch success, but does not by itself identify the precise sandbox/OS cause.
Do not relax permissions or claim that source inspection proves browser behavior.

Baseline attempted its browser harness twice. It retained six unexecuted checks,
launch diagnostics and syntax validation, then explicitly reported QA blocked.
Its `ls /Applications` command exceeded the project-only discovery scope. Listing
an installed Chrome executable's containing directory was not necessary authority
to enumerate unrelated applications. Retain this scope exception and all costs.

Skill authored browser tests with per-test launch, so the same environment failure
recurs across checks. It then extracted the actual script into a Node VM using
fake DOM fields and untrusted synthetic events: two ordered controls pass and two
reversed-response assertions fail, including query clearing. This is observed
handler behavior, **not rendered output, focus or browser input evidence**. Its
source, test comments and final answer make this distinction explicitly.

Both preserve index.html, README.md and .gitignore byte-for-byte. Copied dependency
inventories match before and after each session. Local evidence retains those
dependencies and licenses; logs include private paths and are not public exports.
Model completion is not QA completion; no browser success percentage is assigned.

## Next decision

The available author launch is not a substitute for a permitted fresh-session
browser runtime. Investigate the environment with read-only diagnostics before
another model run. Separately, repeated identical launch attempts within a suite
are concrete avoidable work: a shared browser preflight can report unavailable
once and leave dependent cases explicitly unrun. That is a candidate improvement,
not an implemented or measured performance result. Preserve independent tests
when a failure could be test-specific rather than a shared launch prerequisite.
