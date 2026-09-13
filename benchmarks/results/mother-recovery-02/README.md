# Recovery QA: retained evidence, less repeated harness work

In this **two-case authored development experiment**, Mother-in-law used
**17.2% fewer total tokens and 67.0% less process wall time** than no-skill
baseline. Both arms met the frozen required outcomes in 4/4 sessions: the sticky
error was found twice and the clean implementation was accepted twice.
Baseline performed additional overlap checks, so this is **not identical-work
speedup**, independent real-project validation, or an eight-skill efficiency claim.

한국어 요약: 직접 작성한 오류 복구 과제 2개를 각 조건에서 2회씩 실행했다.
스킬 사용 시 토큰은 17.2%, 실행 시간은 67.0% 줄었다. 양쪽 모두 결함 2/2회를
탐지했고 정상 코드 2/2회에서 오탐하지 않았다. baseline이 더 많은 응답 조합을
검사했으므로 동일 검사량의 속도 비교는 아니다. 소규모 개발 실험이며 기존 대표
벤치마크나 전체 스킬의 성능을 대체하지 않는다.

## What actually improved

Revision `699cdba` adds a current-failure → successful-retry check to the reusable
async component helper. It now catches an error left visible after a successful
retry, in addition to checking nearby normal behavior and stale completions.
Optional `--output NEW.json` retains the same execution's result and refuses
existing files. No duplicate model-authored harness is needed for this interface.

An author replay of the prior helper (`77c1357`) and the changed helper against
the exact same fixture sources found:

| Implementation | Prior helper | Changed helper |
| --- | --- | --- |
| Sticky error after successful retry | Incorrectly all passed | Recovery check failed |
| Correct error clearing | All passed | All passed |

This is helper-level regression evidence, separate from the model comparison.
The model experiment compares changed skill against **no skill**, not old skill.
All four skill sessions used the helper directly and retained its actual JSON.

## Frozen execution

- [Protocol](../../MOTHER-RECOVERY-02.md), [fixtures and criteria](../../mother-recovery-cases.json), [manifest](run.json).
- GPT-6 Astra, medium; Codex CLI 0.153.4; 2 cases × 2 arms × 2 fresh repetitions.
- Seed 20260913; shuffled sequential schedule; 240-second limit per session.
- Source revision: `699cdba036edb559b809f604b46c7f3d2c1b38a0`.
- Skill resource digest: `1b1a515508aa126156b4def81097b6dd937b81b54069bfa0d71396aec335b8fc`.
- Cases digest: `ca0e899eb38527f3da1b0b93c80d294bb3a88edd2b2ffd619baa114baa6fbe0b`.
- All 8 scheduled sessions completed; no timeouts, exclusions, or retries.
- No recorded usage gaps, empty command-output events, rejected patches, or
  changed installed resources. These diagnostics cannot prove complete capture.

## Every measured cell

Tokens are input (including cached input) + output, not billable-dollar estimates.
Time is the whole Codex process, not the millisecond duration of the Python test.
Links lead to the actual answer; adjacent `commands.json`, `metadata.json` and
`project/` contain execution output, usage, retained JSON, and fixture/harness code.

| Case | Arm / repetition | Total tokens | Cached input | Seconds | Reviewed required outcome |
| --- | --- | ---: | ---: | ---: | --- |
| Sticky error | [baseline 1](recovery-sticky-error--baseline--1/answer.md) | 107,517 | 87,424 | 106.039 | Met; recovery defect found |
| Sticky error | [baseline 2](recovery-sticky-error--baseline--2/answer.md) | 87,380 | 72,064 | 101.643 | Met; recovery defect found |
| Sticky error | [skill 1](recovery-sticky-error--skill--1/answer.md) | 84,936 | 71,808 | 31.571 | Met; recovery defect found |
| Sticky error | [skill 2](recovery-sticky-error--skill--2/answer.md) | 84,232 | 76,928 | 34.776 | Met; recovery defect found |
| Guarded clean | [baseline 1](recovery-guarded-clean--baseline--1/answer.md) | 105,066 | 85,504 | 103.292 | Met; no defect reported |
| Guarded clean | [baseline 2](recovery-guarded-clean--baseline--2/answer.md) | 87,769 | 71,936 | 95.652 | Met; no defect reported |
| Guarded clean | [skill 1](recovery-guarded-clean--skill--1/answer.md) | 84,840 | 71,936 | 37.018 | Met; no defect reported |
| Guarded clean | [skill 2](recovery-guarded-clean--skill--2/answer.md) | 67,088 | 60,288 | 30.921 | Met; no defect reported |

Average repetitions within each case/arm first, divide skill by baseline, then
average the two case ratios with equal weight. This produces token ratio
`0.8279259768` and time ratio `0.3304812417`; savings are `1 - ratio`.
Per-case token ratios are 86.8% (sticky) and 78.8% (clean); time ratios are 31.9%
and 34.1%. Two repetitions are insufficient for a robust variability estimate.

## Evidence review and unequal coverage

The review inspected actual execution commands, generated baseline harnesses,
retained execution records and answers, not just final prose. All original fixture
files match the frozen input exactly. All four skill stdout JSON objects match
their retained JSON objects. The helper records checkpoint verdicts and final
states, not every intermediate state's raw fields.

Both arms exercised normal success, current failure/retry, older success after
newer success, and older failure after newer success. Sticky sessions reproduced
the retained error; clean sessions passed those checks. Required reproduction
commands and Python-component limits were reported. No dependency installation
or existing-source change was observed.

Baseline wrote bespoke harnesses with 8–10 scenarios and 19–29 state checks,
including older completions while a newer request is pending and older responses
after a newer failure. Skill ran four targeted sequences. Some baseline checks
also inspect the internal generation counter. These are useful additional checks,
not proven waste. The observed saving combines helper reuse, narrower additional
coverage and shorter reports; this experiment cannot separate those causes.

After the model runs, the author replayed all eight exported projects in separate
temporary directories with a 20-second subprocess cap: sticky executions returned
1 and clean executions returned 0. These replays are not model sessions, are not
included in usage/time, and do not replace the original execution records.
Skill replay used the unchanged committed helper because installed `.agents`
resources are intentionally excluded from exported projects.

The full repository regression at the implementation revision passed **267 tests**
in 45.359 seconds. Skill schema validation and the featured-language/chart sync
check also passed. These checks do not establish broad model performance.

## Limits and next acceptance boundary

These two closely related fixtures were authored to exercise this helper change;
they are not held-out tasks. Explicit skill invocation does not test automatic
selection. Shared host/cache, only two repetitions, and unequal extra coverage
limit generalization. Cooperative async deadlines do not preempt synchronous
blocking. Browser behavior, cancellation, other error contracts, and real project
test-runner integration remain outside this experiment.

The historical featured five-case confirmation stays unchanged. Before promoting
this version as a broad resource improvement, freeze it and evaluate previously
unseen project shapes with existing runners, incompatible helper interfaces and
normal/defective pairs. Preserve adverse outcomes and require actual execution
evidence; do not optimize or select the reporting set to reach a target percentage.

Re-run the frozen matrix only into a new directory (consumes model usage):

```sh
python3 -B benchmarks/run.py --output benchmarks/local-runs/mother-recovery-new \
  --cases-file benchmarks/mother-recovery-cases.json --arms baseline skill \
  --repeats 2 --jobs 1 --seed 20260913 --timeout 240 \
  --model gpt-6-astra --effort medium
```
