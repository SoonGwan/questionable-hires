# Two executable comparison modes, explicit supported-workflow preference

Predecessor `8b73d3a`. In the [uncommitted transfer](results/receipt-uncommitted-01/README.md),
the model read the entire procedure, then rebuilt copying/provenance/execution
instead of invoking the optional helper. The trace does not establish why; do
not attribute that choice solely to example placement or treat the task as a
helper-adoption requirement after the fact.

The procedure now shows complete committed and working-tree commands together,
using the same example paths/tests. The caller chooses the appropriate mode;
neither a recipe file nor a commit/stash is needed. The existing working-tree
syntax is not a new helper feature in this change. Entry description, automatic
selection, implementation and current-bug verification requirements are unchanged.

For supported local unittest/installed-pytest layouts, the procedure prefers the
helper over reimplementing its copy, same-process import, execution and cleanup
work. Existing valid evidence comes first. Unsupported layouts/runtimes or a
retained-copy requirement still use native comparison. If broader original-file
integrity is required, it can be checked around the helper; its selected-file
guarantee is not inflated into a whole-repository guarantee.

An execution test extracts both complete shell examples from the reference and
substitutes only actual installed executable paths. Real local Git histories and
dirty working implementations exercise the literal JSON/runner arguments:
both modes capture the actual before assertion failure and after pass, check
copied import evidence and correct revision/snapshot identity, preserve all
fixture/Git bytes and remove owned temporary copies. This is an executable
documentation check, not a wording-only check or a new model benchmark.

Validation: both commands pass under the default Python and Python 3.11; the
complete fixed-source suite passes 345 tests in 48.589 seconds. An earlier full
run failed the install-equivalence assertion because the author changed this
resource's line wrapping while the two bundles were being built. The mismatched
bytes show exactly that wrapping change. The source was then held fixed for the
complete rerun; no install/test logic was changed to obtain the pass. This is an
author verification mistake, not a discarded model benchmark cell.

This is clearer routing, **not instruction compression or demonstrated token/time
savings**. Preference is not mandatory adoption, and the observed native fallback
remains valid within its recorded limits. Do not repeat the exposed settings task
for better numbers; a separate behavioral task must establish whether this change
actually removes duplicated model work without losing required evidence. Existing
adverse scores, all-eight acceptance gaps and featured/localized charts remain.
