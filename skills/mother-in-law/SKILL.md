---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

Read the applicable requirements, interaction code, and test entrypoint once.
Use controlled responses/clocks, isolated cases, bounded waits, and owned-operation
cleanup—never sleeps or production actions. Preserve user files and scope.

For a UI-less Python component shaped like `async run(query, fetch)`, use
`scripts/sequence_probe.py` unless project rules require another retained-test
layout. Run it directly without reading its source or duplicating its output:

```sh
python3 -B SCRIPT --root . --source FILE --class-name CLASS [--boundary QUERY]
```

Defaults: method `run`, state `result`, queries `old`/`new`, timeout 5. Exit 1
reproduces stale state, 0 means the targeted guard held, and 2 warrants inspection.
Pass `--error-state ATTRIBUTE` only when the component exposes error state; this
adds older-error-after-newer-success without another harness.
Existing adequate project runners and instructions take precedence.

For a rendered UI, read [references/browser.md](references/browser.md).

Return the tested sequence, expected/observed state, tested layer, and complete
bounded command. Stop after the nearest normal and targeted adversarial cases.
Do not add separate evidence files when captured check output already proves them.
Browser unavailability leaves browser QA incomplete. QA does not authorize a fix.
