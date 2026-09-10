# Fast iteration 01: audit scaffolding overhead

Two fresh sessions on `persistence-test`, baseline versus candidate `de1eb4f` (run manifest at `602ff02`), Astra medium, serial, one sample each. Local evidence: `benchmarks/local-runs/fast-con-artist-01`. This is an exposed development case, not independent generalization evidence.

Both answers identify a surviving missing-append mutation and a stronger contents assertion; both leave original production/test files unchanged. Baseline elapsed 41.150 seconds and used 64,177 total tokens; skill elapsed 99.638 seconds and used 127,558 total tokens (input plus output, cached already included). A single sample does not establish a stable performance difference.

The skill created `audit/run_audit.py` and `audit/results.json`, ran the original baseline and another isolated baseline, and made extra inspection/output calls. This is observed overhead, not proof of a sole causal explanation. The task did not request a reusable audit tool. Baseline supplied the same core conclusion without retained scaffolding.

Correction: remove the implied requirement for a retained evidence artifact, explicitly allow one short inline isolated experiment for small tasks, and reuse an already valid baseline. Keep reachability, import verification, original-file preservation and correct/faulty regression checks. Do not trade those requirements away to reduce tokens.

Next check: rerun this same development task once with the revised skill, without re-running a whole matrix. Preserve both earlier runs, report temporal/cache confounding against the prior baseline, and do not call it a held-out performance win. Further evidence must check that larger tasks can still retain useful harnesses.
