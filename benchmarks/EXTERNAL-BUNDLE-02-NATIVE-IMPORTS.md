# External bundle02 native imports — environment not ready, 2026-09-27

Candidate skill resource **`7172b50c`**. Selected source identities remain those
[fixed before inspection](EXTERNAL-BUNDLE-02-SELECTION.md); no selected case is
replaced. [All eight source/probe records](results/external-bundle-02-native-imports/summary.json)
retain archive SHA256,base/version identity,native exits and original/reading hashes.
This is author environment preparation,not model work or task-quality scoring.

Downloaded exact selected GitHub base-commit archives into owned local directories.
Compressed limit16MB and expanded file-byte limit64MB per issue; every entry was
checked for relative regular file/directory paths,one expected commit prefix and
no traversal before extraction. Source trees/history/requirements were not patched.
No project setup script,dependency install,global/account/configuration change.

Fresh native processes use the existing Python3.11.6 validation environment:
python -B -c performs importlib.import_module('requests' or 'pytest'). PYTHONPATH
selects the extracted src/ root when present,then project root. The probe would
require the returned module path to remain in that source tree on success. The
child environment carries PATH,the selected source path,no-bytecode and disabled
optional pytest plugin autoload; it does not pass runtime credential variables.
Each actual import has a20-second bound. All8 return exit1 with preserved tracebacks;
none times out. No public-entry success or native test execution is claimed.

| Selected issue | Actual import exception | Additional gate |
| --- | --- | --- |
| psf__requests-3362 |Missing urllib3 |Required dependencies/runtime unverified |
| psf__requests-863 |collections.MutableMapping import unavailable |Legacy Python/runtime compatibility unverified |
| psf__requests-1963 |collections.MutableMapping import unavailable |Legacy Python/runtime compatibility unverified |
| psf__requests-2674 |collections.Mapping import unavailable |Legacy Python/runtime compatibility unverified |
| pytest-dev__pytest-5221 |Missing six |Generated src/_pytest/_version.py also absent |
| pytest-dev__pytest-5103 |Missing six |Generated src/_pytest/_version.py also absent |
| pytest-dev__pytest-6116 |Missing atomicwrites |Generated src/_pytest/_version.py also absent |
| pytest-dev__pytest-11143 |Missing _pytest._version |Generated src/_pytest/_version.py absent |

The exceptions establish these current-environment failures,not that supplying one
missing module alone would finish bootstrap or issue evaluation. Native pass/fail
controls,required issue regressions and stable runtime identities are still missing.
The installed pytest8.3.4 package or old Requests2.4/pytest5.4 image records cannot
stand in for the selected source/version. Do not invent generated version metadata,
patch legacy imports or reuse cached submodules to turn this into nominal readiness.

Each issue's stdout/stderr is retained as an explicitly path-redacted gzip reading
copy linked by the summary. Original logs and source archives remain local with
hashes; no solution/test patches or model-private contexts are exported. The
native exceptions are setup failures,not assertion-based fault controls,completed
model tasks,skips or performance savings. **Required native tests0/model calls0.**

Existing Docker-route availability remains [unverified/unavailable through the
checked CLIs](EXTERNAL-BUNDLE-02-PREPARATION.md). Requested information is a usable
existing runtime/interpreter path; no new installation or global change is inferred.
This evaluation route remains gated; the overall goal stays active and unmet.

한국어: external-bundle02 native import 확인(2026-09-27,스킬`7172b50c`)에서 고정
외부 소스8개를 실제 기존 Python3.11.6의 새 프로세스로 import했고 모두 종료1이었다.
구버전 collections API,urllib3/six/atomicwrites 의존성,pytest 생성 버전 파일 누락을
원본 traceback으로 구분했다. 코드를 고치거나 의존성을 설치하지 않았다. 이는 실행
환경 실패이며 스킬·이슈 해결 성능 실패나 정상/결함 assertion 대조 검사가 아니다.
필수 프로젝트 테스트와 모델 호출은0회다. 원본 해시·경로를 가린 로그를 보존하고,
호환되는 기존 런타임 정보와 나머지 native 환경 검증이 필요하다.

## Later existing-interpreter check

[Python3.9 follow-up](EXTERNAL-BUNDLE-02-PYTHON39.md) finds an existing Apple runtime
and imports the same4 Requests sources,with real author HTTP assertions. Earlier
Python3.11 failures remain unchanged. Requests3362's missing-global-urllib3 error
follows a bundled collections.Mapping failure in the original traceback; the final
exception alone is not its full cause. Pytest and required-test gates remain unresolved.
