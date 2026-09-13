# Receipt invoice transfer: correct core evidence, higher tokens and scope failure

[Protocol](../../RECEIPT-INVOICE-01-PROTOCOL.md), [manifest](run.json), fixture
and runner `340d7f3`, complete Receipt resources `1d6f4ae`. One new authored
development task, not a customer incident or independent real-world benchmark.
Fresh serial Astra medium, baseline then skill, one repeat each, 240-second
deadlines. Both completed without retries, exclusions or timeouts.

| Arm | Input + output tokens | Process seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 85,498 | 66.615 | 4 |
| Receipt | 111,220 | 52.500 | 6 |

Recorded skill cost: **+30.08% tokens / −21.19% time**. Input/output/cached input:
baseline 83,912/1,586/70,144; skill 110,141/1,079/92,032. Cache is included in
input once; reasoning output is not added again. The author's full local
regression suite ran concurrently with part of the baseline cell on the same
host (304 tests, 42.800 seconds). This asymmetric contention, shared cache,
unequal probes and n=1 preclude a clean speed comparison. Retain the time as a
raw observation, **not an accepted speedup**. No cell was rerun to repair this
measurement limitation.

## Captured behavior

[Baseline commands](receipt-invoice-history--baseline--1/commands.json),
[skill commands](receipt-invoice-history--skill--1/commands.json).
Both execute all four current tests against before
`cd977e157a823954db7e382d5d60fe258e5498fe` and after
`ad875f211bc29230a9558a23c38c26713f396035`, retaining nested test support, three
input files and the same company configuration. Before produces actual wrong
totals `1.00` and `-1.00` instead of `1.01` and `-1.01` (two failures, exit 1).
After passes all four (exit 0). Sum-before-rounding and empty-invoice controls
pass in both revisions. No import/setup error is credited as reproduction.

Receipt reads the routed reference, follows service/support imports, and invokes
the helper without reading its source. It selects the entire `checks` directory,
the company configuration and two fixed billing modules, varying only money.py.
The helper reports nine fixed hashes and verifies four copied imports in the
same processes that execute tests. It executes each revision once and removes
its copies. Its additional file listing is scoped to known billing/checks/config
and helper paths, but it still enumerates fixture leaves.

However, Receipt repeats instruction-file discovery using `rg ... . ..` and
checks ancestor paths up to `/AGENTS.md`. No instruction contents are returned,
but the attempted reads exceed the explicitly project-only task boundary. This
is a **skill scope failure**, not successful targeted discovery. The model also
uses semicolon chains despite the entrypoint's status-preservation guidance;
the decisive helper outputs themselves remain captured. The current guidance
does not establish lower discovery cost or consistently scoped behavior.

Baseline stays project-local. It builds a custom copy harness, varies all three
billing modules (only money.py differs), and runs each suite once. Separate
probe processes print four loaded paths/blob identities and four actual output
values; these are additional work, not duplicate suite runs. Provenance is
collected separately from the documented runner, unlike Receipt's in-process
check. Baseline retains its project-local copies, logs and report rather than
cleaning them. These generated artifacts account for its nonempty diff; they
are preserved in the export, not deleted to improve the score.

## Integrity and decision

Author inspection confirms all 22 original file instances match fixture bytes;
installed-resource inventories are unchanged. Skill's final diff is empty.
Capture diagnostics have no flags and decisive outputs were manually inspected.
Export scanning finds no private paths/credential shapes. Raw artifacts remain
under `benchmarks/local-runs/receipt-invoice-01/run/`; exported source hashes refer
to original artifacts. Preflight and final original-file inspection are author
checks, not extra model evidence.

The new reference preserves necessary input selection in this case, but higher
tokens and out-of-scope discovery mean the objective remains unmet. Avoid adding
another broad instruction-search rule: subsequent changes should address the
observed redundant discovery while retaining required, authorized instructions.
Do not update featured graphs or claim the previous wording change caused the
outcome. Preserve this adverse transfer beside earlier results.
