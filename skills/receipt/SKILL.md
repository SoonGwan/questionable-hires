---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

Use the project's documented runtime/test command and one stable assertion on the actual affected path, preferably its existing regression test. Reuse established before evidence. Otherwise observe the assertion fail for the reported defect, implement the requested fix, and rerun the unchanged assertion and inputs. Preserve relevant neighboring behavior and required project checks.

For an already-present fix requiring historical comparison, use the [isolated comparison procedure](references/existing-fix.md). Don't reverse patches in the user's working tree.

Record each command's own exit status. Dependency/compiler failures aren't defect reproduction; mocks don't prove unobserved effects. Preserve user changes and scope; verification alone authorizes neither implementation nor publication.

Deliver the changed behavior, decisive before/after command and revision/diff evidence, and actual limits. Reuse the regression as the receipt; no separate dossier or unrelated green checks. Stop when the requested outcome is verified, not when every possible check has run.
