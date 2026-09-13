# Query parameter transfer: correct evidence, discovery reuse not demonstrated

Con Artist's assertion-local entrypoint `613d2ee` reaches the required audit
conclusion and preserves scope, but still repeats instruction searches. It uses
**17.7% more total tokens / 12.8% less process time** than the fresh baseline.
The intended discovery-work reduction is not demonstrated; shorter instructions
are not an efficiency result. This single pair does not establish broad savings.

한국어 요약: 새 HTTPX 과제에서도 필요한 결함·정상 검증은 수행했지만, 스킬의
지침 검색 반복은 남았다. 토큰은 17.7% 늘고 시간은 12.8% 줄었다. baseline의
프로젝트 밖 검색 시도와 조건별 검증 차이도 기록했다. 탐색 재사용 지침의 효과나
전체 스킬 성능 향상을 입증한 결과로 해석하지 않는다.

## Frozen evidence

[Protocol and author preflight](../../HTTPX-QUERYPARAMS-01-PROTOCOL.md),
[manifest](run.json). Full HTTPX commit
`26d48e0634e6ee9cdc0533996db289ce4b430177`, frozen resources from `b617800`
(entrypoint last changed at `613d2ee`, helper unchanged). GPT-6 Astra medium,
one author-selected new task, one repetition per arm, serial skill-first order,
360-second deadline. Both complete; no cell retries/exclusions. Preflight suite
14 pass; the author's independent deliberate fault fails the intended assertion,
not test support. Its recipe and verdict are excluded from evaluated projects.

| Arm | Total tokens | Cached input | Seconds | Shell commands |
| --- | ---: | ---: | ---: | ---: |
| [baseline](queryparams-repeated-values--baseline--1/answer.md) | 120,262 | 95,872 | 62.237 | 4 |
| [skill](queryparams-repeated-values--skill--1/answer.md) | 141,545 | 121,344 | 54.257 | 5 |

Total = input (cached included once) + output. Skill/baseline minus one:
+17.6972% tokens, −12.8220% process time. Shared caches, order, n=1 and differing
orchestration prevent causal or equivalent-work conclusions. This is not a
maintainer-submitted task or independently held-out multi-project confirmation.

## Reviewed behavior

Both append `[:1]` to the actual `QueryParams.get_list` return expression in an
isolated copy. Correct suite: 14 pass. Faulty suite: 5 fail / 9 pass, all at
`tests/models/test_queryparams.py:24`, actual `['123']`, expected `['123', '456']`.
Both verify `get_list('b') == ['789']` on correct and faulty implementations.
The exact ordered-list assertion protects the requested behavior; no second
mutation or new production test is demanded. No upstream defect is claimed.

Skill executes one helper call with four fresh-copy phases and no repairs. Its
normal probes also verify public/internal class identity and the method's source
filename in those processes. Listed copied imports execute in the actual test
processes. Baseline builds its own orchestration, runs four processes against
one copy mutated between correct/faulty runs, and checks the package import in
the normal-control processes. These are not identical provenance checks.

Skill searches for AGENTS in three commands: initial visible-file discovery,
hidden-file discovery after skill loading, then another hidden-file search after
source reading. The last repeats completed discovery. It reads the requested
test, configuration, conftest, a 126-line implementation region, package exports
and helper source matches. Thus the new instruction does not establish removal
of redundant discovery or source inspection. Baseline also repeats searches.

Baseline's third command searches `..` despite the explicit project-only
constraint. No paths are returned, but the out-of-scope attempt is a scope
exception, not erased by a correct conclusion. Skill's discovery remains scoped.
All 125 upstream tracked files in both final snapshots compare byte-identically
to the pinned source. Commands and model integrity checks were reviewed; final
snapshots alone cannot establish every transient action.

Both metadata capture diagnostics have no malformed lines, empty command-output,
error-event or rejected-patch flags. Decisive normal/fault/control output is
present. Clear diagnostics are not a full-capture guarantee. No author heavy
regression ran concurrently with the model timing window. Local runner selection
tests pass (11 tests); this is fixture/schedule evidence, not model efficiency.
After model execution, all 281 repository tests pass in 49.784 seconds. Skill
schema, catalog/links, featured-language sync and export pattern checks pass.

## Packaging and next decision

This compact export includes metadata, command/output events, answers, source-log
hashes, original URL implementation and query parameter test excerpts, and
HTTPX's BSD-3-Clause license. Full export copies/diffs remain in ignored local
storage, recoverable and not deleted. The baseline artifact-directory answer
link points to its command log for this partial export. Interpreter prefixes
are redacted to `<ENV>`; no observations or costs are removed.

Replay in a disposable full checkout at the pinned revision, recreating recorded
dependencies and commands with local interpreter paths. Excerpts alone are not
a runnable package. New model runs use `run_httpx.py --profile queryparams-audit`
and an explicit committed skill revision and new output path.

Keep this result and the adverse decoder results intact. Do not rerun this
unchanged task to seek a score. Further efficiency work needs an observable
reduction in discovery/preparation work, not more instructions to avoid work or
another instruction-word-count claim. Featured charts remain unchanged.
