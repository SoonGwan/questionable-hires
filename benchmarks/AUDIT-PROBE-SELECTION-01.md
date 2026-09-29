# Native stronger-probe selection reuse01 — 2026-09-28

Parent **`4dac0d2b`**; [changed source digests](results/audit-probe-selection01/sources.json).
[Native controls](../tests/test_audit_probe_selection.py),
[before](results/audit-probe-selection01/before.txt),
[after](results/audit-probe-selection01/after.txt).

Adopt a bounded helper optimization: identical native file probes can reuse their
successful correct-code observation when only the original test selection differs.
Every required mutant check still executes. This reduces native process work for
that recipe shape; model selection, whole-task tokens/time and all-eight improvement
remain unmeasured by this change.

## Mechanism and prior work

The [selection cache](AUDIT-SELECTION-REUSE-02.md) handles returning original test
selections; [probe cache02](AUDIT-PROBE-CACHE-02.md) handles returning stronger probes
but deliberately retained original test arguments in its shared context. Neither
removes this different source of invalidation. The [compact-entry screen](COMPACT-AUDIT-MODES-01-REVIEW.md)
was declined, including a custom harness's provenance repair and additional native
processes. It motivates examining actual work, not attributing that model's cost to
this helper: that verified candidate did not use the helper at all.

For native file probes, audit() replaces `tests` with `probe_tests` before execute().
The original selector therefore does not reach those processes. Keep the actual
probe arguments in the existing per-entry identity and omit only the superseded
original selector from the file-probe context. This applies to native unittest
(module or bootstrap) and installed pytest. Inline probes retain their existing
context because the original selector remains in the bootstrap payload. Changing
between inline/file modes also changes context. No new cache, helper mandate,
entry instructions, external state assumption or additional fault is introduced.

Selected bytes/modes, imports, ordered roots, precheck, runner/invocation, interpreter,
timeout, environment and authorized project inventory still invalidate the shared
context. Probe text/new/replacement bytes and actual stronger-test arguments remain
per-entry keys. Eight-entry/20 MB retained-payload bounds and direct observation
references remain; no cache crosses batch invocations. Tests dependent on changing
external state or requiring fresh baselines still need separate observations.

## Native reproduction

The new tests use actual imported service code and native runners. Acknowledgment
and boolean-type selections both survive a removed append; a stronger list assertion
passes correct code and rejects the fault. Native binding assertions, real failure
text, original bytes/modes and scratch removal are checked. Wrappers count calls to
the actual executor; they do not substitute fake results.

| Authored selection/probe pattern | Before native processes | After native processes |
| --- | ---: | ---: |
| A,A,B with identical stronger probe, unittest module |10|9|
| A,B,A with identical stronger probe, unittest module |11|9|
| A,A,B with identical stronger probe, unittest bootstrap |10|9|
| A,B,A with identical stronger probe, unittest bootstrap |11|9|
| A,B,A with identical stronger probe, pytest |11|9|
| A,B,A with changed middle probe arguments |11|10|
| A,B,A with changed middle probe bytes |11|10|

For the identical A,B,A pattern, two original correct tests, three mutant tests
and three mutant probes still execute; only stronger correct runs change3→1.
The two removed processes out of11 are18.18% of this authored example, **not18.18%
fewer model tokens or elapsed time**. No timing-performance estimate is collected.
The different-middle cases still execute their distinct correct probes and then
reuse the first when it returns. No required faulty-code observation is cached.

Six test methods before the edit produce seven expected optimization subcase
failures: counts10/11 rather than9, and11 rather than10. Native failures are genuine
list assertion failures; the unchanged implementation still reports correct audit
outcomes. The unittest identical-probe cases check their mutant assertions and
preservation before the failing count assertion. Later reference/provenance checks
in those failed subcases do not execute; do not claim the complete new suite passed
before the change. After the nine-line runtime diff, all six methods pass with no
skips, including actual pytest collection.

Negative controls retain fresh correct probes after changed precheck, environment,
mode or source; changed probe bytes/arguments get their own evidence. Inline probes
retain11 processes. A detected mutant still skips a conditional probe even when a
matching cached result exists, and a failing changed correct probe stops the batch
with the later mutation unrun. Module output retains native suite counts and each
reused reference points directly to its original successful observation.

