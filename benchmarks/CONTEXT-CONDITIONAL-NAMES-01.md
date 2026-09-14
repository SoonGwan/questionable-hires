# Conditional Python name selection — 2026-09-15

This is local helper correctness evidence, not a model benchmark or a token/time
gain. Parent source `1d80f49`; the first regression tests are preserved in
`2f68f14`. Con Artist's optional static context collector remains read-only.

## Reproduced gap

Line selection already traversed conditional/nested definitions. Named selection
only inspected direct body statements, so a known `outer.inner` inside an `if`
and `try` failed with “Missing or ambiguous definition.” A method inside a
handler/loop/class conditional failed similarly. More importantly, an ordinary
`def selected` followed by a conditional definition of the same name incorrectly
returned the ordinary definition instead of reporting ambiguity.

Adding four tests before changing runtime produced **31 tests, three assertion
failure entries**: two unavailable known definitions and one expected ambiguity
that was not raised. Existing line selection, source preservation and nested
scope exclusion provide controls. The tests use deliberately unresolved names
and a top-level exception; source must never execute.

## Correction and checks

Named lookup now descends through non-definition AST nodes at each selected
scope, stopping at class/function boundaries. Every component of the qualified
name must still identify exactly one definition. It neither evaluates branches
nor chooses a preferred branch. Duplicate parent classes remain ambiguous even
if only one contains the requested method. Unqualified names do not leak from
nested functions. Original decorators, line numbers and source hashes remain.

After the correction, the initial **31 tests pass**. One further actual isolated
CLI test checks unique conditional success and duplicate refusal, empty stdout
on refusal, JSON status and unchanged source. The resulting **32 context tests
pass** (0.677s on this host). No per-skill entry text or default workflow is added;
only the optional collector and its focused reference change.

Run:

```sh
python3 -B -m unittest discover -s tests -p test_audit_context.py
```

This is static selection, not runtime binding resolution. A unique definition
may be unreachable, decorated, or overwritten by a later assignment. The index
format/coverage is unchanged: conditional class-body definitions may still need
surrounding source inspection. Existing file/input/output limits, no-import
behavior and scope protections remain. No model adoption measurement, independent
project performance claim or featured chart update is made.

한국어: 조건문 안의 함수를 이름으로 찾지 못하는 문제와, 일반 정의 뒤의 조건부
동명 재정의를 놓쳐 첫 함수만 반환하는 문제를 재현했다. 수정 전 실제 단언 실패
3건을 확인했고, 수정 후 CLI 성공·모호성 거부를 포함한 관련 검사 32개가 통과했다.
조건을 실행하거나 런타임 바인딩을 추정하지 않는다. 선택에 실패한 뒤 같은 코드를
다시 찾는 경로를 줄일 수 있는 기능 수정이지만 모델 토큰·시간 절감은 미측정이다.
