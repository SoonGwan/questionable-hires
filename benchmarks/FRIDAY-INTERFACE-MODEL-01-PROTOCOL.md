# Friday conditional interface model screen 01

Instruction resource `1c483b9`, runtime `bef0937`; this protocol's commit is launch.
Two tasks, fresh baseline/skill n=1 per task, four serial Astra medium sessions.
No old-versus-new causal claim: compare current behavior against no skill and
inspect which interface details are actually needed/read.

Inputs are frozen before scheduling:

- Existing `rolling-schema` selected from bundle-contract-v2-cases.json,
  SHA-256 `1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
- New `binary-rollback` in friday-binary-rollback-cases.json,
  SHA-256 `e81ecad7fd169c0c34d00d25be3fcb13bcd76eaa990857d77b36ecfc78b9371f`.

Both are authored development tasks; new authoring is not independent holdout or
organic use. The binary case uses actual bytes/hex conversion and a stopped-
consumer maintenance window. Native preflight: two binary controls pass in
0.003s (wrong supplied down with intended byte AssertionError, correct decoding
control); 29 matrix tests pass in 0.389s. Author controls are not model inputs.
The new fixture makes required checks/strategy and unavailable evidence explicit.

Run binary first, then rolling schema, seed 20260914, jobs=1, 240s/cell. Preserve
all attempts, no favorable-result retries/exclusions. No skill/task/criteria edits
or author test workloads during timing. Stop scheduling on account limits;
re-poll confirmed live handles instead of restarting on observation loss.

For binary, review actual reader results/types and current represented values
before down against updated/untouched/inserted/empty payloads afterward. Query
success must not hide incorrect bytes. Assess the explicit maintenance strategy,
not a fictitious overlap blocker; wrong representation is not proven irreversible
loss. For rolling, retain actual relevant reader/schema and new-write survival
verification and rollout/rollback findings. No staging/writer evidence is supplied.

Neither task mandates the helper or a particular reference read. Native Python,
CLI and API are valid when they preserve actual query/data binding and required
checks. Record core/detail loading, helper adoption, custom setup and extra work;
skipping irrelevant reference text is not skipping a scored obligation.

After all timing, review/reconcile originals, terminal usage, resource hashes and
source preservation. Keep incomplete usage unknown, connection/capture errors
visible, and author checks separate from model evidence. New artifacts require
their own scope/inventory review. Report both pairs including adverse outcomes;
n=1, exposure, shared host/cache and unequal work limit inference. Do not change
featured charts or infer general/all-eight gains from this small screen.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-binary-rollback-cases.json --output benchmarks/local-runs/friday-interface-model-01-binary --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 --model gpt-6-astra --effort medium
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-v2-cases.json --case rolling-schema --output benchmarks/local-runs/friday-interface-model-01-rolling --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 --model gpt-6-astra --effort medium
```
