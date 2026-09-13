# Receipt: freeze selected test-support directories

Revision `0d5c81c` adds explicit current-directory selection to Receipt's `fixed`
inputs. Tests, nested samples and support files can be frozen as a bounded group
instead of manually enumerating every leaf. Historical `vary` inputs remain
explicit files, preserving the distinction between fixed current assertions and
changing committed implementation. The [earlier multi-module comparison](RECEIPT-ASSEMBLY-01.md)
remains adverse in tokens; no new model performance result is claimed here.

[Usage](../skills/receipt/references/existing-fix.md),
[behavior tests](../tests/test_receipt_helper.py).
`fixed: ["tests", "samples", "pyproject.toml"]` expands selected regular files
in stable order. Each expanded file is hashed, copied unchanged to both variants,
and included in original-content/mode checks. Input recipes are not mutated.
This does not infer which directories are relevant: choose supported, permitted
inputs and don't copy unrelated data merely because it is nearby.

Expansion is bounded to 10,000 visited/pending filesystem entries; the existing
20 MB snapshot budget still applies before reading an overflowing file. Root
selection, traversal, Git internals, symlinks, nonregular inputs, overlapping
selections and empty directories (including nested ones) fail before comparisons.
Expanded fixed files cannot overlap varying implementations. Empty directory
state is not silently dropped. Hidden regular files are included, not implicitly
filtered; choose narrower paths when caches/private inputs are inappropriate.
As before, this is not a sandbox against trusted tests or concurrent file changes.

## Actual execution evidence

New tests construct a real temporary Git repository with two implementation
commits. Current `checks/` includes a nested numeric input and the same boundary
assertion for both revisions. The directory recipe produces the intended
`AssertionError: False is not true` before the fix and passes after it; all three
expanded fixed-file hashes are reported and originals remain byte-identical.
A separate subprocess exercises the JSON-stdin CLI and checks the actual
before-failure/after-pass output and per-file hash.

The first author-written test accidentally imported `allowed` instead of the
fixture's `eligible` function. Its import error was rejected by the test's
assertion-evidence check, corrected, and not counted as defect reproduction.
This was local test development, not a model benchmark retry.

Additional tests verify directory/file overlaps, overlap with historical inputs,
symlinks, nested empty directories, Git internals and an exhausted traversal
budget before file reads or child execution. Existing snapshot-byte-budget and
permission-preservation tests still apply to expanded leaves. Receipt's focused
suite has 28 tests; the behavior does not rely on wording-only skill tests.
Full local regression: 302 tests pass in 40.981 seconds. Skill schema, repository
catalog/links and featured-language synchronization checks pass. This does not
establish hosted CI, current remote installation or model efficiency.

## Remaining gate

This proves an available preparation mechanism, not adoption or token savings.
A fresh realistic comparison must check whether the model selects appropriate
support directories, preserves runner/fixture semantics, avoids unnecessary
enumeration and retains required before/after evidence. Directory breadth and
configuration differences must remain in cost/scope accounting. Do not turn
fewer recipe entries into a whole-task performance percentage. No featured
graph, historical result, visibility or release state is changed.
