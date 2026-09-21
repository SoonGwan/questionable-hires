# Hostage completion boundary — unmeasured candidate

2026-09-21, parent `d971cc2`. Candidate resource:
`benchmarks/candidates/hostage-completion-boundary/skills/hostage-negotiator`.
Production and historical experimental resources are unchanged.

The [conditional experiment](HOSTAGE-CONDITIONAL-01-REVIEW.md) found that both
skill deliveries conflated completed work with an entry awaiting a completion
callback. Merely saying “follow entry, completion and recovery” did not surface
the interval. This candidate replaces only that existing stateful-work paragraph
to distinguish operation completion from deferred cleanup and inspect re-entry
when the requested contract depends on the distinction.

It is not an instruction to add a task.done check everywhere, force async tests
on synchronous work, implement a cache, or rewrite ownership. Existing/specified
values, errors, cleanup, cancellation and scoped tests remain required. All other
entry paragraphs, UI metadata, runtime assets and references match production.
This deliberately does not combine the rejected conditional-routing experiment
with the new hypothesis. No extra reference read is required.

Entry length is 711 → 716 whitespace-delimited words. This is not a tokenizer
measurement or a performance claim. Frontmatter validation and resource diff
inspection verify packaging only, not improved model decisions.

## Forward-test boundary

Do not rerun or tune the exposed shared-fetch task into a favorable replacement.
A new comparison must freeze at most two different tasks before model execution:
one lifecycle-boundary change outside that Python Loader shape, and an ordinary
synchronous change that checks whether irrelevant ceremony/cost increases. Use
contemporary baseline, prior production and this candidate, retain every attempt,
and inspect actual native assertions and complete cost. A real-project task is
preferable to another miniature copy of the exposed fixture; label author-selected
tasks honestly, not as independent holdout.

Native controls must include a contract-violating implementation with the same
API and a valid implementation. Check a boundary the intended fix could still
miss, not just that the old implementation fails. These controls are not a proof
of completeness; the frozen reference's earlier gap remains a counterexample.
Solutions/control outcomes stay outside model inputs. No favorable aggregate can
hide a correctness loss, and one favorable n=1 pair cannot become the featured
benchmark or justify a general 20–30% efficiency claim.

No new model sessions have run for this resource. Adoption remains undecided.

한국어: 작업 완료와 지연된 정리 사이의 재진입을 구별하도록 기존 문단 하나만
바꾼 후보다. 이미 본 과제를 다시 풀어 좋은 점수로 교체하지 않는다. 다른 과제의
실측 전에는 효과를 주장하거나 배포본·대표 그래프에 반영하지 않는다.
