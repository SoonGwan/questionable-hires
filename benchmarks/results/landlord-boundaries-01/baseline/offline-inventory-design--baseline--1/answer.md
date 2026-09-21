I’ll compare the two inventory implementations against `CONTRACT.md`, then identify a shared boundary and trace a concrete maintenance change. I’ll keep the review static and read-only.

The proposed extraction is **not viable with an unchanged archive member list**. The packager explicitly includes `LICENSE`, `scripts/install.py`, skill resources, and generated `CONTENTS.json`; it does not include `scripts/resource_inventory.py`. An installer that imports the new module would therefore fail after extraction outside the repository. Deferring that import to `--check` would still break the existing CLI contract. Offline installation and carrying shared modules through every distribution path are explicit requirements in [CONTRACT.md:1](project/CONTRACT.md#L1); the archive selection is in [package_skills.py:21](project/scripts/package_skills.py#L21).

**What can actually be shared**

Both implementations walk a skill’s descendants in sorted order, exclude paths containing `__pycache__` or a component ending in `.pyc`, skip directories, reject included linked/special resources, and retain file permission bits. This supports a small shared iterator yielding relative POSIX names, source paths, and `stat.S_IMODE` values. See [install.py:19](project/scripts/install.py#L19) and [package_skills.py:27](project/scripts/package_skills.py#L27).

The complete inventories have different purposes:

| Concern | Remains caller policy |
|---|---|
| Reading and hashing | Installation comparison streams SHA-256 and retains `(digest, mode)`. Packaging retains bytes and computes manifest hashes from those same bytes. Do not introduce a separate hash read that could describe different bytes from those archived. |
| Skill selection | Installer discovery uses `*/SKILL.md` and validates requested names. Packaging visits all immediate entries, rejecting linked entries before checking for `SKILL.md`, and refuses an empty package. |
| Link checks | Actual installation rejects source symlinks **even inside excluded cache paths**, before creating destinations. The inventory loops exclude cache paths before validating them. Packaging additionally checks source ancestors and its fixed files. |
| Installation behavior | Destination checks, selected-skill deduplication, conflict refusal, dry-run, exclusive target creation, copying, rollback, comparison reports, and exit codes. |
| Archive behavior | Fixed members, repository-relative member names, manifest format, output restrictions and exclusive creation, sorted output, preserved file modes, and normalized tar/gzip metadata. |

These distinctions are visible in [install.py:41](project/scripts/install.py#L41), [install.py:68](project/scripts/install.py#L68), [install.py:112](project/scripts/install.py#L112), and [package_skills.py:35](project/scripts/package_skills.py#L35). In particular, replacing installation’s symlink preflight with the filtered inventory would weaken its contract.

**Recommended design**

With the member list fixed, keep the shared traversal primitive **in `install.py`**, and have `package_skills.py` import it. The installer already guards command execution with `if __name__ == "__main__"` ([install.py:135](project/scripts/install.py#L135)). This keeps the distributed installer self-contained while eliminating duplicated traversal in the source commands.

Keep thin caller adapters for hashing versus byte collection, root validation, and existing error wording. Leave installation’s copying and preflight intact, and preserve packaging’s additional ancestor validation and deterministic serialization.

If the separate `resource_inventory.py` filename is required, revise the archive-member constraint and explicitly distribute it beside the installer. That also changes `CONTENTS.json`, counts, sizes, and archive digest. A missing-module fallback would retain two implementations to maintain. No unseen distribution paths can be certified from this snapshot.

**Concrete maintenance trace**

Suppose a future, explicitly approved policy change excludes `*.pyo`:

1. Update the shared exclusion predicate; both comparison inventories and packaged skill resources then omit those paths.
2. Also update `shutil.copytree`’s ignore policy at [install.py:97](project/scripts/install.py#L97). Otherwise checkout installation still copies files that comparison ignores and packaging omits.
3. Keep the unfiltered source-symlink preflight: a `.pyo` symlink must still cause installation refusal.
4. Packaging’s existing manifest generation follows the resulting member set automatically; metadata normalization stays unchanged.

That would be an intentional behavior change, not part of the contract-preserving refactor. It demonstrates why shared inventory logic alone cannot own installation policy.

This was a static source review. No commands were executed against installer/package behavior, no files were changed, and the selected snapshot contains no `skills` directory. The explicit archive selection is sufficient to establish the offline dependency failure.
