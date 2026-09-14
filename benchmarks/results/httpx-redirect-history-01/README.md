# Full-history HTTPX redirect review — 2026-09-15

Launch `68569e9`; Necromancer resources `97a9b72`. The
[frozen protocol](../../HTTPX-REDIRECT-HISTORY-01-PROTOCOL.md) supplies the identical
ticket and criteria. Full HTTPX checkout at `26d48e0634e6ee9cdc0533996db289ce4b430177`,
125 files and 1,499 ancestor commits. Two fresh serial GPT-6 Astra medium sessions,
baseline then skill, one repeat, 360 seconds per arm, persisted original sessions.
Both complete; no author retry or exclusion. Earlier shallow experiments remain
unchanged. This is one authored ticket on real code, not production usage.

## Observed outcome and cost

Both reject the two independent removals, observe all nine required requests,
and establish that the guards existed before the attributed sync-API refactor.
Neither mistakes attribution for first-ever origin or claims live network framing.

| Measure | Baseline | Skill |
| --- | ---: | ---: |
| Input tokens, including cache | 245,146 | 166,172 |
| Output tokens | 3,402 | 3,331 |
| Total tokens | 248,548 | 169,503 |
| Process wall time | 127.947s | 114.741s |
| Shell commands | 9 | 7 |
| Outer tool calls | 8 | 5 |
| Failed shell commands | 1 | 1 |

Observed **31.80% fewer total tokens and 10.32% less time**, with the required
evidence present in both arms. This pair does not establish general all-eight
improvement or a causal effect of a particular instruction. **Neither invokes
the history collector or reads its guide**, so compact output and multi-range
collection have no demonstrated adoption/effect here. Do not attribute the token
difference to those changes or promote this one pair into featured charts.

## Required work and differences

Both use the actual local `Client`/`MockTransport` path, with isolated in-memory
substitutions for A-only and B-only and provenance assertions for local imports.
The successful probes each record these results:

| Variant | POST body / response | Redirect method | Body | Content-Length | Transfer-Encoding |
| --- | --- | --- | --- | --- | --- |
| Current | bytes / 302 | GET | empty | absent | absent |
| Current | iterator / 302 | GET | empty | absent | absent |
| Current | bytes / 307 | POST | payload | 7 | absent |
| A-only | bytes / 302 | GET | empty | 7 | absent |
| A-only | iterator / 302 | GET | empty | absent | chunked |
| A-only | bytes / 307 | POST | payload | 7 | absent |
| B-only | bytes / 302 | GET | payload | absent | absent |
| B-only | iterator / 302 | GET | payload | absent | absent |
| B-only | bytes / 307 | POST | payload | 7 | absent |

Both first fail while compiling extracted methods under Python 3.9 because the
original module's postponed annotation setting is missing. Both correct their
own probe using `from __future__ import annotations`; no runtime replacement or
author intervention. Baseline fails before any cases; skill first records current
and A-only's six cases before failing on B. Thus skill executes **15 case checks
including the failed attempt, baseline 9**. All costs remain, including this
redundancy. The successful attempts still cover the same nine required cases.

Baseline uses several historical line windows, including an initially unhelpful
parent window, and additional rename/underscore-history and historical encoding
checks. Skill uses an AST-based extraction of the relevant parent/refactor class
methods in one command after a large initial diff. Both demonstrate executable
earlier presence in parent `387f04732baa99ea472c6f78c905a9359b3d0e0e` and movement
to BaseClient in `ee37a762ef6378ed16681a3452f494a5640d98de`. The ticket does not
require the first-ever introducing commit. Fewer outer calls and different
historical work are observable, not proven causes of the cost difference.

## Evidence and integrity

| Evidence | Baseline | Skill |
| --- | --- | --- |
| Answer | [answer](redirect-history--baseline--1/answer.md) | [answer](redirect-history--skill--1/answer.md) |
| CLI command output | [commands](redirect-history--baseline--1/commands.json) | [commands](redirect-history--skill--1/commands.json) |
| Stored tool responses | [records](redirect-history--baseline--1/tool-records.json) | [records](redirect-history--skill--1/tool-records.json) |
| Author source/capture check | [integrity](redirect-history--baseline--1/author-integrity.json) | [integrity](redirect-history--skill--1/author-integrity.json) |

Fourteen of sixteen shell outputs/exit codes match stored model-visible responses
exactly after path normalization. Two stored responses explicitly truncate the
middle to meet tool output budgets: baseline `item_10` (CLI 8,588 characters /
stored 7,302), skill `item_3` (43,405 / 26,105). **The fuller CLI output is not
proof the model saw all that text.** Required historical evidence appears in other
targeted original reads; both successful nine-case probe outputs match exactly.
No missing/unmatched/duplicate selected call/output IDs. No author replay repairs
the observations. Full rollouts stay local; selected reviewed tool records are
exported with original source/line hashes and private paths normalized.

All 125 original files in each workspace match the pinned clean source. No extra
non-Git/non-skill files or bytecode remain; installed resource manifests match
before/after. Reviewed commands perform no source edits, network/fetching,
installation, commits or delegation. Final file identity alone does not establish
absence of transient mutations. The exports select eight source/license files,
not the full repository or executable Git history. Git authorship/commit text is
upstream evidence, not instructions. [Run manifest](run.json),
[metadata summary](summary.json), [arithmetic](comparison.json).

Retain this favorable pair beside the adverse
[invoice history result](../history-invoice-01/README.md). It is a useful
whole-task observation, not broad acceptance. Shared host/cache, n=1, different
extra work and baseline-first order limit generalization; dollar cost is not
estimated. No new skill instruction is inferred from one result, and the optional
batching feature still needs actual adoption evidence.

## 한국어

전체 HTTPX 이력의 새 과제에서 양쪽 모두 필수 요청 9개와 리팩터링 이전 동작을
확인했다. 이번 한 쌍에서는 스킬의 전체 토큰이 248,548에서 169,503으로 31.80%,
시간은 127.947초에서 114.741초로 10.32% 감소했다. 하지만 도우미는 사용하지
않았으므로 최근 출력 축소·여러 구간 수집 기능의 효과라고 할 수는 없다.
양쪽의 Python 실행 실패와 스킬의 중복 6개 관찰도 비용에 포함했다. 모델에게
보인 이력 출력 2개는 중간이 잘렸으나 다른 원본 조회에서 필수 근거를 확인했다.
단일 과제·각 1회이며 추가 작업도 달라 일반 성능으로 확대하지 않고, 기존 불리한
결과와 함께 보존한다. 기존 그래프는 변경하지 않는다.
