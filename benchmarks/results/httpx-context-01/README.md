# Context collector adopted: duplicate discovery removed, token costs higher

Con Artist uses the new context collector and does not repeat instruction-file
searches. It also uses **47.1% more total tokens / 23.9% less process time** than
the fresh baseline. Both arms produce the required correct fault/normal evidence.
The work-removal mechanism is partly observed, but the token objective is not met.

한국어 요약: 새 수집기를 실제로 사용했고 지침 파일 재검색은 사라졌다. 하지만
구현 파일 전체를 읽고 helper 소스도 추가로 확인하면서 토큰은 47.1% 늘었다.
시간은 23.9% 줄었으나 한 과제·한 번의 비교이고 검증 방식이 달라 전체 성능
향상으로 확정할 수 없다. 채택 성공과 비용 개선을 구분한다.

## Frozen comparison

[Protocol](../../HTTPX-CONTEXT-01-PROTOCOL.md), [manifest](run.json).
Full HTTPX source at `26d48e0634e6ee9cdc0533996db289ce4b430177`, Con Artist
resources at `d442b3b`. GPT-6 Astra medium; unchanged exposed query parameter
task, one repetition per arm, serial skill-first order, 360-second limit.
Preflight: 14 existing tests pass. Both sessions complete; no retries or
exclusions, no resource changes during execution. Earlier comparisons remain
intact and are not paired causal estimates of this change.

| Arm | Total tokens | Cached input | Seconds | Shell commands |
| --- | ---: | ---: | ---: | ---: |
| [baseline](queryparams-repeated-values--baseline--1/answer.md) | 120,231 | 95,616 | 63.862 | 5 |
| [skill](queryparams-repeated-values--skill--1/answer.md) | 176,916 | 140,672 | 48.596 | 5 |

Total = input (cached included once) + output. Skill/baseline minus one:
+47.1467% tokens, −23.9047% process time. Shared caches, order, n=1 and unequal
provenance/preparation work prevent broad or equivalent-work savings claims.

## Observed mechanism and remaining work

Skill first reads the entrypoint, context interface and audit interface together.
It then runs the collector once for the full requested test **and full
`httpx/_urls.py`**, not the available `file:qualified.definition` selector.
Original captured collector output is 41,124 characters. The full JSON parses;
it includes source/configuration, checked ancestor instruction paths and a
conftest index. No later AGENTS search occurs.

The session reads `clean_environ`'s actual autouse fixture body, concurrency
support and public exports/value conversion afterward. It also reads helper
lines 1–310 across two commands. These are observed preparation costs, not a
claim that all such inspection is unnecessary. No separate manual copy wrapper
is written; one audit helper call executes all four phases. Both arms issue
five shell commands overall, so discovery deduplication does not imply fewer
total calls. Baseline uses narrower implementation slicing but custom execution
orchestration and two instruction-discovery commands.

This establishes usable collector routing and reuse in one session. It does not
prove token savings. The full-file selector added substantial source context;
future changes should address evidence selection without hiding relevant imports,
fixtures or surrounding semantics. Do not rerun unchanged cases to seek a score.

## Actual outcome and scope review

Both arms append `[:1]` to the real `QueryParams.get_list` return expression in a
copy. Correct suite: 14 pass. Faulty suite: 5 fail / 9 pass at
`tests/models/test_queryparams.py:24`, actual `['123']` versus `['123', '456']`.
Both run the single-value `get_list('b') == ['789']` control on correct and faulty
code, passing in both. Neither demands a redundant stronger test or alters the
production tests. The result is existing protection, not a current-upstream bug.

Skill verifies copied implementation imports in each actual test/probe process;
its probes also assert public/internal class identity and the method's source
file inside the copy. Baseline checks the package import in separate control
processes, then uses pytest subprocesses against its copy. These are different
provenance depths. Baseline mutates one retained copy between phases; skill uses
fresh copies and removes them. No internal syntax/path repair was observed.

Both sessions stay within the permitted project. All 125 upstream tracked files
in each final snapshot compare byte-identically to the pinned source. Actual
commands and original-file checks were reviewed; snapshots alone do not prove
every transient action. No dependency install or upstream write was observed.

Both capture diagnostics have no invalid JSON lines, empty command output,
error events or rejected patches. Decisive outcomes and assertion differences
are present; helper phases report no timeout or output truncation. These checks
do not guarantee complete capture of every tool output. No author heavy tests
ran during model timing. This exposed authored task is not a maintainer ticket
or independent multi-project confirmation. Featured charts remain unchanged.

## Compact evidence and reproduction

Each cell retains command/output events, metadata, answers, original-log hashes,
original URL implementation/query parameter test excerpts and HTTPX's BSD-3-Clause
license. Full exported projects and generated diffs remain in ignored local
storage, recoverable and not deleted. Interpreter prefixes are redacted to
`<ENV>`. These excerpts are not a runnable full checkout.

Replay in a disposable full checkout at the pinned revision with the recorded
dependencies. Commands retain the actual collector selectors, mutation and normal
control; adapt interpreter paths. For new model runs use
`run_httpx.py --profile queryparams-audit`, explicit source/interpreter, a new
output path and a committed skill revision. Preserve failures and differing work;
author replay is not another model observation.
