# Receipt guide-first candidate — 2026-09-27

Parent `e6d5e663`; changes only `skills/receipt/SKILL.md`. The same helper
implementation and evidence/preservation requirements remain. This is **not yet
model-measured** and must not inherit effort01's costs measured on `7172b50c`.

The [effort01 original review in progress](ALL-EIGHT-EFFORT-01-TERMINAL16.md)
found routine helper source reads in both Receipt conditions before using the
existing CLI recipe. The guide already limits implementation inspection to a
concrete trust, adaptation or diagnosis question. This candidate places that
routing in the entrypoint: use the matching documented CLI guide first, execute
supported use directly, and inspect relevant source for unresolved questions or
explicit requirements. It does not forbid trust review or change access scope.

The [earlier read-order candidate](RECEIPT-READ-CANDIDATE.md) is a separate,
rejected discovery-order change: tokens+30.89%,time+5.42%. That adverse evidence
prevents treating fewer reads or shorter instructions as proven cost savings.
This candidate targets CLI documentation routing rather than known-path discovery.
No extra paid model run was launched for this change.

Local validation, separate from model evidence: existing native tree-guard suite
9 tests and native-invocation suite17 tests pass. These retain original preservation,
actual runner/provenance and incomplete-evidence controls; they do not prove the
model follows the new instruction or uses fewer tokens. The skill validator first
failed because the system Python lacked PyYAML, then passed with the existing
owned validation interpreter; no system dependency/configuration was changed.
README English/Korean helper guidance is synchronized without performance claims.

한국어: 후보는 Receipt 진입점에서 기존 사용 가이드를 먼저 읽도록 안내한다.
구체적인 신뢰·수정·진단 의문이 있거나 요청된 경우 구현 검토를 유지한다.
기존 보존9개·네이티브 실행17개 검사가 통과했으나 실제 모델의 토큰·시간 절감은
아직 미측정이다. 이전 읽기 순서 후보의 비용 증가와 effort01의 원본 품질 검토
한계도 유지하며 기존 측정 수치를 새 후보의 성과로 바꾸지 않는다.
