# Proportional provenance candidate — 2026-09-15 KST

Parent `ec5d7d4`. The [HTTPX exception audit](results/httpx-exception-example-01/README.md)
shows full helper reading plus a bespoke pytest collection plugin, one setup
failure and repair despite already available copied-import and behavioral evidence.
Costs regress substantially. This motivates a narrower decision rule, not a claim
that one plugin alone caused the measured overhead.

The entry now establishes the exercised path through copied-import evidence,
traced bindings and defect-specific observations. Extra instrumentation addresses
an explicit requirement or unresolved dispatch; it does not duplicate established
evidence. The optional guide says its unittest precheck example is not a request
to build a pytest plugin. Post-collection checks remain appropriate for material
later rebinding. Separate import processes still cannot establish what tests load;
setup errors still cannot count as killed faults. Trust/adaptation/troubleshooting
can still justify implementation reads. Helper code and defaults are unchanged.

Local controls in `tests/test_audit_documented_probe.py` include an actual consumer
import switching from `service.save` to `fallback.save`: with the former, native
correct tests pass and the storage-removal mutant fails the actual assertion;
with the latter, the same-process identity precheck fails with exit 6 before
running tests. No arbitrary `assert False` substitutes for the wrong binding.
Original files remain intact and owned scratch is removed. Existing three
conditional/unconditional documented-recipe subcases still pass. These controls
test execution boundaries, not whether a model follows the new prose.

Two tests / five subcases pass in 0.535s; 76 helper tests pass in 13.526s; 12 build
tests pass in 3.312s. Skill validation passes. Entry grows 4,012→4,155 bytes and
optional guide 5,308→5,567 bytes. Added instruction cost is real; no token savings
are inferred from native tests, fewer expected commands or this candidate's intent.
Actual model uptake and net performance remain unmeasured. No benchmark rerun,
chart update or regression claim against the old run.

한국어: 출처 확인을 매번 새 pytest 플러그인으로 확장하지 않도록 수정했다.
명시적 요구·실제 바인딩 불확실성은 계속 검사한다. 테스트가 다른 구현을 호출하는
대조에서는 사전 확인이 실제로 실패하고, 올바른 호출에서는 정상 통과·결함 실패를
확인했다. 관련 90개 테스트가 통과했지만 모델 행동·비용 개선은 미측정이다.
본문 143바이트·선택형 안내 259바이트가 늘어난 비용도 숨기지 않는다.
