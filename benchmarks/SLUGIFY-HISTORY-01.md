# Slugify history01 — reviewed 2026-09-21

**Both arms meet5/5; current costs more.** One author-inspected development
request, one session per arm, baseline then current, Astra medium, serial360s
limit. Resource `92afe96`, launch `27558d1`; [frozen protocol](SLUGIFY-HISTORY-01-PROTOCOL.md).
Both attempts completed; no timeout, account limit, retry or exclusion. This is
a new history task on the already-used Slugify project, not a blind holdout.

| Arm | Input (cache included) | Cached subset | Output | Total tokens | Seconds | Recorded responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 119,406 | 101,504 | 1,894 | 121,300 | 72.342 | 6 |
| Current | 160,644 | 117,888 | 2,291 | 162,935 | 82.449 | 6 |

Current uses **34.32% more total tokens and13.97% more elapsed time**. Shared
host/cache, fixed order and n=1 preclude causal/general conclusions. Do not
promote this pair or alter featured charts. No helper was used in either arm.

## Original evidence and outcomes

[Baseline answer](results/slugify-history-01/baseline/slugify-replacement-history--baseline--1/answer.md),
[current answer](results/slugify-history-01/current/slugify-replacement-history--skill--1/answer.md),
[manifest](results/slugify-history-01/run.json), and
[scope/counter/capture checks](results/slugify-history-01/scope-and-costs.json).
Each arm's directory includes CLI events, commands, selected MIT-licensed source,
metadata, original tool records, exposure and response-level usage. Full private
rollouts remain local with mode0600; private initial instructions are not exported.

| Frozen criterion | Baseline evidence | Current evidence |
| --- | --- | --- |
| Nine real outputs; independent specified removals; local import binding | `item_4`: module path/decoder, exact unique source replacements, all nine outputs | `item_4`: module path/decoder, two structural matches and one independent deletion per variant, all nine outputs |
| Separate compatibility decisions and intervening operations | Final answer explains lost original symbols and lowercase-enabled match | Final answer explains both counterexamples and unchanged default control |
| Both introducing ancestor commits, parent/child evidence | `item_3`, `item_4`, `item_6`: patches, parents, ancestry checks, old/current source | `item_3`, `item_5`, `item_7`: blame, patches, ancestry checks, all four parent/child function reads |
| Accompanying tests/docs; no invented historical intent | Early README/tests and late changelog inspected; late rationale explicitly limited | Same evidence; distinguishes the current FOO effect from historical rationale |
| Preserve scope and clean up |19 original files' bytes/modes and HEAD unchanged; no scratch or extras | Same19 files and HEAD unchanged; all installed resources unchanged; no scratch or extras |

Both observed, without exceptions:

| Variant | Symbol replacements | FOO with foo→bar | Plain Text |
| --- | --- | --- | --- |
| Current source | `10-or-20-percent` | `bar` | `plain-text` |
| Early removed only | `10-20` | `bar` | `plain-text` |
| Late removed only | `10-or-20-percent` | `foo` | `plain-text` |

Both identify `646761e5b4c73b9be7285c60eab4e10c30fe32f4` (early) and its child
`8aea5c49b960b66e5c81bf20f17ec23e41c8d157` (late). Both additionally inspect the
late commit's changelog example `['-', '_']`, beyond the author's initial selected
preflight patch paths. They correctly treat it as consistent with generated-dash
replacement, not proof of the FOO rationale. No historical module was executed.

## Failures, exposure and capture limits

Both mistakenly run `git log --all=false` (exit128) and recover with valid commands.
The costs remain included. Current's `item_3` also exits1 after an instruction-file
search with no matches; blame/log output is retained. Neither error is behavioral
detection. Baseline uses checked exact-text replacement; current uses a valid AST
substitution preserving future imports. Neither has a probe setup failure.

Current receives the exact skill body in initial context and rereads it in
`item_1`; it reads no supporting guide or helper. Baseline has no exact-body
match in recorded context/output. That is unobserved exposure, not proof of
absence of every catalog/provider instruction.

Baseline's five shell outputs match original stored output exactly. Five of
current's six match exactly. Current `item_2` reads the full module, tests and
README; its stored tool response has a `…473 tokens truncated…` middle marker.
CLI retains39,740 output characters, versus37,968 in the parsed stored response.
The prefix/suffix and exit128 match;1,794 characters of Unicode truncation,
separator and order test text are omitted from the stored response. Do not
claim the model saw that middle. The relevant nine observations, introduction
patches and final historical function read are in other exact-matched outputs.
The automatic capture report conservatively marks this record unresolved; the
separate supplement documents the manual reconciliation without rewriting it.
No author behavioral replay is credited.

## Cost diagnosis and next action

Both have six recorded responses. Exact accounting attributes the41,635-token
delta to first-input term4,284, later-input term36,954 and output397. These are
arithmetic terms, not causal savings; first input includes all initial context.
Current's whole-test/README read and repeated historical source are observable
extra context. Its AST strategy is correct, and this pair does not establish
that AST itself caused the regression. Do not remove correctness safeguards
merely because baseline used another strategy.

Next, clarify the entrypoint's ambiguous “read known ... files together” wording:
large contract/test documents should be located by relevant section, with
enclosing logic and unresolved dependencies preserved. This is a proposed narrow
instruction correction, not a demonstrated speedup. Evaluate any correction
separately; no favorable rerun of this unchanged pair. A later skill edit does
not change which resource these numbers measure.

한국어: 양쪽 모두5개 기준을 충족했지만 스킬 사용 시 토큰34.32%, 시간13.97%가
증가했다. 두 실행의 잘못된 Git 옵션과 복구도 비용에 포함했다. 전체 테스트·문서
읽기에서 기록 일부가 생략됐고, 실제 동작9개와 도입 이력은 별도 원본 출력으로
확인했다. 불리한 결과를 보존하고 큰 파일의 관련 부분을 먼저 찾도록 안내를
좁히되, 아직 그 수정의 성능 향상을 주장하지 않는다.
