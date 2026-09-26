# Interpreter route01 costs — 2026-09-27

Measured Necromancer candidate `e918d02d`, predecessor `75183f2f`, launch
`07d9d2ed`. [Frozen protocol](INTERPRETER-ROUTE-01-PROTOCOL.md),
[all six cells](results/interpreter-route-01/comparison.json),
[exact response arithmetic](results/interpreter-route-01/input-cost-analysis.json).
All six serial sessions completed without timeout, replacement or account-limit
stop. Original matching session counters reconcile with CLI totals; original turn
contexts confirm GPT-6 Astra medium. Cache is a subset of input, counted once.

| Project interpreter | No skill tokens / seconds | Predecessor tokens / seconds | Candidate tokens / seconds |
| --- | ---: | ---: | ---: |
| Unspecified |109,955 /141.554 |118,008 /128.155 |100,978 /137.556 |
| Documented |92,165 /129.471 |95,599 /115.923 |102,492 /110.740 |
| Sum |202,120 /271.025 |213,607 /244.078 |203,470 /248.296 |

Candidate versus no skill: tokens **+0.67%**, time **−8.39%**.
Candidate versus predecessor: tokens **−4.75%**, time **+1.73%**.
Neither aggregate improves both costs. Preserve both tasks and every attempt;
the favorable unspecified/no-skill pair does not justify a general efficiency claim.

Initial original-output inspection shows unavailable `python` launches in the
unspecified no-skill/predecessor cells, followed by `python3` recovery. Candidate
discovers the executable with initial source reads instead. The instruction's
intended behavior is observed, but avoiding that launch is not demonstrated joint
cost saving. Complete original native assertion/binding, command-output, scope,
artifact and cleanup review remains pending. CLI completion is not a quality score.

These tasks share identical code/history and differ only in documented interpreter.
Source and cancellation controls were previously exposed development material;
this is a correlated n=1 control pair, not independent validation or causal proof.
Reconstructed local commits are not complete upstream ancestry. Native author
controls, older integration05 evidence and original model work remain separate.
Full private sessions stay in local storage; published tool records are path-redacted
derivatives with original line hashes. No private initial contexts are published.

No featured promotion, all-eight efficiency claim or completed update. The owner
objective and final candidate release checks remain unfinished. Do not rerun this
pair until favorable or remove required behavioral checks to lower its cost.

한국어: 실행기 미지정/문서 지정 조건 6회를 모두 보존했다. 후보 `e918d02d`는
미적용 대비 합계 토큰0.67% 증가·시간8.39% 감소, 이전 후보 대비 토큰4.75%
감소·시간1.73% 증가다. 두 비용이 함께 줄지 않았다. 없는 명령 재시도를
피한 동작은 관찰했지만 비용 절감 원인으로 단정하지 않는다. 노출된 개발
코드를 재사용한 상관된 비교이며 원본 품질·보존 상세 검토는 미완료다.
