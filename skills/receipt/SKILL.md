---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

Reuse applicable instructions already supplied. Discover missing project guidance only within authorized roots; a project-only request does not authorize parent-directory searches or an ancestor-file sweep. If required evidence lies outside scope, report the gap rather than broadening access.

For a current bug, use the affected code and documented runner to select a stable regression on the actual path. Reuse valid before evidence; otherwise observe its defect-specific failure, implement the requested fix, then rerun unchanged assertions/inputs. Inspect history only for unresolved behavior or implementation. Preserve neighboring behavior and required checks.

For an already-present fix requiring historical comparison, use the [isolated comparison procedure](references/existing-fix.md). Don't reverse patches in the user's working tree.

A required suite executing the unchanged regression with matching inputs/runtime supplies the after evidence: don't also run it separately. Skipped, undiscovered or differently configured tests don't qualify. Retain distinct required coverage. Reuse results only while their relevant inputs remain unchanged.

After edits, collect independent final checks in one shell call. Adapt this fail-fast example to the actual runner and touched files:

```sh
python3 -B -m unittest -v && git diff --check -- app.py test_app.py && git diff -- app.py test_app.py
```

With `&&`, failure leaves later checks unrun; if all must run, retain each exit explicitly. A semicolon chain's final status doesn't establish earlier outcomes. Review new/untracked files separately: `git diff` omits them. Don't rerun checks merely to recover discarded statuses.

Dependency/compiler failures aren't defect reproduction; mocks don't prove unobserved effects. Preserve user changes and scope; verification alone authorizes neither implementation nor publication.

Inspect the focused diff. Deliver changed behavior, decisive before/after observations and commands, historical revision identities when applicable, and actual limits. The regression is the receipt: no separate dossier or unrelated green checks. Stop once the requested outcome and required checks are verified.
