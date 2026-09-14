# App-server native capture preflight — 2026-09-15

The [previous CLI localization](CLI-OUTPUT-LOCALIZATION-01.md) reproduced missing
leading command output. This separate native check tests a potential streaming
transport, not a skill, a model turn, or a replacement performance benchmark.

[Official app-server documentation](https://learn.chatgpt.com/docs/app-server)
describes separate output notifications. The installed codex-cli 0.153.4 generated
schema additionally specifies that `command/exec` streaming requires a process ID,
emits base64 chunks with per-stream truncation flags, and does not duplicate them
in the final response. This standalone method is distinct from the model-turn
notification `item/commandExecution/outputDelta`.

## Native observations

[Evidence](results/app-server-native-capture-01/) comes from one invocation of
`app_server_capture_probe.py`, with four sequential commands. No model or thread
was created, no skill loaded, no global configuration edited and no service
published. Each command used the project-local writable root, disabled network
access and excluded general temp-directory write grants. The owned stdio server
terminated at the end.

| Command | Observed evidence |
| --- | --- |
| Same frozen delayed emitter | Full 92 bytes in two chunks; witness SHA-256 matches; exit 0 |
| Deliberate assertion failure | Leading stdout plus actual=1 / expected=2 AssertionError retained; exit 1 |
| 128 bytes with 16-byte cap | 16 bytes retained, explicit `capReached: true`, exit 0 |
| Wait beyond 500 ms deadline | Leading output retained, exit 124 |

Final responses have empty stdout/stderr, as specified for streamed execution.
The client preserves raw notifications independently and joins bytes per stream,
in arrival order. It does not infer application-level ordering across stdout and
stderr. The assertion probe produced a genuine assertion failure, not setup error.
The capped probe illustrates why exit 0 alone is not complete evidence.

`python3 -B -m unittest discover -s tests -p test_app_server_capture.py` reconciles
the four records against original exported notifications, terminal responses and
the delayed-output witness. It replays no commands. Source artifact hashes are
retained; export replaces local paths and server/installation identifiers only.

## Decision and boundary

The native streaming channel passes this preflight. It is not yet verified for
model-issued commands: that separate notification has a different schema. Before
changing the benchmark runner, test one fresh delayed-output model session with
raw incremental and completion records both retained. Preserve current model,
effort, permissions and skill isolation, and disclose any transport differences.
Do not retrofit these author-side outputs into old model evidence.

한국어: 모델 없는 사전 검사에서는 중간 출력 수집으로 기존 누락 사례의 전체
출력을 보존했다. 실제 assertion 실패, 출력 잘림 표시, 시간 초과도 확인했다.
하지만 모델이 호출하는 도구 경로까지 검증한 것은 아니다. 기존 벤치마크나
그래프는 그대로 두고, 다음에는 모델 실행에서 별도 출력 이벤트를 확인한다.
