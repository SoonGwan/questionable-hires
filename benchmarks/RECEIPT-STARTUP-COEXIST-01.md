# Receipt native invocation with conventional startup hooks

2026-09-15. Runtime change `79a3d2e`; test-precedence correction `7a59de8`.
Addresses the actual Ubuntu default-hook refusal in the
[preceding archive gate](LINUX-ARCHIVE-619-01.md), not a model efficiency result.

## Behavior

The temporary native startup adapter removes only its own lookup path/identity,
imports the real system/user `sitecustomize` and enabled `usercustomize` in order,
then checks that requested imports resolve in the comparison copy. Real hook
module identities are retained. The child environment carries copy lookup but
not the adapter. Native argv remains `python -B -m unittest ...`.

Python documents [site then enabled user customization](https://docs.python.org/3.12/library/site.html#sitecustomize).
The adapter follows this order and uses normal imports; the subsequent startup
import reuses the cached user module. When no real site module exists, the adapter
identity remains only to let the in-progress outer Python import finish.
Hook exceptions/early exits deliberately yield incomplete check 7, rather than
continuing after startup warnings. This is not a claim of transparent equivalence
for arbitrary startup rewrites, stack inspection or import machinery replacement.
Project-local hooks and disabled site initialization remain unsupported. User-site
disabling is preserved; no hook or global Python settings are modified.

## Native controls

Four added tests exercise real child processes:

- Both configured hooks run once and in order, with actual module identities and
  effects visible before checked imports. The same original regression fails on
  before code and passes on after code. A child also receives real hooks once,
  without inheriting the Receipt adapter. Original tree contents are unchanged.
- A hook's SystemExit(0), missing dependency or RuntimeError stops comparison with
  diagnostic evidence and no next comparison; no successful-ready marker.
- A hook providing an external `rule` module is still rejected by copied-import
  verification, not accepted merely because startup succeeded.
- Disabled user-site settings prevent either configured user-site hook running.

Replaying the initial four-control version against only the previous
`f985200` startup constant yields five assertion failure entries and no test
errors: the old adapter refuses hooks before the intended checks. The later child
assertions were not part of that author replay; it is not a model run or historical
full-suite result. All four current controls and thirteen existing native tests
pass on macOS/Python 3.9.6.

## Full-platform verification and retained failure

| Source / environment | Discovery | Outcome | Seconds |
| --- | ---: | --- | ---: |
| `79a3d2e`, macOS Python 3.9.6 | 623 | All pass | 99.093 |
| `79a3d2e`, Linux archive Python 3.12.3 | 623 | Five failure entries, four skips | 38.701 |
| `7a59de8`, Linux archive Python 3.12.3 | 623 | 619 pass, four skips | 36.270 |

Full logs: [macOS](results/receipt-startup-coexist-01/macos-79a3d2e.txt),
[initial Linux](results/receipt-startup-coexist-01/linux-79a3d2e.txt),
[corrected Linux](results/receipt-startup-coexist-01/linux-7a59de8.txt).
macOS and the first Linux run overlapped; timings are not speed comparisons.

The first Linux run passes the formerly blocked ordinary comparisons but exposes
a test-fixture assumption: Ubuntu's stdlib `sitecustomize` precedes a same-named
user-site fixture. The real runtime correctly chooses the distro module. Fix the
fixture's ordinary lookup using a test-owned `.pth` file (keeping the first
PYTHONPATH entry first), and first verify which hooks a direct unwrapped Python
actually executes. The configured-user-hook error test now uses `usercustomize`.
No runtime algorithm, distro hook, host setting or production lookup order changed
in this correction, and no failing behavior check was skipped. Seventeen targeted
macOS checks pass after it; the full macOS count remains tied to `79a3d2e`.

Linux: arm64, Node v24.20.0, existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Each unmodified committed archive excludes Git/ignored local-run state, is mounted
read-only then copied into disposable `/work`, and runs with networking disabled.
Existing PyYAML 6.0.3 pure-Python mount only; no downloads or code overlays.
Catalog/localization validation passes. Four skips remain explicit: three pinned
Git-provenance checks and one unavailable-ripgrep discovery check. Containers use
`--rm`; owned host archives remain in ignored local runs.

This establishes local compatibility with this conventional startup environment,
not hosted CI, a fresh installation, arbitrary hooks or improved model token/time
performance. Featured charts are unchanged; the all-eight efficiency goal remains
unmet. Previous failed archives retain their original evidence and identities.

한국어: Ubuntu 기본 시작 훅을 보존하면서 Receipt의 native before/after 비교가
동작하도록 수정했다. macOS 전체 623개 통과, 최종 Linux 배포본 619개 통과·4개
명시적 생략을 확인했다. 첫 Linux 재검사의 테스트 경로 가정 실패도 보존했다.
훅 순서·단일 실행·하위 프로세스·오류·외부 모듈 차단을 실제로 검증했지만, 모든
시작 훅이나 원격 설치·호스팅 CI·모델 성능 개선을 입증한 것은 아니다.
