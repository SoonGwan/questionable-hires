# Refresh-owner 03 — incomplete adoption and an upstream evidence gap

2026-09-15; [protocol](HOSTAGE-REFRESH-03-PROTOCOL.md), launch `37322ce`, resources
`6b6962c`. Both scheduled skill sessions complete, no timeout, limit or retry.
Exposed development tasks, n=1, no fresh baseline.

| Variant | Tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| a | 121,201 | 104.015 |
| b | 142,656 | 117.079 |
| Sum | 263,857 | 221.094 |

Relative to **historical skill run 02**, sum tokens are 17.55% lower and time
10.00% lower; b's tokens increase from 126,499 to 142,656. This is not a comparison
to a current baseline, a causal estimate or a performance win. Work differs:
run 02 a demonstrated pre-fix failure; run 03 a tests only after fixing.

## Adoption and native evidence

Both sessions combine known-file reads with initial status/discovery. Neither
uses the documented complete-usage excerpt: both read the entire Python helper
in another call and repeat inventory. There are 5 completed shell commands in a,
8 in b (run 02 skill: 12/7). Variant a batches final integrity/diff/status with
separate exit markers. Variant b runs integrity separately and repeats its final
diff checks. These observations do not justify claiming complete adoption or
attributing token differences to the instructions alone.

Both native tests are dedicated commands. **Variant a item_6 has empty output
in `stdout.original.jsonl` itself**, though its recorded process exit is 0. Its
final answer claims seven tests passed without retained native count/results.
There is no report-reading or evidence recovery command. Variant b item_6 has
eight named tests, native summary `OK` and exit 0, matching its final answer.

Collector inspection shows `run_cell` saves `process.communicate()` output before
parsing or redaction. Empty a output is already in that saved CLI event: it is
not introduced by export/redaction or the transcript parser. This locates the
observed gap upstream of those stages, **not its underlying cause**. We cannot
establish from this record what the model saw internally or that tests never ran.
Dedicated commands do not guarantee complete telemetry; earlier positive run 02
is not proof that the reporting issue was permanently solved.

## Separate controls

All final production files equal the correct generation guard; valid b, frozen
requirements and notes remain unchanged. Installed resources are stable and both
helper copies match measured bytes. [Eight author controls](results/hostage-refresh-03-controls/author-replay.json)
accept retained final suites (7/8 methods), detect faulty cleanup with actual
pending-state assertions, accept valid alternate counter increments, and run the
six-method frozen oracle on final production. No timeout/setup error; original
projects remain unchanged. These narrow replays cannot fill a's original gap or
prove every task requirement; detailed retained-test path review remains due.

[Both exported cells](results/hostage-refresh-03/run.json) retain original commands,
answers, metadata and complete project text. Raw usage matches metadata; exported
events, filename sets and project text reconcile to redacted originals; source
hashes match. Home/temp/key-pattern scan finds no matches, not universal privacy
proof. No historical/featured chart changed.

## Decision

Do not promote this candidate as a measured success. Before another model run,
investigate a concrete durable-evidence path and why the cheaper reading route is
not used. Preserve needed implementation review and native results. Do not rerun
the same sessions until a favorable percentage appears. After supported adoption,
move to different workflows and fresh comparisons as preregistered; the all-eight
real developer usefulness and cost objective remains unmet.

## 한국어

새 스킬 2세션이 완료됐다. 이전 스킬 실행 합계보다 토큰 17.55%·시간 10.00%
감소했지만 한 과제는 토큰이 늘었고 작업량도 다르다. 새 기본 모델 비교가 아니므로
성능 우위로 쓰지 않는다. 두 세션 모두 도우미 전체를 읽었고 한 세션은 점검을
반복했다. 지시 채택은 불완전하다.

오류 과제는 테스트 명령을 분리했는데도 원본 CLI 이벤트부터 출력이 비어 있고
통과를 보고했다. 수집 후 파싱이나 가림 단계가 누락을 만든 것은 아니지만 정확한
원인은 아직 모른다. 정상 과제는 8개 통과 근거가 있다. 별도 대조 8회는 통과했으나
원본 누락을 메우지 않는다. 다음 실험 전에 증거 보존 경로와 읽기 비용을 개선해야
하며, 후보를 검증 완료로 올리거나 기존 그래프를 바꾸지 않는다.
