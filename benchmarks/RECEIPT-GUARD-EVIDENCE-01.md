# Receipt preservation failure evidence01 — 2026-09-28

Parent **`1b6ae5f5`**. The [bridge error controls](TOOL-BRIDGE-CANCEL-ERRORS-02.md)
exposed an adjacent ordinary-helper limitation: a final original/tree guard error
throws away completed native comparison observations from the CLI output.
This change retains those observations while preserving failure. It is not a
model-cost experiment or a retry of the rejected direct-tool routing candidate.

## Observable contract

When at least one `run_check`/`run_node_check` result has been collected and final
preservation fails, keep its exact native result, output, loaded-source evidence,
revision identities and original hashes. CLI emits JSON with `status:"incomplete"`,
`preservation_error`, actual copy-path absence and the relevant guard state. It
still exits2 and prints the original error diagnostic. Selected/tree `unchanged`
is false only for a detected change, null for unavailable/unreached checks.
Unexecuted phases have no check. No automatic restoration or retry is introduced.

The direct API raises the original exception type/message and carries partial
observations in `comparison_result`. A completed native before1/after0 pair does
not override failed preservation. Errors before any collected check retain their
existing diagnostic behavior. This does not recover an interrupted runner's
unreturned result or prove that arbitrary child processes are gone.

## Failing before, passing after

[Six new native regression controls](../tests/test_receipt_guard_evidence.py) use
an author-owned temporary Git fixture and deliberate owned-source side effects.
The existing one-test fixture actually fails on `eligible(18)` before and passes
after. Both bootstrap and native module invocation are exercised. No user project
is mutated and no model is called.

- Selected-file mutation: before/after observations survive, original remains
  intentionally changed, CLI2 and false preservation.
- Unselected tree mutation: native module observations survive; selected originals
  true, whole-tree false, changed path retained.
- Timeout plus selected mutation: only the before timeout−9 remains; no invented
  after run or completed-suite credit.
- Direct API: still raises RuntimeError and retains native evidence.
- Unreadable final inventory: still raises OSError, selected checks true but tree
  unchanged is null; unavailable inventory never becomes preservation success.
- Controlled cleanup failure plus mutation: completed observations survive but
  copy removal is false; author cleanup subsequently removes its retained copy.

[Before](results/receipt-guard-evidence-01/before.txt):6 actual assertion failures
because partial evidence is absent, not import/setup errors.
[Initial after](results/receipt-guard-evidence-01/after.txt):6 pass.
Initial compatibility checks then expose one ValueError→RuntimeError change in
[helper checks](results/receipt-guard-evidence-01/helper.txt) and an old empty-stdout
expectation in [tree checks](results/receipt-guard-evidence-01/tree-guard.txt).
The [initial candidate patch](results/receipt-guard-evidence-01/initial-candidate.patch)
is retained. The final implementation attaches evidence to the original exception
instead of replacing its type. The tree regression now requires incomplete JSON,
failed guard and confirmed cleanup while retaining CLI2/diagnostic/source-change
assertions. Original failure logs are not overwritten.

[Final new controls](results/receipt-guard-evidence-01/after-compatible.txt):6 pass;
[existing helper](results/receipt-guard-evidence-01/helper-compatible.txt):50 pass;
[tree guard](results/receipt-guard-evidence-01/tree-guard-compatible.txt):9 pass;
[recipe errors](results/receipt-guard-evidence-01/recipe-errors.txt):7 pass.
The new test assertions were retained across the first code fix; unused imports
were removed, and API assertions subsequently use the compatibility-preserving
`comparison_result` field. No model evidence is attributed to these author tests.

Both README languages and Python/Node helper references describe this changed
failure output. Featured evidence/graphs remain frozen. Personal installation
and hosted download are separate delivery checks; they are not established by
these checkout tests. Whole-task token/time improvement remains unproven.

한국어: 최종 원본 보존 검사가 실패하면 완료한 실행 근거까지 사라지던 문제를
수정했다. CLI는 불완전 JSON과 종료값2를 유지하고, API는 원래 예외 종류·메시지를
유지한 채 부분 근거를 제공한다. 수정 전6개 실패를 재현했고 수정 후 통과했다.
초기 호환성 실패도 보존했으며 예외 종류 변경을 바로잡았다. 원본 자동 복구나
토큰 절감을 의미하지 않고, 전체8개 품질·토큰·시간 목표는 여전히 미달이다.

## Archive and runtime checks

The Git-free copied skill/test archive passes [72 methods](results/receipt-guard-evidence-01/archive.txt)
without repository history or local experiment artifacts. This repeats the72
focused methods above in a separate packaging context, not72 new obligations.
The existing Node24.16.0 comparison suite separately passes
[9 methods](results/receipt-guard-evidence-01/node.txt), no skips.
[Source and evidence identity](results/receipt-guard-evidence-01/identity.json)
pins both the old helper and changed sources. Metadata/link validation, Receipt
skill validation, featured synchronization check and whitespace checks pass.

## Personal installation and prepared download

Source **`11c9b0a7`**. Before replacement, every installed Receipt resource byte/mode
matches parent`1b6ae5f5`; the complete old directory is preserved outside discovery.
[Installation identity](results/receipt-guard-evidence-01/personal-install.json),
[all-eight resource comparison](results/receipt-guard-evidence-01/all-installed.json)
and [six actual installed-helper controls](results/receipt-guard-evidence-01/installed-tests.txt)
pass. These controls import and execute the installed helper, not the checkout copy.
The other seven installations are unchanged.

The landing download is rebuilt from the new source;
[byte/hash identity](results/receipt-guard-evidence-01/download.json) and
[three packaging checks](results/receipt-guard-evidence-01/package.txt) are retained.
All63 generated files pass builder consistency. Only download bytes/checksum change;
no featured benchmark, artwork, page layout or numerical claim changes. These are
local installation/package checks; public delivery remains a separate check.
