# Receipt startup compatibility 01 — compatible, no efficiency transfer

2026-09-20. Resource `ca668a4`, launch `f5acd6f`;
[protocol](../../RECEIPT-STARTUP-01-PROTOCOL.md),
[fixture](../../RECEIPT-STARTUP-CASE.md), [all rows](comparison.json).
The unchanged isolated support-routing candidate is compared with fresh original
and no-skill sessions on one new authored CSV task requiring native project startup.

| Arm | Input + output tokens | Process seconds | Responses | Task / scope |
| --- | ---: | ---: | ---: | --- |
| No skill | 65,704 | 48.928 | 4 | pass / pass |
| Original | 75,355 | 55.875 | 4 | pass / pass |
| Candidate | 74,166 | 61.303 | 4 | pass / pass |

Candidate versus original: **−1.58% tokens, +9.71% time**. Versus no skill:
**+12.88% tokens, +25.29% time**. The earlier routine-screen savings did not
transfer into a joint token/time improvement here. Production Receipt remains
unchanged; do not adopt or promote the candidate as an efficiency improvement.

Full input counts cached input once; reasoning is not added again. GPT-6 Astra
medium, serial baseline/original/candidate, n=1, same shared host/cache. All three
scheduled cells completed without retries, replacements, exclusions or timeouts.
Fixed order, nonidentical extra checks and one authored case prohibit general,
causal, held-out-real-project or all-eight claims. No dollar estimate/confidence
interval. Keep this dataset separate from historical routine measurements.

## Reviewed native work

All three use handwritten disposable project-local isolation, not the helper's
unsupported project-startup replacement. They freeze the same current
`test_manifest.py`, `sitecustomize.py` and `format.json` bytes in both copies,
materialize the actual committed implementation and report full revision IDs:

- Before `dc1a0044e39c1af367031fce15027b9276caf7d5`.
- After `d973477c2b299730d2643a03f2ade52bb0c6e453`.

Each native child runs `PYTHONPATH=. python3 -B -m unittest -v test_manifest`.
The outer skill-arm orchestration uses `-S`; the native **test child does not**.
Do not confuse these distinct processes. Supplied unchanged tests verify the
project startup hook was already loaded before test import, configured `;`, and
same-process copy-local implementation/startup paths with native PIDs.

Before fails the quoted-separator and escaped-quote assertions, not setup:
`['a', '"b', 'c"', 'd']` instead of `['a', 'b;c', 'd']`, and
`['a', '"b""c"', 'd']` instead of `['a', 'b"c', 'd']`. Plain, empty and Unicode
controls pass. After all five pass. Native exits 1/0 are recorded; no skips,
monkeypatch, startup bypass or assertion rewrite. All final answers accurately
limit verification to supplied requirements/tests.

All copies are removed in finally blocks; original content, owner notes/cache,
HEAD and skill resources remain unchanged, with no extra harness/report.
Baseline checks content hashes excluding `.git` and does not audit modes;
its original operations are read-only. Both skill arms additionally inventory
all 72 original entries' bytes/modes/link text, including Git and ignored files,
and retain separate final check exits. Do not claim identical audit work or a
baseline whole-Git-metadata check. Every frozen task criterion and scope passes.

The candidate's final inventory expression repeatedly recalculates the entire
inventory inside a comprehension. This avoidable work is retained in measured
cost; its effect is not separately timed or claimed to explain wall-time changes.
Original reads both reference files, candidate only the routine guide, neither
reads helper implementation. Reading less did not reduce the response count or
avoid rebuilding native comparison/preservation orchestration.

## Evidence provenance and limitations

Original commands and correlated stored outputs were manually reviewed, not
graded from a wrapper exit alone. Baseline captures match exactly. Original
CLI item 4 omits leading fixed-input hashes retained in original output line 31.
Candidate CLI item 3 omits fixed hashes and before revision/command identity
retained in original line 29. These are capture omissions, not model retries;
the complete native assertions/provenance and preservation outputs remain.
Mechanical truncation hints on reference text are false positives; no real
tool-output truncation was found in these three sessions. Selected original
records are exported; private initial instruction text is not. Exposure reports
confirm Receipt body in initial skill-arm messages and none in baseline.

Separately labelled author preflight in [run.json](run.json) exercises native
before/after, deliberate disabled-startup RuntimeError and helper rejection of
project-hook replacement, plus preservation/cleanup. It is not model behavior or
a post-run replay. Models were not required to force helper failure; avoiding
that incompatibility directly is correct. This checks compatibility selection,
not recovery from an observed runtime error or every necessary source inspection.

No production change, featured-chart update or release approval follows. Further
read-order/routing prompt tuning on these cases is not justified by this result;
the observed remaining work is native setup/preservation code, whose safe reuse
would need its own design and verification rather than another favorable rerun.

## 한국어 요약

프로젝트 시작 설정 과제는 무스킬·기존·후보 모두 실제 오류 재현과 수정 후
검사, 원본 보존을 충족했다. 모두 지원하지 않는 도우미를 강제로 사용하지
않고 프로젝트 기본 실행 방식을 유지했다. 후보는 기존보다 토큰 1.58% 감소,
시간 9.71% 증가였고, 무스킬보다 토큰 12.88%·시간 25.29% 증가였다.

후보가 참고 문서를 덜 읽어도 비교·보존 코드를 다시 작성했고 응답 수는
같았다. 반복 파일 검사와 추가 검증 비용도 그대로 포함했다. 한 과제·각 1회,
고정 순서의 작은 실험이므로 광범위한 성능 주장에 사용하지 않는다. 호환성
선택은 검증됐지만 실제 오류 복구 전체를 검증한 것은 아니다. 이 후보를
성능 개선으로 채택하지 않으며 실제 스킬과 기존 그래프는 유지한다.
