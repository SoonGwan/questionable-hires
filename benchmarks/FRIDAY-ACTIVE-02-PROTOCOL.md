# Friday discovery screen 02 — 2026-09-15 KST

Candidate resources `636935e`: only the entry's grouped-read/discovery paragraph
changes from active-01. See [candidate rationale](FRIDAY-DISCOVERY-02.md) and
[adverse prior observations](FRIDAY-ACTIVE-01-REVIEW.md).

Two new explicit-Friday sessions, one per already exposed active-release variant,
one repeat, serial Astra medium, seed 20260911, 240 seconds/cell. No fresh baseline;
any cost comparison is historical development feedback, not a paired experiment
or held-out validation. Same frozen `friday-active-cases.json`, SHA-256
`c3fdfb8392a7608dd634365291d6326c2560fd934c81a3d95f87790fac0d0ede`.
Existing native positive/negative preflight and model-visible contracts remain
unchanged. No author oracle or earlier conclusions are provided to the model.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-active-cases.json --output benchmarks/local-runs/friday-active-02 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

Inspect actual initial reads, repeated inventories, Git object discovery, scoped
instruction discovery and follow-up source reads. Reduced command count alone
does not pass: retain current SQL/query binding, exact columns/rows, active-reader
classification, first failure, post-write rollback recovery and production unknowns.
Equivalent native methods and justified evidence reuse remain valid. No helper
adoption requirement or ban on needed follow-up questions/checks is introduced.

Retain both scheduled outcomes, failed commands, capture gaps, timeouts and unknown
usage. Stop on account limits, no selected retries or author workloads/edits during
timing. Reconcile raw usage, input/resource integrity and export all evidence before
reporting. No historical/featured graph changes. If discovery does not improve,
reconsider the extra paragraph instead of adding increasingly rigid instructions.

The [official OpenAI evaluation guide](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
informs the task-specific behavioral review and separation from broad claims.

## 한국어

수정된 Friday를 기존 과제 2종의 새 세션에서 확인한다. 신규 기준군이 없고 이미
본 과제이므로 개발용 행동 검사이며, 과거 수치와의 차이를 일반 성능 향상으로
해석하지 않는다. 탐색 횟수뿐 아니라 중간 오류·실제 데이터 복구·파일 보존·
미검증 범위가 유지되는지 확인한다. 두 결과와 불리한 관측도 모두 보존한다.
