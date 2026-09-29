# External bundle02 Python3.9 route — partial native preparation, 2026-09-27

Candidate skill resource **`7172b50c`**. Same eight selected source archives and
base commits; no case replacement or source patch. Existing Apple CommandLineTools
Python **3.9.6** is executable at /Library/Developer/CommandLineTools/usr/bin/python3.
It was outside the earlier PATH/known-runtime inspections. No install,dependency,
account/global settings change or Docker restart.

[Eight cold-import records](results/external-bundle-02-python39/imports/summary.json)
use the identical probe from the earlier Python3.11 preparation and verify archive
hashes before execution. All four Requests public entries now load from the selected
source root and report the expected0.14.0/2.3.0/2.7.0/2.10.0 source versions.
All four pytest entries still fail:three on atomicwrites and pytest8.0 on pluggy.
Missing generated version metadata and further dependencies remain unresolved.
Imports alone do not establish test readiness.

The original [Python3.11 failures](EXTERNAL-BUNDLE-02-NATIVE-IMPORTS.md) stay frozen.
For Requests3362,the final missing-global-urllib3 exception followed an earlier
collections.Mapping import failure in its bundled urllib3. Original traceback
already contains both. Success on3.9 with no dependency installation shows why the
last exception alone was not a complete diagnosis. It is not evidence that every
runtime discrepancy is fixed by switching interpreters.

## Actual author HTTP controls

[Corrected control source](results/external-bundle-02-python39/http-corrected/control.py)
uses actual requests.get from each selected source and an owned loopback HTTP server,
with request/process bounds and server shutdown/close/bounded thread drain. Each
unittest checks status200 and exact binary bytes including NUL/0xff. One separate
fresh-process control expects the deliberately wrong payload and must fail with
native AssertionError,not setup/import/timeout failure.

| Requests source | Normal native control | Wrong expected payload |
| --- | --- | --- |
|0.14.0 |1test,pass,exit0 |1test,actual binary AssertionError,exit1 |
|2.3.0 |1test,pass,exit0 |1test,actual binary AssertionError,exit1 |
|2.7.0 |1test,pass,exit0 |1test,actual binary AssertionError,exit1 |
|2.10.0 |1test,pass,exit0 |1test,actual binary AssertionError,exit1 |

[All eight corrected native outputs](results/external-bundle-02-python39/http-corrected/summary.json)
are retained. The initial control incorrectly called Response.close,absent in0.14:
its [two setup errors plus six valid controls](results/external-bundle-02-python39/http-first/summary.json)
and [original control](results/external-bundle-02-python39/http-first/control.py)
remain separate. Correction uses the source-supported raw.release_conn after consuming
content; application code is unchanged. Do not count these two errors as detected
project faults or silently replace the initial observations. Syntax warnings from
legacy source remain in original logs.

All24 author records (eight imports,eight initial HTTP controls,eight corrected
controls) retain original and path-redacted reading/gzip hashes. Full sources/raw
logs remain local. [Reading-copy index](results/external-bundle-02-python39/reading-copies.json)
explicitly separates these records. Public control code contains no issue solution
or grader; it is not supplied as a task hint to future solving contexts.

## Remaining gates

These are authored bootstrap/transport assertions,**not existing project tests or
selected-issue regression checks**. Required native project tests0/model calls0.
TLS/httpbin readiness,all selected dependencies/generated metadata,stable complete
runtimes and the execution protocol remain absent. The unavailable Docker adapter
cannot be assumed usable; old pilot images cannot stand in for different versions.
Do not label Requests' partial success as readiness of all8 or a whole-team gain.
Existing cost evidence is unchanged; the original objective remains unmet.

한국어: external-bundle02 Python3.9 확인(2026-09-27,스킬`7172b50c`)에서 이미
설치된 Apple Python3.9.6을 찾았다. 같은 원본 Requests4개는 import에 성공했고
실제 loopback HTTP의 정상 assertion0/고의 실패 assertion1을 각 버전에서 확인했다.
최초 작성자 검사에서0.14에 없는 close를 호출한2개 오류도 보존하고 검사만 보완했다.
Pytest4개는 의존성·생성 메타데이터가 여전히 부족하다. 환경 설치나 소스 변경은
없으며,24개 작성자 관찰은 원본 프로젝트 테스트나 모델 성능 결과가 아니다.
필수 이슈 검사와 모델 호출은0회이고 전체8개 역할의 개선 목표는 미달이다.
