# Receipt: reuse hashes of captured original bytes

2026-09-22, parent `20380c9`. Small helper optimization, not a model benchmark
or evidence that the broad performance target is met.

Receipt computed SHA256 of the same frozen original bytes separately for
`fixed_sha256` / working-tree-after identity and the final `originals` report.
Compute those digests once per selected path and reuse them in the result.
No filesystem observations, historical reads, native tests or output fields are
removed. Mutable input checks still reopen and compare the original bytes and
modes after execution; no cross-call cache is introduced. The tree guard and
its separate inventories are unchanged.

In the existing two-file native fixture with working-tree after, selected-byte
digest calls fall from4 to2. For committed after, only fixed-file duplication is
removed; varying originals already needed one report digest. Watch-only inputs
also still need one. This arithmetic is **not** 50% fewer total helper operations,
50% faster execution, token savings or a whole-task performance claim. Git,
copying, subprocesses, import verification and tests retain their costs.

The new behavior test first fails on the previous implementation (`2 != 1`).
An initial test revision incorrectly compared a macOS `/var` temporary path to
its resolved `/private/var` alias; corrected the test to compare resolved paths,
without changing production path handling. It checks each selected input is
still read twice, all public identity mappings agree, before fails/after passes
in real native execution, and owned copies are removed.

Validation:50 Receipt helper tests and8 tree-guard tests pass on system Python;
the new behavior test also passes in a source archive without repository history.
The skill-creator schema validator passes. No instruction, description, selection
policy or optional-resource route changes. Existing mixed/adverse model results
and featured graphs remain applicable; this optimization has no model measurement.

한국어: 이미 읽어 둔 원본 바이트의 해시를 결과 항목마다 다시 계산하던 중복을
제거했다. 두 파일의 작업 트리 비교에서는 해당 해시 계산4회가2회로 줄지만,
전체 실행시간·토큰50% 개선이라는 뜻은 아니다. 실제 파일 재확인과 수정 전후
테스트는 그대로이며, 모델 성능 효과는 아직 측정하지 않았다.
