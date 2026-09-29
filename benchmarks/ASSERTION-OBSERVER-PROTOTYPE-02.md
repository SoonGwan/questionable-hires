# Bounded assertion observation prototype02 — 2026-09-27

Follow-up to [prototype01](ASSERTION-OBSERVER-PROTOTYPE-01.md); standalone local
source only, no installed skill/helper changes or model calls.
[Final source, hashes and native controls](results/assertion-observer-prototype-02/)
close the missing shared serialized-report byte-budget gate.

The compact ASCII JSON report includes scope/completeness/reason metadata within
the configured128..65,536-byte budget. Records share the budget, capped at64;
primitive encoding shares a32-node budget and explicit depth/container/value
limits. Unsupported values mark unavailable evidence. Newline or outer runner
framing is not part of that report budget. This bounds observation transport,
not all native test stdout, process memory, runtime or benchmark prompt tokens.

Only actual standard unittest assertEqual/assertIsNot entry calls on the current
thread are observed by exact function code identities. No assertion replacement,
arbitrary object repr or automatic success inference. Empty/unsupported-method-only
runs explicitly report no observations. Existing profile hooks are rejected
without replacement. The owning close operation restores only its own hook;
if another hook replaces it, preserve that hook and mark incomplete. Repeat close
is idempotent. Consumers must close the observation window before final reporting.

Final code passes11 native controls on each existing Python3.9.6/3.11.6 interpreter:
correct three-method suite passes and real regression has one assertion failure
with observer off/on, byte/record limits or encoder errors. Existing-hook control
also passes. Four current-interpreter controls distinguish complete primitive
capture, empty capture, unsupported methods and replacement-hook preservation.
Initial prototype02 checks were rerun after final ownership changes; source
hashes identify the final code, not intermediate experiments. These are26 local
controls, not26 model tasks or independent quality evidence.

No production readiness or token/time reduction claim. Native startup/runner
integration, discovery, installed-resource compatibility and whole-task model
comparison remain required. Coverage beyond selected methods/current thread is
not supplied; unavailable values cannot support a claim that their arguments
were observed. Historical custom-observer errors and adverse document experiments
remain. The owner all8 next-update objective remains unmet.

한국어: 전체 관찰 JSON 보고서에 공유 바이트 한도를 적용하고 한도·관찰 오류가
실제 테스트 결과를 바꾸지 않는지 Python3.9/3.11에서 확인했다. 관찰값 없음·지원
범위 밖·다른 훅의 교체를 불완전한 근거로 표시한다. 최종 코드의 로컬 검사26개가
통과했지만 실제 스킬 실행 통합이나 모델 토큰·시간 절감 검증은 아직 아니다.
