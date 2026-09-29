# Con Artist execution exception evidence01 — 2026-09-28

Parent **`be5a8780`**. The earlier [guard repair](AUDIT-GUARD-EVIDENCE-01.md)
retains results when final integrity checks fail. Further inspection found an
adjacent loss: a copy/runner/context-cleanup exception can leave those final
guards successful while previously returned checks disappear. A retained scratch
can also make the project guard supersede the original cleanup exception without
recording that earlier error. This is a native correctness repair, not a claim
that the [mixed interface costs](AUDIT-GUARD-OUTPUT-01-REVIEW.md) improved.

## Observable contract

After at least one returned check, ordinary copy/runner/cleanup exceptions retain
those checks in incomplete `audit_result`, with `execution_error` type/message.
Direct API exceptions keep their original types/messages. CLI keeps its existing
error diagnostic and exit2, adding incomplete JSON. Final guard failures can
still supersede the execution exception as before; that result retains both
`execution_error` and `integrity_error`. No new native execution is performed.

Removal is checked: a retained owned directory is false, unavailable checks are
null. With an already pending execution error, unconfirmed removal is reported
without replacing that error with a newly introduced exception type. Existing
project/selected guard failures still raise. No original restoration or automatic
cleanup retry is added. Evidence cannot establish successful audit/preservation
when any required operation failed.

A check which started but did not return a result remains unavailable. Its absence
does not mean it never executed. Batch composition retains earlier audits and
references to already executed baselines, stops later mutations and preserves
the existing later-input/I/O incomplete-return versus RuntimeError/first-error
raise behavior. No-observation failures retain the existing stderr-only behavior;
interruptions are not caught as ordinary execution errors.

## Failing-before controls and compatibility

[Seven tests](../tests/test_audit_execution_evidence.py) use real native checks in
author-owned temporary fixtures plus explicit exception injection at operation
boundaries. [Before](results/audit-execution-evidence-01/before.txt): six assertion
failures for missing evidence; the existing no-observation/interruption behavior
passes. [After](results/audit-execution-evidence-01/after.txt): all seven pass.

- Runner completes its second real native process, then the wrapper raises before
  returning that result. Only the first returned check is retained. There is no
  invented second observation or later phase.
- Mutant-copy write raises after two actual passing baseline checks. Both returned
  checks survive; originals and removal verify unchanged/removed.
- Controlled context cleanup raises PermissionError and leaves its copy after
  all four real checks. The original exception survives and removal is false;
  the actual stronger assertion failure `AssertionError: 2` is retained. Author
  test cleanup subsequently removes the directory, not the audit helper.
- The same retained copy with project guard enabled triggers the existing final
  RuntimeError. Both cleanup and guard errors survive with four native results.
- A later batch runner error retains the first four checks and the second audit's
  two baseline references. These references are not extra native executions; the
  third mutation remains unrun.
- The real CLI `main` path, with controlled runner injection and real first native
  execution, emits incomplete JSON and exit2. This is an in-process CLI test, not
  an independently launched model command.
- First-runner failure has no partial observations; KeyboardInterrupt after a
  returned check still propagates without ordinary-error conversion. Owned copies
  are removed in both controls.

[Git-free source archive](results/audit-execution-evidence-01/archive.txt) passes
all188 methods across22 affected helper/guard/cache/recipe/native-invocation/pytest
modules, no skips. These native controls do not test arbitrary OS cleanup failures
or every descendant-process condition. [Source identity](results/audit-execution-evidence-01/identity.json)
pins the parent and changed helper, guide and regression tests. English/Korean
capability descriptions are synchronized. Frozen featured numbers are unchanged.

No model was called for this change, and no token/time improvement is claimed.
Additional error evidence may itself cost tokens. Earlier measured versions and
their adverse/mixed results remain tied to their original resources. Broader
all-eight improvement is not established by these native checks.

한국어: 복사·실행·정리 예외가 기존 검사 근거를 버리는 추가 경로6개를 재현하고
수정했다. 실제 반환된 결과만 남기며, 반환되지 않은 검사는 실행 여부를 추정하지
않는다. 원래 예외·CLI 실패·잔존 폴더·기존 최종 보호 실패를 유지한다. 새 검사7개와
Git 이력 없는 관련 검사188개가 통과했다. 모델 절감은 미측정이며 이전 정상 배치
토큰 증가를 새 수정의 성과로 덮거나 전체8개 목표 달성으로 주장하지 않는다.

## Installation and prepared download

Source **`db46dcdc`** is personally installed. Every previous Con Artist resource
matched parent`be5a8780` bytes and Git file modes; the complete old folder is
preserved outside discovery. [Installation identity](results/audit-execution-evidence-01/personal-install.json),
[all-eight resource comparison](results/audit-execution-evidence-01/all-installed.json)
and [seven controls using the installed helper](results/audit-execution-evidence-01/installed-tests.txt)
pass. Tests import the installed source; the CLI control invokes its real main
function in-process with injected runner failure, not a separate shell process.

The63-file landing build passes consistency; only archive/checksum bytes change.
[Download identity](results/audit-execution-evidence-01/download.json) records
106,466 bytes, SHA-256`19be55fca19c1f6e6be294c0631aef3c05b0e5f6ae18720489d10d508967567e`, and exact packaged helper bytes.
[Three packaging controls](results/audit-execution-evidence-01/package.txt) pass.
These local checks do not yet establish public delivery or model efficiency.

## Public delivery

Hosted release **`486453a690fc0cb63d369dcdbe3c176c508afe18`** is live at
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
[Public HTTPS observations](results/audit-execution-evidence-01/public.json) confirm
health revision, exact106,466-byte download, checksum and packaged helper source,
plus both canonical URLs, index/follow directives and download links. Mac origin
and Cloudflare delivery are verified separately from native behavior. No layout,
featured benchmark or numerical efficiency claim changed.

한국어: 소스`db46dcdc`을 개인 설치와 공개 다운로드에 반영했다. 배포`486453a6`의
공개 파일·해시·소스 일치와 한영 메타데이터를 확인했으며 모델 절감은 주장하지 않는다.
