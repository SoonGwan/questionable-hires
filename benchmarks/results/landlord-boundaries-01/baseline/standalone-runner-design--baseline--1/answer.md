I’ll read the three helpers, their callers, the installer, and the contract to assess whether a shared runtime preserves their behavior and installed distribution.

The proposed repository-level import conflicts with installation: the installer copies only each selected skill’s directory. The process loops are similar, but their callers differ on unconfirmed cleanup and incomplete evidence. I’m checking those boundaries to compare keeping the local implementations with shipping a shared implementation inside each skill.

**Recommend keep the three local implementations and remove the proposed repository-level runtime dependency.** The shared mechanics are real, but the proposed distribution violates the contract, and sharing code would still require caller-specific adapters.

[CONTRACT.md](project/CONTRACT.md#L1) requires each skill to work alone in an arbitrary consumer directory, without the repository, another skill, or dependency installation.

**Distribution is the decisive problem.** [Installation](project/scripts/install.py#L92) copies only `skills/<name>` into the destination. A repository-level `scripts/common_process.py` would not accompany any installed helper. Searching parent directories or adjusting `PYTHONPATH` cannot make an absent module available.

Shipping one shared file beside installed skills would require a new installation and ownership model: independently installed versions must coexist, conflicts must be handled, and rollback must cover the new resource. Currently, existing skill destinations are refused and rollback removes only directories created by that invocation. Symlinking to the checkout is also incompatible with standalone operation and the installer’s source-symlink rejection. [Installer safeguards](project/scripts/install.py#L68)

The current `--check` compares each installed skill against that skill’s source-tree bytes and modes. An external runtime would be outside that comparison; injecting an extra module only during installation would instead appear as an extra file unless the comparison model changed. [Inventory and comparison](project/scripts/install.py#L19)

**Behavioral obligations extend beyond a subprocess timeout.**

All three loops start a new POSIX session, disable stdin, merge stderr into stdout, incrementally decode UTF-8 with replacement, retain the last 12,000 **characters**, and track truncation. They use a monotonic deadline, initiate group cleanup when the foreground process exits, kill the group again through guarded finalization, close the pipe, and allow five seconds to confirm child exit. Replacing this with a simple `subprocess.run(timeout=...)` would not preserve those mechanics. Sources: [audit execution](project/skills/con-artist/scripts/audit.py#L184), [receipt capture](project/skills/receipt/scripts/compare.py#L249), [probe execution](project/skills/exorcist/scripts/run_probe.py#L15).

Their callers impose different policies:

| Caller | Obligations a refactor must preserve |
|---|---|
| **Audit** | Constructs a Python bootstrap and removes inherited Python path/optimization settings. Unconfirmed cleanup raises `RuntimeError` unless another error is already propagating. Phase execution stops for timeout, exit 7, unsuccessful correct baseline, or precheck exit 6. Batch handling deliberately lets cleanup/integrity `RuntimeError` escape. [Phase decisions](project/skills/con-artist/scripts/audit.py#L390), [batch handling](project/skills/con-artist/scripts/audit.py#L458) |
| **Receipt** | Uses copy-local temporary-directory settings and the same raise-on-unconfirmed-cleanup policy. Native Python mode retains `native_exit_code` but maps missing readiness to check exit 7 when not timed out. Node mode also treats malformed, missing, or truncated provenance as incomplete. Comparison stops before the next variant on timeout or check exit 7. [Python adapter](project/skills/receipt/scripts/compare.py#L221), [Node adapter](project/skills/receipt/scripts/compare.py#L302), [comparison caller](project/skills/receipt/scripts/compare.py#L539) |
| **Exorcist** | Runs the supplied command with inherited environment; defaults to 10 seconds versus 30 for the other CLIs. Reports elapsed time and `cleanup_complete`; unconfirmed cleanup maps to CLI 125, ahead of timeout 124. An actual child exit 124 maps to CLI 1 while remaining 124 in JSON. [Interface and exit mapping](project/skills/exorcist/scripts/run_probe.py#L75) |

Receipt’s separate Git subprocess path returns binary data, accepts input, and has a 20-second timeout; it should not accidentally be folded into this text-tail abstraction. [Git caller](project/skills/receipt/scripts/compare.py#L210)

**A viable alternative is one maintained implementation, distributed as a regular local module inside each skill.** Commit generated copies under each skill’s `scripts/` directory and check their consistency during development. Installed helpers would import their bundled sibling; existing copy and inventory behavior would cover it. Keep command construction, environment choices, evidence interpretation, JSON shape, and CLI mapping in local adapters.

That reduces repeated loop edits but adds generation, consistency checks, and an internal result/exception contract. Keeping three local loops costs coordinated maintenance, but avoids those mechanisms. For this snapshot and three consumers, keeping them is the simpler choice.

**Concrete future change:** suppose profiling justifies increasing pipe reads from 4,096 to 16,384 bytes while preserving all observable semantics. Today, maintainers change three read sites and validate split UTF-8 decoding, tail/truncation boundaries, foreground-exit cleanup, and timeout handling across the callers. With bundled generated modules, they change the canonical implementation once, regenerate three copies, and perform the same caller validation—especially Node’s truncation-sensitive provenance. Installed copies still need explicit replacement: the installer refuses overwriting existing skills. Centralizing source maintenance does not automatically update consumers.

**Evidence status:** this was static review using file listing, searches, and source reads only. No helpers, installer, tests, or subprocess experiments were run; no files were changed. The selected snapshot settles the distribution conflict but does not establish what tests or packaging machinery exist upstream.
