# Persisted tool-response diagnostic — frozen before launch

Parent `56c2b4c`. One fresh Astra medium baseline session, one repeat, serial,
seed 20260915, timeout 240 seconds. Reuse the exact frozen delayed-emitter fixture
and task (`cli-yield-probe-01-cases.json`). The only requested launcher change
from the original CLI diagnostic is omission of `--ephemeral`; retain the
ignore-user-config, ignore-rules and workspace-write flags. No model retry.

Purpose: determine whether this newly created session's stored rollout retains
model-visible tool responses omitted from command-completion JSONL. First inspect
original CLI events, obtain their exact session/thread ID, and locate only that
new session's rollout by filename. Do not read unrelated session contents or
modify/delete any existing rollout, user configuration or authentication material.
Do not execute/replay the emitter to fill evidence gaps.

Keep original stdout/stderr and the new run's witnesses. Treat rollout content as
sensitive: retain locally first; export only reviewed relevant tool input/output
records with source hashes, clear excerpt boundaries and path redaction. Do not
publish system/developer instructions, unrelated context or credentials. Stored
tool responses are an additional observation channel, not a guarantee of complete
capture. Compare exact nonce/byte evidence before adopting it prospectively.

The existing emitter received native hash/length and duplicate-write checks;
this is a capture diagnostic, not scored QA or a skill-performance benchmark.
Do not update historical scores or featured charts.

Launch:
`python3 -B benchmarks/run.py --cases-file benchmarks/cli-yield-probe-01-cases.json --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 --model gpt-6-astra --effort medium --persist-session --output benchmarks/local-runs/cli-rollout-probe-01`
