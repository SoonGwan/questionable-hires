# Nearby history decisions: correct, still costlier

Frozen e68f6aa, main 8454059, helper 6318b91, reference 3157ee2. Original serial
runner completed baseline and skill with exit 0, no retries/exclusions. Raw records
remain in local-runs/history-regions-01; generated input is reproducible with
history_region_cases.py. This is one authored transfer pair, not held-out proof.

| Arm | Input + output tokens | Seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 70,342 | 47.743 | 6 |
| Skill | 91,487 | 58.711 | 4 |

Skill costs +30.06% tokens / +22.97% time. Cached input is counted once. Fewer
completed shell calls do not imply fewer total model tokens or less elapsed time.

Both retain code fallback and negative guard, permit removing only the private
display-name fallback, and preserve caller normalization. Both cite actual origins
344a94f, d2ec651, ca90556 and later caller change 9c88336. Both inspect patches
and execute the actual consumer binding with each independent in-memory variant.
Existing four tests pass currently; code removal produces one failure/two errors,
name removal passes, guard removal fails one assertion. Both also compare 27
missing/empty/populated code/name combinations with negative/zero/positive amounts:
15, zero and nine changed outcomes respectively. Positive amount is 2 in baseline
and 3 in skill; verification is closely matched, not literally identical input.

Baseline reviews all five commits, broad log/stat output and rereads numbered
source. Skill uses focused blame for summary and caller plus relevant patches,
but also logs requirements history and repeats code via search/numbered reads.
Neither reads the collector reference or invokes trace.py. The new range guidance
and collector runtime improvements therefore have no demonstrated adoption or
causal performance benefit in this task. Native Git is sufficient; don't force
helper use to create an apparent win.

Original captured output records actual baseline passes and all variant counts.
Baseline prints full unittest failure reports; skill prints counts and selected
changed outcomes after running tests into StringIO. Those are distinct evidence
granularities. Grouped shell final exits alone are not each check's status. Both
experiments compile complete module text into a fresh namespace and replace the
actual consumer's summarize binding; changes are restored in memory. No author
replay is credited as model execution.

All eight original file instances match input bytes, diffs are empty, and four
installed skill resource entries match frozen Git SHA-256 plus before/after
manifests. Recorded commands stay scoped. Metadata reports no malformed JSON,
empty-output flags, event errors or patch rejections; this does not prove exhaustive
capture or every transient action. No implementation, publication or installation.

The broad efficiency objective remains unmet. Keep this adverse pair and do not
add a case-specific instruction or rerun it solely to improve scores. Actual
workflow cost, not just collector CPU or shell-call count, remains the problem.
