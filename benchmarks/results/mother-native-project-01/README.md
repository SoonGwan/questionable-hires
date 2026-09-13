# Native test integration: useful transfer, flawed clean control

Mother-in-law used the existing unittest setup in both project-shaped cases,
reused its controlled API support and did not attempt its incompatible generic
helper. Baseline did the same. All original files stayed byte-identical; additions
were confined to permitted `tests/test_qa*.py` files.

Recorded equal-case costs were **21.6% lower tokens and 21.7% lower process time**
with skill. **This is not an accepted broad efficiency or quality win:** additional
coverage differs, one repetition is small, test support has a naming defect, and
the author-designated clean control has an underspecified failure contract.

한국어 요약: 스킬이 범용 helper에 맞지 않는 구조에서도 기존 unittest와 테스트
지원 코드를 활용했고 원본을 보존했다. 기록상 토큰 21.6%, 시간 21.7% 감소지만,
추가 검사량 차이와 평가 과제의 결함 때문에 성능 우위의 확정 근거로 사용하지 않는다.
양쪽이 발견한 OSError 문제를 평가자의 의도와 다르다는 이유로 오탐 처리하지 않는다.

## Frozen run and all cells

[Protocol](../../MOTHER-NATIVE-PROJECT-01.md),
[fixtures/criteria](../../mother-native-project-cases.json), [manifest](run.json).
GPT-6 Astra medium; 2 cases × 2 arms × 1 fresh session, sequential shuffled
schedule, seed 20260914, 240-second session limit. Four completed; no timeouts,
reruns or exclusions. Skill resources stayed unchanged during the experiment.

- Source revision: `c6d0fc1014fe08d4acd0c6f06b9dcd19d803534d`.
- Resource digest: `d2007607adb02f51f59be5d8e84322e0fb364a3b056b59a78e684b182d6cf908`.
- Fixture digest: `390ff81667b828e8ce88fcc112457b47602902996fc897669164132e5615afcf`.

Tokens = input including cached input + output. Seconds = model process wall
time, not test runtime. Adjacent per-cell files retain commands/output, answers,
metadata, source hashes and final project snapshots.

| Case | Arm | Tokens | Cached input | Seconds | Actual final suite |
| --- | --- | ---: | ---: | ---: | --- |
| Unguarded | [baseline](native-catalog-unguarded--baseline--1/answer.md) | 115,405 | 98,560 | 91.666 | 15 tests, 5 failures |
| Unguarded | [skill](native-catalog-unguarded--skill--1/answer.md) | 98,125 | 72,960 | 76.751 | 10 tests, 4 failures |
| Guarded | [baseline](native-catalog-guarded--baseline--1/answer.md) | 128,204 | 107,264 | 104.421 | 10 tests, 1 failure |
| Guarded | [skill](native-catalog-guarded--skill--1/answer.md) | 92,079 | 72,320 | 76.052 | 8 tests, 1 failing subtest |

Per-case skill/baseline token ratios: `0.8502664529`, `0.7182225204`.
Time ratios: `0.8372897257`, `0.7283209316`. Average the two ratios equally,
then subtract from one: 21.5756% tokens / 21.7195% time. These are descriptive
measurements, not adjusted for unequal additional work or cache differences.

## Review: what the execution proves

Both unguarded sessions reproduce stale successful responses replacing newer
titles and restoring cleared results. Older errors remain guarded; nearby normal
behavior and retry pass. They also observe older success clearing a newer error
and modifying state while a newer search is pending. Baseline adds more normal
variants and multi-request coverage; skill relies more on the existing tests.

Both guarded sessions exercise ordering, clearing and recovery successfully for
RuntimeError. Both additionally inject OSError and reproduce an escaping task
exception with no displayed error. Their retained unittest output includes actual
and expected failure states. This is not a timeout or an inferred code-only claim.

Review covered each retained QA file, imported production/support code, actual
command outputs, and original-file comparisons. All four exported projects were
replayed separately in temporary directories with a 20-second subprocess cap.
Replays returned the same test/failure counts shown above. They are **author
replays**, excluded from model usage/time, not replacements for original evidence.

## Authoring defects and evidence limitations

1. `CatalogCase.fail` accidentally overrides unittest's assertion method. Passing
   smoke tests do not expose this. Sequence assertions can raise `TypeError`
   instead of preserving expected/actual mismatch details. Both unguarded arms
   repair the collision only in their added test subclass and rerun. Guarded
   baseline handles the collision too; guarded skill's scalar OSError mismatch
   reports an actual AssertionError through unittest's scalar comparison path.
   The repair work is included in measured costs. This was an authoring mistake,
   not an intended benchmark challenge.
2. The requirements describe current failures without restricting exception
   types, while implementation/support cover RuntimeError. The frozen guarded
   criterion expected no defect. Both agents reasonably explore OSError and find
   the same real behavior; **the clean-control criterion is not satisfied and its
   premise is invalid for a false-positive comparison**. It is not retroactively
   rewritten or used to penalize these findings. No clean-case accuracy or overall
   superiority score is claimed.
3. Empty command-output events: unguarded baseline `item_8` (silent file edit);
   unguarded skill `item_7` (first test run) and `item_9` (silent edit); guarded
   skill `item_5` (first test run). Subsequent outputs retain decisive assertions
   and final summaries. Some nonempty captures begin partway through verbose
   output. The missing first outputs remain missing; no complete-capture claim.
4. These are authored synthetic projects, explicit invocation, shared host/cache,
   one repetition, and unequal extra cases/subtests. They do not establish
   automatic selection, browser QA, real external-project utility, or an
   identical-work speedup. The original three smoke tests alone were inadequate
   to validate the evaluation harness.

The frozen data and skill remain unchanged. New benchmark authoring rules require
negative assertion-path preflight and explicit failure contracts before labeling
a fixture clean. Local tests preserve and document this historical support defect
so a future edit cannot silently rewrite its effect on the reported experiment.
Existing featured charts remain tied to their own frozen revision.

Post-review local regression: 273 repository tests pass in 43.328 seconds,
including the generator/frozen-file match, an independent ordering oracle and
the support collision regression. Catalog/link and featured synchronization
checks pass. These are repository checks, not additional model sessions.

## Reproduce

Model run into a new directory (consumes account usage):

```sh
python3 -B benchmarks/run.py --output benchmarks/local-runs/mother-native-new \
  --cases-file benchmarks/mother-native-project-cases.json --arms baseline skill \
  --repeats 1 --jobs 1 --seed 20260914 --timeout 240 \
  --model gpt-6-astra --effort medium
```

Use the recorded skill snapshot to reproduce this experiment, not later changes.
For model-free inspection, copy a cell's `project/` into a disposable directory and
run `python3 -B -m unittest discover -s tests -t . -v` there. Nonzero exit is expected
for the documented reproduced defects. Do not repair the archived fixtures in place.
