# Slugify native01 — frozen model comparison

2026-09-21. One verified-audit task on unchanged selected python-slugify files
at `f85f9488520148d5f6899b5639199882b605e30a`. Three Astra medium sessions,
n=1, serial current/baseline/prior order,360s each, shared host/cache.
Prior resources `387c53b`; current `a7dcbd8`; no-skill baseline contemporary.
Both skill arms have the same runtime/entrypoint; only the native recipe differs.
No helper use is required. Equivalent native orchestration is permitted.

Hypothesis: describing existing-witness selections in the native recipe avoids
unnecessary probe/common-guide reads without sacrificing required verification.
The task is a root-package project, not a source-root test. It is author-inspected
development evaluation, not a blind holdout, full-project test or all-eight gain.
[Preparation and upstream identities](SLUGIFY-NATIVE-01-PREFLIGHT.md) retain
real assertion controls. The runner repeats those controls before freezing.

Every arm receives identical selected files, scope and task. Three faults are
confined to slugify(): omit custom separator conversion, ignore save_order when
calling smart_truncate, and omit requested truncation. Selected methods are
test_non_word_characters and test_max_length. Existing or newly added disposable
assertions must verify custom separators and order-preserving truncation.
Correct controls, all six faulty outcomes, actual stronger assertions, copied
same-process function binding, original preservation and scratch cleanup are
explicit model-visible obligations. Individual native method results in a grouped
suite are valid; separate exit codes are not required. Correct observations may
be reused when identified. No extra full-suite requirement is introduced later.

Expected selected exits: `[0,0]`, `[0,0]`, `[0,1]`. Original custom-separator and
save-order witnesses distinguish the matching gap faults; the save-order witness
also fails omitted truncation, so diagnosis must not confuse independent faults.
Exact author patches and expected outcomes are not added to model inputs. All
arms can read the full unchanged upstream test file and its existing witnesses.
The common runner suffix calls prepared fixtures a synthetic project; AGENTS
explicitly identifies this selected upstream tree. Scoped interpreter/dependencies
are supplied, read/execute only, with no installation allowed during model work.

Freeze fixture/runner/protocol/test hashes, interpreter, resource snapshots,
schedule and settings before launch. Exclusive execution marker prevents repeats.
Recognized account limits stop later scheduling, preserving unrun slots. Keep
all original attempts, repairs, failures, extra work, timeouts and unused-helper
outcomes. No concurrent author tests during measured sessions. Do not change the
candidate or fixture after launch, or replace an unfavorable attempt.

Review actual original tool evidence, native assertions, startup/binding checks,
scope and cleanup. Initial skill-body exposure must be checked separately from
later rereads. Preserve raw sessions privately, export reviewed/redacted records,
and disclose capture omissions. Author replay is not original model evidence.
Report input+output tokens with cached input counted once, process wall time,
response counts and actual work. Even a favorable n=1 does not establish general
20–30% gains or justify changing the featured graph.

한국어: 이전 안내·현재 안내·무스킬을 과제1개, 총3세션으로 비교한다. 실제
원본 테스트를 유지하고 결과·검증·정리 요구를 동일하게 고정한다. 도구 사용을
강제하지 않으며 문서 탐색과 복구 비용도 모두 포함한다. 불리한 결과나 미사용
시도를 버리지 않고 대표 그래프와 전체 성능 주장은 별도로 유지한다.