## Validation and delivery boundary

Python3.11.6 focused suite:6 methods pass. The initial system `python3` is not used
for pytest coverage; validation uses the existing project validation environment.
A Git-free source copy passes137 focused methods across nine modules, zero skips
([complete log](results/audit-probe-selection01/gitfree-complete.txt)); these include
native unittest/pytest, packaged recipes, invalidation, retention bounds and execution
error handling. Structural mock controls are not native performance measurements.
The first copy omitted the benchmark scratch parent and plan fixture:125 pass and
12 setup errors ([initial log](results/audit-probe-selection01/gitfree.txt)). A new
copy includes the required unchanged fixture before the full rerun; no runtime or
test expectation changed to resolve those preparation errors. This is a copied
source tree without Git, not a claim that a Git archive command was used.

Both English/Korean capability rows and the two relevant batch guides describe the
actual native-probe reuse boundary. Historical checkpoints, featured numbers and
integration07 measurements remain tied to their original resources.

This is local native evidence. Installation, standalone distribution and hosted
release checks are separate delivery evidence; no new model result follows.

한국어: 기존 테스트 선택이 달라도 실제 강화 검사 코드·인자·환경이 같으면 정상
강화 결과를 재사용한다. 작성한 A→B→A 예제의 실제 실행은11회→9회이며 결함
검사는 모두 유지했다. 강화 검사나 입력이 달라지면 새로 실행하고, 실패·조건부
생략·원본 보존도 확인했다. 실행 횟수18.18% 감소는 해당 예제의 네이티브 수치이며
모델 토큰·시간 또는 전체8개 개선율이 아니다. 이전 축약 후보의 실패도 그대로 유지한다.

## Installed and packaged source

Source **`625a0440`** is installed after every prior Con Artist resource matched
parent `4dac0d2b` bytes and Git modes. The old directory is backed up outside skill
discovery. [All eight installations](results/audit-probe-selection01/installation.json)
match current resources; [six installed-helper controls](results/audit-probe-selection01/installed.txt)
pass with the actual installed helper, including pytest.

[Standalone archive checks](results/audit-probe-selection01/package.txt):4 pass.
[Landing/server checks](results/audit-probe-selection01/landing.txt):27 pass.
The151-file build changes only the download archive and checksum. [Download identity](results/audit-probe-selection01/download.json)
verifies all52 packaged skill resources' bytes/modes against source; the archive is
107,239 bytes. The first inventory query incorrectly included the parent directory's
README, which is not an installable skill; the corrected comparison selects the eight
SKILL.md directories used by packaging. Layout, bilingual landing copy, OG and frozen
measurements are unchanged, so no new browser-layout or model-performance result follows.

Original unittest failure logs retain their trailing progress-line spaces; whitespace
checks exclude only those existing transcript spaces, not edited source/documents.

한국어: 소스625a0440를 개인 설치와 배포 패키지에 반영했다. 이전 설치본은 별도
백업하고 전체8개 자원 일치·설치본6개·패키지4개·랜딩/서버27개 검사를 통과했다.
다운로드 자원은 소스와 파일·권한이 같으며 기존 웹 실험 수치와 화면은 유지한다.

## Public delivery

Release **`32a2c4b6c967164ea90d4f218a3e4a512778976e`** is live on the existing
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/) addresses.
[Six HTTPS checks](results/audit-probe-selection01/public.json) verify actual release
identity, exact locale pages/JavaScript, canonical/indexable metadata and checksum.
All52 skill resource bytes/modes inside the public archive match source. Archive
SHA-256 is `a03f45fee906b87abed1c4fb88bc0d224b31630834e53f729d261d577c0e5753`.
Existing integration07 values and measured resource `1be35120` are unchanged.
These HTTP/source checks do not establish browser interaction or model efficiency;
no GitHub push is implied.

한국어: 배포32a2c4b6의 실제 HTTPS 다운로드에서52개 스킬 자원의 파일·권한
일치를 확인했다. 한영 페이지와 체크섬을 포함한6개 경로가 통과했으며, 기존
실험 수치의 측정 대상과 날짜는 바꾸지 않았다.
