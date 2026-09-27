# Receipt execution evidence01 — 2026-09-28

Parent **`f7ced67d`**. This repairs an ordinary Receipt helper evidence-loss path,
not another wording candidate or a model-cost experiment. The earlier final-guard
repair retained results only when preservation failed; a later copy, runner or
cleanup exception could still discard already returned native observations.
[Source/log identities](results/receipt-execution-evidence-01/identity.json).

## Observable change

After at least one returned check, ordinary ValueError/OSError/RuntimeError or
subprocess.TimeoutExpired during comparison now attaches partial `comparison_result`
to the original API exception. CLI emits JSON with `status:"incomplete"`, retained
checks and `execution_error` type/message, alongside the diagnostic and exit2.
Only returned results are retained; an absent phase may have started without
returning evidence. No later version is run after the error. No retry or restoration.

Existing final-preservation exception precedence remains. If a final guard fails
after an execution/cleanup error, both `execution_error` and `preservation_error`
remain in the partial result. Returned native outcomes never override either failure.
Selected/tree guard false means observed change and null means unverified.

On error paths, `comparison_copies_removed` now uses lstat: true=absent,
false=present, null=lookup unavailable. Previously `lexists` could convert a denied
lookup into false and thus incorrectly report confirmed removal. Normal successful
comparison and its cleanup path are unchanged; no additional successful-path file
read is added. Errors before a returned check and KeyboardInterrupt keep their
existing no-partial-result behavior. This does not recover unreturned observations,
prove arbitrary descendant termination, or provide atomic filesystem protection.

## Reproduction and native validation

[New controls](../tests/test_receipt_execution_evidence.py) reuse the actual owned
Git fixtures, one native failing-before/passing-after assertion and Node24.16.0
native tests. Exceptions are deliberately injected at copy, runner, cleanup or
lookup boundaries around actual executions, not observed production incidents.

The initial [before log](results/receipt-execution-evidence-01/before.txt) has eight
methods: seven evidence-loss assertion failures, one existing first-error/interruption
control passes. After the first correction, [the same eight pass](results/receipt-execution-evidence-01/after.txt).
An added lookup-boundary control then [fails](results/receipt-execution-evidence-01/unknown-removal-before.txt)
because unverified copy absence becomes true. That log contains the actual failed
assertion; its enclosing shell's final tail command masked the unittest exit, so
no separate native exit observation is claimed there. After correcting this boundary,
[all nine pass](results/receipt-execution-evidence-01/after-copy-state.txt).

The controls establish:

- A second Python runner actually executes but raises before returning: keep only
  the first returned failure, not the second native outcome known solely to the
  injected test wrapper. Original exception identity is preserved.
- An after-copy write error retains before evidence and starts no after runner.
- Cleanup failure keeps both native1/0 outcomes and reports the remaining copy.
  A subsequent whole-tree failure retains both diagnostics and its prior exception
  precedence; the author later cleans the intentionally retained owned directory.
- A later multi-version exception retains before/before_2 and no invented after
  check; the third runner attempt's missing result stays unknown.
- In-process CLI `main` with a real first native result emits partial JSON and
  diagnostic while returning2. This is not an external-shell CLI failure test.
- A second Node runner error retains the actual native age-boundary failure.
- An unavailable post-cleanup lookup remains null without replacing the original
  runner exception. Actual author-owned copies are removed after verification.
- First-run exceptions and interruption still propagate without new partial data.

[Git-free compatibility](results/receipt-execution-evidence-01/archive-tests.txt):
**135 methods in11 modules pass**, zero skips,49.967s. The same ten native modules
used for the prior split rejection are retained, plus the new module. Coverage
includes bootstrap/module/unittest/pytest/Node, assertion observation, bindings,
multiple versions, timeout/cleanup, guards, recipes and existing one-file CLI
relocation. Existing failing tests are not removed or relaxed. No model is invoked.

The Python/Node references, CLI help and both README capability rows now describe
returned-result retention and unknown copy removal. Entry/description and skill
selection are unchanged. Featured synchronization, documentation/catalog validation
and whitespace checks are separate from native behavior. No token/time savings are
inferred; original integration07 still measures `1be35120`, not this changed helper.

한국어: Receipt도 복사·실행·정리 예외에서 이미 반환된 네이티브 근거를 잃지 않게
수정했다. 원래 API 예외와 CLI 실패를 유지하며, 반환하지 못한 결과는 추정하지 않고
후속 비교를 중단한다. 제거 여부 조회 실패는 성공 대신null로 남긴다. 최초7개 근거
유실 실패와 추가 상태 오판을 재현했고, 최종 새 검사9개 및 Git 없는 사본의 기존
호환성 포함135개가 통과했다. 실제 모델 절감 실험이나 전체8개 목표 달성은 아니다.

## Installation and prepared download

Source **`0c4d261e`** is installed personally. The previous Receipt directory matched
parent `f7ced67d` in bytes and Git modes before being preserved outside discovery.
[Installation identity](results/receipt-execution-evidence-01/personal-install.json),
[all-eight comparison](results/receipt-execution-evidence-01/all-installed.json) and
[nine controls importing the actual installed helper](results/receipt-execution-evidence-01/installed-tests.txt)
pass; Node uses24.16.0 explicitly. The CLI control calls main in-process.

The151-file landing build changes only the downloadable archive and checksum.
[Download identity](results/receipt-execution-evidence-01/download.json) records
106,932 bytes, SHA-256 `7c6470b3c69fd75f96fcc3b14654c0234d0f1a9039393e604c1f788220739d96`,
and all nine Receipt resources matching source bytes and modes.

A separate standalone-package check exposed an outdated Con Artist expectation:
[the first run](results/receipt-execution-evidence-01/standalone-package-before.txt)
expected empty stdout on a final guard failure, predating the adopted retained-evidence
interface. The test now requires incomplete JSON, all four native exit codes,
selected-source preservation, failed project guard and removed scratch, while
retaining exit2, stderr, original changed notes and filesystem assertions. This
is a test-contract correction, not a newly repaired production defect. The
[final package run](results/receipt-execution-evidence-01/standalone-package.txt)
checks offline installation, source/mode identity and actual extracted helpers.
Historical model evidence is unchanged; these are local delivery checks.

한국어: 소스`0c4d261e`을 개인 설치와 다운로드에 반영했다. 설치본9개 검사와
전체8개 파일·권한 일치를 확인했다. 독립 패키지 검사에서 발견한 과거의 빈 출력
기대값은 현재 실패 근거 보존 계약으로 수정했으며, 첫 실패 기록도 남겼다.

## Public delivery

Hosted release **`1f81be81393b4485d3d98eb10c83fc8d14045f7b`** is live at
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
[Seven public HTTPS observations](results/receipt-execution-evidence-01/public.json)
verify health revision, both locale pages and canonical URLs, absence of noindex,
robots, download/checksum identity and the unchanged integration07 evidence ZIP.
All nine Receipt resources inside the fetched archive match current source bytes
and modes. The page still identifies integration07's measured resource `1be35120`;
this newer download is not relabeled as that experiment. No layout change or fresh
browser interaction matrix is claimed. Four final standalone-package tests pass.

한국어: 공개 배포`1f81be81`의 한영 페이지·주소·다운로드 해시와 Receipt9개
파일·권한 일치를 확인했다. 기존 실험의 측정 자원과 수치는 유지한다. 전체8개
품질·토큰·시간 동시 개선 목표는 여전히 미달이며 이번 배포는 오류 근거 보존 수정이다.
