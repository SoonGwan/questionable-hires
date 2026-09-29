# Interpreter route01 original evidence follow-up — 2026-09-27

Measured resource remains `e918d02d`, predecessor `75183f2f`, launch `07d9d2ed`.
[Costs](INTERPRETER-ROUTE-01-COSTS.md) remain mixed. This follow-up adds original
output recovery and scoped artifact evidence, not a new model run or cost claim.
Complete per-cell quality labels remain pending.

[Artifact review](results/interpreter-route-01/artifact-review.json) verifies all
six exact original inventories, bytes and initial tracked modes, Git HEAD,
captured before-model/before-collector index bytes/mode, and installed-resource
identity. All specified controls hold; owned scratch is absent from final files.
The four original files include LICENSE and source-origin.json. This is final-state
evidence, not every transient action or all Git metadata. Post-collector skill
files have intent-to-add status because the existing collector runs `git add -N`;
that is not model staging, and is distinct from the captured unchanged model index.

Both documented skill CLI aggregates omit the beginning of the native execution.
Matching retained original tool records recover it without author replay:

- [Predecessor line36](results/interpreter-route-01/predecessor/interpreter-history-documented--skill--1/native-tool-output-line-36.txt)
- [Candidate line40](results/interpreter-route-01/current/interpreter-history-documented--skill--1/native-tool-output-line-40.txt)

The native scripts load complete current/proposal modules, register them in
sys.modules and assert actual __call__/started globals retain module bindings.
Only the proposal's historical started method is substituted; current constructor,
producer and neighboring source remain. Ordinary exact-object completion and
repeated independent handles/futures with reversed completion execute before the
cancellation assertion. No rewritten service or setup error supplies the failure.

At cancellation callback time the waiter is pending, queue size1 and cancel()
accepted. Current ultimately cancels its waiter and keeps queue size1; proposal
returns a handle despite cancellation and leaves queue size0. Application tasks
remain pending; recovered/returned handles produce their exact selected object.
Native current exits0 and proposal exits1 with the actual cancellation-contract
AssertionError. Separate after-delivery controls keep consumed handles consumed.
Scheduling is bounded cooperative call_soon checkpoints, not elapsed-time delays.

Documented baseline separately executes five scenarios per variant, ten processes:
ordinary, repeated, empty cancellation, delivered cancellation and wakeup
cancellation. The two skill arms execute two processes each containing their
required scenarios. Those different process counts and extra baseline controls
remain included in recorded costs; do not attribute cost differences solely to
interpreter discovery or claim identical extra coverage. Python3.11.6 observations
do not prove every supported interpreter; predecessor's scratch diagnostic uses
Task.cancelling(), and is not verified on Python3.9.

Candidate documented coordinator prints individual process exits but does not
assert their expected vector. Original outputs supply the actual0/1 observations;
the coordinator's exit0 alone would be insufficient evidence. Predecessor asserts
its expected [0,1] vector. Preserve this evidence-quality distinction instead of
relabeling coordinator completion as task success.

No original source is repaired, model execution repeated, feature promoted or
quality score assigned by this partial review. Remaining complete six-cell source,
history reasoning and scope review must use original records. The all-eight
developer quality, lower whole-task tokens and faster completion goal remains open.

한국어:6회 최종 원본 파일·모드·HEAD·모델 실행 전후 인덱스·설치 리소스는
명시한 범위에서 일치한다. 수집기가 나중에 만든 intent-to-add 상태를 모델
스테이징으로 오인하지 않는다. 문서 지정 조건의 스킬2회에서 빠진 출력은
원본 기록에서 복구했으며 재실행하지 않았다. 실제 취소 assertion과0/1
종료를 확인했지만 후보의 조정자는 예상 종료 벡터를 assert하지 않는다.
부가 검증·프로세스 수도 다르므로 실행기 발견만 비용 차이의 원인으로
단정하지 않는다. 전체 품질 검토와8개 스킬의 동시 비용 개선은 미완료다.
