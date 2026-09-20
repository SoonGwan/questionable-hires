# Hostage input-contract pilot 01 — frozen before model execution

2026-09-21. Two authored tasks × no-skill/original/candidate × one fresh session.
GPT-6 Astra medium, serial, 360 seconds per cell. Original resources `6516f5e`;
candidate applies only `hostage_input_candidate.revise` from `563d68a` to that
entrypoint. All supporting assets/references remain byte-identical. Production
skill stays unchanged pending evidence. This pilot is diagnostic, not release
approval or proof of the eight-skill objective.

## Schedule and preservation

Fixed order: opaque baseline → opaque original → opaque candidate → normalized
candidate → normalized original → normalized baseline. Use `run.py` with frozen
`hostage-input-cases-01.json`, one `--case`, `--arms baseline` or `--arms skill`,
`--repeats 1 --jobs 1 --seed 0 --timeout 360 --model gpt-6-astra --effort medium
--persist-session` and a new directory per cell. Snapshot identities and the
candidate transformation must be checked before execution. Stop on account limits;
preserve scheduled/unattempted cells. No candidate/fixture changes, retries,
replacement attempts or outcome exclusions after launch.

## Model-visible contracts and author controls

Both tasks fix failure/cancellation cleanup in a small Sender and add focused
unittest regressions. Existing success assertions stay. Duplicate suppression,
pending ownership, retry, separate instances, exact result/error propagation,
bounded tests and original preservation are explicit. One task accepts opaque
payloads and requires exact passthrough; the other requires strip/casefold values
and expressly does not require argument identity. Callback inputs must distinguish
the stated contract, not merely use trivial values. Helper adoption is optional.
No queue, dependencies or production refactoring is authorized.

The two tasks are authored, related synthetic inputs, not real-world issues or
independent holdouts. The author regression suite and corrected implementation
are not included in model-visible files. Preflight runs exact prepared projects
in temporary local copies: six native tests each, original cleanup failures,
healthy passes, argument-contract mutants fail by assertion, and an equivalent
fresh normalized string passes. Inputs and native transcripts are retained in
`hostage-input-preflight-01.json`. Original tree inventory is preserved and copies
removed. Initial preparation used `dict(payload)` as a copy mutant, which also
caused an unrelated string-input type error; before freeze this was replaced by
generic `copy.copy(payload)`. That preparation failure is not a model attempt.

## Review and decision

Review all five frozen criteria from actual edits, native commands/results and
final artifacts, not prose or method count. Confirm existing assertions remain,
new assertions distinguish the argument contract, state/error/cancellation checks
are bounded and cleanup is owned. Retain all additional work and repairs. Author
post-run checks may exercise a copied final project, never alter original evidence:
healthy behavior, a callback argument-copy mutation for opaque payloads, or missing
normalization for normalized payloads; a semantically equivalent fresh normalized
string must not be penalized. Separate those replays from original model evidence.
Review assertion failures versus support/setup errors before accepting a control.

Reconcile original session/CLI usage and inspect exact skill exposure privately.
Export only reviewed artifacts; never private initial instruction text. Report all
costs: input+output tokens with cache counted once, wall time, recorded responses,
success/scope and incomplete observations. Fewer tokens with weaker required
coverage is not a win. More generated tests do not prove stronger coverage.

Do not promote a single favorable pair or these related n=1 cells to a broad
efficiency claim. Do not retune the old refresh-owner task or these exposed tasks
after results. A candidate that over-constrains valid normalization, loses coverage
or adds unjustified cost is not adopted merely because it catches one copying fault.

한국어: 서로 다른 전달·정규화 계약의 두 과제를 무스킬·기존·후보 총 6회로
비교한다. 요구사항과 정상·결함 대조를 먼저 고정하며 기존 테스트를 약화시키거나
허용된 정규화를 잘못으로 판정하면 통과로 보지 않는다. 모델 실행과 개발자
재검증을 구분하고 토큰·시간·실제 결과를 모두 기록한다. 아직 새 모델 결과는 없다.
