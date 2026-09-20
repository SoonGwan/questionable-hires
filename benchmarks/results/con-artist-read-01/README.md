# Con Artist known-input reading 01 — not adopted

2026-09-20. Resources `eeadccb`, launch `b9c29e9`.
[Frozen protocol](../../CON-ARTIST-READ-01-PROTOCOL.md),
[isolated candidate](../../con_artist_read_candidate.py),
[reviewed observations](comparison.json).

One entrypoint paragraph changes: read supplied paths/contracts/instructions
together, obtain needed line numbers on that read, discover only missing paths
alongside it, and recover changed/truncated/unresolved context. Other instructions
and all helper/reference files are byte-identical. The motivating repository-cache
task is not rerun. This transfer uses the existing authored SQLite lost-commit task;
it is exposed, not held-out, independent or a new real-project sample.

| Arm | Full input + output tokens | Wall seconds | Recorded responses | Task / scope |
| --- | ---: | ---: | ---: | --- |
| Original | 90,593 | 76.531 | 5 | Pass / pass |
| Candidate | 74,939 | 80.023 | 4 | Pass / pass |

**−17.28% tokens / +4.56% time.** Two fresh serial GPT-6 Astra medium sessions,
n=1, original first, shared host/cache, no fresh no-skill baseline. Cache is part
of input, not additional tokens; reasoning is not added again to output. No
scheduled retry, replacement or exclusion. Candidate does not meet the frozen
both-costs-decrease gate and is **not adopted**. Do not retune this same case until
favorable. No causal latency conclusion, dollars, confidence intervals, featured
chart promotion or whole-eight performance claim.

## Behavior and equal requirements, not identical work

Both satisfy the four frozen criteria. Same-process native checks bind actual
`test_receipts.accept` to `endpoint.handle_upload` and its `_record` to
`ledger.write_event`; copied paths and actual writer calls are observed. Both
remove only `connection.commit()`, preserving acknowledgment/close. Two original
tests pass on correct and faulty copies. Each arm runs its identical stronger
assertion on both versions: a new SQLite connection reads complete ordered rows,
preserving `(10, b'previous')` and exact `(20, b'\x00\xffnew')`. Correct code passes;
faulty code fails for the missing committed binary row, not setup/import errors.

Original strengthens both binary and empty-payload tests by subclassing the
original test class; its mutant therefore has two failures. It invokes a disposable
native unittest runner script with `TextTestRunner`, checks two endpoint and writer
calls per phase, and prints row observations. Candidate strengthens only the
required binary test in both copies, keeping the empty acknowledgment control;
its mutant has one failure. It uses native `-m unittest -v audit_probe` with a
`load_tests` binding check and writer tracing, printing writer source in each
phase. These are different amounts/forms of work, not isolated prompt-cost effects.

Both inspect sources before execution. Original uses a listing/skill-read turn,
a partial source read, then the endpoint/contracts read. Candidate still starts
with listings/skill read: the proposed no-listing-only behavior is **not fully
followed**. Its next read groups all project source/contracts with line numbers,
eliminating one observed response. No installed collector/audit helper is used.

All four native phases are present in original command-correlated records.
Original bytes/modes are checked for the production/tests/contracts; tests create
project-local SQLite scratch and remove it through existing fixture cleanup.
Owned comparison directories are removed. Mechanical review also finds no
original changes, retained extras or installed-resource changes. No author replay
replaces model outcomes. Native positive/negative preflight in `run.json` is
separate setup evidence, not additional model observations.

## Capture and exposure

Both skill bodies are observed in initial context; later SKILL.md reads repeat
that exposure. Metadata and selected tool records are exported, not private
initial instructions. Captured CLI output is incomplete even without a truncation
marker: original `item_6` omits the initial correct-existing phase and leading
fault/faulty-command text retained at original record line 37; candidate `item_5`
similarly omits the first phase/prefix retained at original line 32. Both original
records preserve all native exits/assertions and cleanup. Other outputs match
after normalization. Candidate `item_2`'s truncation hint matches the skill's
word “truncated”; it is prose, not an actual truncated output.

## 한국어 요약

첫 읽기에 필요한 소스·계약·줄 번호를 모으는 후보를 별도로 만들고 SQLite
커밋 누락 과제로 비교했다. 원본 90,593토큰·76.531초, 후보
74,939토큰·80.023초로 **토큰 17.28% 감소 / 시간 4.56% 증가**였다.
모델 응답은 5회에서 4회로 줄었지만, 후보도 첫 목록 조회를 없애지는 못했다.

양쪽 모두 실제 연결 관계와 호출을 확인하고 정상·결함의 원래 테스트를 실행했다.
강화된 바이너리 행 검사는 정상에서 통과하고 커밋 누락에서 실패했다. 원본은
빈 데이터 검사도 강화했고 후보는 요구된 바이너리 검사만 강화해 작업량이 다르다.
원본 보존·임시 파일 정리도 확인했다. CLI가 누락한 첫 실행 결과는 해당 원본
기록에 남아 있으며 검증을 재실행해 대체하지 않았다.

이미 공개된 작성 과제 한 개·각 1회·고정 순서 비교다. 토큰과 시간 모두 감소라는
사전 기준에 못 미쳐 **배포용 스킬에는 채택하지 않는다**. 같은 과제로 좋은
결과가 나올 때까지 조정하지 않고 기록을 보존한다. 대표 차트·전체 성능·배포
준비 완료 주장은 바꾸지 않는다.
