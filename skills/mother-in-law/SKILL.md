---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

Read the applicable requirements, interaction code, and test entrypoint once.
Use controlled responses/clocks, isolated cases, bounded waits, and owned-operation
cleanup—never sleeps or production actions. Preserve user files and scope.

For a UI-less Python component with a zero-argument constructor, an async
`run(query, fetch)` method and state storing the fetched payload directly, use
`scripts/sequence_probe.py`. Existing adequate project runners and instructions
take precedence; use project-specific checks for other contracts, not source
changes to fit this helper. Run directly without reading or duplicating it:

```sh
python3 -B SCRIPT --root . --source FILE --class-name CLASS [--boundary QUERY]
```

Defaults: method `run`, state `result`, queries `old`/`new`, timeout 5. Exit 1
means a checked behavior failed, 0 means the targeted checks passed, and 2 warrants inspection.
Pass `--error-state ATTRIBUTE` for JSON-serializable error state where falsy means
clear and truthy means displayed. This checks errors on success, current failure,
recovery and stale failure. Failure output retains the failing checkpoint.
If retained evidence is requested, use `--output NEW.json` for the same execution's
JSON. Existing files are refused. Missing console output requires inspecting that
file or marking verification incomplete; final prose is not execution evidence.
The timeout bounds cooperative async waits, not blocking imports or callbacks.

For a rendered UI, read [references/browser.md](references/browser.md).

Return the tested sequence, expected/observed state, tested layer, and complete
bounded command. Stop after the nearest normal and targeted adversarial cases.
Do not add separate evidence files when captured check output already proves them.
Browser unavailability leaves browser QA incomplete. QA does not authorize a fix.
