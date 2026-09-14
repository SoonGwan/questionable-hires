# Model-issued output streaming diagnostic — frozen before launch

Parent `bd52397`; one fresh GPT-6 Astra medium ephemeral app-server turn, no skill,
240-second observation deadline, no automatic retry. Use exactly the frozen
`cli-yield-probe-01-cases.json` emitter and task, in a separate initialized project.
Do not read witnesses into model context or re-execute the command to repair logs.

Retain every incoming JSONL event, request and stderr. Compare command completion
output and separately concatenated `item/commandExecution/outputDelta` values
against the independent witness hash, then inspect final nonces and actual command
count. Keep streams separate; never add the completion aggregate to deltas and
thereby double-count bytes. Output-capture success is not task-performance success.

This installed app-server rejects the exec-specific `--ignore-user-config` and
`--ignore-rules` flags. Therefore this diagnostic is **not** cost-comparable to the
existing CLI runs. User config/rules/hooks remain in force; no global files or
credentials are edited. Process-local overrides suppress notify callbacks,
configured MCP servers, plugins, multi-agent tools and discovered personal skills.
Those restrictions are not proof of identical runtime instructions; inspect the
retained events for contamination before interpreting even this narrow result.

The preceding [native preflight](APP-SERVER-NATIVE-CAPTURE-01.md) covered full
delayed output, an actual assertion failure, truncation and timeout. It did not
test this model-issued event route. Existing featured results remain frozen.

Launch: `python3.11 -B benchmarks/app_server_model_probe.py --output benchmarks/local-runs/app-server-model-capture-01`.

## Startup defect, before any model turn

Launch `74fba98` exited before initialization with `invalid transport` for the
quoted MCP config key. The CLI override path did not interpret JSON key quoting
as intended. Keep `app-server-model-capture-01` as failed startup evidence.
The launcher now accepts only simple validated bare server names and refuses
ambiguous key escaping. Use a new output `app-server-model-capture-02` after this
correction; fixture/model/task remain unchanged. This is not a repeated model draw.

## Outcome — do not adopt this transport as a capture fix

[Startup evidence 01](results/app-server-model-capture-01/) retains the configuration
failure. [Model evidence 02](results/app-server-model-capture-02/), launch `de00a23`,
completed one Astra medium turn in 14.483 seconds of client observation. One recorded
command executed the frozen emitter once, exit 0. Supplied file contents remain
unchanged; the expected witness is present.

The single `item/commandExecution/outputDelta` contains only the 45-byte END line.
The completion aggregate contains the same END line. Neither contains the 47-byte
BEGIN prefix, although the model's final answer reports both fresh nonces correctly
and says a live-session poll was needed. The witness's intended 92-byte payload
hash matches the reconstructed BEGIN+END, not either captured command channel.
Reconstruction is author verification, not replacement model evidence.

The native standalone streaming success does **not** transfer to model-issued
commands. Do not replace the benchmark runner on that assumption. Installed personal
hooks ran, and built-in `codex_apps` initialized despite disabling named configured
MCP servers and plugins. No MCP tool call appears; only the prescribed command is
recorded. These environment differences further rule out cost comparisons. This
diagnostic neither isolates hooks as the cause nor proves complete skill-discovery
isolation. No controls, skill scores or featured graphs are changed.

Five offline reconciliation tests in `test_app_server_capture.py` pass, including
this adverse model result. Exports retain complete event/request streams and
source artifact hashes; local paths and server/installation identifiers are masked.
Next investigate prospective retention of model-visible tool responses, not another
unchanged model draw or more instructions on this already exposed fixture.

한국어: 실제 모델 호출에서는 중간 출력 이벤트도 END만 보존했다. 모델 답변에는
BEGIN도 정확히 있어 기존 누락 문제가 해결되지 않았다. 개인 훅과 내장 앱 연결도
존재해 기존 실행기와 동등한 성능 비교가 아니다. 실패한 시작과 실제 모델 결과를
모두 남겼으며 이 수집 방식은 해결책으로 채택하지 않는다.
