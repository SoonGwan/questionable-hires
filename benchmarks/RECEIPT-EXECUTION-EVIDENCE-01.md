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
