# pytest5103 warning-policy diagnosis01–02 — 2026-09-28

**A controlled warning-policy change reproduces the missing assertion messages.**
The same authored generator/list examples show expanded messages under default
warnings and plain AssertionError under `error::SyntaxWarning`. A scalar false
assertion retains its expanded message. This explains a concrete compatibility
boundary in the prepared runtime; it does not repair or accept the original
[failed official pair](EXTERNAL-BUNDLE-02-PYTEST5103-CONTAINER-01.md).

[First protocol](EXTERNAL-BUNDLE-02-PYTEST5103-REWRITE-01-PROTOCOL.md) `5c9a7070`,
storage recovery `10acee70`, [second protocol](EXTERNAL-BUNDLE-02-PYTEST5103-REWRITE-02-PROTOCOL.md)
and first results `9dde927b`. Twelve original diagnostic cells, two fresh containers,
zero issue-test replays, zero models. No altered original warning policy, test,
required label, source patch or scoring rule. No token/time performance claim.

| Authored expression | Direct/default | Native/default | Direct/warning-error | Native/warning-error |
| --- | --- | --- | --- | --- |
| Scalar false |expanded|expanded|expanded|expanded|
| all(generator) false |expanded|expanded + SyntaxWarning|expanded|plain AssertionError|
| all(list comprehension) false |expanded|expanded + SyntaxWarning|expanded|plain AssertionError|

All six native processes actually fail their single assertion with exit1. The
direct probes catch and record the actual AssertionError and exit0; their process0
does not mean the authored assertion passed. Every expanded result includes the
actual false predicate value. Both warning settings use identical three fixture
byte strings, the same pinned image/gold source/wheels and the same isolation.
[Comparison](results/external-bundle-02-pytest5103-rewrite02/comparison.json) and
[original default](results/external-bundle-02-pytest5103-rewrite01/authored-results/observations.json)/
[warning-error observations](results/external-bundle-02-pytest5103-rewrite02/authored-results/observations.json)
retain each cell and native output hashes.

## What the evidence distinguishes

The first six cells disprove a general inability to transform/load these expressions
in the prepared Linux interpreter. Actual native configuration remains `rewrite`
and an AssertionRewritingHook is present. The two complex expressions emit a
SyntaxWarning about an identity comparison with a literal. The project's original
tox.ini has `filterwarnings = error`; the second control isolates just the observed
SyntaxWarning category without loading or weakening that original configuration.
Only the corresponding native messages change. This is a causal observation for
these authored controls, not an independent model validation or replay of the issue.

Static source tracing explains why direct and native paths differ. In the selected
source, `AssertionRewriter.visit_Assert` adds its None-warning guard only when a
module path is supplied. Native file loading supplies that path; the direct helper
probe does not. With the special transformed expression this guard compares a
numeric sentinel by identity, generating the observed compiler warning. Native
`_rewrite_test` catches SyntaxError from compilation and returns no rewritten code;
the import hook then permits ordinary loading. Source functions were inspected,
not instrumented or changed during these runs. No claim is made that native
fallback's exception object was directly captured.

One prospective prediction was **not observed**: direct warning-error probes still
produce expanded assertions instead of a compiler error. The source-path-dependent
guard explains that difference; preserve these results rather than describing all
six as confirmation of the original prediction. No further probe is needed merely
to repeat an established policy/output boundary.

The first diagnostic's `rewritten` field is also incomplete: it looks only in the
test function's `co_names`. For both special expressions it is false even when
actual native output is expanded; transformed function-local imports need not
appear in that global-name tuple. Keep the original flag unchanged, and do not
interpret it as proof of plain loading. Actual assertion text is decisive here.

## Preserved failure, storage and cleanup

Before the first container, an inherited8GiB free-space check stops startup with
7,957,454,848bytes free. No diagnostic cell starts. The host and guest copies of
the already-loaded owned image transport are verified against their frozen hash;
only the redundant1,025,771,520-byte guest archive is removed. Host archive and
loaded image remain, the unchanged space threshold then passes. This retained
preparation failure is not a discarded diagnostic result or relaxed limit.

Both preparations verify418 original source hashes, apply the unchanged private
gold patch, install successfully with the same three offline wheels and preserve
patched source bytes. Python3.9.20, actual pytest4.5.1.dev41+g5df4d131.d20260928,
source imports under `/testbed/src`. No original test patch or required labels
enter either diagnostic container. Original issue data stays private.

All diagnostic inputs match their freezes. Both executions retain network none,
no mounts, cap-drop ALL, no-new-privileges, default seccomp,1GiB/1CPU/64PIDs and
90-second installation/15-second cell/180-second driver limits. No timeout, OOM or
container execution failure. [First cleanup](results/external-bundle-02-pytest5103-rewrite01/cleanup.json)
and [second cleanup](results/external-bundle-02-pytest5103-rewrite02/cleanup.json)
each verify zero containers, inactive/disabled services, VM Stopped and no owned
Lima/SSH processes.

The next useful environment decision must preserve the original warning/error
contract and distinguish an actually compatible runtime from changing assertions
or suppressing warnings to get a green result. No original pair retry or new model
measurement follows this diagnosis. Whole-task costs, ordinary skill resources,
public download, featured charts and the full eight-role objective stay unchanged.

한국어: 같은 간단한 검사에서 SyntaxWarning을 오류로 처리하면 두 표현식만
상세 메시지가 사라지고 일반 대조군은 유지됐다. 실제 파일 로딩 때만 추가하는
None 경고 코드와 컴파일 오류 후 일반 로딩 경로를 소스에서 확인했다. 직접 변환은
계속 상세 메시지를 내므로 사전 예측 일부가 틀렸다는 사실도 보존한다.
전역 이름만 보는 불완전한 표시를 실제 변환 부재로 해석하지 않는다. 원본 채점은
반복하거나 완화하지 않았고 불합격은 유지한다.12개 작성자 진단·모델0회이며,
두 실행의 컨테이너·서비스·VM 종료를 확인했다. 전체8개 절감 목표는 여전히 미달이다.
