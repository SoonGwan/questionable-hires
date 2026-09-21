# Ancestry scope 01 — reviewed 2026-09-21

Launch `6baa5b7`; prior resources `31a68d5`, current `99301e9`.
[Frozen protocol](ANCESTRY-SCOPE-01-PROTOCOL.md) and
[all six attempts](results/ancestry-scope-01/README.md).
Two requests on one authored four-file project, one attempt per condition;
not independent projects, causal confirmation or generalization evidence.

## Outcome: no efficiency promotion

All three arms meet5/5 history criteria and4/4 current-only criteria. The explicit
base is used in current's history query, but prior and baseline also remain in
scope. No arm queries history in the current-only request. This therefore does
not demonstrate a scope-accuracy advantage over the controls.

| Request | Arm | Total tokens | Process seconds | Recorded responses | Criteria |
| --- | --- | ---: | ---: | ---: | ---: |
| History | Prior | 69,253 | 56.323 | 4 | 5/5 |
| History | Baseline | 66,569 | 51.003 | 4 | 5/5 |
| History | Current | 87,303 | 63.982 | 5 | 5/5 |
| Current-only | Prior | 67,163 | 53.702 | 4 | 4/4 |
| Current-only | Baseline | 64,411 | 46.061 | 4 | 4/4 |
| Current-only | Current | 67,043 | 50.576 | 4 | 4/4 |

Total tokens are input plus output, with cached input counted once. Original
response usage reconciles all terminal totals; cached usage is not an additional
cost. Wall time includes the full model process, not just test runtime.

Current versus prior: history **+26.06% tokens/+13.60% time**; current-only
**−0.18%/−5.82%**. Versus no-skill: history **+31.15%/+25.45%**; current-only
**+4.09%/+9.80%**. The frozen efficiency gate fails. All6 complete, no timeout,
account-limit interruption, retry or excluded scheduled attempt. Shared host/cache,
serial order and n=1 preclude causal/latency generalization.

Retain the narrow command-correctness guidance, not an efficiency claim: both
tasks' behavioral conditions hold and local Git semantics remain correct. The
experiment does not prove the added sentence caused the extra work, nor does a
passing scope control establish improved accuracy. Do not rerun this exposed
fixture for a better number or add another generic read-less rule. The all-eight
objective remains unmet; featured charts remain tied to their original evidence.

## Criteria evidence

Every arm imports local `catalog` and exercises the real `Catalog.lookup` with an
in-memory key substitution restored afterward. Shared current values are east:17,
west:17,east:17 with two fetches; proposed values are east:17 three times with
only the east fetch. Both single-tenant variants return east:17,east:18 with two
fetches. Existing tests run in both variants: normal2pass; proposed shared test
fails with actual east:17 versus west:17, single-tenant passes. This is not an
import failure, simulated consumer, or an inference from an exit code alone.

All final decisions explain the actual lookup consumer, documented tenant-local
ID/shared-instance contract and insufficiency of the single-tenant control.
History arms inspect parent/child implementation and changed tests/docs, citing
`a79c6a095450012ee6ff27ca345067b4c0df13b0` rather than merge
`1a7537a164647952831f79571aceae76529a9026`. Parent
`c6a8c060152df848f39a2c3be0185b1678684652` has the item-only key. Queries target
pinned HEAD/known ancestors; no `--all`, other-ref query or future commit read
appears. Current-only answers do not invent historical origins.

History evidence is in prior item2/item3, baseline item1/item2, current item2/item3;
native observations are prior item3, baseline item3, current item4. Current-only
native observations are prior item3, baseline item3, current item4.

All four original file bytes/modes, HEAD and installed skill resources are
unchanged; no extra top-level scratch remains. [Author integrity inspection](results/ancestry-scope-01/integrity.json)
is separate from the actual model probes and does not replace them. Current-only
skill arms hash Git files as part of preservation inventories. That is not scored
as historical investigation: they do not interpret/query commits or other refs
to support the review. HEAD/status/diff preservation checks are permitted by the
task. No application or resource write is observed.

## Extra work, exposure and capture limits

Current history takes four shell commands/five responses versus three/four for
both controls. It splits historical review and behavioral execution into separate
responses, repeats a broad text search after reading the four-file project, and
asks for a parent test file whose absence is already visible in the addition
patch. The resulting Git fatal message is retained in cost; later commands and
native assertions succeed. No savings attribution follows from these observations.

All four skill sessions read the installed entrypoint. Exact-body exposure tools
detect it in original tool output, not in structured initial skill messages in
these runs. This does not prove the complete initial context was otherwise equal.
No exact current body is detected in baseline sessions. Neither guide nor optional
helper is used; do not attribute this result to collector efficiency.

The original prior-history item3 contains4,691 output characters; the CLI artifact
retains only its2,149-character suffix, omitting the2,542-character history prefix.
The matching original stored output includes the full parent/child diff and
implementations and is retained in redacted tool records. All other18 shell
outputs match their originals exactly; no unresolved shell-output match remains.
These counts concern shell output matching, not proof of every runtime event.
Full private session messages are local-only; public evidence contains redacted
tool records, usage profiles, exposure metadata, task files and CLI records.
The evidence pattern scan finds no flagged paths/credentials; that is not a
universal privacy guarantee. No model command was replayed to fill an evidence gap.

한국어: 6개 실행 모두 정확한 동작·범위 조건을 충족했다. 다만 이력 과제에서
현재 버전은 이전 버전보다 토큰26.06%·시간13.60% 증가했고, 무스킬 대비로는
두 과제 모두 비용이 증가했다. 명령 안내는 정확성 보완으로만 유지하며 성능
개선으로 홍보하지 않는다. 원본 출력 누락1건은 실제 저장 기록과 대조해 보존했고
불리한 결과를 제외하거나 재실행하지 않았다.
