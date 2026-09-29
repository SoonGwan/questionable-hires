# Integration07 original review — 2026-09-28

Resource **`1be35120`**, execution **`47a00692`**. [Frozen protocol](ALL-EIGHT-CURRENT-07-PROTOCOL.md), [costs and limitations](ALL-EIGHT-CURRENT-07-COSTS.md), [original comparison](results/all-eight-current-07/comparison.json).

**The all-eight improvement requirement is not met:** summed tokens +1.67%, elapsed −9.63%, only 2/8 pairs lower both. The reviewed bounded task outcomes are preserved in both conditions; this is not evidence of superior quality. No skill edit, promotion to featured, model retry or native replay is part of this review.

## Original evidence and preservation

All 16 scheduled Astra/medium sessions completed. Actual context metadata, reconciled per-response usage, original selected tool records with source-line hashes, commands, answers and final synthetic projects are retained. These are reused authored development cases, not independent validation. Initial context equality and causal attribution are not assumed. All eight current entries have exact full-body tool-output observations, with no exact initial-body match; a missing match is not proof of absence.

[Capture review](results/all-eight-current-07/capture-review.json) associates all 78 command records with paired original output by redacted command text and output order, including nested `Promise.allSettled` envelopes. Exits agree. Seventy-six outputs equal the CLI text after redaction. Both Con Artist CLI outputs omit a leading portion: baseline item_5 lacks the correct-code suites; current item_6 lacks the first existing/correct suite. The complete text is recovered from each exact original paired response in `recovered-item_5.txt` and `recovered-item_6.txt`, with line hashes and call IDs recorded. No replay supplies missing observations. No truncation marker appears in these 78 original command-output envelopes. Absence of a marker alone is not a universal completeness guarantee. Original automated suffix-matcher statuses remain untouched; they do not independently prove command identity. This manual association is not an assertion of unredacted byte equality.

[Artifact review](results/all-eight-current-07/artifact-review.json) compares original file inventories with final local workspaces: all 16 retain installed-resource bytes/modes, the pre-collection index and HEAD. Only the expected Mother `test_editor.py` changes and Hostage `preview.py`/new `test_preview.py` changes occur. Other project files, including ignored notes and requirements, remain identical. No owned scratch artifact remains in the file inventories. This is before/after evidence, not proof against transient changes or directory-metadata changes. Mother’s original test method is AST-identical and each arm adds two methods. Hostage’s production diff is exactly the generation guard below. Reviewed command scope stays in the synthetic project and its installed matching skill; no external services, delegation or model-created commits are observed.

## Per-role observations

### Necromancer — `history-invoice-boundary`

Both trace the introducing history: integer minor-unit importer branch `ee9689a2`, HALF_UP quantization `1d38dfc0`, importer retirement/current string boundary `9b050b62`. The live invoice path converts strings to Decimal before `amount_cents`. Both accept removal of the unreachable integer branch (A) and reject replacing rounding with truncation (B).

Original probes for 1.005/−1.005/2.34 return 101/−101/234 for current and A, versus 100/−100/234 for B. Baseline runs three native tests per variant (current/A pass, B two failures); current directly probes all variants and runs the three current native tests. Baseline’s unavailable `python` command exits 127 and is recovered with `python3`; its cost is retained. Unequal extra verification limits the −17.19% token/−14.31% elapsed comparison.

### Receipt — `ledger-delivery-b`

Both reject the return-only fix between `72113958` and `56285458`: repeated credit/debit still doubles durable state. Before results are `(True,250)`/`(True,-100)`; after `(False,250)`/`(False,-100)` instead of `(False,125)`/`(False,-50)`. Each revision runs the same five tests/schema: two failures, three passes, zero skips. Independent-account, distinct-event and zero-delta controls pass. Passing assertion arguments themselves are not captured.

Baseline authors copy/cleanup code and checks bindings in a separate import-only process before each actual suite; that is not same-process provenance. Current invokes the installed Receipt CLI once, uses module invocation and actual copy-local test-process import verification, with five tests per revision and native exits 1/1. It does **not** request optional v3 argument observation. The helper correctly reports observed execution even though the application fix fails. [Original native JSON](results/all-eight-current-07/current/ledger-delivery-b--skill--1/original-native-result.json) retains preservation and cleanup results. Token +8.55%/elapsed −55.88% does not establish a joint win or measure adoption of the recently changed optional capability.

### Landlord — `store-check-scope`

Both keep Store because it translates meaningful behavior, despite one consumer. Two native contract tests pass. Direct Backend witnesses show creation yields `{'created': None}` instead of literal True and duplicates raise `Duplicate` instead of False; existing value is preserved and operational `OSError` propagates. Neither fabricates the unavailable externally produced staging receipt. Both use native tests plus direct witnesses and leave implementation unchanged. Tokens +0.80%, elapsed −3.74%; staging remains unverified.

### Mother-in-law — `editor-snapshot-present`

Both preserve production/support and the original initial-state test, adding two tests with independent nested expected dictionaries and supplied acknowledgment support. Each native run executes three methods: two pass; the pending-save payload assertion fails with `solarized` where `dark` is required. The existing shallow copy exposes subsequent nested mutation.

