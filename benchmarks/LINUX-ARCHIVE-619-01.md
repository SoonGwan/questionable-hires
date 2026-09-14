# Current Linux archive: gate fails, portability assumptions corrected

2026-09-15; local Linux arm64/Python 3.12.3/Node v24.20.0. Existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
No network/downloads, code overlays, model sessions or hosted workflow changes.
Each committed `git archive` is mounted read-only, copied into disposable `/work`,
and verified to contain neither `.git` nor ignored local-run state. Existing
PyYAML 6.0.3 is mounted read-only in pure-Python mode, not freshly installed.

| Source | Discovered | Reported failures | Skips | Seconds | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| `f43c931` | 619 | 15 | 4 | 35.667 | 1 |
| `fd8c926` | 619 | 13 | 4 | 34.775 | 1 |
| `80360c3` | 619 | 11 | 4 | 34.900 | 1 |

Failure counts include subtest entries; do not derive a passed-method count by
subtracting them from discovery. This is **not a passing Linux gate** or a model
performance comparison. Full logs:
[initial](results/linux-archive-619-01/initial-f43c931.txt),
[intermediate](results/linux-archive-619-01/intermediate-fd8c926.txt),
[current](results/linux-archive-619-01/current-80360c3.txt).
Catalog and featured/localization checks pass before each suite.

## Corrected assumptions

- Necromancer's growth regression injected enlargement on the first Path.stat.
  Python 3.12 path resolution reached that hook before the explicit size check;
  the oversized file was correctly rejected without reading, so the intended
  post-check growth was never tested. Inject growth at the binary open instead.
  The test still requires exactly a 2,000,001-byte read and no Git collection.
  Runtime code/bounds did not change.
- Hostage Negotiator's capture test assumed empty unittest discovery always
  exits 0. This runtime exits 5. Compare the captured exit against direct native
  execution, requiring both outputs to say `Ran 0 tests`. Never credit it as a
  passing regression. The shipped capture recipe did not change.
- Receipt's native-mode tests/help made the same zero-exit assumption. Compare
  with the actual native invocation, including `-S` for disabled-startup controls.
  Preserve provenance rejection independently from the native exit. Reference
  and CLI help now describe runtime-dependent empty-discovery exits, not a fixed 0.

macOS/Python 3.9.6 targeted checks: 29 history + 5 native-evidence tests pass after
`fd8c926`; 13 Receipt native-invocation tests pass for `80360c3`.
These are 47 targeted checks, not a new full macOS suite.

## Remaining real compatibility boundary

All eleven final failure entries concern Receipt's native module invocation.
This Ubuntu Python includes `/usr/lib/python3.12/sitecustomize.py`, an optional
Apport exception-handler hook. Read-only inspection shows it imports
`apport_python_hook` when available. Receipt's startup provenance adapter refuses
**any discoverable existing customization**, including this distro default, with
`RuntimeError: Native invocation does not replace startup customization: sitecustomize`.
The tests expecting normal before/after observations therefore receive incomplete
check 7. This is the helper's documented conservative boundary, not evidence of
a production regression caught by the tests. It nevertheless prevents this
native mode from serving the default runtime, and leaves the archive gate red.

Do not delete or hide the hook, disable provenance, skip these failing behavior
tests, or claim the bootstrap mode satisfies a user's exact native-invocation
requirement. Supporting coexistence needs a separately verified design preserving
startup behavior and same-process copied-import evidence. The usage reference
now explicitly discloses distribution hooks, rather than implying only custom
project/user setups are affected. No hook or global Python configuration changed.

Four skips: three existing pinned Git-provenance comparisons (archive has no
history), and the Friday ripgrep-discovery test (image has no rg). Their other
behavioral checks execute; unavailable rg coverage is not credited as passed.
Owned archives/logs remain under ignored local runs; containers use `--rm`.

한국어: 최신 Linux 배포본 검증은 아직 실패다. 파일 증가 시점과 빈 테스트 종료
코드의 플랫폼 가정을 고쳐 실패 항목이 15→11개로 줄었지만, 남은 항목은 Ubuntu
기본 시작 훅 때문에 Receipt의 native 비교가 중단되는 문제다. 훅을 숨기거나
검사를 생략하지 않았으며 정확한 미지원 조건을 안내에 반영했다. macOS 관련
47개 검사는 통과했지만 전체 Linux 지원·모델 성능 개선으로 주장하지 않는다.
