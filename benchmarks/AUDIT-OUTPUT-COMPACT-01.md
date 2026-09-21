# Audit output: lossless CLI formatting

2026-09-21, parent `bf936a4`. This is a local representation change, not a new
model experiment. Prior compact-output work concerned the context collector and
other helpers; the audit runner still emitted indented JSON unconditionally.

The audit CLI now emits compact JSON by default. `--pretty` preserves the previous
indented representation. Keys, values, string escaping, native transcripts,
provenance, truncation flags, observation references, integrity and exit semantics
are unchanged. No test output is summarized, suppressed or re-executed. Existing
JSON consumers remain supported; consumers depending on indentation must use
`--pretty`. Reference guidance documents the switch without lengthening SKILL.md.

## Same-object size comparison

Decode the final audit object from each listed ZIP original tool output, then
compare UTF-8 lengths of `json.dumps(object, indent=2)` and
`json.dumps(object, separators=(',', ':'))`, excluding the trailing newline.
Assert both deserialize to the original object. The source records are retained
under [ZIP audit01](results/zip-audit-01/README.md); no original artifact is edited.

| Original report | Indented bytes | Compact bytes | Reduction |
|---|---:|---:|---:|
| Prior / single | 8,719 | 7,522 | 13.73% |
| Prior / multiple | 14,752 | 12,762 | 13.49% |
| Candidate / multiple | 13,673 | 11,683 | 14.55% |

These are output bytes, not tokenizer counts, total model tokens, execution time
or expected savings. Fixed tool-output budgets and readability can affect model
behavior differently; no whole-task efficiency claim or featured-chart change.

## Checks

- New serialization tests exercise single/batch observed/incomplete reports,
  native assertion text, Unicode/control characters, reuse references, CLI exits,
  pretty compatibility and invalid JSON with no misleading stdout report.
  Their mocked report boundary checks serialization, not native execution.
- The existing actual packaged native recipe tests still execute normal and
  faulty sources, stronger probes, import bindings and preservation under the
  new default output. No new model session was launched.
- Python3.9.6 audit suite:109 discovered,98 passed/11 skipped,12.293s.
- Python3.11.16 audit suite:109 passed,16.323s.

한국어: 감사 도구의 JSON 기본 출력에서 불필요한 들여쓰기만 제거했다.
`--pretty`로 기존 형식을 사용할 수 있으며, 실행 근거와 데이터는 모두 동일하다.
기존 세 보고서의 출력 바이트13.49–14.55% 감소를 확인했지만, 모델 전체 비용이나
시간 개선으로 주장하지 않는다. 실제 네이티브 감사 회귀 테스트도 통과했다.
