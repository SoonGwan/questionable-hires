I’ll use the landlord skill to review the three callers, installation layout, and contract, then compare the shared module with a viable alternative. This will be a read-only review.


The installation boundary is decisive: the installer copies only each selected skill’s directory, so a repository-level runtime module would not travel with an installed helper. The execution loops also have different obligations: audit and receipt raise on unconfirmed cleanup, while exorcist reports it in JSON and returns CLI status 125. Receipt already shares its local capture function between Python and Node callers.


**Recommend remove the proposed repository-level runtime dependency and keep the three implementations local.** There is real shared process machinery, but the proposed placement conflicts with standalone installation. Its maintenance savings do not yet justify changing distribution and introducing a shared compatibility boundary.

**Distribution is the blocking issue.** [CONTRACT.md:1](project/CONTRACT.md#L1) requires each skill to work alone in an arbitrary consumer directory, without the repository, other skills, or dependency installation. The installer copies only `skills/<name>` into the destination; repository-level `scripts/common_process.py` would be omitted. Adding repository discovery, `PYTHONPATH` requirements, or a sibling-skill dependency would violate that contract. Symlinking the shared module is also incompatible with the installer’s explicit rejection of source symlinks. [install.py:68](project/scripts/install.py#L68)

Bundling a private copy into every skill could satisfy standalone operation, but that is a different design. Installer-time injection would also require updating `--check`: it currently compares installed resources against the selected source skill’s files, hashes, and modes, so an injected module would otherwise appear as an extra resource. Existing installations are deliberately left untouched; changing one canonical source would not update deployed copies. [install.py:41](project/scripts/install.py#L41)

The actual callers establish these behavioral obligations:

| Consumer | Behavior an extraction must preserve |
|---|---|
| Con-artist | `audit()` invokes `execute()` for correct/mutant tests and probes. Timeout, setup exit 7, a failed correct baseline, and applicable precheck exit 6 stop the audit as incomplete. Unconfirmed cleanup raises, preventing further checks. [audit.py:390](project/skills/con-artist/scripts/audit.py#L390) |
| Receipt | Both Python and Node call the existing local `capture_check()`. Python module mode retains the native exit separately and maps missing startup provenance to exit 7 unless timed out. Node additionally treats truncated, malformed, or missing load evidence as incomplete. These interpretations belong to their adapters. [compare.py:221](project/skills/receipt/scripts/compare.py#L221), [compare.py:302](project/skills/receipt/scripts/compare.py#L302) |
| Exorcist | Runs the supplied command with inherited environment, reports elapsed time and `cleanup_complete`, and maps failed cleanup to CLI 125 ahead of timeout 124. A child exiting 124 maps to CLI 1 while its actual status remains in JSON. [run_probe.py:15](project/skills/exorcist/scripts/run_probe.py#L15), [run_probe.py:103](project/skills/exorcist/scripts/run_probe.py#L103) |

The shared mechanics are substantial: argument-list execution, closed stdin, merged output, incremental UTF-8 replacement decoding, a **12,000-character tail**, monotonic deadlines, foreground-exit detection, process-group killing, and a five-second cleanup wait. Extraction must preserve cleanup during interruption and retain the original exception. Audit and receipt raise on otherwise-unconfirmed child exit; exorcist returns that condition. [audit.py:184](project/skills/con-artist/scripts/audit.py#L184), [compare.py:249](project/skills/receipt/scripts/compare.py#L249)

Environment preparation must remain caller-owned: audit strips Python import/optimization overrides; receipt also directs child temporary files into its copy and constructs native-runner instrumentation; exorcist inherits its environment. Preserve the 30-second audit/receipt defaults, 10-second probe default, existing CLI/JSON interfaces, and POSIX limitation. Process-group cleanup supplies no sandbox or containment of escaped groups. [run_probe.py:75](project/skills/exorcist/scripts/run_probe.py#L75)

**The nearest viable alternative is deliberate local duplication**, including receipt’s already-useful internal sharing. Its cost is reviewing and applying common fixes three times. A canonical implementation bundled as private skill-local modules would reduce source edits, but adds synchronization, packaging validation, import resolution, and adapter compatibility work. That alternative becomes attractive if repeated coordinated fixes demonstrate the need.

For a concrete future change, suppose a defect requires **bounded draining of buffered output after timeout**:

- With local implementations, update all three capture loops. Keep audit/receipt’s cleanup exception behavior and exorcist’s flag/status mapping; review receipt’s provenance parsing against the changed captured tail.
- With bundled shared machinery, update the drain mechanism once, synchronize three shipped copies, and validate every adapter and standalone installation. Caller policy still remains separate.
- With the proposed repository-only module, the central fix remains unavailable to standalone installations.

Either approach needs verification of timeout bounds, split UTF-8 decoding, truncation, descendants holding pipes, and interruption cleanup. Centralization reduces implementation edits; it does not eliminate consumer verification or deployment work.

**Evidence boundary:** I executed only local file inventory, searches, and source reads. I did not run helpers, installations, or tests, and changed nothing. These are static conclusions from the selected snapshot, not claims about upstream test coverage or observed runtime behavior. The distribution contract settles the recommendation without an experiment.
