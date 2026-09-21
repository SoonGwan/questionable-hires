# Contract audit transfer 01 — frozen before calls

2026-09-21. Two authored Python test-audit tasks; baseline, prior Con Artist
`903e7c8`, current `19d63ec`. The only skill difference is the contract-focused
assertion guidance described in [the candidate](CON-ARTIST-CONTRACT-01.md).

JSON response contract permits serialization differences but requires decoded
content/order/duplicates. Registry contract requires original object identity and
shared edits, separate keys and missing-key behavior. Both initial suites have a
real assertion gap. Author preflight executes original and stronger tests on
correct, narrowly faulty and alternate-valid actual implementations: 12 native
runs, with actual count/identity failures and neighboring controls preserved.
The oracle, alternate and author mutation are not model-visible inputs.

Six serial fresh GPT-6 Astra medium sessions, n=1, 360 seconds each. Frozen order:
response baseline/prior/current, identity current/prior/baseline. Do not retry,
substitute or omit a failed/slow cell. Stop on account limit; preserve unattempted
schedule. Store full original sessions privately; export only reviewed redacted
tool evidence, never private initial messages. Inspect actual initial skill
exposure and original native outputs; CLI suffix omissions are not replayed.

Freeze task/criteria/files, instructions, runner hashes, resource bytes/modes and
interpreter before calls. Preparation and execution are separate; exclusive
marker refuses restarting. Use existing Python stdlib, no installs. Audit scope,
native binding, original preservation and project-local cleanup are explicit.

Review all five obligations per case from actual commands/assertions/artifacts,
not answer confidence or green exits. Keep repair costs and unsupported stronger
assertions visible. Report input plus output tokens (cache/reasoning included
once), process wall time, responses and tool calls, with prior/current/baseline
comparisons and unequal work disclosed. Efficiency is meaningful only with the
required contract preserved. Never reward omission of required identity checks.

These are small, closely authored candidate-targeting tasks, not an independent
holdout, real-production study or causal whole-skill estimate. A good result is
only a transfer signal; a bad result remains evidence. No featured promotion.

한국어: 표현의 자유를 허용해야 하는 과제와 객체 동일성이 필수인 과제를 함께
비교한다. 필수 검증 누락으로 얻은 절감은 개선으로 인정하지 않는다. 2개 작성
과제의 결과를 전체 스킬 성능이나 실무 일반화의 증거로 과장하지 않는다.
