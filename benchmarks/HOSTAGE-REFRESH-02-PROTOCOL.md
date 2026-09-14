# Refresh-owner 02 — prospective follow-up, 2026-09-15

Measured candidate `0a94dab` separates native test commands from final review
commands. [Prior run](HOSTAGE-REFRESH-01-REVIEW.md) exposed two unsupported skill
pass claims. This is an exposed development set, **not a held-out confirmation**.
No new task, oracle, scoring obligation, model or helper implementation is added.

Use the identical `hostage-refresh-cases.json`, SHA-256
`7b0bc8120865802a29dd97b6fedb9863bdbe19742ce68bb93307588b55a04c21`.
Four fresh sessions: two variants × baseline/explicit skill × one repeat, serial,
Astra medium, seed 20260911, 240 seconds/cell. Keep both arms fresh; do not reuse
prior baseline costs as contemporaneous controls. No selected retries. Stop
scheduling on account limits and retain failed/unattempted/unknown-usage cells.

The model sees only its project contract and task, plus the installed skill in
that arm. No prior conclusions, bug labels, oracle or protocol are passed in.
Freeze input/resources before launch; no author tests, edits or other benchmark
workloads during measured execution.

## Decision criteria

Review original native test identities/count/results and test-specific exit,
separately from application correctness. A printed exit or final Git output alone
does not substantiate a pass claim. Record if tests use dedicated commands,
whether results are captured and whether the model responds correctly to missing
evidence. Dedicated commands alone are not a success criterion or proof of cause.

Retain the first protocol's explicit behavior/scope obligations: concurrent
callbacks, latest ownership across success/failure/cancellation/retry, exact
per-call results/errors, prior display, synchronous failure and independent
instances; preserve valid production and owner notes. Review actual test paths,
not their names alone. Preserve every adverse observation and original gap.

After timing, reconcile original usage, source/resource hashes and installed
resource stability. Replay retained tests in disposable project-local copies
against final production, faulty cleanup and a valid counter-step alternative;
run the frozen separate author oracle on final production. These controls do not
repair original evidence. Publish all four cells with raw-derived per-pair and
sum costs, scope, work differences, reports and limitations. No general 20–30%
claim, historical chart rewrite or featured promotion from this development run.

This design keeps scoped criteria and log review separate from broader production
validation, consistent with [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-refresh-cases.json --output benchmarks/local-runs/hostage-refresh-02 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

## 한국어

테스트 명령을 분리한 `0a94dab` 후보를 같은 과제로 다시 확인한다. 이미 개선에
사용한 개발용 과제이므로 새로운 과제에서의 일반화 검증으로 부르지 않는다.
기본/스킬을 모두 새로 4세션 실행하고 원본 테스트 출력·통과 보고·동시성 동작·
비용을 함께 본다. 출력 누락과 불리한 결과를 제외하지 않으며 별도 재실행을
원본 증거로 대신하지 않는다. 실행 중 수정이나 작성자 테스트는 하지 않는다.
