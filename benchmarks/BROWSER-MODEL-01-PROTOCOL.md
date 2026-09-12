# Browser interaction model screen

Freeze before model execution. One synthetic catalog task, baseline and explicit
Mother-in-law, one fresh session per arm, serial, Astra medium, 240-second outer
deadline. Retain both attempts and all costs, including launch restrictions and
incomplete cleanup. No retries, exclusions or permission relaxation to obtain a
successful result. The model may author local QA code; it may not alter originals.

Task: QA the catalog interaction against its README using actual browser input
and rendered observations. Demonstrate any reproducible failure and nearby normal
behavior, report commands and limits, and retain focused checks under qa/.

Source is `benchmarks/browser/model-project/`. Stage identical copies plus the
already installed `playwright-core` dependency and its license, with file hashes
recorded before either session. Do not provide the author's `input-check.mjs`,
existing review reports, model answers or expected assertion outputs. No other
project or host profile is in scope. Chrome and Node are execution dependencies;
their availability does not authorize external browsing.

Review actual browser launch, trusted input, normal and overlapping completion
observations, empty-query behavior, error/retry coverage, retained originals and
deadline/cleanup evidence. Missing or unexecuted behavior remains unknown. Compare
total input-plus-output tokens and full model-process wall time with differences
in coverage disclosed. One synthetic pair cannot establish broad superiority.

Author preflight is separate from sandboxed model execution. A sandbox launch
failure must be retained and investigated without silently changing permissions.
The model runner and dependency manifest must be in place before launching this
screen; this protocol alone is not evidence of any completed model session.

Runner: `python3 benchmarks/run_browser_model.py --output benchmarks/local-runs/browser-model-01`.
Order is fixed baseline then skill. `--stage-only` verifies local copying without
model usage; it creates a new output and cannot be resumed as a model run.
Local snapshots retain dependencies and licenses; they are not intended as a
public export. The manifest records their bytes/modes and checks them after each
session. No dependency files are silently excluded from local evidence.

Runner status follow-up: CLI 1 now reports an incomplete model session, an
account-limit stop, or changed dependency inventory. CLI 0 means scheduled model
sessions completed with unchanged dependencies (or successful stage-only work),
**not** that browser QA passed. A model can complete honestly while reporting
browser launch blocked, as both original screen sessions did. Account limits
stop the remaining schedule; other incomplete attempts remain in the full pair.
Offline tests cover these exit/status paths without model calls. This change does
not alter the historical screen's records or score its browser outcomes.
