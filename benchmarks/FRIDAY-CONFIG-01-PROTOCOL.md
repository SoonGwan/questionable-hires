# Friday configuration transfer 01 — 2026-09-15 KST

Resources `636935e`, unchanged since discovery screen 02. This new authored
configuration domain and nested project layout replace the repeatedly exposed
flat SQLite pair. It is still synthetic, authored after the candidate, not an
independent production dataset or proof of real-user impact.

`friday-config-cases.json` SHA-256:
`674bce852c6dbb3a50349e13aa285207d31cdc2dc9e173d06b4b7d8fb95ccd8f`.
[Generator](friday_config_cases.py), [native preflight](friday-config-preflight.json).
Both variants share actual Python loaders and all files except the release plan's
rollback-overlap configuration. Old/new consumers coexist at forward and rollback
checkpoints. Root and nested AGENTS.md carry visible scope and exact service
contract; no hidden obligation is introduced in grading. The model must discover
the manifest's versioned code paths and execute actual functions, not infer from
literal SQL or use the SQLite matrix. Any equivalent native Python method is valid.

Native author unittest accepts A and rejects B with an actual value assertion:
the old consumer silently defaults to 1000 ms during rollback overlap instead of
the contracted 7500 ms. Calls do not raise; final recovery returns 7500 ms for both
variants. Thus exception-only or final-state-only witnesses are insufficient.
Caller mappings and all input files remain unchanged; scratch is project-local
and cleaned. This author oracle is not among the ten model-visible files.

## Frozen execution and review

Four fresh sessions: baseline/explicit Friday × two variants × one repeat.
Serial Astra medium, seed 20260911, 240 seconds/cell. Preserve all scheduled cells,
limits, gaps, failures and adverse costs. No favorable retries. Stop scheduling
on account limits; no author test workloads or input/resource edits during timing.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-config-cases.json --output benchmarks/local-runs/friday-config-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

Review actual nested instruction reads, source binding, each active version's
effective timeout/attempts, config preservation, earliest failure, recovery and
production unknowns. No requirement for a fixed command count or bundled helper.
Track discovery/read duplication separately from task success. Reader grouping
must not skip relevant instructions or mixed-version consumers. Local config
evidence does not certify network latency, actual reloads or process orchestration.

After timing reconcile raw turn usage, all ten original files, installed resources
and public exports. Inspect native output before accepting final claims. Retain
author replays separately if needed; they cannot fill missing original captures.
Report both pairs and unequal work, not only favorable totals. With n=1 and two
related variants, no general 20–30% claim or automatic featured-chart promotion.

The [official OpenAI evaluation guide](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
informs scoped criteria and the need to distinguish this authored sample from
real-world distributions.

## 한국어

SQL 대신 실제 Python 설정 로더와 중첩 프로젝트 지침을 사용하는 새 과제 2종을
고정했다. 설정 키가 바뀌는 혼합 버전 롤백에서 함수 호출은 성공하지만 제한시간이
7500ms 대신 1000ms가 되는 결함을 포함한다. 정상 과제·실제 값 불일치·최종 복구를
사전 실행으로 확인했다. 정답 테스트는 모델에 주지 않는다.

새 기준군과 Friday를 각각 실행해 4세션을 비교할 예정이다. 지침 읽기와 코드
실행·설정 보존을 함께 검토하며, 명령 수나 유리한 합계만으로 성공을 판정하지
않는다. 새 작성 예제이지만 실사용 데이터는 아니고, 전체 성능 개선도 아직 미입증이다.
