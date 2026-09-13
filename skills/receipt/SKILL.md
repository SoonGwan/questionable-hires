---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

Reuse applicable instructions already supplied. Discover missing project guidance only within authorized roots; a project-only request does not authorize parent-directory searches or an ancestor-file sweep. If required evidence lies outside scope, report the gap rather than broadening access.

For a current bug, start with the affected code and project's documented test command; inspect history only if the required behavior or before implementation is unresolved. Choose one stable assertion on the actual affected path, preferably its existing regression test. Reuse established before evidence. Otherwise observe the assertion fail for the reported defect, implement the requested fix, and rerun the unchanged assertion and inputs. Preserve relevant neighboring behavior and required project checks.

For an already-present fix requiring historical comparison, use the [isolated comparison procedure](references/existing-fix.md). Don't reverse patches in the user's working tree.

Choose the after check before running it. If a required suite actually executes the unchanged regression with the relevant inputs and runtime, its result is the after evidence; don't also run that regression separately. A skipped, undiscovered or differently configured test does not qualify. Retain required checks with distinct coverage and inspect the focused diff.

Collect final checks together when no intermediate result changes the next action. In a shell supporting `&&`, a fail-fast chain preserves the failing exit; later checks are unrun, not passed. If every check must run, capture each exit explicitly. A semicolon chain's final exit does not establish earlier statuses. Reuse established check results until their relevant inputs change; don't discard a status and rerun just to recover it.

Dependency/compiler failures aren't defect reproduction; mocks don't prove unobserved effects. Preserve user changes and scope; verification alone authorizes neither implementation nor publication.

Deliver the changed behavior, decisive before/after observations with their commands, focused diff and actual limits. Include revision identities for historical comparisons. Reuse the regression as the receipt; no separate dossier or unrelated green checks. Stop when the requested outcome is verified, not when every possible check has run.
