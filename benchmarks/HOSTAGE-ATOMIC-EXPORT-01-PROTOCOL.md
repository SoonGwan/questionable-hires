# Atomic report export: prospective Hostage transfer

Candidate skill: `5867752` known-path routing; runner/fixture revision is recorded
when executed. [Frozen task file](hostage-atomic-export-cases.json) contains one
new authored developer task, not a maintainer ticket or independent real-repo
holdout. Existing form/packaging cases and their adverse results are unchanged.

The task names the exporter but leaves test and nested guidance discovery to the
agent. Root instructions specify the same standard-library unittest command for
both arms. Requirements make destination/input/exception/cleanup contracts
explicit and exclude unrelated durability, mode preservation, symlink and
concurrent-writer guarantees. Streaming and the existing API remain required;
success by buffering all rows is not accepted. Do not add new safety criteria
after observing outcomes, or treat reasonable findings as false positives.

Author preflight: `tests/test_hostage_atomic_fixture.py` executes four actual
assertion-bearing tests. Original code has two passing compatibility controls
and two failures: existing destination bytes are replaced with partial output,
and an absent destination is created on late iterator failure. Both failure
checks also require original exception-object identity and no leaked output.
The author-only temporary-file/replace implementation passes the identical four
tests. Original model-visible test bytes remain unchanged. This verifies the
fixture contract, not a model solution; author checks and implementation are
outside the task file and must never be supplied to either model.

## Schedule and review

Two fresh serial GPT-6 Astra medium sessions, baseline and skill, one repetition
each, seed 20260911, 240-second deadline, no retries/exclusions. Before scheduling,
commit the fixture/protocol and verify the installed skill is still `5867752`.
Use an unused output directory with the existing runner:

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-atomic-export-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 \
  --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/hostage-atomic-export-01
```

Do not run heavy author tests during model timing. Preserve every scheduled
cell, failed call, repair, skipped check and missing output. The manifest's
task/resource hashes and schedule are authoritative. If interrupted, inspect
the live handle; do not restart because output has not yet appeared.

Review actual before failure and unchanged after assertions, both failure
contracts, exception identity, cleanup, success/Unicode/empty output/count,
streaming, original test AST preservation, production scope, applicable guidance
and dependency use. Compare final artifacts and commands, not just final prose.
Run the same hidden contract tests after timing on disposable copies of both
solutions and label those as author replay, not original model evidence.

Inspect known-path reuse versus repeated inventories and command/output capture.
Report total input including cache once plus output tokens, process wall time and
workload differences. Equal core requirements do not guarantee identical work.
One synthetic pair cannot establish broad gains or causally isolate the wording
change; it can reject a broken candidate or expose further workflow costs.
No representative chart update or whole-bundle acceptance follows from this pair.
