# Existing-runner interaction screen

Freeze this protocol and fixture before any model session. One exposed synthetic
task, baseline and explicit Mother-in-law, one repeat each, serial execution,
GPT-6 Astra medium, seed 20260912, outer session timeout 240 seconds. No retries,
exclusions, prompt edits, or skill edits during the run. This is a small adoption
screen, not held-out superiority evidence or an estimate of broad performance.

Both arms receive identical source, requirements and an existing documented
POSIX runner copied from the repository's Exorcist helper at b1722f4. No other
skill is required or installed for the skill arm. Existing runner reuse is an
observed implementation choice, not a retrospective correctness criterion.
The fixture intentionally makes this route available; transfer is unproven.

Review actual commands, assertions, normal/reversed outputs, deadline handoff,
original-file preservation and complete usage. Missing decisive output remains
unknown. Compare input-plus-output tokens and process wall time only with the
observed coverage differences disclosed. Prior cancellation-resistant cleanup
checks validate this runner separately; they are not model behavior evidence.

Run from repository root:

```sh
python3 benchmarks/run.py --cases-file benchmarks/interaction-runner-cases.json --output benchmarks/local-runs/interaction-runner-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260912 --timeout 240
```
