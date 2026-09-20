# Context collector: unrelated expression recursion — 2026-09-20

Prior source `812ff14`. A valid 3,039-byte Python file containing a module-level
sum of 1,500 constants followed by a small `target` function parsed successfully,
but both named and line-based discovery raised `RecursionError`. The CLI emitted
`status: incomplete` and exit2 instead of returning the available definition.
The same failure also affected line selection when the expression was inside the
function or its decorator. No project code needs executing to reproduce this.

Cause: `scope_definitions` and `definition_spans` recursively walked every AST
expression node, although expressions cannot contain function/class statements.
Both traversals now skip expression subtrees while preserving statement containers,
definition ordering, nested scopes, decorators and ambiguity handling. Parsing and
deep statement nesting remain subject to interpreter limits; no total-memory or
arbitrary-depth guarantee is made.

Evidence:

- New regression suite before fix: three tests, one CLI assertion failure and
  three subtest recursion errors. Control for nested/conditional ambiguity passed.
- After fix: all three new tests pass. Actual CLI selectors return exact source
  and hashes; missing definitions still exit2 with no partial stdout. A source
  containing an unconditional `raise` is inspected without execution.
- Python3.11: 43 context/line/decorator/read-race checks pass. Python3.9: seven new
  depth/line-index checks pass.
- Differential comparison of every definition-start line in the eleven shipped
  Python helpers: 95 selected excerpts, batched up to eight per invocation, all
  full result dictionaries identical to prior implementation on the same files.

Reproduce regression checks:

```sh
PYTHONPATH=tests python3 -B -m unittest test_context_expression_depth test_context_line_index -v
```

This is an actual collector failure correction, not another run of the exposed
model benchmark and not a measured model token/time improvement. No frozen task,
reported model result, skill activation rule or featured chart changed.

한국어: 유효한 약 3KB Python 파일에서도 긴 수식 때문에 무관한 함수 선택까지
재귀 오류로 실패하는 문제를 수정했다. 정의가 들어갈 수 없는 수식 하위 노드만
건너뛰며 중첩·조건부 정의와 모호성 검사는 유지한다. 관련 검사 43개와 실제
코드의 95개 선택 결과 대조를 통과했다. 모델 전체 토큰·시간 개선의 증거는 아니다.
