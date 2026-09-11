# Conditional runner routing: selection recovers, efficiency remains mixed

Revision `3ededb6`, clean execution HEAD `413922f`. One fresh Astra-medium skill
session on `runner-environment-timing`; no baseline rerun, model retry, exclusion
or full-team screen. Raw evidence: ignored `local-runs/exorcist-conditional-01`.

| Same development case | Input including cache + output tokens | Seconds |
| --- | ---: | ---: |
| Earlier setup-routing `a060148` | 69,483 | 53.601 |
| Direct helper interface `34aedd4` | 116,325 | 90.214 |
| Conditional helper route `3ededb6` | 88,482 | 61.371 |

Against the immediately preceding adverse sample: 23.9% fewer tokens, 32.0% less
time. Against the earlier setup-routing sample: 27.3% more tokens, 14.5% more time.
Both references matter. These single separated samples do not isolate causality
or establish stable efficiency recovery.

The current trace does not read the optional helper/reference or invoke the
wrapper. It uses a retained three-child harness with ten-second subprocess limits.
No overlapping async signal wait exists here. The generated harness correctly
observes the actual test's setup on its first attempt, unlike the preceding sample;
avoiding that repair is another confound, not solely a routing effect.

The original unittest command reproduces `AssertionError: 3 != 1`. Fresh child
processes then run the actual test and setup with startup variable absent versus
zero: environment becomes zero in both, but the imported retry constant is two
versus zero, producing failure versus success. A separate standalone actual-worker
callback runs once with startup zero. The answer explains the import boundary,
preserves startup semantics and leaves live-configuration policy unspecified.

Author inspection confirms all three original files and four installed skill
resources match fixture inputs and committed blobs. A separate direct replay of
the retained harness passes its assertions. No rejected patch, timeout or capture
diagnostic. These checks support behavior and preservation, not broad scope or
performance guarantees. The captured harness output omits its initial absent-
environment child's two print lines, despite a successful final status. The
separately captured original unittest does show `3 != 1`; the author replay
supplies the full setup-observation output. Do not retroactively attribute that
replayed output to the model capture. A clean diagnostic flag is not proof of a
complete stream, as this case again demonstrates.

Disposition: retain the conditional route as successful avoidance of redundant
tool use in this sample, not a proven efficiency win. The async branch after this
routing change remains unmeasured; screen 05 also predates it. Do not repeatedly
rerun this unchanged control or discard the higher-cost history.
