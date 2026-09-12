# Automatic selection on small edits

Two tasks, one fresh Astra-medium baseline/auto pair each, serial: four sessions
total, no retry or exclusions. Auto installs all eight without naming a skill.
Raw evidence: ignored `local-runs/auto-label-01` and `auto-plain-label-01`.
The first uses snapshot `7e7d6b1`; the plain control is frozen at `23f83ff`, with
identical skill resources. These are development observations, not held-out scores.

| Task | Arm | Input including cache + output tokens | Seconds |
| --- | --- | ---: | ---: |
| Label edit with explicit optional redesign cue | Baseline | 62,410 | 19.790 |
| Same | Auto | 65,285 | 22.844 |
| Plain label edit, no redesign cue | Baseline | 62,518 | 19.724 |
| Same | Auto | 80,370 | 27.837 |

All four produce the exact same authorized label-only change and preserve state.js
and submit behavior. None adds a testing framework or speculative investigation.

The original label-change case explicitly mentions an optional state-system
replacement outside scope. It is therefore not a clean negative routing control:
auto selects Hostage Negotiator for a reason consistent with its description.
It reads that entrypoint only and performs focused diff review. Baseline is also
equally focused. Auto costs 4.6% more tokens and 15.4% more time in that pair.

The new plain control removes only that scope-negotiation cue, preserving the
project and requested change. Auto neither announces a skill nor reads any skill
body in its trace. Thus no unnecessary skill activation is observed in this sample;
this does not prove the model saw no skill metadata or no installation overhead.

Plain auto costs 28.6% more tokens and 41.1% more time. Its stderr records one
rejected patch, unlike baseline. The eventual edit is correct, but the rejected
target is not established. That extra attempt is a major confound; neither the
overhead nor complete attempted-scope compliance can be attributed to skill routing.
The result is retained rather than retried for a cleaner number.

All installed resource hashes match their committed snapshots and are unchanged
before/after; each auto cell has 26 regular-file entries, baseline has none. Author
inspection verifies exact expected checkout bytes and unchanged state.js in all
four cells. No invalid JSON or empty-output marker. These are file/capture checks,
not proof of general reliability.

Disposition: the two observations support contextual selection—scope skill with
the redesign cue, no observed activation without it. They do not establish an
efficiency win. Do not narrow Hostage Negotiator or disable implicit selection
based on this evidence: the selection itself is appropriate. The outstanding
resource and rejected-patch variability needs to remain separate from skill behavior.
