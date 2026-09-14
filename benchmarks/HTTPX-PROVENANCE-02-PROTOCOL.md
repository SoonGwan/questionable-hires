# Provenance adoption screen 02 — 2026-09-15 KST

Completed: [original evidence review and public trace](results/httpx-provenance-02/README.md).

Freeze resources `b044a19` after the [proportional provenance change](CON-ARTIST-PROVENANCE-01.md).
Use unchanged HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, the existing
`audit` / `asgi-exceptions` task, same supplied interpreter and native configuration.
One fresh **skill-only** Astra medium session, repeat 1, seed 20260912, timeout
360 seconds. No fresh baseline: previous costs are historical observations, not
a concurrent performance comparison. This is an exposed authored task, not a
new holdout or maintainer request. Keep previous adverse results accessible.

Review whether the agent establishes actual native fault detection and copied
implementation provenance without adding redundant post-collection instrumentation.
An explicit requirement or unresolved binding can still justify a hook. Native
test identities/results, real failure mechanism, preservation and scope remain
required. No fixed command count or helper-adoption requirement; no stronger test
is needed for an already detected fault. The original task does not mandate deleting
retained diagnostics. Reject support errors as behavioral evidence.

Repeat the existing author preflight before launching; normal 24-pass ASGI suite,
4 actual missing-exception failures after propagation removal, and discriminating
client witness. Keep its output outside model context at
`benchmarks/local-runs/httpx-provenance-02-preflight.json`. The runner also performs
its unchanged 36-test WSGI/ASGI preflight. Do not alter fixtures or resources or run
author test workloads during model timing. Preserve failed/incomplete outcomes;
no retries, stop on account limits and re-poll live handles after observation timeout.

```sh
python3 -B benchmarks/run_httpx.py \
  --source /tmp/qh-httpx-preflight.3Slnqw/httpx \
  --python /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python \
  --profile audit --case asgi-exceptions --arms skill --repeats 1 \
  --skill-revision b044a19 --output benchmarks/local-runs/httpx-provenance-02
```

Retain original native outputs, usage and resource hashes; reconcile before public
claims. Report total input (cache included once) + output and process elapsed time,
with unequal-work limitations. No causal or broad 20–30% claim and no featured
chart update from this one adoption check. If uptake is supported, move to a different
workflow with fresh comparisons instead of repeatedly tuning this exposed case.

한국어: 수정한 출처 확인 지침을 기존 HTTPX 과제에서 스킬 1회로 확인한다.
새 기본 모델이 없어 과거 비용 비교는 참고치일 뿐이다. 실제 결함 탐지·호출 출처·
원본 보존은 유지하고 중복 계측을 줄였는지 본다. 실패·누락도 보존하며 재추첨하지
않는다. 채택이 확인되면 이 과제 반복 대신 다른 작업의 새 비교로 이동한다.
