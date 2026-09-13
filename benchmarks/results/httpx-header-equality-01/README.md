# Duplicate equality gap found; token objective still fails

[Frozen protocol](../../HTTPX-HEADER-EQUALITY-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json), [author integrity verification](author-integrity.json).
Launch `be12479`, Con Artist resources `400c7c3`, unchanged full HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Two fresh serial Astra medium
sessions, skill first, n=1, 360-second limits. Both completed without retries,
exclusions, account stops, candidate edits or concurrent author test workloads.

| Arm | Input + output tokens | Process seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 97,652 | 74.264 | 4 |
| Con Artist | 161,447 | 62.438 | 6 |

**+65.33% tokens / −15.92% time.** Cached input is included once; reasoning
output is not added again. Faster time does not satisfy the similar/lower-token
objective. This author-selected boundary in an already-exposed real project is
not an independent holdout or a maintainer ticket. n=1, shared host/cache, order
and different extra work prevent a causal efficiency claim or all-eight acceptance.

## Actual outcomes

Both arms run the unchanged 27-test header suite on correct code and one isolated
sorted-list-to-set equality fault. Both versions pass all 27 tests. Each arm's
same stronger assertion compares two identical header pairs with one, expecting
inequality: correct code passes, faulty code fails with actual equality True
versus expected False. Both check reordered/case-varied distinct pairs and unequal
values on both implementations, preserving those normal controls.

The [skill](headers-duplicate-equality--skill--1/commands.json) uses four fresh
helper copy/check processes with `precheck` and conditional `probe_when: survives`.
Prechecks verify copied imports, the exported Headers class and equality global,
code filename/source, and normal controls. The inline stronger probe then fails
with the intended AssertionError. There is no collector/reference load, no
temporary recipe or binding module. Direct project reading was adopted, but the
agent reads the audit reference and audit.py lines 1–345, plus the full header
test, conftest/configuration and targeted production sections. Thus the new routing
does not eliminate substantial helper-source inspection. Compact collector output
is unused and has no demonstrated contribution in this run.

The [baseline](headers-duplicate-equality--baseline--1/commands.json) writes an
inline orchestration script creating two project-local copies, a pytest provenance
plugin and a three-case diagnostic test in those copies. Four native pytest
processes run the existing suites and diagnostics; correct diagnostics are 3 pass,
faulty diagnostics 1 AssertionError / 2 pass. Each process verifies copied paths,
equality source/code filename and implementation hash. It also hashes original
files and copied inputs, then removes copies in finally. Native child processes
have no individual timeout; the outer model limit remains. The diagnostic uses
pytest `-s` and a provenance plugin, while the skill uses inline probes and repeats
controls in all four prechecks. These are unequal mechanics, not identical work.

No original production bug is claimed: upstream equality is correct; the narrow
deliberate fault demonstrates a gap in this particular existing test selection.
Neither result justifies a general claim about all header behavior.

## Preservation and capture

Post-run author comparison finds exact original **125-file** inventories, bytes
and permission bits in both final snapshots, no extras and empty agent diffs.
Installed skill resources are unchanged. Terminal usage matches metadata and
original event logs reconcile with their workspace/home-redacted versions.
Recorded capture diagnostics have no invalid/empty-output/rejected-patch flags.
The baseline orchestration output starts at `COPY VERIFIED faulty`, omitting the
earlier printed correct-copy line; decisive native outputs remain present. This
is retained, not reconstructed; capture diagnostics do not guarantee every output
byte was delivered. Author final-file verification is separate from model evidence.

This export preserves complete available events, commands, answers and diffs plus
four selected upstream files including its MIT license. project-export.json lists
the excerpts; it is not a standalone full checkout. Full snapshots and original
logs remain local. `<PYTHON>` redacts the supplied interpreter, workspace/home
paths are redacted, and source-sha256.json identifies original unredacted logs.

Previous adverse results and featured graphs remain unchanged. The next candidate
needs to reduce actual repeated reading/orchestration costs without suppressing
necessary trust review, assertion evidence or isolation. This run is not a reason
to rerun the same task until its percentage improves.

Post-run repository verification: **380 tests pass (52.895s)**; catalog/local
links, featured synchronization, whitespace and exported private-path checks
pass. These author checks are not additional model performance evidence.

## Later reference-routing candidate

After this measurement, the default Python audit reference was shortened from
6,997 to 5,445 UTF-8 bytes (**22.18% fewer bytes**, not model tokens). Detailed
empty-suite/precheck/assertion-helper/cleanup diagnostics now live in the existing
advanced reference, linked from the normal contract when those conditions arise.
The default retains all blocking warnings and interpretation requirements:
nonzero exit is not coverage, precheck/empty suites are incomplete, actual failures
must be inspected, warning policy is preserved and unconfirmed children must not
be retried. Copy limits, original integrity, same-process bindings, output limits
and the executable JSON example remain in the normal reference.

Helper implementation and entrypoint are unchanged. This uses skill-creator's
progressive-disclosure guidance, not a ban on justified source inspection. No
model run yet measures adoption or savings for this later candidate, and no
percentage above is reassigned to it. Total installed documentation is not claimed
smaller: detail is routed, not discarded.

Candidate verification: packaged executable examples **12 tests pass (2.988s)**;
full repository **380 tests pass (52.455s)**. Skill validation, local links,
featured synchronization and whitespace checks pass. An initial test-discovery
pattern matched zero tests; it was not credited as validation and was replaced
with the actual test_build.py suite and full discovery.
