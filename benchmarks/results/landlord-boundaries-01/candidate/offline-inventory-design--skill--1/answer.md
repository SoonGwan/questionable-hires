I’ll use the landlord skill to compare both implementations with `CONTRACT.md`, identify the shared mechanics and caller policies, and check the proposal’s effect on offline installation. This will be a read-only static review.


**Simplify the proposal: share a narrow helper, but keep it in `install.py` while the archive member list must remain unchanged.** A new `resource_inventory.py` imported by the installer would break the offline distribution as proposed.

The packager explicitly includes `LICENSE`, `scripts/install.py`, and skill resources; it does not collect sibling Python modules ([package_skills.py:21](project/scripts/package_skills.py#L21)). After extraction outside this repository, the shared module would be missing. That violates the offline-installation requirement and the condition that every distribution path carry any shared module ([CONTRACT.md:1](project/CONTRACT.md#L1)). A checkout import succeeding would not establish that the archive works.

### What can actually be shared

Both implementations perform the same basic traversal: sort descendants, exclude paths containing `__pycache__` or components ending in `.pyc`, skip directories, and reject remaining linked or special resources ([install.py:19](project/scripts/install.py#L19), [package_skills.py:27](project/scripts/package_skills.py#L27)).

A small iterator yielding regular resource paths, relative names, and permission modes can serve both consumers. Keep hashing and byte loading outside it:

- Installation comparison streams SHA-256 and returns skill-relative names mapped to `(digest, mode)` ([install.py:33](project/scripts/install.py#L33)).
- Packaging retains file bytes under repository-relative names and hashes those retained bytes for its manifest ([package_skills.py:39](project/scripts/package_skills.py#L39)). Computing an inventory digest and then rereading files for the archive would add work and could separate manifest hashes from the bytes archived.

### What remains caller policy

| Concern | Policy that must remain |
|---|---|
| Discovery and scope | Installation validates and deduplicates selected names. Packaging scans all eligible skill folders, rejects linked top-level folders, and refuses an empty selection ([install.py:46](project/scripts/install.py#L46), [package_skills.py:22](project/scripts/package_skills.py#L22)). |
| Link checks | Installation preflights **every selected skill before writing**, including links in cache paths that copying would exclude. Both inventory traversals exclude cache paths before resource validation. Replacing installation’s preflight with the iterator would weaken its contract ([install.py:80](project/scripts/install.py#L80)). |
| Source boundaries | Keep source-root checks and packaging’s ancestor-link checks, including checks covering `LICENSE` and the installer itself ([package_skills.py:41](project/scripts/package_skills.py#L41)). |
| Installation behavior | Preserve destination restrictions, conflict refusal, exclusive target creation, rollback, copy exclusions, comparison reports, and CLI/exit behavior ([install.py:68](project/scripts/install.py#L68), [install.py:112](project/scripts/install.py#L112)). |
| Archive behavior | Preserve member selection, file modes, manifest format, sorted output, fixed gzip/tar metadata, exclusive output creation, and partial-output handling ([package_skills.py:47](project/scripts/package_skills.py#L47)). |

### Viable design and maintenance cost

Place the narrow traversal helper in `install.py`, and let `package_skills.py` import it. The installer already guards its CLI entry point ([install.py:135](project/scripts/install.py#L135)), and the archive already carries that file. This creates an explicit dependency from packaging to installer-owned resource rules without adding a runtime dependency to offline installation.

Keep the packager’s extra-file validation and archive construction separate. Avoid a configurable inventory framework: these two consumers justify shared traversal, not a generalized policy engine.

For a concrete maintenance change, suppose `.pyo` files should also be excluded:

1. Update the shared traversal exclusion rule once; comparison and packaging both adopt it.
2. Update installation’s `copytree` ignore patterns, which are a separate consumer of exclusion policy ([install.py:97](project/scripts/install.py#L97)).
3. Leave installation’s full source-link preflight intact: an excluded `.pyo` symlink must still trigger refusal before any destination is created.

With the current duplicated traversals, that change needs two traversal edits plus the copy-rule edit. The helper removes one synchronization point; it does not eliminate copy policy or security checks.

A standalone shared module would offer cleaner ownership, but requires changing the archive member list and ensuring every supported distribution carries it. Under the stated constraint, the installer-owned helper is the viable compromise.

This conclusion comes from static review of the supplied snapshot. I made no edits and ran no behavioral tests; distribution paths outside this snapshot remain unreviewed.
