# Cookie transfer: lower recorded cost, qualified comparison

Current Con Artist records **13.93% fewer tokens / 36.91% less process time**
on one new scoped-cookie audit. Both arms detect the same fault and verify the
same domain-only control. Baseline repairs an interpreter-path assertion and
changes pytest settings; provenance and artifact work also differ. This is not
an accepted broad or equal-work performance win.

한국어 요약: 새 쿠키 감사 작업에서 토큰 13.93%, 시간 36.91% 감소를 기록했다.
양쪽 모두 같은 결함을 검출하고 정상 대조를 통과했다. 그러나 baseline의 경로
오류 수정, pytest 실행 설정 및 검증 방식 차이가 있어 일반적인 성능 향상으로
해석할 수 없다. 전체 8개 스킬 목표는 여전히 미달이며 대표 그래프는 유지한다.

## Frozen run

[Protocol](../../HTTPX-COOKIES-01-PROTOCOL.md), [manifest](run.json).
Con Artist `36e201c`, full HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`.
GPT-6 Astra medium, two fresh serial sessions, skill first, n=1 per arm,
360-second limit. Preflight 7 pass. Both complete, no retries or exclusions,
and no concurrent author regression tests during timing.

| Arm | Total tokens | Cached input | Seconds | Shell commands |
| --- | ---: | ---: | ---: | ---: |
| [baseline](cookies-scoped-clear--baseline--1/answer.md) | 143,957 | 116,736 | 89.777 | 6 |
| [skill](cookies-scoped-clear--skill--1/answer.md) | 123,906 | 96,384 | 56.641 | 4 |

Total = input including cache once + output. Ratios minus one:
−13.9285% tokens / −36.9092% time. Shared cache/host, order, one author-selected
task in an already exposed project and unequal work prevent causal attribution.
This is not a maintainer ticket, independent holdout or direct before/after test
of the latest instruction change.

## Actual outcomes and differences

Both independently omit forwarding the path in `Cookies.clear`, leaving domain
handling intact. Correct suite: 7 pass. Mutant: 1 fail / 6 pass, with the actual
`assert len(cookies) == 1` at `test_cookies.py:50` observing zero. Both domain-only
controls assert the exact surviving other-domain cookie tuple and pass on both
versions. Both additionally rerun the existing domain-only test on both versions.
Both limit the result: this fault tests same-domain over-deletion, not direct
coverage of other-domain preservation during path-scoped clearing.

Skill adopts `--full` with the test file and `Cookies.clear` selector, followed
by relevant source/fixture inspection. No separate test-body readback occurs.
The cookie test is under 200 lines, so default mode would also return its body;
this confirms instruction adoption, not the large-file route's efficiency.
It also reads the advanced audit reference despite using single-audit mode and
searches helper internals. These remain potential setup costs, not attributed
avoidable model tokens.

Skill executes four fresh-copy phases, verifies copied imports in each, and
checks public/internal class identity, method path and collected test caller
bindings inside control processes. Baseline executes six child processes from
two copies, checking package import location in separate control processes.
Core assertions agree, but provenance work differs. Baseline's first wrapper
invocation fails a literal `sys.executable` comparison before checks; it repairs
the wrapper to use the supplied interpreter explicitly. Failed call and repair
remain included in all recorded costs.

Baseline disables pytest plugin autoload and the cache provider; skill retains
the anyio plugin and cache defaults. This prevents treating the run as an
identical-runner comparison. Baseline writes and retains a report, wrapper and
copies; skill removes its helper copies. No costs are subtracted for these
differences to manufacture an efficiency result.

All 125 upstream tracked files compare byte-identically in both final snapshots.
Reviewed commands stay project-local without dependency installation or observed
external network calls. Snapshot checks alone do not prove all transient actions.
No capture invalid-JSON/empty-output/error-event/rejected-patch flags; skill
reports no phase timeout or truncated output. Installed skill resources remain
unchanged. These checks do not prove every original tool output is complete.
After timing, all 320 repository tests pass in 43.919 seconds.

## Evidence and next decision

Exports retain commands/events, answers, metadata, original artifact hashes,
source/test excerpts and HTTPX's BSD-3-Clause license. Baseline wrapper/control
and report are included; full snapshots, logs and diffs remain in ignored
`benchmarks/local-runs/httpx-cookies-01` and its full export. Environment prefixes
are redacted to `<ENV>`. Source hashes describe original artifacts, not redacted
bytes. Excerpts are not a standalone runnable checkout: replay using the pinned
full source and recorded dependencies.

Do not repeat this exposed task until its score improves. Confirmation needs
broader independent work and comparable runner/provenance requirements, retaining
failures and checking scope/quality as well as cost. The all-eight objective and
hosted release gate remain unresolved. No featured charts change.
