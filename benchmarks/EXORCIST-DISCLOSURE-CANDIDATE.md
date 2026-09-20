# Conditional detail candidate — not adopted or model-tested

2026-09-21, source `104e010`. This investigation uses the already reviewed
[HTTPX upload experiment](results/httpx-upload-replay-01/README.md); it is not a
new execution, rescore or performance result.

## What the original records actually support

Both conditions use five recorded responses and four shell commands, with all
five task criteria satisfied. Source-reading commands `item_2` and `item_3` emit
33,139 captured characters for baseline versus 23,235 for skill. These are output
character counts, not source coverage or token savings. Baseline's missing CLI
probe output remains recoverable only from its original stored response; it is
not counted as zero evidence or used in these source-reading totals.

The existing `analyze_response_costs.compare` applied to their retained
`usage-profile.json` files reconciles the total +1,474 tokens as:

| Arithmetic term | Skill minus baseline |
| --- | ---: |
| Response-count term | 0 |
| First-input term | +4,105 |
| Later-input term | −2,773 |
| Output term | +142 |

First-response input is 15,001 versus 15,822; both have five responses.
These are accounting identities, not causal attribution to the skill or estimates
of recoverable cost. Initial context includes more than skill instructions; later
context includes required evidence and generated work. In particular this trace
does **not** support another rule to suppress source inspection: the skill already
reads less source output, yet has higher total recorded cost.

## Narrow candidate and its tradeoff

`exorcist_disclosure_candidate.revise` accepts only the frozen entrypoint SHA-256
`8bab259a8b49f9e653ce289dea938d32bdae98137ab8ab80f08cdb8cec484f20`.
It moves optional runner invocation/format specifics out of the main body, using
the already existing `references/bounded-probe.md` as the conditional destination.
Description, diagnostic method, synchronous hang-risk routing, async cancellation
warning, owned-task cleanup, scope, and evidence requirements remain. The guide
and executable stay byte-identical. The main body still says to read the guide
before using that runner, so cleanup-after-normal-exit limits remain discoverable.

UTF-8 entrypoint size is 3,712 → 3,356 bytes (356 fewer, **not measured tokens**).
Candidate SHA-256:
`41a58b6df6f812bf58f148336c5ac3ffc9e4504547bafc2e3df922ec8c271de9`.
Two transformation-integrity tests and 15 unchanged process-runner tests pass.
Neither validates model routing or efficiency. The candidate is benchmark-only;
installed skills, invocation metadata, production documentation and charts do not
change. It is not a second global lean rewrite or an instruction to bypass
host-required skill reads.

## Disposition before spending more model calls

Do not launch a comparison solely because this saves 356 entrypoint bytes.
There is no evidence it could deliver the requested large whole-task improvement;
it may add a reference-read turn on process-contained tasks. No percentage of
whole-session savings is predicted. Keep this candidate unadopted rather than
repeatedly running an exposed HTTPX case until a favorable result appears.

Reconsider only with a concrete repeated loading bottleneck worth testing, using
both bounded normal work and a genuinely blocking/cancellation-suppressing path.
Any such experiment must freeze the task, native positive/negative controls,
model-visible obligations, original/candidate/baseline resources and complete
schedule before launch. Observe original exposure and guide use, required process
containment, actual diagnostic outcomes, source preservation, and all cost records.
The previously exposed HTTPX case can only be a regression, not a blind holdout.
Faster incomplete diagnosis or missing cleanup is not an improvement.

한국어: 기존 HTTPX 기록에서 스킬은 소스 출력량을 줄였지만 총 토큰은 더 썼다.
선택적 도구 설명을 기존 안내문으로 옮기는 후보는 본문 356바이트만 줄이며,
필요한 작업에서는 안내문 읽기가 늘 수 있다. 후보를 배포하거나 새 모델 실험을
실행하지 않았다. 큰 성능 개선을 입증한 것으로 보지 않고, 실제 반복 비용과
일반·멈춤 위험 작업의 대조가 마련되기 전에는 채택하지 않는다.
