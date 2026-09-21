I’ll use the landlord skill to compare both implementations against `CONTRACT.md`, identify shared mechanics and caller policy, and trace a maintenance change. This will be a read-only review within the project.

**Simplify the proposal: share a small resource walker, but keep it in `install.py` while the archive member list must remain unchanged.** Adding a required `resource_inventory.py` import to the installer would break standalone offline installation: the packager explicitly includes `LICENSE` and `scripts/install.py`, plus skill resources and the generated manifest—not the proposed module. That conflicts with [CONTRACT.md:1](project/CONTRACT.md#L1). See [package_skills.py:21](project/scripts/package_skills.py#L21).

A viable design is for `package_skills.py` to import that helper from its sibling `install.py`. The installer’s CLI is already guarded by `if __name__ == "__main__"` ([install.py:135](project/scripts/install.py#L135)). This creates some coupling between commands, but avoids a new distribution dependency, duplicated fallback implementations, or build-time code embedding. A separate module becomes viable only if every distribution path carries it, including an explicit archive-member change.

What actually earns sharing:

| Concern | Shared mechanism or caller policy? |
|---|---|
| Sorted traversal within one skill directory | Shared mechanism |
| Excluding any relative component named `__pycache__` or ending in `.pyc` | Shared rule |
| Rejecting included links/special files; skipping directories | Shared mechanism |
| Relative POSIX names and file modes | Shared representation |
| Selecting skills, validating source ancestors, and deciding when to validate | Caller policy |
| Hashing, byte retention, comparison reports, copying, and archive construction | Caller policy |

The overlap is between the installer’s **comparison inventory** ([install.py:19](project/scripts/install.py#L19)) and packaging’s resource enumeration ([package_skills.py:22](project/scripts/package_skills.py#L22)). It is not a replacement for the installation procedure.

Have the helper yield regular-file paths, relative names, and modes after applying the existing exclusions and `lstat` validation. Keep it free of hashing and retained file contents:

- Comparison streams SHA-256 and records `(digest, mode)`; missing/changed/extra reporting remains unchanged ([install.py:33](project/scripts/install.py#L33)).
- Packaging reads each file into its member map and hashes those same bytes for `CONTENTS.json`. Reusing digest-only inventory would require another read and would not bind the digest to the bytes actually archived ([package_skills.py:39](project/scripts/package_skills.py#L39)).

**Keep the security and operational boundaries in their callers.** Normal installation checks *every selected skill* for symlinks before creating destinations, including links beneath names excluded from copying. Both inventory loops apply exclusions before validating entries. Substituting the filtered walker for installation’s preflight would therefore weaken existing source-link checks. Preserve selection, conflict refusal, destination containment, dry-run behavior, exclusive target creation, and rollback ([install.py:68](project/scripts/install.py#L68)).

Packaging must retain its own skill discovery—including rejection of linked top-level entries before checking for `SKILL.md`—and final source-ancestor/file checks. Keep `LICENSE` and the installer as explicit members, archive-output protection, exclusive output creation, source modes, manifest format, sorted member order, and deterministic gzip/tar metadata ([package_skills.py:19](project/scripts/package_skills.py#L19), [package_skills.py:37](project/scripts/package_skills.py#L37)). The CLI and comparison exit codes remain caller-owned ([install.py:112](project/scripts/install.py#L112)).

For a concrete maintenance trace, suppose `.pytest_cache` becomes an **explicitly approved new exclusion**. Update the shared exclusion rule and installation’s copy-ignore rule together; comparison and packaging then inherit the inventory change. Keep installation’s unfiltered symlink preflight intact. A small shared tuple of ignore patterns could serve both the walker and `shutil.ignore_patterns`, preventing those policies from drifting. This would deliberately change resource membership and therefore requires a contract decision separate from the behavior-preserving refactor.

This recommendation is based on static review of the supplied snapshot. No behavior was executed or tested, and no files were changed. Before implementation is accepted, verify extracted offline installation, CLI/check compatibility, selected-skill and conflict behavior, excluded-path symlink rejection, and archive membership/modes/deterministic metadata. Distribution paths outside this snapshot remain unreviewed.
