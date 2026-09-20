# Receipt Node comparison 01 — frozen before model execution

2026-09-21. Two authored related tasks × no-skill/original/current × one fresh
session: six serial GPT-6 Astra medium sessions, 360 seconds each. Prior Receipt
resources `310d483`, Node-enabled resources `8fa20dd`, copied byte/mode-exact from
Git. The case factory and runner are committed before execution; preparation saves
full case contents, criteria, native controls, resource digests and input hashes.
No production edits or new performance claims are part of this pilot.

## Tasks, order and controls

`receipt_node_cases.py` supplies an incremental two-byte-length binary decoder.
The ESM case verifies HEAD^ versus HEAD; the CommonJS case verifies HEAD versus an
unstaged working-tree fix. Current test bytes are the same in both versions of each
comparison. Four native tests cover a split header, split binary payload, coalesced
frames, and zero-length payload/empty input. Earlier code consumes a header before
its payload is complete: only split payload fails, showing `[]` versus `['00ff0d0a']`.
Fixed code retains the header until the whole frame exists; all four pass.

Order: ESM baseline → original → current; CommonJS current → original → baseline.
Native Node/TAP, copy-local actual test-bound module origin/PID, source identities,
original bytes/modes and Git HEAD/index preservation, no code/test edits, and
project-local scratch cleanup are explicit model-visible obligations. The tests
already print diagnostic module identity; no condition must invent or adopt the
new observer to pass. The source identity field is not adversarial attestation.

Independent author preflight uses ordinary Node commands, not the comparison
helper, in disposable local copies. Both cases establish before native exit 1 with
three passes/one actual assertion failure and after exit 0 with four passes.
The helper is then checked against those native observations, including preservation
and cleanup. No dependencies, services, code fixes or favorable model attempts are
used to repair the fixture. These are authored synthetic transfer tasks, not real
issues or independent generalization evidence; no percentage target is promised.

## Execute and retain

`python3 -B benchmarks/run_receipt_node_01.py` prepares once. Review its retained
manifest and clean committed inputs before `--execute`. The execution guard is
exclusive; an existing marker is not permission to restart. Observe a live handle;
preserve stopped, failed and unattempted cells. Do not retry model failures or
change cases/resources/criteria mid-run. Account-limit signals stop remaining cells.
Resource/input digests are checked before launching. The existing runner retains
original sessions for later private capture/exposure review.

## Review before claims

Review all five criteria against original commands, outputs and artifacts, not a
completion flag: unchanged native test identities/bytes, defect-specific assertion,
neighboring controls, after results, copy-local loaded source, source revisions or
working-tree hash, originals/modes/HEAD/index/resources, and scratch cleanup.
Unchanged-byte inspections by the author are separate from original model actions.
An import/setup failure is not the regression; skipped or incomplete checks cannot
earn efficiency credit. A helper load record alone is not dispatch or coverage.

Reconcile original session/tool capture, input including cache once plus output,
wall time, response count and resource exposure. Never export private initial
messages. Note whether either skill was actually exposed and whether the helper
was adopted, but adoption is not a success criterion. Include extra inspection,
setup costs, incomplete work and adverse results. Compare current to both prior
skill and baseline; a single favorable pair is not stable or broad improvement.
Freeze charts and featured pointer until an independently justified publication
decision; do not relabel old experiments with these new resources.

한국어: 합성 Node 과제 두 개를 무스킬·이전·현재 스킬로 총 6회 비교한다. 실제
정상·결함 실행과 원본 보존을 먼저 검증했으며, 필요한 테스트나 출처를 생략한
실행은 비용이 작아도 개선으로 인정하지 않는다. 모든 결과를 보존하고 단일 유리한
결과를 전체 성능 향상으로 주장하지 않는다.
