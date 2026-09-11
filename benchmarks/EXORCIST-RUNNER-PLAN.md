# Select the execution path before its setup

Prior HTTPX diagnosis traces read pytest fixtures/configuration but then execute
standalone probes. Revise Exorcist to choose its execution path first and inspect
setup only when execution or the reported symptom makes it relevant. Preserve
the ability to investigate fixture/environment causes and upstream ambiguity.

Before model execution: one changed-skill sample on the unchanged HTTPX redirect
task, then one changed-skill sample on `exorcist-runtime-cases.json`. Two tasks,
two executions, Astra medium, serial; no full repeated matrix. The second task
is an author-designed regression control, not held-out or real incident evidence.
It deliberately requires fixture inspection: module configuration initializes
before unittest setUp, unlike an environment set before a fresh-process import.
Its criteria are frozen in the case file; use local subprocess checks to verify
that the fixture itself distinguishes these states before model execution.

Compare HTTPX cost to all retained earlier samples, not only the most favorable
baseline. No paired cost claim for the new control without a baseline. Inspect
actual executions, original-file integrity and scope. Lower cost only counts
with the required original behavior/control checks preserved; do not reward
skipping fixture setup in the new control. If this routing fails or costs more,
retain the evidence rather than adding new mandatory checklists.
