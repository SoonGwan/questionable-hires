# Persisted tool-response diagnostic — frozen before launch

Parent `56c2b4c`. One fresh Astra medium baseline session, one repeat, serial,
seed 20260915, timeout 240 seconds. Reuse the exact frozen delayed-emitter fixture
and task (`cli-yield-probe-01-cases.json`). The only requested launcher change
from the original CLI diagnostic is omission of `--ephemeral`; retain the
ignore-user-config, ignore-rules and workspace-write flags. No model retry.

Purpose: determine whether this newly created session's stored rollout retains
model-visible tool responses omitted from command-completion JSONL. First inspect
original CLI events, obtain their exact session/thread ID, and locate only that
new session's rollout by filename. Do not read unrelated session contents or
modify/delete any existing rollout, user configuration or authentication material.
Do not execute/replay the emitter to fill evidence gaps.

Keep original stdout/stderr and the new run's witnesses. Treat rollout content as
sensitive: retain locally first; export only reviewed relevant tool input/output
records with source hashes, clear excerpt boundaries and path redaction. Do not
publish system/developer instructions, unrelated context or credentials. Stored
tool responses are an additional observation channel, not a guarantee of complete
capture. Compare exact nonce/byte evidence before adopting it prospectively.

The existing emitter received native hash/length and duplicate-write checks;
this is a capture diagnostic, not scored QA or a skill-performance benchmark.
Do not update historical scores or featured charts.

Launch:
`python3 -B benchmarks/run.py --cases-file benchmarks/cli-yield-probe-01-cases.json --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 --model gpt-6-astra --effort medium --persist-session --output benchmarks/local-runs/cli-rollout-probe-01`

## Outcome — a useful additional evidence channel

Launch `bcd761d` completed in 13.338 seconds, one emitter command, exit 0.
[Original CLI evidence](results/cli-rollout-probe-01/) still has only the 45-byte
END line in its command aggregate. The final answer reports both fresh nonces.
Supplied emitter/instructions are unchanged. This is not a skill-performance run.

The matching new session's stored rollout retains the actual tool exchanges:

| Source line | Record | Retained observation |
| --- | --- | --- |
| 13 | custom tool call | `exec_command`, requested yield 1000 ms, output budget 20000 |
| 15 | matching tool response | 47-byte BEGIN line and live session ID 51463 |
| 18 | custom tool call | `write_stdin` on session 51463, empty input, yield 1000 ms |
| 20 | matching tool response | 45-byte END line and exit 0 |

[Reviewed tool records](results/cli-rollout-probe-01/tool-records.json) preserve
those four records, original line numbers/hashes and full-source SHA-256. Joining
the two recorded output strings yields exactly 92 bytes and the witness SHA-256.
Both call IDs have matching outputs. Unlike earlier diagnostics, requested tool
settings and the actual polling call are now available for independent review.
No author replay or inferred replacement output is used.

The full 58,024-byte / 26-line rollout is retained in local-only run storage, not
committed: it includes non-tool context. Extraction verifies its session identity
against the CLI events before selecting records. Source hash:
`d46d6f5ac8a9143f344b4121f93069b509cdba1b86eca38a8efea02d5e3bbf0c`.
Only reviewed tool records are exported, with the normal path redaction.

Validation: 27 runner tests cover explicit opt-in/default ephemeral behavior and
preserved isolation flags. Four extraction/reconciliation tests cover unrelated
session rejection, omitted private message records, missing-output diagnostics and
this real two-chunk result. These are not performance gains or universal proof
of rollout completeness. The extractor is read-only toward session storage; it
does not search other sessions, resume a model, or automatically publish contents.

Decision: retain CLI transport; use explicitly opted-in, reviewed rollout tool
evidence prospectively for comparisons requiring complete observations. Keep
equivalent persistence settings across comparison arms. Never retrospectively
rescore ephemeral runs from new outputs. Historical featured graphs stay frozen.

한국어: 새 세션 저장 기록에서 BEGIN과 END를 받은 실제 도구 응답을 모두 찾았고,
합친 출력은 92바이트로 원본 해시와 일치했다. 호출 인자와 동일 세션 폴링도
확인된다. 전체 기록은 로컬에만 보존하고 검토한 도구 기록 4개만 내보냈다.
이는 추가 증거 수집 경로의 검증이지 스킬 성능 향상은 아니다. 앞으로 비교군
모두에 같은 저장 설정을 적용하고, 이전 결과를 소급해서 바꾸지 않는다.
