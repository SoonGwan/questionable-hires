# External bundle02 preparation — 2026-09-27

Skills resource **`7172b50c`**. [Selection policy](EXTERNAL-BUNDLE-02-SELECTION.md)
was committed before fetching new issue data. [Identity manifest](results/external-bundle-02-selection/identities.json)
retains the pinned test-split revision,three100-row response hashes,eligible counts,
selection hashes,base/environment commits and issue-statement hashes. All300
identities are unique; responses identify revision b0dde1093fe417d83b7184254edf8199c1f0dff5.

| Selected issue | Version | Base commit |
| --- | --- | --- |
| psf__requests-3362 |2.10 |36453b95b13079296776d11b09cab2567ea3e703 |
| psf__requests-863 |0.14 |a0df2cbb10419037d11d04352b3175405ab52941 |
| psf__requests-1963 |2.3 |110048f9837f8441ea536804115e80b69f400277 |
| psf__requests-2674 |2.7 |0be38a0c37c59c4b66ce908731da15b401655113 |
| pytest-dev__pytest-5221 |4.4 |4a2fdce62b73944030cff9b3e52862868ca9584d |
| pytest-dev__pytest-5103 |4.5 |10ca84ffc56c2dd2d9dc4bd71b7b898e083500cd |
| pytest-dev__pytest-6116 |5.2 |e670ff76cbad80108bde9bab616b66771b8653cf |
| pytest-dev__pytest-11143 |8.0 |6995257cf470d2143ad1683824962de4071c0eb7 |

After excluding the two previously exposed pilot IDs,eligible counts are Requests5
and pytest16. The fixed hash order picks4 per repository without statement,
difficulty,patch/test/version filtering. No inconvenient case is replaced. Issue-only
projections remain local; public records contain identity/hash metadata, not issue
bodies or answer-bearing patches/hints/grading labels. Response bytes including
answer fields were transient and not printed/saved into solving contexts. No model
call,grade or quality/cost result. Public training exposure remains possible.

## Actual environment state

[Read-only availability inspection](results/external-bundle-02-selection/environment-availability.json)
finds no Docker/Colima on PATH or at the checked known install paths. The existing
/usr/local/bin/docker is a dangling link. Inspected podman/nerdctl/limactl commands
are also unavailable; Python3/Node/Git exist. This does not prove no daemon,VM or
image exists; their current state is unverified without a supported executable.
No installation,restart,global/account/dependency change or container mutation.

The existing adapter invokes Docker in colima-qh-bench. Its old cached image IDs
cover Requests2.4 and pytest5.4 pilot resources,not these selected versions/base
commits; they cannot be promoted into native readiness for new issues. Legacy
project interpreter compatibility must be verified rather than assumed from the
modern helpers' Python3.9+ support. Optional helpers must not force another runtime.

Selected public entry imports,generated metadata,native pass/assertion-fail controls,
required regressions and runtime/resource isolation are **not yet established**.
A separate frozen execution protocol is also absent. Do not launch comparisons
until both gates hold. The unavailable Docker route constrains this evaluation;
it is not a reason to mark the overall goal blocked while other useful work exists.

## Interpretation boundary

This is a fresh externally authored issue selection with unchanged candidate skills,
not independent-of-training validation,representative sampling or role-specific
all8 superiority. Auto-discoverable bundle adoption must be observed; eight fixes
alone would not show each skill's contribution. The full requested quality/lower
whole-task tokens/faster completion objective remains unmet. Existing adverse
results and local author/functionality versus model evidence stay separate.

[Official dataset documentation](https://www.swebench.com/SWE-bench/guides/datasets/)
identifies issue statements separately from gold and test patches. The selected
pinned test split defines300 records; the documentation's all-split size is not used.

한국어: external-bundle02 준비(2026-09-27,스킬`7172b50c`)에서 이전2개를 제외한
외부 이슈8개를 본문·정답 평가 없이 고정 해시 순서로 선택했다. 원본 응답의 리비전·
해시·개수와 선택된 커밋·버전을 보존한다. Docker·Colima·확인한 대체 런타임 명령이
없고 Docker 링크는 끊겨 있어 기존 이미지 상태나 새 이슈의 native 실행은 미검증이다.
다른 버전의 과거 이미지 통과를 재사용하지 않고 모델 호출·성능 평가도 하지 않았다.
새 환경과 실행 규약이 필요하며 외부 선택 자체가 전체8개 역할 목표 달성은 아니다.
