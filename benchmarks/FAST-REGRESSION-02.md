# Combined candidate regression screen

Run revision `92db259`, nine unchanged development tasks, Astra medium, serial, one fresh skill session each. Every recorded skill hash matches the current corresponding instruction file. No retries, exclusions or timeouts. All nine processes completed and the author inspected each answer, command trace and final fixture changes against the existing criteria.

| Case | Criteria result | Total tokens | Seconds |
| --- | --- | ---: | ---: |
| history-active | Pass | 67,441 | 28.163 |
| boundary-fix | Pass | 84,120 | 36.490 |
| formatter-review | Pass | 83,518 | 31.790 |
| search-order | Pass | 67,526 | 42.717 |
| search-diagnosis | Pass | 84,421 | 43.935 |
| necessary-state | Pass | 102,734 | 51.819 |
| persistence-test | Pass | 68,300 | 43.372 |
| rolling-schema | Pass | 67,543 | 31.930 |
| search-protected | Pass | 67,262 | 42.857 |

Input plus output totaled **692,865 tokens**, with cached input included once. Summed process time was **353.073 seconds**. The earlier combined screen used 695,097 tokens and 354.333 seconds. Differences of about -0.32% tokens and -0.36% time do not establish a meaningful gain in these temporally separated, single-sample screens. Individual improvements cannot be substituted for an aggregate performance claim. Neither screen includes a contemporaneous no-skill baseline.

Boundary verification records the same age-18 assertion failing before and passing after alongside ages 17/19. Pending-state checks exercise duplicate suppression, success values, propagated errors and retry. The audit records correct/mutated existing tests and the same stronger assertion, with copied imports verified. Search cases distinguish a real reverse-completion defect from a working generation guard; diagnosis explains no-cache's limitation. Historical review cites the current caller and introducing commit. Formatter review ties removal of registration machinery to fixed USD requirements. Rollout review probes old/new readers across up/down schemas, including representative newly written data, without claiming staging verification.

Original fixture files change only in the two implementation cases: eligibility plus its regression test, and form state. QA and diagnosis add only local reproductions; other input files are preserved. Some shell commands combine checks with later printing, so final command exit alone is not treated as proof. These outcomes were reviewed from traces and artifacts, not independently replayed in this screen. They establish only the listed development criteria, not browser behavior, comprehensive safety, reliability or production readiness.

Complete local evidence is retained under `local-runs/fast-regression-02` (manifest, session traces, metadata, answers, diffs and final projects). Local package/fixture checks also passed: 42 unit tests plus repository validation.

Decision: the exact combined candidate has now received its required nine-case regression screen. It is behaviorally viable on these fixtures, but the all-skill efficiency objective remains unmet. Do not continue rerunning this unchanged set hoping for a favorable sample. Select the representative real workload and its acceptance/resource targets before additional performance tuning; preserve all unfavorable comparisons.
