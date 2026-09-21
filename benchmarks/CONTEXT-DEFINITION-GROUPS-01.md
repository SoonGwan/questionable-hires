# Complete named definition groups — 2026-09-21

Parent `75a46c9`; Con Artist collector capability, not model-performance evidence.
Recent Click design reviews required overloaded methods in a large source file.
The existing collector rejects `core.py:Parameter.get_default` as ambiguous;
this was reproduced before modification. Its strict default is correct: three
definitions exist, and static spelling does not prove a unique runtime binding.

Optional `--all-matches` now returns complete same-name leaf groups instead of
selecting a presumed implementation. Every definition includes original line
numbers/decorators and the file hash. Unique selectors become one-member groups;
file/line selectors remain unchanged. Missing names and ambiguous parent scopes
still fail. No decorator-name heuristic, runtime import, execution or dependency
on another skill. Ancestor context, invocation-local caching and exact serialized
output limits remain; groups are never silently shortened.

Six tests cover overload+implementation preservation without importing a module
that raises, conditional alternatives, ambiguous parents, unchanged line/full
selection, ancestor/context cache reuse, exact compact/pretty output boundaries
and actual CLI success/default refusal. Python3.9.6:6 pass in0.237s;
Python3.11.16:6 pass in0.088s. All26 context tests and32 audit-context tests pass
on both interpreters, including the pre-existing safety and selection controls.

## Real-source capability check

Pinned Click `6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1`; source SHA-256
`9b329605c6f3543358bfabeefa9ab9d72a2279c211c1c9c166644cbdbf1e4c08`.
One collection with four known names returns all eight definition spans:

| Selector | Complete spans |
| --- | --- |
| `Parameter.get_default` | 2463–2466,2468–2471,2473–2504 |
| `Parameter.consume_value` | 2509–2555 |
| `Context.lookup_default` | 780–783,785–788,790–810 |
| `Context._default_map_has` | 766–778 |

Compact result is15,174 characters including ancestor configuration and its final
newline; all eight selected definitions are complete. This is
not a model token count, complete caller review or measured session saving.
Context needed outside those definitions still requires inspection. The previous
Click model sessions did not use this new option and cannot establish its benefit.
No additional model run or featured chart change is made here. Landlord remains
self-contained and has not acquired a dependency on Con Artist.

한국어: 같은 이름의 오버로드 선언과 구현을 한 번에 빠짐없이 읽는 선택 기능을
추가했다. 기본 모드의 모호성 거부는 유지하고 실행 시 쓰이는 정의를 추측하지
않는다. 실제 Click 소스와 단위·CLI 검사에서 동작을 확인했지만 모델의 전체
작업 비용 감소를 입증한 것은 아니다.
