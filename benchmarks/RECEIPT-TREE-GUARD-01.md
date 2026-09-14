# Receipt optional tree guard — 2026-09-14

Previous source `41b5f28`. The two exposed Receipt guide executions construct
whole-tree hash wrappers; the [output-choice run](RECEIPT-OUTPUT-CHOICE-01-REVIEW.md)
also prints a separate full inventory. Compact selection alone did not improve
whole-task cost. This candidate implements the repeated operation instead of
adding another general admonition to avoid work.

## Capability and boundary

Add optional recipe `"guard_tree":true` to the existing comparison helper.
Only use it for requested whole-project preservation when all source reads are
authorized. It inventories the source root immediately before native comparison
and after owned-copy cleanup: regular-file SHA-256 and permission modes, directory
entries/modes (including empty directories/root), and symlink text/modes without
following link targets. Git metadata, ignored files and installed resources are
included. No exclusions or extra report/recipe files.

Success adds a compact `tree_guard` object: unchanged flag, entry count, file-byte
count, inventory digest and scope. Full per-file hashes stay internal. Added,
removed or changed entries raise an error naming up to 20 paths plus total count;
CLI returns 2 without claiming an established comparison. It does not restore
changes. Existing selected-file evidence and native transcripts are unchanged.
Absent/false option performs no tree inventory and adds no output field.

Each inventory has a separate 20 MB file-read budget and 10,000-entry bound
including root. Files stream in at most 64 KiB chunks, with at most one overflow
byte; known oversize files reject before opening. Regular-file opens reject
symlink substitution and check device/inode/type. Special files reject without
reading. Existing 20 MB copying budget and native timeouts remain unchanged.

This is trusted-test change detection, **not isolation**. It does not cover link
targets, ownership, timestamps, ACLs/xattrs, concurrent changes, writes restored
between observations or operations outside the comparison interval. It is not an
atomic/race-proof snapshot. Other processes can cause a reported change. It does
not replace diff review or later checks. Larger repositories need another suitable
native method; the guard must not silently exclude inconvenient files to pass.

## Actual validation

`tests/test_receipt_tree_guard.py`: **8 tests / 3.707s**, including:

- Real failing-before/passing-after native comparison with unchanged full tree,
  unrelated binary bytes, an empty directory and a dangling link.
- Nine actual native mutations: unrelated bytes, file mode, deletion, added file,
  added directory, directory mode, root mode, Git metadata and symlink target.
  Each retains the real before assertion failure/after pass yet rejects overall
  comparison for the original-tree change. Changes are not restored; owned copies
  are removed. These are subcases, not nine additional counted test methods.
- Invalid flags, entry/byte limits, file growth beyond budget, special files and
  link-target non-reading; disabled guard never inventories the tree.
- A copied standalone helper outside the checkout runs native comparison with
  the guard; a CLI native-mutation case exits 2 with no success JSON.

Existing helper **47 tests / 15.014s** and packaging **12 / 3.249s** also pass.
Skill validation, repository links/structure, featured EN/KO synchronization and
diff whitespace checks pass. Earlier development run: seven guard tests passed
before adding the CLI failure case; the final eight-test run above is authoritative.

## Cost and next evidence

Entry/discovery and resource count stay unchanged. Compared with `41b5f28`, helper
source grows 18,454 → 21,873 bytes (+3,419); guide grows 5,786 → 6,682 (+896).
Opt-in inventories add two bounded source reads. This is a deliberate capability
tradeoff, not an instruction-size optimization or measured model saving.

Model adoption, actual wrapper removal, whole-task cost and transfer remain
unmeasured. The next screen must preserve native suite, source identity, complete
original-tree requirements and cleanup, and retain unnecessary duplicate work if
it occurs. Do not extrapolate a cost win from compact result fields or passing
local tests. No featured/historical measurements or charts change.
