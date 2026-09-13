# Receipt directory candidate: model adoption check

Freeze the existing assembly fixture and complete Receipt resources at
`b6d31ec4388797534b136a5f25de5d29ae2f211f`. Do not modify the task to mention
directories or the helper. This is an exposed authored development case, not a
fresh independent task. The directory-support implementation changed since the
previous assembly comparison; this run checks current adoption, not a causal
estimate or a retry of an unchanged candidate for better scores.

Generate cases with `receipt_assembly_cases.py`; record its JSON digest in the
runner manifest before execution. Run baseline and skill once each, serially,
using `run.py`, seed 20260911, Astra medium, 240-second cell deadlines. Retain
both scheduled cells, all costs, failures and capture limitations. No retries
or exclusions. Stop after account limits; do not change the frozen inputs.

Before execution, the existing fixture integration tests must reproduce both
original assertion failures and both after passes with identical current fixed
inputs. Author replay is not model evidence.

Review captured commands and outputs for the same criteria as the earlier
assembly protocol: both implementation modules vary; current tests, settings
and samples remain fixed; actual numeric-order and empty-output failures before
and passes after; loaded-copy/revision provenance; originals unchanged and
project-only scope. Inspect resource integrity and capture diagnostics.

Additionally record whether the skill reads the routed reference, invokes the
helper without reading its implementation, selects a support directory, and
avoids enumerating that directory's leaves. Non-adoption is a result, not a
reason to discard the cell. Compare input-plus-output tokens (cache counted
once) and process wall time only after reviewing coverage and unequal work.
No broad percentage claim, pooled headline or featured-chart update follows
from one exposed pair. Preserve earlier adverse results.
