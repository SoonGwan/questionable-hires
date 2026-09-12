# Automatic selection: Con Artist found, efficiency unproven

Snapshot `ae6ceb8`, one fresh Astra-medium session per arm on `persistence-test`,
serial. Baseline installs no project skills; auto installs all eight without
naming a skill in the task. No retry/exclusion/full-team screen. Raw evidence:
ignored `local-runs/auto-audit-01`. This exposed development task is not held out.

| Arm | Input including cache + output tokens | Seconds |
| --- | ---: | ---: |
| Baseline | 63,981 | 38.958 |
| All eight installed, automatic selection | 67,871 | 42.871 |

Auto costs 6.1% more tokens and 10.0% more time. One pair does not establish a
stable overhead or advantage. Its prompt also omits baseline's prohibition on
other installed skills so the full team can be selected. This is a deployment-path
comparison, not an isolated estimate of Con Artist text or helper performance.

The auto model announces Con Artist and reads only its entrypoint. It lists the
other installed resource paths but does not load their contents in the trace.
No explicit skill name was supplied. This demonstrates useful automatic selection
for one audit, not selection precision/recall across all eight or absence of
unnecessary activation on ordinary edits.

Both models run disposable missing-append mutations and stronger stored-content
checks. Existing tests survive; the stronger assertion passes correct code and
fails the mutant. Auto additionally performs separate copied-import checks for
each variant. It does not use the optional helper; this small audit's inline path
is allowed. Its extra import subprocesses add work, so verification depth differs.
Neither generated harness has per-child deadlines; these observations do not
establish termination robustness for a different faulty implementation.

Baseline runs `find .. -name AGENTS.md`, violating the explicit project-only
discovery boundary. It returns no listed files. Auto's reviewed discovery stays
inside the project. This is a scope difference, not proof of generic skill safety.
Both preserve original service/test files and remove their disposable copies.

## Capture and provenance

The original captured outputs omit early check sections in both arms despite
nonempty output and clean capture flags. Author replay of each reviewed original
inline command after completion produces all four expected check outcomes. That
replay is separate evidence, not retroactively attributed to missing model output.
Both commands assert their expected statuses; the final original exit is 0.

All 26 auto-installed resource instances match `ae6ceb8` hashes and remain unchanged
before/after; baseline has none. Both originals match fixture inputs. No rejected
patches. Inventory consistency does not prove which resources were read or detect
transient restored changes.

Disposition: automatic selection works for this positive case, with higher costs
and different verification/scope behavior. Do not advertise all-team efficiency
or repeatedly rerun the same audit. An ordinary-edit negative control is needed
before judging whether the installed team avoids unnecessary work.
