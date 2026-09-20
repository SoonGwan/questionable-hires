# Receipt read-order 01 — candidate rejected

2026-09-20. Resources `ca668a4`, frozen launch `62234cf`;
[protocol](../../RECEIPT-READ-01-PROTOCOL.md),
[candidate](../../RECEIPT-READ-CANDIDATE.md), [all six rows](comparison.json).
Only the first read/discovery paragraph differs. Helper, references, scope and
evidence requirements are unchanged. **Do not adopt this candidate:** summed
tokens rise **30.89%**, process time **5.42%** versus the original skill.

## Observed resources and outcomes

GPT-6 Astra medium, six fresh serial sessions, one repeat per cell. Full input
(including cached input once) plus output; reasoning is not added again.
Seconds are process wall time, responses are recorded model responses.

| Variant | Condition | Tokens | Seconds | Responses | Task / scope |
| --- | --- | ---: | ---: | ---: | --- |
| Complete fix (a) | No skill | 67,639 | 65.964 | 4 | pass / pass |
| Complete fix (a) | Original | 89,987 | 41.078 | 4 | pass / pass |
| Complete fix (a) | Candidate | 117,472 | 41.604 | 5 | pass / pass |
| Partial fix (b) | No skill | 70,215 | 65.106 | 4 | pass / pass |
| Partial fix (b) | Original | 90,453 | 40.155 | 4 | pass / pass |
| Partial fix (b) | Candidate | 118,707 | 44.033 | 5 | pass / pass |
| **Sum** | **No skill** | **137,854** | **131.070** | **8** | **2 / 2** |
| **Sum** | **Original** | **180,440** | **81.233** | **8** | **2 / 2** |
| **Sum** | **Candidate** | **236,179** | **85.637** | **10** | **2 / 2** |

Candidate versus no skill: **+71.33% tokens, −34.66% time**. These are ratios of
sums, not task-ratio averages or causal speedup estimates. Neither comparison
establishes lower token and time cost together. No failures, retries, timeouts,
exclusions or replacements were removed from these six scheduled cells.

## Native evidence review

All six execute the same five current native unittest tests and schema against
full identified `HEAD^` / `HEAD` revisions, using actual SQLite and fresh
connections for balances. Before has two real retry assertion failures and
three passing controls. Variant a passes all five after. Variant b still has
two balance failures despite returning False: credit `(False, 250)` instead of
`(False, 125)` and debit `(False, -100)` instead of `(False, -50)`. All three arms
correctly report the incomplete fix; that is task success, not a failing agent.
Native exits are 1/0 for a, 1/1 for b. No setup exception substitutes for a
defect assertion, and no skipped test substitutes for coverage.

Both baseline sessions write disposable comparison orchestration, with explicit
current-input hashes, full revisions, implementation identity, separate import
prechecks and actual `python3 -B -m unittest -v checks.test_delivery` execution.
Their import precheck is a **different process** from the test runner; do not
equate it with the skill helper's same-native-process path/PID evidence. Both
baseline sessions snapshot originals (including ignored cache, Git and owner
notes), verify database cleanup and remove comparison copies in finally blocks.

All four skill sessions use the unchanged helper in native module mode, verify
same-process copy-local imports, fixed-input hashes, individual native exits,
whole-tree preservation and copy removal. All final review/check/status exits
are retained separately. Original-arm calls explicitly use `--python python3`
and contain macOS xcodebuild launcher warnings; candidates use the helper's
absolute-interpreter default. Preserve those warnings and costs: they do not
invalidate the genuine assertions but prevent attributing time solely to the
read-order instruction. No original files, HEAD or installed resources changed;
no extra harness/report remains in any project.

Before freezing, separate author preflight exercised the native complete and
partial comparisons, genuine negative assertions, positive controls, preservation
and cleanup. See `native_preflight` in [run.json](run.json). These are author
controls, not additional model samples or a post-run replay of model behavior.

## Read behavior and capture limitations

Original arms already combine inventory and known-input reads in the first
command. Candidate arms omit that inventory, but add another discovery/read
round trip later: 5 versus 4 responses. All skill arms read both reference files
and the full helper implementation; this output is truncated at the outer tool
wrapper (item 2, stored line 22). Candidate b subsequently reads a bounded helper
section. A shorter first command did not reduce whole-task work or context cost.
This observation motivates better support selection, not a ban on legitimate
implementation/trust inspection or a proven causal explanation of all overhead.

Native helper evidence is complete, not truncated: original item 4 / stored
line 31, candidate item 5 / stored line 38. Mechanical `cli_output_has_truncation`
flags can falsely match the JSON field `output_truncated:false` or source text;
they are retained as hints, not verdicts. Candidate a's intermediate rg exit 1
means no search matches, not test failure. Baseline a CLI item 4 omits leading
current-input hash lines; matching original output at line 30 retains them.
Baseline b's comparison output matches the original capture. Selected original
tool records preserve these differences; no model rerun repaired a capture.
Private initial instruction text is not exported. Exposure reports record the
Receipt body in the initial skill-arm messages and no skill-body exposure in
baseline; later skill reads must not be described as first exposure.

These are two **already-exposed variants of one authored task**, not independent
real projects or held-out validation. Fixed order is baseline/original/candidate
for a and candidate/original/baseline for b; original is always in the middle.
Shared host/cache, n=1, launcher differences and nonidentical extra checks limit
interpretation. No confidence intervals, dollar estimates, all-eight claim or
featured-chart promotion. Production Receipt stays unchanged.

## 한국어 요약

알려진 파일을 먼저 묶어 읽게 한 Receipt 후보는 채택하지 않는다. 6개 새 세션에서
완전 수정·부분 수정의 판단과 범위 준수는 모두 충족했지만, 기존 스킬보다 합산
토큰 **30.89%**, 시간 **5.42%**가 늘었다. 무스킬 대비로는 토큰 **71.33% 증가**,
시간 **34.66% 감소**다. 기존 스킬도 첫 읽기를 이미 묶었고, 후보는 뒤에 추가
읽기 응답이 생겼다. 모든 스킬 실행이 긴 구현·참고 문서를 읽었다.

부분 수정의 남은 잔액 오류를 정확히 보고한 것은 성공이다. 실제 SQLite 검사,
원본 보존과 정리를 확인했다. 무스킬의 별도 프로세스 import 확인과 스킬의
동일 테스트 프로세스 확인은 증거 강도가 다르다. 구현 읽기 잘림, CLI 누락,
런처 경고도 원본과 함께 보존했다. 노출된 한 과제의 두 변형을 각 1회 측정한
개발 실험으로, 일반 성능 향상·배포 완료를 뜻하지 않는다. 실제 Receipt와
기존 공개용 그래프는 변경하지 않는다.
