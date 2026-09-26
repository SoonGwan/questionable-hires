# Native-split02 output follow-up — 2026-09-27

Measured resource remains `6c099d68`; predecessor `33530f98`.
[All six reconciled costs](NATIVE-SPLIT-02-COSTS.json) and
[frozen protocol](NATIVE-SPLIT-02-PROTOCOL.md) remain unchanged.
No full-quality score or efficiency promotion follows from this partial review.

Original retained tool records contain native counts for all six cells:

| Task / condition | Native counts in execution order |
| --- | --- |
| Single / baseline |13,13,5,5 |
| Single / predecessor |13,13,3,3 |
| Single / candidate |13,13,3,3 |
| Multiple / baseline |13,12,13,12,13,12,13,12 |
| Multiple / predecessor |13,13,16,16,13,16,13,16 |
| Multiple / candidate |13,13,19,19,13,19,13,19 |

These are observed counts, not quality rankings. Reused observations are not
additional executions. Different requested/additional selections stay in costs.
Five captured final native outputs have no outer truncation marker. The
predecessor/multiple output has a **391-token truncation** in the command and
copied-import boundary. Test counts and assertion text elsewhere do not recover
that missing portion. No replay replaces missing original evidence. Complete
binding, assertion, preservation and cleanup review remains unfinished.

The native batch reference now explains how to retain a large report in owned
temporary scratch outside the guarded project and inspect its executed checks
separately. This addresses an observed tool-capture failure; it does not reduce
native coverage, change helper behavior or claim measured whole-task savings.
A tool transcript cutoff differs from the helper's per-check 12,000-character
tail limit. A saved report cannot recover output already discarded by the helper.
No mandatory report, new helper, dependency or formatter is introduced.

Packaged guide controls:4 tests, zero skips, exit0. Catalog and Skill Creator
metadata checks pass in the existing Python3.11 validation environment. The
system Python lacks PyYAML, so its first catalog invocation did not run; no
package was installed to hide that environment limitation.

[Actual installed behavior](INSTALLED-BEHAVIOR-6C099D68.json) separately exercises
pinned source archive `6c099d68` through the cached local skills CLI:8 skills,
exact copied bytes/modes,9 Python entrypoint help checks, installed Python and
JavaScript controlled callbacks, named-region selection plus missing-name exit1,
and Receipt native before1/after0 with unchanged source tree. All21 command exits
match their expected status. This is macOS local installation, not a fresh remote
install, Linux/hosted matrix, or candidate model-efficiency evidence. The new
reference wording is later than that installed resource and is not retroactively
included in its result.

한국어: 이전 버전의 실제 도구 출력391토큰 잘림을 보존한다. 큰 보고서를 한 번
실행해 임시 보관하고 검사별로 읽는 경로를 보강했으며, 누락 증거를 재실행으로
대체하지 않는다. 가이드4개 검사와 이전 후보의 실제 설치21개 명령 검증은
통과했지만 전체 품질·토큰·시간 개선 및 원격 배포 검증을 뜻하지 않는다.
