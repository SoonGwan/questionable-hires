# Scoped discovery: configured caller retained, mixed efficiency evidence

[Protocol](NECROMANCER-DISCOVERY-PROTOCOL.md), fixture/runner `b220872`;
predecessor `0143ef2`, candidate `51ce19e`. Four fresh serial Astra medium sessions
ran in declared order, one per task/version, 240-second limits. All completed,
without retries, exclusions or timeouts. Raw local artifacts and pre-run resource
hashes: `local-runs/necromancer-discovery-01/`.

| Task | Predecessor tokens / seconds | Candidate tokens / seconds |
| --- | ---: | ---: |
| Configured consumer | 87,213 / 37.448 | 87,081 / 37.483 |
| Packaging review | 119,591 / 64.462 | 93,600 / 59.790 |

Configured consumer: −0.15% tokens / +0.09% time. Packaging: −21.73% / −7.25%.
Input/output/cache respectively: configured predecessor 86,423/790/72,704,
candidate 86,280/801/78,848; packaging predecessor 118,206/1,385/102,528,
candidate 92,321/1,279/72,960. Cache is included in input once; reasoning output
is not added again. No no-skill baseline, dollar estimate or causal attribution.

## Configured consumer

Both inspect app.py, JSON configuration, records and the active adapter under
integrations/archive. Both keep the None fallback and execute its removal in
memory through the actual application, observing AttributeError on the null
record. Both restore the original binding and assert the original application
returns `["A", "unknown"]`. Neither mistakes the archive directory for dead code.

Candidate's captured standalone command shows the original application result
and one passing unit test. Its mutation probe checks string trimming directly.
Predecessor instead reruns the unit suite against the mutation and asserts success
before printing the application failure and successful restoration. Its earlier
original app/unit commands are present, but those initial outputs are missing
from the captured combined result. The final shell exit cannot prove those
earlier commands passed. Original application correctness is separately asserted
after restoration; original-unit execution success remains incompletely captured
for this arm. Do not mark every original check fully evidenced merely because
the answer claims success. No author rerun fills this model-evidence gap.

Candidate uses a file inventory excluding examples/vendor/generated directories
but follows the explicit configuration into integrations/archive. This single
countercase does not prove it would recover every legitimately configured path
in an excluded directory. Shell calls increase from four to five; costs are
essentially unchanged, not a speed gain.

## Packaging

Both pass five original build tests and demonstrate removal leaving partial
output for OSError, RuntimeError and KeyboardInterrupt. Candidate runs the focused
cleanup test against the mutation; predecessor runs all five tests. Both inject
a catalog-copy failure and compare original successful retry against failed
retry after removal. Predecessor fails before copying the catalog, candidate
after copying it. These are unequal probes, not identical executed work.

Candidate searches concrete import/caller patterns in scripts, tests, packaging,
metadata and README instead of broad package contents. It still performs separate
discovery and skill-read commands. Both use eight completed shell calls.
Candidate's empty AGENTS search exits 1; predecessor's search of an absent .github
path exits 2. These are discovery results, not behavior-test failures. Candidate
has one empty-output diagnostic for that search. Some tool results start
mid-stream, so clean flags elsewhere do not prove complete output capture.

Both original test runs emit local Xcode cache/filesystem warnings. Predecessor
also removes a generated xcrun_db file before its final clean diff. Shared-host
effects, different cleanup and test scope prevent assigning the measured savings
solely to narrower discovery. Neither excavates the snapshot as upstream history.

All 84 original file instances match fixture bytes, all diffs are empty, and all
16 installed resource instances match frozen hashes and before/after manifests.
No production edits, installation or publication occurred. Packaged skill text
and helper execution remain part of the real packaging fixture, as documented
in the [previous adverse transfer](NECROMANCER-PACKAGING-REVIEW-01.md).

Retain the candidate as a scoped-discovery candidate, not a broadly faster skill.
The observed configured path remains protected and packaging has a favorable
single pair, but incomplete predecessor capture, unequal work, shared host/cache
and exposed development fixtures limit acceptance. The requested whole-bundle
token/time improvement is still unproven. Preserve all prior favorable and adverse
results; do not rerun unchanged cells to select a better score.
