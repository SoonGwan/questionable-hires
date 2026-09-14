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
