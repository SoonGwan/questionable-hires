# Unpromoted all-eight entry redesign — 2026-09-15

Base resources: `3aaef96`. [Candidate builder](lean_entries.py) rewrites only
entry bodies in an isolated benchmark snapshot. It preserves the exact original
frontmatter; no production skill file, helper, UI metadata, installation flow or
featured result is changed. Candidates are Python data, not extra discoverable
`SKILL.md` directories in the repository.

## Hypothesis

Recent narrow guide/AST changes have not established whole-task gains. Optional
helpers were often unused, and fewer shell commands did not guarantee fewer
outer calls. Test a different level of change: concise outcome/decision guidance
across all eight roles instead of continuing single-case wording additions.
This may reduce instruction/context cost and leave the model more room to choose
its workflow. It may also lose useful operational reminders; that risk must be
measured, not dismissed because entries are shorter.

The candidate retains role-specific obligations, scope boundaries, actual-runtime
evidence, uncertain-result handling, bounded async cleanup, compiler/binding
context where applicable, and conditional access to existing resources. It removes
repeated workflow recipes and case-specific procedural elaboration from entries.
No forced helper adoption, reduced user requirements or weaker pass criteria.

| Role | Base entry bytes | Candidate bytes | Entry reduction |
| --- | ---: | ---: | ---: |
| Necromancer | 2,943 | 1,570 | 46.7% |
| Receipt | 2,006 | 1,479 | 26.3% |
| Landlord | 2,216 | 1,487 | 32.9% |
| Mother-in-law | 2,794 | 1,704 | 39.0% |
| Exorcist | 3,712 | 1,672 | 55.0% |
| Hostage Negotiator | 4,362 | 1,876 | 57.0% |
| Con Artist | 3,958 | 1,887 | 52.3% |
| Friday | 3,549 | 1,801 | 49.3% |

These are UTF-8 entry-file lengths including unchanged frontmatter, **not model
token savings or speedups**. The descriptions used for skill selection are unchanged.

## Verification completed

Three [packaging tests](../tests/test_lean_entries.py) pass: exact all-eight coverage
and unchanged metadata, deterministic/idempotent transformation, valid in-skill
resource links, invalid-frontmatter rejection, and unchanged original entry bytes.
All eight generated entries pass the skill validator in an owned temporary directory,
removed after validation. No model has evaluated these candidates yet; these
checks establish packaging, not behavioral adequacy.

## Next evidence required before promotion

Freeze no more than eight unique development tasks, covering all eight roles,
before launching any comparison. Include meaningful known failure boundaries,
normal controls and required deliverables; disclose reused inputs. Each task must
have author-verified native positive and defect-specific negative controls.
Keep no-skill/current/lean conditions separate with identical inputs/resources
except the entry body. Record full outcomes, original outputs, costs and failed
attempts; balance order and disallow favorable reruns. Preserve the exact candidate
and protocol hashes. Do not claim broad superiority from one development screen.

Review lost reminders explicitly: current-versus-historical evidence; native
before/after verification; justified single-consumer abstractions; intermediate
interaction states and mutable snapshots; causal diagnostics versus simulations;
scoped changes with native test evidence; assertion plumbing versus real fault
detection; and new writes surviving rollback. Compare correctness/scope before
resource totals. A cheap incomplete answer fails, and an unmeasured condition
remains unknown. The current released entries remain default until stronger
evidence supports replacing them.

한국어: 8개 스킬의 핵심 판단 기준과 도구 접근을 남긴 짧은 진입 지침 후보다.
기존 설치본은 바꾸지 않았다. 문서 길이는 26~57% 줄었지만 성능 개선율은 아니다.
다음 비교는 최대 8개 작업으로 전 역할을 다루고, 실패를 놓치거나 요구 결과를
줄인 답변은 빠르더라도 탈락시킨다. 실제 모델 검증 전에는 배포본으로 승격하지 않는다.
