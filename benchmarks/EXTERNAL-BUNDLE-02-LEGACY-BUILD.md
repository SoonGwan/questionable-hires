# External bundle02 — legacy pytest bootstrap, 2026-09-27

Parent `211ab91a`; skill resource stays `7172b50c`. Author environment preparation,
zero model calls, no whole-task efficiency or issue-success claim. Selected cases
and tracked application sources are unchanged.

Create an owned venv from existing Apple Python3.9.6. Pin dependencies within all
three sources' declared ranges (not a claim that those ranges guarantee complete
compatibility). Initial binary-only installation of atomicwrites1.4.1 exits1,
with no matching binary candidate; preserve [original error](results/external-bundle-02-legacy-build/environment/initial-install.stderr.txt).
A second explicit pin uses1.4.0, also satisfying >=1.0. Download all pinned wheels
from public PyPI with isolated pip/no cache/zero retries/bounded timeouts, then
install offline from that owned wheelhouse. Pip check passes; freeze and wheel
hashes are retained in the [environment evidence](results/external-bundle-02-legacy-build/environment/v2-summary.json).
Existing environments/global packages/accounts stay unchanged.

Acquire each exact upstream base in owned depth500 checkouts, find an actual
reachable upstream tag using the earlier cached tag identity listing, fetch that
tag and require native merge-base ancestor success. This bounded shallow process
makes no claim about all upstream refs. Compare complete tracked path sets and
hashes to exact-base archives before build and all tracked hashes after controls:
433/418/474 files remain equal, respectively.

The first wheel builds all exit0, but pip's default out-of-tree build leaves the
source version files absent. The4.4/4.5 public imports return `unknown`; their
assertion controls work, but metadata readiness is incomplete. The5.2 public
import and both controls exit1 with missing `_pytest._version`, not valid assertion
failures. [Initial results](results/external-bundle-02-legacy-build/initial-summary.json)
and all original build/control reading logs remain unchanged.

Correct only the build invocation with pip's supported `--use-feature=in-tree-build`,
keeping no-build-isolation/no-deps/no-index and the unchanged native build system.
All three source version files are now generated. Fresh public imports print the
actual source entrypoint and versions; native fresh-process assertion controls use
normal rewriting, owned config/TMPDIR/basetemp and disabled plugin autoload:

| Selected issue | Native generated version | Import | Pass / deliberate assert fail |
| --- | --- | --- | --- |
| pytest5221 |4.4.2.dev174+g4a2fdce6 |0 |0 /1, both valid |
| pytest5103 |4.5.1.dev40+g10ca84ff |0 |0 /1, both valid |
| pytest6116 |5.2.3.dev198+ge670ff76 |0 |0 /1, both valid |

Each passing process reports1 passed; each failing process reports1 failed with
`assert 41 == 42`. No plain-assert bypass, application patch, pretend-version
variable or fabricated generated file was used. Public
[v2 evidence](results/external-bundle-02-legacy-build/v2-summary.json) includes native
statuses, generated-file/output hashes and source preservation. Per-case folders
retain raw-output hash manifests and path-redacted deterministic gzip reading logs,
control source and complete tracked-source hashes. Raw logs/wheels/upstream history
remain local; build and control subprocesses have terminated.

Together with the previous modern pytest and Requests work, all8 selected sources
now have successful cold import routes. These are author bootstrap/transport
controls, not native existing-project suites, issue regressions, model-generated
repairs or training-independent evidence. Required project tests and supporting
services/dependencies, solver history isolation, frozen runtime identities and
execution protocol still gate any model comparison. All8 role quality plus lower
whole-task tokens and faster completion remains unproven.

한국어: 구버전 pytest3개도 원본 빌드로 버전 파일을 생성했고 cold import와
정상/실패 native assertion 검사가 모두 통과했다. 첫 의존성 선택 실패와
빌드 복사본에만 파일이 생성되던 실패를 보존한다. 전체8개 소스의 import 경로는
확보했지만 실제 프로젝트 필수 검사·모델 성능·각 역할 개선 검증은 아직 남아 있다.
