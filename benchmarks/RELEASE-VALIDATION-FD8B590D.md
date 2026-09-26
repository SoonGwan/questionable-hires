# Local release validation — 2026-09-27, source `fd8b590d`

[Exact summary and hashes](results/release-validation-fd8b590d/summary.json).
This source includes Receipt completion, collector diagnostics, history body-offset
selection and the namespace/Fast scheduling controls added after the historical
[ba2713d5 validation](RELEASE-VALIDATION-BA2713D5.md). It is not a completed
all-eight efficiency release. Original model comparisons retain their own resources.

| Source form | Native unittest suite | Exit | Local elapsed |
| --- | --- | ---: | ---: |
| Checkout |1,290 discovered,17 skipped,zero failures/errors |0 |195.505s |
| Git-free archive |1,290 discovered,47 skipped,zero failures/errors |0 |180.240s |

Both run python -B -m unittest discover -s tests -q on macOS26.5.2/arm64,
Python3.11.6 in the existing validation environment. No model calls or dependency
updates. Archive entries were checked for relative regular files/directories without
traversal before extraction into an empty owned directory; no .git. Source archive
SHA256 `c8d8f54e6d1f6b48c6dcf61258f8894c42f1eb9f6daa2e8a1b189779da2c0975`.
Skips are not passes. These times describe local tests, not performance comparisons.

Path-redacted reading copies of actual full logs are retained separately:
[checkout](results/release-validation-fd8b590d/checkout-reading.log.gz),
[archive](results/release-validation-fd8b590d/archive-reading.log.gz).
Summary records original unredacted log hashes and derivative hashes; originals
remain local. Redaction does not change native results, assertions or counters.

## Actual installer failure and repair

The original local CLI check exited1: the source had generated
con-artist/scripts/__pycache__/audit.cpython-311.pyc, but the CLI excludes
__pycache__ directories from installation. The checker incorrectly required that
local bytecode to be installed. [Original failure reading copy](results/release-validation-fd8b590d/installer-reading.log.gz)
is preserved. This failure is not a failed skill behavior check or a passing install.

Checker-only correction **`e9ab80e1`** excludes cache-directory descendants from
installation expectations. Full source inventory still includes caches and must
remain byte/mode identical afterward; actual installed inventory remains complete,
so unexpected files are still rejected. The local cache is not deleted or changed.
No broad ignore list or installer/runtime change.

With the same source cache present, actual cached skills CLI1.5.18 copy/install
passes: **8skills/51files**, byte/mode parity,9 Python help entrypoints,25 actual
command exits. [Full corrected observations](results/release-validation-fd8b590d/installed-behavior-after.json)
retain native Receipt before1/after0, Con Artist0/0/0/1 plus wrong-binding incomplete7,
Exorcist child failure17/timeout124/cleanup, named-region selection and installed
Python/JavaScript callback assets. Source and installed inventories remain unchanged.
No global installation, account/configuration changes or remote availability claim.

Existing installed-helper tests pass2/2 in checkout and2/2 in a Git-free copy of
fd8b590d with the exact corrected checker. [Archive reading log](results/release-validation-fd8b590d/checker-archive-reading.log.gz)
and source hashes are retained. The full1,290-test suites preceded this checker-only
repair; they are not relabeled as full-suite validation of e9ab80e1. Skill bytes are
unchanged by the repair. Hosted/platform, current public-history and website release
checks remain separate. Whole-task quality/token/time objective is still unmet.

한국어: fd8b590d(2026-09-27)의 실제 전체 검사는 체크아웃1,290개·17개 건너뜀,
Git 없는 아카이브1,290개·47개 건너뜀으로 실패 없이 끝났다. 최초 설치 검증은
로컬 바이트코드를 설치 파일로 잘못 비교해 종료1이었다. e9ab80e1에서 검증기의
설치 기대 목록만 보완했으며 캐시 포함 원본 보존 검사는 유지한다. 같은 캐시가
남은 실제 CLI 설치에서8개 스킬51개 파일·25개 명령이 통과했고, 보완 후 관련
검사2개는 체크아웃·Git 없는 복사본 모두 통과했다. 원본 실패·로그 해시·경로를
가린 열람용 로그를 보존한다. 전체 검사 커밋과 이후 검증기 보완을 구분하며 모델
비용 절감·원격 출시·전체8개 역할 목표 완료로 확대하지 않는다.
