# Receipt Node startup-transfer preflight

2026-09-21, parent `107a0cf`. This is fixture validation, not a model benchmark
or evidence that the shorter Node guide saves tokens. No model calls have been
made for this pair. A frozen resource/input manifest and execution protocol are
still required before scheduling any sessions.

`receipt_node_startup_cases.py` defines two related authored synthetic cases,
not real issues or independent holdouts. Both compare actual Git HEAD^/HEAD using
the same current four native tests: explicit zero disables retries, a positive
integer survives, omitted and null use three. The only fix is `||` to `??`.
Unspecified inputs are not scored. Native tests print their bound implementation
origin/PID; this diagnostic field is not tamper-proof attestation.

The plain case supports the existing comparison helper. The second requires
`NODE_OPTIONS='--import ./bootstrap.mjs'` in both copied roots. That startup is
outside helper support and must remain intact in a native workflow. Removing it
causes an import-time TypeError in both revisions, before the diagnostic identity;
that is setup failure, not a defect reproduction or performance improvement.
Helper adoption is not an outcome criterion.

Native preflight on Node v24.16.0 observes three passes/one assertion failure
(`actual: 3`, `expected: 0`) before and four passes after in both cases. Two
additional missing-preload controls fail at setup. The plain helper agrees with
native exits; required custom startup is rejected instead of silently removed.
Full normalized native output remains in the returned control records; only copy
paths, process IDs and timing values are normalized. Original tree/Git inventories
match after all checks, and owned temporary copies are removed.

The five model-visible obligations cover native startup/equal tests, the actual
before assertion, after controls/mechanism, full revisions/native copy identity,
and original bytes/modes/Git/resources plus scratch cleanup. Any future comparison
must retain failures and incomplete work, inspect original evidence, and compare
the candidate with both prior skill and no skill. The prior adverse token result
is unchanged; no graph or featured pointer changes follow from fixture validation.

한국어: 일반 실행과 필수 시작 설정이 있는 실행을 실제 Node로 대조했다. 설정을
빼서 생긴 오류를 결함 재현으로 오인하지 않도록 검증한다. 모델 실험이나 토큰
절감 결과는 아직 아니며, 기존 수치와 그래프를 바꾸지 않는다.
