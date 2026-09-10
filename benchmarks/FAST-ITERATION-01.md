# Fast iteration 01: audit scaffolding overhead

Two fresh sessions on `persistence-test`, baseline versus candidate `de1eb4f` (run manifest at `602ff02`), Astra medium, serial, one sample each. Local evidence: `benchmarks/local-runs/fast-con-artist-01`. This is an exposed development case, not independent generalization evidence.

Both answers identify a surviving missing-append mutation and a stronger contents assertion; both leave original production/test files unchanged. Baseline elapsed 41.150 seconds and used 64,177 total tokens; skill elapsed 99.638 seconds and used 127,558 total tokens (input plus output, cached already included). A single sample does not establish a stable performance difference.

The skill created `audit/run_audit.py` and `audit/results.json`, ran the original baseline and another isolated baseline, and made extra inspection/output calls. This is observed overhead, not proof of a sole causal explanation. The task did not request a reusable audit tool. Baseline supplied the same core conclusion without retained scaffolding.

Correction: remove the implied requirement for a retained evidence artifact, explicitly allow one short inline isolated experiment for small tasks, and reuse an already valid baseline. Keep reachability, import verification, original-file preservation and correct/faulty regression checks. Do not trade those requirements away to reduce tokens.

Next check: rerun this same development task once with the revised skill, without re-running a whole matrix. Preserve both earlier runs, report temporal/cache confounding against the prior baseline, and do not call it a held-out performance win. Further evidence must check that larger tasks can still retain useful harnesses.

## Follow-up observation

Revision `1ec2490`, one fresh skill-only session in `fast-con-artist-02`: 45.965 seconds, 86,223 total tokens. The agent used one short inline isolated experiment rather than retained runner/report files. It verified copied imports, showed the existing test surviving the lost write, and ran the same stronger contents assertion against correct and faulty implementations. Source and tests stayed unchanged; diff was empty and no patch rejection was recorded.

Relative to the immediately preceding skill sample, observed tokens fell about 32.4% and elapsed time about 53.9%. Against the earlier no-skill sample, tokens were still about 34.4% higher and time about 11.7% higher. These are descriptive single-sample development observations with temporal/cache confounding, not a general improvement claim.

A remaining avoidable step was trying unavailable pytest despite the existing test importing unittest, then falling back to unittest. The next narrow correction directs runner selection from the repository's documented command or test imports/configuration, without adding a framework. No criteria or expected outcome changed.

## Compressed decision rules

Revision `b7a768d` consolidates repeated setup, evidence and delivery instructions while retaining fault reachability, baseline validity, copied-import verification, isolation, test configuration, identifiable statuses, same stronger check on correct/faulty code and user scope. No general-purpose audit helper was added: its configuration overhead has not been shown cheaper than the small inline experiment.

One fresh session in `fast-con-artist-03` used 67,931 total tokens and 39.295 seconds. [Sanitized evidence](results/fast-con-artist-2026-09-11/run.json) retains the trace, output, source hashes and final files. The author inspected the actual commands: a single isolated experiment ran the existing test and stronger contents assertion on both correct code and the missing-write mutant, verified the copied import, and checked original source/test hashes before cleanup. The resulting diff is empty. All three fixed development criteria are met.

Compared descriptively with the most recent paired skill sample (86,228 tokens, 44.919 seconds), tokens were 21.2% lower and time 12.5% lower. Against that run's baseline (80,188 tokens, 44.416 seconds), they were 15.3% and 11.5% lower. These temporally separated single samples do not establish a causal or stable speedup. Against the earlier, cheaper baseline in the first section, this sample still uses more tokens. Do not select only the favorable baseline or advertise a general win.

Four shell calls were used, the same count as the most recent paired skill sample; different orchestration inside a call and model turns matter. Shorter skill text or shell-call count alone cannot explain the token difference. This checks a lost-write survivor, not larger repository audits, already-detected faults, or unavailable environments. Those remain validation gaps for the compressed candidate.
