# Receipt directory adoption: used, token objective still unmet

[Preregistered protocol](../../RECEIPT-DIRECTORY-MODEL-01-PROTOCOL.md),
[run manifest](run.json). Receipt resources and the unchanged assembly fixture
are frozen at `b6d31ec`; runner revision `b496966`. Fresh serial Astra medium,
baseline then skill, one repeat per arm, 240-second deadlines. Both completed;
no retries, exclusions or timeouts. This is one exposed authored development
case, not an independent real-world validation.

| Arm | Input + output tokens | Process seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 106,379 | 59.370 | 7 |
| Receipt | 109,601 | 40.073 | 5 |

Recorded skill cost: **+3.03% tokens, −32.50% time**. Input/output/cached input:
baseline 104,905/1,474/95,232; skill 108,821/780/85,632. Cached input is already
included once; reasoning output is not added again. Shared host/cache, unequal
work and a single pair prevent a broad or causal efficiency claim. This does
not replace the [earlier adverse assembly pair](../../RECEIPT-ASSEMBLY-01.md).

## Observed behavior, not inferred from answers

[Baseline commands](receipt-assembly-history--baseline--1/commands.json),
[skill commands](receipt-assembly-history--skill--1/commands.json).
Both hold current tests/settings/samples fixed and vary all four assembly
modules between `8049ad168aa16233dbee11dcb04c9f9270551e16` and
`171834cfcdab209e892292434872e617123bc428`. Both reproduce two actual assertion
failures before and two passes after: numeric order changes from
`one|ten|two\n` to `one|two|ten\n`, and empty output changes from `\n` to `''`.
Actual runner and copied-module provenance are present.

Receipt reads the routed reference, invokes the installed helper without
reading its implementation, and selects `fixed: ["test_assembly.py",
"settings.json", "samples"]`. The helper expands all three samples, reports
five fixed-file hashes, and runs each revision's current suite once, with four
imports verified in each process. It also checks final Git status and cleanup.
Directory selection is adopted, but the earlier repository-wide `rg --files`
still enumerates sample leaves: discovery-work reduction is **not** established.

Baseline builds a custom harness. It runs the documented suite and then runs
the same suite again inside a provenance/output probe for each revision. The
probe additionally prints output values, reader ordering, writer constants and
loaded Git blob hashes; a final Git query checks expected blob identities.
Baseline also issues `rg --files -g AGENTS.md ..`, outside the requested project
boundary. It returns no paths, but this remains a scope exception, not a clean
scope pass. Skill commands remain project-local. Unequal probes and that scope
exception must not be converted into an accepted equal-work speedup.

Both final diffs are empty. Author inspection confirms all 20 original file
instances still match fixture bytes; installed-resource inventories are
unchanged. Capture diagnostics report no flags; the decisive command outputs
were manually inspected as well. Pattern scanning of this export finds no
private paths or credential shapes. Original unredacted artifacts remain under
`benchmarks/local-runs/receipt-directory-model-01/run/`; exported source hashes
refer to those originals. Author checks are separate from model execution.

## Decision

Keep directory support: its correctness is author-tested and its use is now
observed in a model session. Do not promote this pair to the featured graph or
claim the all-eight performance objective is met. The remaining issues are
whole-task token cost, redundant discovery, and transfer to independent tasks
with equivalent required coverage. No rerun of this unchanged candidate is
justified merely to seek a better score.
