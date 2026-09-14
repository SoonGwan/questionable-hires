# Provenance adoption 02: supported uptake, efficiency still unproven

Launch `670e708`, resources `b044a19`, unchanged HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177` exception task.
[Frozen protocol](../../HTTPX-PROVENANCE-02-PROTOCOL.md). One fresh skill-only
GPT-6 Astra medium session; no fresh baseline, timeout, account limit or retry.

Recorded input 152,292 + output 993 = **153,285 total tokens**, including cached
input once. Process time **45.817s**. Compared with the previous exposed skill
run, observed tokens decrease **31.38%**, time **43.83%**. Compared with that
run's historical baseline, tokens remain **93.27% higher**, time **5.65% lower**.
These are historical descriptive differences with unequal work, not causal or
general savings. No whole-task efficiency win against the no-skill condition.

## Original execution review

[Commands and outputs](asgi-exceptions--skill--1/commands.json): six completed
commands, all exit 0. Item_2 reads the new entry and optional guide. The model
does not create a pytest plugin/precheck or stronger probe. It searches helper
implementation and reads a small argument-handling excerpt, not its full source.
Client dispatch tracing and multiple reads remain; adoption is not zero overhead.

Item_7 uses the installed audit helper with the requested interpreter, selected
HTTPX/tests/configuration, and one mutation changing the actual ASGI constructor
default from `True` to `False`. Native copied-module provenance records distinct
implementation hashes. Correct tests: **24 pass**, exit 0. Mutant: **4 fail /
20 pass**, exit 1. `test_asgi_exc` and `test_asgi_exc_after_response` each fail on
asyncio/trio at :172/:180 with `DID NOT RAISE RuntimeError`. No output truncation
or timeout. The helper preserves selected bytes/modes across 65 files and removes
owned scratch. No setup failure/retry occurs. The final scoped coverage claim is
supported by original native output, not an author replay.

Read-only integrity review verifies all 125 original tracked files preserved and
all eight installed/frozen skill resources matching. Raw CLI usage and all six
command/output items reconcile to exported metadata/commands after path redaction;
source hashes and all seven selected source/configuration/license excerpts match.
Excerpts are not a complete runnable HTTPX distribution. Final snapshots do not
prove absence of transient edits or arbitrary side effects. No new scoring rule
or hidden deletion requirement is introduced.

Decision: keep the candidate provisionally. The intended less-instrumented path
is observed with native detection intact, but a single exposed session cannot
prove that wording caused the change. Stop repeating this case. Next evaluation
should transfer to another workflow with fresh baseline/skill conditions and
retain required unresolved-binding checks. Do not promote this into a featured
chart or advertise the 31%/44% differences as broad developer productivity gains.

한국어: 새 지침을 읽은 모델이 별도 pytest 플러그인·재시도 없이 실제 결함을
잡았다. 정상 24개 통과·결함 4개 실패와 원본 보존을 원래 실행에서 확인했다.
이전 스킬 대비 토큰 31.38%·시간 43.83% 감소했지만 과거 기본 모델보다 토큰은
여전히 93.27% 많다. 새 기준군 없는 1회 결과이며 전체 성능 개선은 미입증이다.
이 과제를 더 반복하지 않고 다른 작업의 새 비교로 이동한다. 기존 그래프는 유지한다.
