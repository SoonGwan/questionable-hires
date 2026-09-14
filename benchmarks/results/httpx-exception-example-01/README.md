# HTTPX exception example 01: adverse cost, supported core audit

Launch `d14e03b`, Con Artist resources `bec12d6`, HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`. GPT-6 Astra medium, one serial
skill-first pair. [Frozen protocol](../../HTTPX-EXCEPTION-EXAMPLE-01-PROTOCOL.md).
This is an exposed authored task on real upstream code, not an organic ticket or
independent holdout. Both scheduled sessions completed without timeout or limit.

| Arm | Total input + output | Process seconds | Commands |
| --- | ---: | ---: | ---: |
| baseline | 79,312 | 48.563 | 3 |
| skill | 223,391 | 81.563 | 7 |

Skill observed costs are **181.66% more tokens / 67.95% more time**. Input includes
cached tokens once; these totals reconcile to original CLI completion events.
Unequal work and one sample prevent a causal estimate; this is not an efficiency
win. Both arms avoid a stronger probe, so conditional-probe wording is not shown
to be the cause of that choice or any saving.

## Original execution evidence

- [Baseline commands](asgi-exceptions--baseline--1/commands.json), item_4:
  copies production/tests/configuration into two disposable directories, changes
  only the constructor default `raise_app_exceptions=True` to `False`, checks
  imports in the native pytest process, then runs unchanged ASGI tests.
  Correct: 24 pass, exit 0. Mutant: 4 fail / 20 pass, exit 1. Actual failures are
  `DID NOT RAISE RuntimeError` at test_asgi.py:172 and :180 on asyncio and trio.
- [Skill commands](asgi-exceptions--skill--1/commands.json), item_7: the same
  constructor-default mutation and native test outcomes, with copied module
  hashes, same-process collection/client-binding diagnostics and 29-file helper
  integrity/cleanup. No probe is supplied. Correct: 24 pass, exit 0; mutant:
  4 fail / 20 pass, exit 1, same detecting assertions. No truncation or timeout.
- Skill item_6 is retained as **incomplete setup**, CLI 2: the dynamically
  pre-imported `audit_binding_check` plugin triggers `PytestAssertRewriteWarning`,
  escalated by project warning policy. No native tests ran in that attempt and
  no mutant evidence is credited. Item_7 adds a `PYTEST_DONT_REWRITE` module
  docstring for this diagnostic plugin; project warning configuration is unchanged.
  The later success is a separate execution, not a repaired earlier result.
- Skill item_8 exits 1 because the final `rg` finds no matching scratch names;
  status output lists only the installed `.agents/` folder. This is not a failed
  native test. Helper integrity already reports owned scratch removal. Baseline
  deliberately retains its copies/logs. The unchanged task did not require
  deletion, so this difference is not retroactively scored as a violation.

Both final answers' core scoped coverage claims are supported by original native
output. No author rerun was needed to fill missing evidence. The preliminary
author preflight used a different narrow fault (removing propagation), whereas
both model sessions independently changed the default; do not conflate them.

## Integrity, export and limitations

Read-only review compared all 125 tracked originals in each final snapshot with
the clean pinned source: no changed/missing originals. All eight installed and
frozen Con Artist resource files match recorded hashes. This does not establish
absence of transient changes, unselected side effects or permission changes.

All exported commands and outputs reconcile to path-redacted original CLI items;
raw usage matches metadata, and `source-sha256.json` matches retained source files.
Seven selected source/configuration/license files per arm also reconcile; they
are **excerpts, not a runnable full HTTPX distribution**. Original commands,
including failures and full diffs, remain unfiltered. Baseline's large diff includes
its retained copies, not production edits. Windows `/C:/Users/Domenic/…` URL-test
strings in that diff are upstream fixture data, not this machine's private paths.
The upstream license is included with each selected source export.

The skill reads its full helper plus another prefix excerpt and traverses client
dispatch code before constructing a custom pytest collection hook. These are
observed additional work, not a measured causal cost breakdown. Next candidate:
make provenance checks proportional to unresolved binding evidence; don't add a
new hook merely to duplicate an already established copied import and behavioral
failure. Preserve explicit provenance requirements and real binding uncertainty.
Review and test that distinction before another model run; no favorable retries.

한국어: 양쪽 모두 실제 출력에서 정상 24개 통과·결함 4개 실패를 확인했다.
스킬은 토큰 181.66%·시간 67.95%가 늘었고, 전체 소스 읽기와 별도 pytest
진단 플러그인 설정 오류·수정이 추가됐다. 두 조건 모두 추가 검증을 생략했으므로
예제 수정의 효과라고 단정할 수 없다. 원본 보존·사용량·명령 출력·공개 파일을
대조했고, 실패 시도도 그대로 남겼다. 다음 개선은 출처 확인을 필요한 범위로
한정하는 것이며, 필수 검증 삭제나 좋은 숫자가 나올 때까지 재추첨하는 것이 아니다.