Owned save tasks and callback-entry signals are bounded; support records a deep copy after acknowledgment, so the assertion observes the actual later payload. Completion checks after the failing payload assertion exist but are **not executed** on this defective source. No author replay is counted as model evidence, and no external persistence/browser behavior is claimed. Current adds one model response, with tokens +33.42%/elapsed +17.16%; it does not deliver a better reviewed outcome.

### Exorcist — `runner-environment-timing`

Both distinguish import-time configuration from intermittency: unset at import gives RETRIES=2 and three callbacks even after test setup changes the environment to zero; fresh startup with zero gives RETRIES=0 and one callback. No cache hypothesis or production change is needed.

Baseline runs an initial failing native test, a direct startup-zero probe, then four instrumented actual native tests (unset/zero twice each): five native one-test suites total, three failures/two passes. Current runs two native suites (one pass/one fail) plus two direct probes, one invoking actual setup/cleanup without a native suite. Baseline’s extra repeats are fully charged. Both restore the observed environment, but the −17.73% tokens/−9.97% elapsed is not equal-work speed evidence.

### Hostage Negotiator — `refresh-owner-a`

Both make only this production change:

```python
finally:
    if generation == self.generation:
        self.pending = False
```

Their retained tests exercise actual Preview with controlled callbacks: overlap and completion orders, stale success/failure/cancellation, latest failure/cancellation and retry, synchronous failure, duplicate keys, prior value and instance isolation. Error/result identity and pending ownership are asserted. Owned tasks use bounded cooperative cleanup and waits without sleeps. No async override of a synchronous unittest runner method appears.

Baseline runs five passing native methods with subtests; current seven with subtests. Neither records a before-fix native failure; the task does not explicitly require one, but these are after-only suites, not failing-before/passing-after evidence. More methods do not imply stronger coverage. Hostile coroutine/global deadline behavior is unverified. Tokens +5.26%, elapsed −7.16%.

### Con Artist — `sqlite-commit-audit`

Both use custom isolated-copy harnesses; current neither invokes `audit.py` nor reads its guide. The recently repaired helper error paths are not exercised. The sole fault removes `connection.commit()` while retaining acknowledgment and close. Both prove existing acknowledgment tests pass despite lost persistence and strengthen the binary-upload case with full ordered rows from a fresh SQLite connection: correct `[(10,b'previous'),(20,b'\x00\xffnew')]`, faulty only `[(10,b'previous')]`.

Baseline launches two Python test processes (correct/faulty), each with existing two-test and stronger one-test suites: four logical suites, six method executions total. Same-process bindings and runtime profiling verify writer/commit/close on correct code, writer/close on faulty code. Correct existing/stronger pass; faulty existing passes/stronger raises the intended AssertionError; process exits 0/1.

Current launches four native unittest processes with two methods each: existing correct/faulty, stronger correct/faulty, exits 0/0/0/1. Same-process binding/path assertions establish copy-local dispatch; source inspection checks commit presence, not a runtime commit trace. Only binary-upload persistence is strengthened; the empty-upload test is unchanged. Faulty stronger has one intended failure/one pass. Neither demonstrates a stronger empty-payload persistence assertion. Original recovered prefixes establish the omitted passing controls. Originals and modes are preserved and copies removed. Tokens +5.15%, elapsed −2.66%; process grouping and extra method work differ.

### Friday — `view-contract`

Both execute the supplied scripts verbatim in one in-memory SQLite sequence and both literal queries at all five checkpoints, verifying exact ordered labels, complete rows and BLOB types/bytes. OLD is compatible at 1/5, actively incompatible at 2/3/4 despite successful SELECT; NEW is compatible at 2/3/4 and has inactive errors at 1/5. The first blocker is step 2’s label→title change. Full written rows survive down migration, including updated and inserted BLOBs. Restarting OLD alone at step 4 cannot restore its view contract.

Both recommend coordinated draining/cutover, or separate interfaces if coexistence is required; adding aliases breaks OLD’s exact `SELECT *` shape. Both inspect base rows at every phase. This covers SQL-only role simulation, not actual application restarts, concurrency, crash recovery or staging deployment. Tokens +3.04%, elapsed +12.78% with the same decisive bounded outcome.

## Decision

Retain all adverse and unequal-work observations. Do not promote this exposed n=1 screen to featured or infer an optimization from the difference against integration06. The normal installed bundle remains unchanged. Local correctness, model costs, independent validation and hosted delivery are separate; this review establishes no new deployment. The limited native preflight and four Git-free synthetic runner checks were completed before freeze, not counted as model evidence.

한국어: 원본 16회 검토에서 한정된 과제 결과와 보존 조건은 양쪽 모두 유지됐지만 품질 우위는 입증되지 않았다. 전체 토큰은 1.67% 늘고 시간은 9.63% 줄며 동시 감소는 2/8이다. Con Artist 출력 앞부분 두 건은 재실행 없이 같은 원본 응답에서 복구했다. Receipt의 선택적 v3 관찰과 Con Artist의 수정된 도우미는 이 비교에서 사용되지 않았다. 반복 노출·검사 횟수 차이·조건별 1회 한계를 남기며 전체 완료나 대표 성과로 승격하지 않는다.
