# Short Friday guide: adoption screen 01

2026-09-14, resources `ce82fcb`. One fresh explicit-skill Astra medium session,
one job, seed 20260911, 240-second bound, no favorable retry. Unchanged exposed
`rolling-schema` case from bundle-contract-v2-cases.json (SHA-256
`1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`).
No prior answers, author recipes or intended findings are supplied to the model.

The core reference is smaller, runtime and entrypoint unchanged by that edit.
Existing 35 matrix tests pass, including actual guide JSON/API execution,
incompatible readers and rollback data. During timing: no author tests or
resource/task edits. Preserve all attempts, errors, unknown usage and capture gaps.

Review actual loaded references and implementation reads, helper/API adoption,
extra source extraction or repeated SQL, required initial/up/down reader queries,
new-schema insert/update and surviving values. Distinguish observed SQL from
unprovided application-writer/staging evidence. Reconcile raw usage/events,
installed hashes, unchanged release files and any added artifacts. Capture full
original recipe/results where available; a later author replay cannot fill gaps.

Report absolute tokens/time. Earlier checkpoint 07 used 109,377 tokens / 45.151s
for its skill cell; different generated work, intervening changes, n=1 and shared
host/cache prevent causal efficiency attribution. Document-byte reduction is not
token reduction. No featured promotion or identical retry to seek a better number.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-v2-cases.json --case rolling-schema --output benchmarks/local-runs/friday-core-guide-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
