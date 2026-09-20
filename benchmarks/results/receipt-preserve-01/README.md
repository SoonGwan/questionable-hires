# Receipt preservation support 01 — adopted in-session, higher token cost

2026-09-20, launch `6bdf2bd`. Original `f4943e8`, current `55fe666`;
[protocol](../../RECEIPT-PRESERVE-01-PROTOCOL.md), [reviewed rows](comparison.json).
Current adds optional bounded preservation support, not the rejected read-routing
candidate. The native comparison implementation and test runner are unchanged.

| Arm | Input + output tokens | Wall seconds | Responses | Task / scope |
| --- | ---: | ---: | ---: | --- |
| No skill | 67,154 | 53.675 | 4 | pass / pass |
| Original | 76,892 | 60.167 | 4 | pass / pass |
| Current | 95,374 | 60.190 | 5 | pass / pass |

Current versus original: **+24.04% tokens / +0.04% time**. Versus fresh no skill:
**+42.02% tokens / +12.14% time**. This is not a model-efficiency improvement.
The optional API has demonstrated behavior, but has no demonstrated token/time
benefit here. No performance promotion or featured-chart update follows.

GPT-6 Astra medium, one repeat, serial baseline/original/current, same host/cache.
Full input includes cached input once; reasoning is not added to output again.
All scheduled cells complete; no timeout, retry, replacement or exclusion. This
is now an exposed authored task, not held-out real-project validation. Fixed
order, n=1 and differing audit work limit interpretation; no causal guarantee,
confidence interval, dollars or broad all-eight claim.

## What the current skill actually did

It read the routine guide and native-preservation guide, then read `preserve.py`
in a separate interaction. It loaded that module with bytecode disabled, placed
native copying/execution/cleanup/final checks inside `preserved_tree(root)`, and
printed the successful report **after** context exit. No second handwritten tree
inventory was added. The final report records 75 entries/54,686 bytes unchanged.
This is genuine use, not a source-read-only adoption claim. The existing native
startup hook and runner stayed intact. Module import automatically loads the
adjacent inventory implementation, not its native comparison runner.

Original writes its own tree inventory and reads both older reference files;
baseline writes a different snapshot and copies the current tree excluding Git
and its owned scratch parent. Current adds one model response for source review
and an additional committed-diff whitespace check. Smaller generated inventory
code did not make the whole task cheaper. Preserve these costs; no attribution
of all token/time differences to a single read or helper call is warranted.

## Reviewed evidence and obligations

All three use the same current five tests, startup hook and format configuration
against full before/after revisions `dc1a0044e39c1af367031fce15027b9276caf7d5` /
`d973477c2b299730d2643a03f2ade52bb0c6e453`. Original commands and correlated native
outputs establish exact inputs/hashes, actual committed implementation, and the
documented `PYTHONPATH=. python3 -B -m unittest -v test_manifest` child command.
The outer orchestration's `-S` or `-I` is not inherited by that child.

Before has genuine quoted-separator and doubled-quote assertion failures, with
plain/empty/Unicode controls passing. After all five pass, native exits 1/0.
Supplied unchanged tests verify startup occurred before test import, the configured
semicolon and copy-local implementation/startup paths in the same native process.
There is no setup error counted as reproduction, skipped coverage or monkeypatch.
Every final answer correctly limits the claim to supplied requirements/tests.

Owned copies are removed and original contents/user notes/ignored cache/HEAD and
installed resources stay unchanged; no harness/report remains. All five criteria
and scope pass in all arms. Preservation strength is not identical: baseline's
snapshot excludes `.verify-owned-*` names (none preexist here); original's manual
inventory excludes the root entry; current uses the bounded root-inclusive guard.
Neither handmade inventory has the helper's read/entry bounds. Original's final
status runs **before cleanup** and lists scratch, then deletion/inventory equality
and collected state confirm removal. Do not mistake that intermediate status for
a retained artifact or imply all arms did identical extra audit work.

The positive path does not establish model recovery from a guard exception.
Separate pre-launch local API tests cover change detection, exception propagation,
cleanup ordering and bounds. Author native preflight is recorded separately in
[run.json](run.json); it is not another model sample or post-run replay.

## Capture and exposure

Baseline CLI item 5 omits before revision/root/fixed hashes/command prefix; original
stored output line 33 retains it. Current CLI item 4 omits the leading revision
map/fixed hashes; original line 34 retains them. Native assertions, paths/PIDs,
exits and cleanup remain present. Original-arm native item 4 matches stored output.
Mechanical truncation hints on reference text are prose matches, not actual
truncation. No model execution was repeated to repair these captures. Selected
original tool records are exported, private initial instructions are not.
Exposure inspection confirms initial Receipt body only in skill arms; reading
the file later is not first exposure.

Stop further Receipt tuning on this small task. Keep the utility explicitly
optional and unproven for model efficiency. A useful bounded guard is not the
same claim as a faster developer skill, and the all-eight objective remains open.

## 한국어 요약

현재 스킬은 새 보존 도구를 실제로 사용했고 정상·오류 검사와 원본 보존을
통과했다. 그러나 소스 검토 응답이 추가되어 이전 대비 토큰 **24.04% 증가**,
시간 **0.04% 증가**였다. 무스킬보다도 토큰 **42.02%**, 시간 **12.14%** 증가했다.
도구가 동작한다는 증거와 전체 작업이 빨라진다는 주장은 구분해야 한다.

원본 출력과 요약 캡처 차이, 임시 폴더 삭제 전 상태 출력, 조건별 보존 검사
차이를 모두 검토·기록했다. 이 작은 과제에서 Receipt를 계속 조정하지 않는다.
도구는 선택적 기능으로 유지하되 성능 개선으로 홍보하지 않고 차트도 바꾸지
않는다. 8개 전체의 실제 성능 향상 목표는 아직 충족하지 못했다.
