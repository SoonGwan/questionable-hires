# Signal transfer: correct diagnosis, mixed efficiency

Frozen e0c0f9d, entrypoint/reference ca2e179, helper 34aedd4, runner fd8d578.
Two new cases, Astra medium, serial one baseline/skill repeat, seed 20260911,
240-second deadline. Order: retained skill, lost skill, lost baseline, retained
baseline. All four complete. No author retries/exclusions. Original private logs
remain in `local-runs/exorcist-signal-01/`.

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| lost signal | 146,364 | 111,645 | 115.011 | 108.083 |
| retained signal | 84,399 | 110,097 | 80.008 | 73.189 |
| sum | 230,763 | 221,742 | 195.019 | 181.272 |

Summed skill cost is **3.9% fewer tokens / 7.0% less time**. Cached input is already
included in input tokens. These are descriptive single samples on shared host/cache,
not a causal gain. The retained-signal skill still uses more tokens than baseline.

Both arms correctly diagnose both implementations using actual worker.process and
documented immediate callbacks, retain JSON/reproduction artifacts, preserve
original files and distinguish local behavior from unknown production behavior.

Lost baseline runs three bounded child trials, recording callback completion and
stack dumps at ready.wait(), then kills each at 1.5 seconds. Its first probe exits
1 because its stack predicate rejects an actually captured worker stack (traceback
format mismatch); it repairs the predicate and repeats all three trials successfully.
The failed original result remains in captured stdout even though its JSON file
is replaced by the successful rerun. This repair cost is included, not excluded.

Lost skill uses a five-second subprocess deadline around a harness thread. It
observes the actual callback's Event becoming set, then cleared with the worker
blocked at wait. A separately labelled diagnostic resignal releases the same call
and the owned thread finishes. It does not claim that intervention is an ordinary
callback or a production fix. It records timed_out=false: the bounded observation
and stack/state evidence establish blocking before intervention; no wrapper timeout
was necessary. A separate Event control also passes. No additional skill wrapper
is layered onto its own subprocess deadline.

Retained baseline runs 20 successful bounded child trials. Retained skill runs
one successful direct callback probe through the installed helper, reading its
reference first. It selects the wrapper because wait has no timeout despite the
inspected callback contract ensuring the signal remains set. This is not a task
failure or evidence that defensive deadlines are always waste, but selective
avoidance of the extra wrapper is not demonstrated.

Lost skill saves detailed JSON and emits a compact result, then reads selected
fields and stack entries for verification. Retained skill instead redirects helper
JSON to the required evidence file and reads the entire result back. Evidence
delivery adoption is mixed, not consistently fixed. Baseline also retains detailed
JSON with compact initial summaries; lost baseline reads its failed evidence to
repair the predicate and retained baseline reads selected verification fields.

Completed shell commands: lost baseline 7, lost skill 6, retained baseline 4,
retained skill 8. Original captured commands stay scoped; no patch rejections,
invalid JSON or event errors. Retained skill's one empty-output flag is its stdout
redirection, followed by a successful captured read. Some discovery commands exit
1 because AGENTS.md is absent, not because the diagnostic experiment failed.
All eight original fixture files match frozen inputs; all eight installed resource
records across skill cells match frozen hashes and before/after manifests. Grouped
shell final exits do not establish each intermediate status; preservation was also
checked independently from actual retained files. No author replay is credited.

All 156 repository tests pass (18.169 seconds), including the new actual-process
fixture test; repository validation passes. No candidate edits during or after
these model sessions. The favorable sum is confounded by baseline repair and
unequal verification, and does not meet the whole-bundle performance objective.
Do not rerun these exposed cases merely to chase favorable samples.
