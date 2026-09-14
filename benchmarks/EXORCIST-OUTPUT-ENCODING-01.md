# Probe output encoding — 2026-09-15, parent `3d763e7`

The existing runner retains Unicode correctly but its CLI serialized every
non-ASCII character as JSON escapes. The existing Korean-tail regression makes
this concrete: the 12,000-character output bound is not a 12,000-byte JSON bound.

The CLI now defaults to compact JSON, emitting Unicode directly on UTF-8 stdout.
Other stdout encodings retain ASCII escapes. `--pretty` before the command `--`
restores indentation; both modes have identical decoded fields. `run()` results,
child invocation, 12,000-character tail, truncation flags, process deadlines,
group cleanup and exit mapping are unchanged. No helper-adoption instruction added.

## Measured serialization, not model performance

[Recorded profile](exorcist-output-encoding-01.json) uses three actual new CLI
outputs and applies the pinned legacy `json.dumps(result, indent=2)` serializer
to the identical returned object, with one trailing newline. Each comparison
round-trips to the same dictionary, including the same elapsed value. The child
is not rerun for the comparison. Sizes are UTF-8 bytes, not tokenizer estimates.

| Synthetic log | Previous JSON bytes | New JSON bytes | Change |
| --- | ---: | ---: | ---: |
| ASCII | 3,244 | 3,219 | −0.77% |
| Korean | 10,744 | 5,919 | −44.91% |
| Mixed Korean/emoji | 3,944 | 2,519 | −36.13% |

To reproduce the payloads, repeat each of these strings 100 times (including LF):
`phase=done; observed=expected\n`, `진단 완료: 예상 값과 실제 값이 같습니다.\n`,
`phase=done 진단 😀\n`. A Python child writes the UTF-8 bytes using `os.write(1, ...)`.
Run with UTF-8 stdout, parse the result and serialize the same object with the
old serializer. Actual timings may change the byte count slightly; payload hashes
and measured lengths are retained. These are authored serialization samples,
not model sessions, a real-user corpus or an all-eight efficiency result.

## Verification and unsuccessful controls

New tests first failed against the old CLI: no `--pretty` option and escaped
Unicode output. After implementation, all 19 probe tests pass on macOS
(3.614s) and Linux Python 3.12 (3.407s). The Linux run used the existing image
offline, with the repo read-only. Twelve installation-bundle tests also pass
(3.338s). Metadata/link/featured-sync checks pass.

The first Linux run found an author-test issue: embedding a large byte literal in
one argument exceeded Linux's argument limit before the runner executed. It had
18 passes and one error. The test now generates the identical large Unicode text
inside the child; no smaller output, skip or weakened assertion. The final Linux
19-test run passes. Final revised format tests also pass on macOS (3 / 0.103s).

The format tests preserve Unicode, escapes and all status fields across success,
failure, timeout and incomplete cleanup; exercise UTF-8 and ASCII streams; and
run an actual child producing more than the tail limit. Model adoption, total
model tokens and whole-task time remain unmeasured. Featured charts stay unchanged.

한국어: UTF-8 환경에서 한글·이모지를 불필요하게 이스케이프하던 출력을 줄였다.
표본의 JSON 전송량은 한글 44.91%, 혼합 36.13% 감소했지만 모델 토큰 절감률은
아니다. 내용·상태·잘림·프로세스 정리 동작은 유지한다. ASCII 출력 환경과 Linux
검증도 통과했으며, 테스트 준비 과정의 오류도 기록했다.
