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
