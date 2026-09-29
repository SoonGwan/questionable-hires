# urllib3 inline transfer02 — native build gate, 2026-09-27

Parent `ae2b681b`; candidate `80c06e2e` remains unadopted. This is a new
resource prepared by the author, not a repair/rescore of transfer01 or model
performance evidence. The missing-version/import-retry defect was already
reported in [the original preflight qualification](URLLIB3-HISTORY-01-PREFLIGHT.md)
and [partial-import audit](AUDIT-PARTIAL-IMPORT-01.md); transfer01 rediscovered
that known limitation. Retain those earlier adverse outcomes.

A separate local full clone of pinned commit
`2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df` was made without hardlinks or hooks.
An isolated Python3.11 build environment installed the repository-declared
`hatchling>=1.6.0,<2` and `hatch-vcs==0.4.0`. The actual `hatchling.build.build_wheel`
backend generated `src/urllib3/_version.py` from Git/tag metadata; no handwritten
version stub, global installation, source adaptation or wheel installation.
Exact resolved build packages and outputs are in
[execution](results/urllib3-inline-transfer-02-native/execution.json).
The local clone and package installation completed, but their commands had no
independent parent watchdog; backend60s/import30s/observer30s bounds apply only
to recorded execution stages. Future scheduling must preserve this distinction.

A fresh process using the original host interpreter and selected source path
imports the public package and Retry implementation, asserts both local paths,
and observes version2.2.3. The retained transfer01 observer then executes15
actual calls: current `[False,False,True,True,True]`; A-only
`[True,False,True,True,True]`; B-only `[False,True,True,True,True]`.
Its complete reports have5 evaluated cases each,0 unrun/ungraded, and
mismatches0/1/1. Inputs and original method binding are preserved.

[Preservation](results/urllib3-inline-transfer-02-native/preservation.json)
verifies all39 selected tracked files match the untouched original, clean
tracked Git status, pinned HEAD, wheel/metadata hashes, and absent version file
in the original clone. A separate author replay verifies generated metadata
survives observer execution unchanged. That replay is not independent validation.
The original failed import and empty stdout remain frozen in transfer01.

Zero model calls, HTTP requests or historical native execution. This completes
only the actual-package observer gate. Before a paired model schedule, freeze
the new fixture identity including ignored generated metadata and its lifecycle;
keep existing task/history/criteria and all adverse prior evidence accessible.
Native success does not establish lower whole-task tokens/time or all8 quality.

한국어: 별도 복제본과 격리 빌드 환경에서 공식 빌드 백엔드로 버전 파일을
생성했다. 원래 인터프리터로 새 프로세스의 공개 패키지 import와 후보 관찰기
15개 호출을 확인했으며 원본 소스·바인딩·입력·생성 파일을 보존했다. 이 결함은
과거에도 기록돼 있던 것으로 새 발견이나 이전 결과의 재평가가 아니다.
모델0회이며 토큰·시간 절감 또는 전체8개 품질 향상 증거는 아직 없다.
