---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

For a current bug, start with the affected code and project's documented test command; inspect history only if the required behavior or before implementation is unresolved. Choose one stable assertion on the actual affected path, preferably its existing regression test. Reuse established before evidence. Otherwise observe the assertion fail for the reported defect, implement the requested fix, and rerun the unchanged assertion and inputs. Preserve relevant neighboring behavior and required project checks.

For an already-present fix requiring historical comparison, use the [isolated comparison procedure](references/existing-fix.md). Don't reverse patches in the user's working tree.

After the edit, collect the regression, required checks and focused diff in one execution step when no intermediate result changes what should run next. Preserve each command's own output and exit status, not just the last command's success. A failed check needs diagnosis, not another identical run without a relevant change. Dependency/compiler failures aren't defect reproduction; mocks don't prove unobserved effects. Preserve user changes and scope; verification alone authorizes neither implementation nor publication.

Deliver the changed behavior, decisive before/after command and revision/diff evidence, and actual limits. Reuse the regression as the receipt; no separate dossier or unrelated green checks. Stop when the requested outcome is verified, not when every possible check has run.
