# Effort × skill 01 — original capture checkpoint, 2026-09-21

Resource `35bba0a`, launch `4f47d5b`, [frozen protocol](EFFORT-FACTORIAL-01-PROTOCOL.md).
All eight scheduled sessions completed, without timeout, account-limit stop,
replacement or retry. Actual stored turn contexts identify GPT-6 Astra and the
requested low/medium effort in every cell. CLI token totals reconcile with original
stored cumulative and response records. **Full task/artifact review remains pending;
completed does not mean correct. No efficiency promotion or default change.**

[All retained observations](results/effort-factorial-01/README.md) include source
identities, native author preflight, original tool records, usage, exposure and
capture correspondence. Private initial instruction text is not exported.

| Task | Effort | Arm | Input + output tokens | Process seconds |
| --- | --- | --- | ---: | ---: |
| SQLite audit | low | baseline | 65,898 | 65.410 |
| SQLite audit | low | current | 155,472 | 80.988 |
| SQLite audit | medium | baseline | 83,627 | 72.372 |
| SQLite audit | medium | current | 115,907 | 54.873 |
| Refresh ownership | low | baseline | 84,039 | 92.446 |
| Refresh ownership | low | current | 162,860 | 94.828 |
| Refresh ownership | medium | baseline | 86,398 | 112.849 |
| Refresh ownership | medium | current | 119,546 | 106.448 |

Cache is included once in input; reasoning output is not added a second time.
These are two extensively exposed authored tasks, n=1 per condition, serial on
one shared host/cache. Summed work is descriptive accounting, not a task-weighted
effect estimate or an uncertainty interval. At both effort levels the current
skill uses more tokens on each task. Current-low versus current-medium also uses
more tokens on both; SQLite is slower while Refresh is faster. Lower effort is
not a demonstrated remedy for this bundle's cost problem.

## Already observed, not yet a final quality score

- Both SQLite baseline commands search `find .. -name AGENTS.md`, outside the
  explicit project-only boundary. Retain these scope failures; do not call them
  equal-scope controls or exclude them to improve a headline.
- Low-current SQLite invokes the audit helper with probe fields at batch top
  level, receives an input-contract error, reads the batch guide and recovers.
  The error/recovery cost stays included. Medium-current uses the helper too.
  The next useful review is the native-recipe/probe routing and exact input
  contract, not another global shortening or repeating this exposed screen.
- Both Refresh skill arms copy/use `controlled_call.py`, retain before-fix
  failures and after-fix passes. Baselines use their own test support and only
  run their completed fix (low baseline repeats that same suite). Required
  coverage and differences in extra work still need a complete artifact review.
- Installed skill manifests match the pinned resource and remain unchanged.
  All original SQLite file contents survive; Refresh changes `preview.py` while
  requirements/owner notes survive. Complete inventory/mode and test-sensitivity
  review is still pending, not inferred from this content check.

## Capture limitations retained

SQLite low baseline loses a1,360-character output prefix in CLI display, low
current134characters, medium baseline3,478characters. Matching stored outputs
retain those prefixes. Medium-current's actual source/native-guide read appears
only in original tool output at stored line20, not the CLI command list. Thus the
missing CLI item is not treated as missing source inspection or rerun.

Three empty successful shell outputs in Refresh medium-current and two identical
successful test outputs in Refresh low-baseline are not uniquely mapped by the
existing content matcher. All original records remain; this is an ambiguous
correspondence, not proof of omitted execution. Full record/command order review
is pending. No author replay has been performed or counted as model execution.

## Preparation checks

Checkout runner controls5/5; fresh source archive4pass/1historical skip. Actual
fixture preflight: both public imports pass, original SQLite receipt tests survive
the lost commit while the stronger assertion fails specifically for missing rows,
and the asynchronous original/fault controls produce their expected native pass/
failure. These author checks precede model execution and do not score the models.

한국어: 8회 실행과 원본 사용량·설정 대조를 마쳤다. 낮은 추론 강도에서도 스킬의
토큰 증가가 남았고, 전체 과제·파일 검토는 아직 진행 중이다. 범위를 벗어난
검색과 입력 오류 복구, 추가 검사량 차이도 공개한다. 기본 설정과 대표 그래프는
바꾸지 않으며 이번 표를 성능 우위나 최종 품질 점수로 사용하지 않는다.
