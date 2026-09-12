# Tool-backed audit on real HTTPX

Pinned HTTPX revision and preinstalled environment are unchanged. Both preflights passed 36 tests. Two separate one-cell runs used Astra medium, serial, a 360-second cap, identical task text apart from the skill invocation, no retries or exclusions. Skill resources were frozen at `8c56744`. The skill session ran first and baseline second; this is not a randomized or repeated controlled comparison.

| Condition | Input + output tokens | Process seconds | Behavior demonstrated |
| --- | ---: | ---: | --- |
| No skill | 194,786 | 135.817 | No-op cleanup caught indirectly; early-close fault survives; explicit close and context-exit proposed tests detect it |
| Con Artist + helper | 113,784 | 57.846 | Early-close fault survives; explicit-close probe detects it, with generator retention preventing incidental GC cleanup |

Cached input is already included once. Descriptive differences are about 41.6% fewer tokens and 57.4% less time for the skill session. **Coverage effort differs:** baseline explores two mutations and tests two closing modes; skill explores one mutation and tests explicit close inside a stream context. Both establish the targeted early-close coverage gap, but this is not equal-depth verification or proof of equivalent general coverage. Do not present these percentages without that qualification, extrapolate to all eight skills, or treat one pair as a stable speedup.

Compared with the earlier no-helper skill sample in [HTTPX-COMPRESSED-01](HTTPX-COMPRESSED-01.md), the tool-backed sample used about 26.7% fewer tokens and 44.4% less time. Those sessions also differ in mutation mechanics and probe details, and are temporally separated.

## Behavioral evidence

The helper recipe moves iterable cleanup to completed iteration and makes the close method a no-op. Its unchanged upstream tests pass on correct and faulty code (12 each). The same additional probe passes correct code and fails the mutant specifically because closing the response did not release its partially consumed iterable. It keeps the generator alive so garbage collection cannot hide the defect.

The author inspected the complete recipe and commands, extracted the actual JSON recipe from the trace, and independently replayed it through the frozen helper: correct tests 0, correct probe 0, mutant tests 0, mutant probe 1, with the intended cleanup assertion failure. Four frozen resource hashes were independently checked. Provenance audits for both runs confirm all 125 tracked upstream files preserved, source revision matches, and no recorded patch rejection. Final snapshots cannot prove absence of every transient or outside effect. No ancestor-directory inspection appears in the four skill command traces, unlike the earlier no-helper skill run.

The baseline's additional experiments and stronger two-mode test are genuine evidence, not automatically waste. They are retained and must not be silently excluded from the comparison. Baseline outcomes were reviewed from retained output/artifacts, not independently replayed in this iteration.

Local complete evidence: `local-runs/httpx-tool-01` and `local-runs/httpx-tool-baseline-01`. These include manifests, original logs, traces, snapshots and metadata. Full upstream evidence has not been exported for publication; preserve its BSD license when doing so.

## Mechanism and next validation

The skill session used four shell calls and one stdin recipe rather than constructing standalone copy/mutate/run scripts and reports. This supports the intended orchestration change; it does not isolate its causal contribution from model variation or narrower exploration. The helper remains optional because tiny synthetic tasks showed increased total context cost in [CON-ARTIST-TOOL-01](CON-ARTIST-TOOL-01.md).

Before the run, the HTTPX runner was corrected to freeze the entire skill tree, not just its two original instruction/metadata files. File-level resource hashes now accompany the historical instruction hash. A regression test covers helper/reference export and no-overwrite behavior; all 55 local tests pass. The character identity and scope of the eight hires remain unchanged. The overall performance goal is still open; broader, bounded workload evidence is required.
