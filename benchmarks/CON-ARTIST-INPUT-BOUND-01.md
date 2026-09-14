# Con Artist bounded input reads — 2026-09-15 KST

Parent `f19186c`. Inspection of existing audit orchestration found that shared
baseline/probe reuse was already implemented; this change does not duplicate it
or claim a new execution-speed win. It fixes a concrete resource-limit defect.

Before the change, `snapshot()` charged `stat().st_size`, then called unbounded
`read_bytes()`. A file growing between those operations could exceed the documented
20 MB collected-input limit, either alone or across a selection. Original-file
integrity comparison also read the entire later file before detecting a change.

The new collection read requests only remaining bytes plus one overflow byte,
rejects overflow before copying/execution, and charges the bytes actually read.
Final comparison rejects changed size/mode before reading; if growth occurs after
that stat, it reads only the original length plus one byte. It still reports
original changes instead of restoring them. Ordinary exact-limit and overlapping
file/directory selections retain their content and existing budget semantics.

## Actual regression evidence

`tests/test_audit_input_budget.py` writes real files in owned project-local scratch
and grows them immediately before the read via an intercepted `Path.open`.
This is deterministic interleaving, not a claim that a production race occurred.
The pre-fix run had 3 tests, 2 failures (`ValueError not raised`): a single file
growing to 20,000,001 bytes and two files whose actual sum grew above 20 MB.

After the fix, all 4 input tests pass in 0.026s. They confirm:

- A growing oversized input is rejected; recorded read request is 20,000,001 bytes.
- Actual collected size, not stale stat size, determines the shared budget.
- Exactly 20,000,000 bytes and overlapping selections still preserve content.
- Final comparison of an originally one-byte file requests just two bytes when
  it grows to 20,000,001 bytes after stat. Already-known size mismatch opens no
  stream. The changed file remains changed; the test removes only its owned scratch.

Final helper suite: **76 tests pass in 13.519s**, including real mutation outcomes,
baseline identity, import provenance, native probe behavior, timeout and cleanup.
**12 build/installed-bundle tests pass in 3.301s**. Skill validation passes.
An earlier 76-test run (13.443s) covered collection-only changes; the final run
above also covers the updated original comparison. Durations are not speed claims.

This bounds selected-file payload reads, not total process memory, total wall time,
concurrent path replacement, source snapshot isolation or hostile test execution.
No new model session, skill-entry paragraph or benchmark chart change. Broader
developer usefulness and lower model cost remain separate, unmet goals.

## 한국어

기존 도우미에는 기준 실행 재사용이 이미 있어 중복 기능을 추가하지 않았다.
대신 파일 크기를 확인한 뒤 무제한으로 읽어 20MB 제한을 우회할 수 있는 결함을
고쳤다. 실제 파일 증가를 재현한 테스트가 수정 전 2개 실패했고 수정 후 통과했다.

종료 시 원본 확인도 읽기 상한을 적용했다. 1바이트 파일이 확인 직후 20MB 넘게
커진 재현에서는 2바이트만 읽고 변경을 감지했다. 파일을 원래대로 덮어쓰지는 않는다.
새 검사 4개·기존 도우미 76개·빌드 12개가 통과했다. 메모리 전체나 파일 경합을
완전히 격리하는 기능은 아니며, 모델 성능 향상 수치로 표현하지 않는다.
