# Source release check — 2026-09-28

Parent `53129f98`; publication remains separate. After the local installation
sync, the full ordinary regression run exposes one stale installation-verifier
expectation: the adopted Receipt producer emits v3, but the checker still requires
v2. The actual installed helper is not failing its application tests; the author
checker rejects the correct new report version.

The checker now requires v3 and also runs a native pathlib equality before the
age-boundary assertion, verifying typed path arguments and primitive values in
both observed phases. Native before1/after0, same-process import verification,
source preservation and cleanup remain required. The regression test requires
the new version and path-evidence flag; no historical v2 report is relabeled.

| Check | Actual result |
| --- | --- |
| Full initial regression, Python3.11.6/pytest8.3.4 |1,365 methods;1,347 pass,1 failure,17 skips;200.357s, exit1. |
| Affected installed-helper tests after correction |2 pass in checkout. |
| Same two tests from a56-file Git-free source archive |2 pass; actual isolated installed CLIs, no checkout imports/history. |
| Exact17 skipped experimental reporter controls, Node24.16.0 |17 pass,1.511s; selected only in the child test process. |

The Node runtime was downloaded into an owned temporary directory from the
[official versioned archive](https://nodejs.org/dist/v24.16.0/node-v24.16.0-darwin-arm64.tar.gz)
and matched against its [official SHA-256 list](https://nodejs.org/dist/v24.16.0/SHASUMS256.txt).
No global runtime or host configuration was changed. These controls test the
unadopted native reporters, not a claim that they improve whole-task costs.

[Initial full output](../benchmarks/results/release-source-check-20260928/full-tests-before.txt),
[archive output](../benchmarks/results/release-source-check-20260928/archive-tests-after.txt),
[source identities](../benchmarks/results/release-source-check-20260928/archive-sources.json),
[Node follow-up](../benchmarks/results/release-source-check-20260928/node24-tests.txt),
[runtime identity](../benchmarks/results/release-source-check-20260928/node24-identity.json)
and [summary](../benchmarks/results/release-source-check-20260928/summary.json)
retain the evidence. Public paths are redacted; original/public hashes distinguish
the representations. The first full run remains failed with skips. Together the
scoped follow-ups cover all1,365 distinct methods; this is not a single all-green,
no-skip full process. The unaffected passing tests were not rerun for presentation.

Fetching origin also confirmed that the recent local changes were not yet in
origin/main (`995c67f7`). This check neither pushes commits nor claims a fresh
remote installation or hosted deployment. The source diff and publication of
historical evidence need their own review; local native success does not settle
those gates. Whole-task model efficiency across all eight roles remains unproven.

한국어: 전체1,365개 검사에서 구버전 v2를 요구하던 설치 검증기1건을 발견해
v3와 실제 경로 인자를 확인하도록 고쳤다. 해당2개 검사와 Git 없는 복사본 검사가
통과했고, Node24가 필요해 건너뛴17개도 별도 임시 런타임에서 모두 통과했다.
초기 실패·건너뜀은 보존하며 여러 실행의 검증 범위를 하나의 무조건 통과 결과로
바꾸지 않는다. 공개 소스·호스팅 배포와 전체 모델 비용 목표는 여전히 별도다.
