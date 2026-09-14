# Observation candidate 02 — rejected after screen, 2026-09-15 KST

Launch/resources `3105de1`; [candidate and protocol](../../EXORCIST-OBSERVATION-02.md).
One fresh skill-only Astra medium session on the unchanged exposed reporter task,
serial, 240-second deadline. Completed at **166,501 total tokens / 101.776 seconds**,
eight commands, no timeout or author retry. Versus the historical prior skill:
**+42.67% tokens / +23.91% time**. No fresh baseline or causal performance estimate.

The paragraph was read, and source inspection was separated from the diagnostic.
But the model generated 87 detailed lifecycle events, including every directory
removal, without a retained record. [Item_7](reporter-lifecycle--skill--1/commands.json)
begins at event **39** in the original CLI stream. Events 1–38, early native headers
and the stated nearest-normal-control observations are absent. The updated collector
correctly flags four reported tests versus one retained verbose header. This is
not an automatic behavioral failure; manual inspection establishes missing output.

Unlike screen 01, the captured cancellation portion does contain decisive evidence:
event 39 enters rmtree with both targets/marker present; 56–57 removes the destination;
61–62 finishes cleanup and enters result reporting; 63–64 receives the original
AssertionError then catches the reporter FileNotFoundError. Actual installer call
lines are retained. The fourth test's normal cleanup and success are also present.
But the final answer cites events 37–38 and a full normal-control comparison absent
from the original stream, and says no evidence is missing. That stronger claim is
not supported by available capture. Model-visible tool output is not independently
available, so the layer responsible for the omission is not established.

Item_4 reproduces the original reporter crash. Item_8 independently runs the four
unchanged native tests with **all four verbose headers**, three passes, one actual
line-303 assertion failure, exit 1. Native test recovery is established, but it does
not recreate the earlier missing lifecycle observations. Item_9 confirms no temp
directories/bytecode and shows the actual relevant source lines. No original
implementation/test changes, setup retries or author repair supplied the evidence.

Every original completed-command object/output, usage and source-hash manifest
reconciles with the export. All 13 final supplied file bytes equal frozen inputs,
no scratch remains, and installed resource manifests are unchanged. Original
item.started has empty output; no item.updated/delta events contain a recoverable
prefix. Export did not delete the missing events. Native command output remains
available only as received, not a guarantee of complete upstream capture.

Decision: **revert the candidate paragraph to the previous wording**. This single
screen does not prove causal harm, but it fails its adoption/completeness objective
and adds instruction length without a demonstrated net benefit. Preserve the code
and evidence at `3105de1`; the reversion does not relabel this run. Stop tuning the
same task with more generic instructions. Investigate capture separately before
using more such runs for efficiency claims. No featured/localized chart changes.

한국어: 수정 안내를 읽고 소스 출력은 분리했지만, 87개 사건을 출력해 앞부분이
다시 누락됐다. 이전 스킬보다 토큰 42.67%·시간 23.91% 증가했고, 누락 복구도
확인되지 않아 추가 문단을 되돌렸다. 실제 취소 삭제 순서와 별도 테스트 4개 결과는
남았으나 최종 답변 전체를 뒷받침하지는 않는다. 불리한 실행과 후보를 보존하며
같은 문제에 지침을 계속 덧붙이는 대신 출력 수집 문제를 별도로 확인한다.
