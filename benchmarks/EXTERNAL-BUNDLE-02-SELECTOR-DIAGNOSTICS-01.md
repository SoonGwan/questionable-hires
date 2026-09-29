# External bundle02 — required selector diagnosis01, 2026-09-27

Parent `e795c505`; skills remain `7172b50c`. Author collection only, zero model
calls and no grading retries. Original16-cell grade01 stays unchanged.

Collect the complete required test-file sets in the existing private gold trees
for the three native exit4 cases. A native collection hook records actual item
nodeids in private JSON; no gold/test body, label or native collection list is
exported. All3 collection commands exit0. Public
[diagnostics](results/external-bundle-02-selector-diagnostics-01/summary.json)
retain counts and original collection/capture hashes.

Requests3362 has76 required labels among185 native items, with zero differences
when comparing collected identities after legacy instance-syntax normalization.
Its single rejected selector contains :: inside a bracketed parameter; pytest2.8's
native selector parsing splits on ::. The item exists but direct argument parsing
cannot select that literal safely. No application/test change is implied.

pytest5221 has172 required labels among173 native items. All11 rejected selectors
have an unclosed parameter bracket; each uniquely matches the first whitespace-
delimited token of an actual collected nodeid. pytest11143 has115 required labels
among116 items;10 labels have the same truncation, nine unique and one mapping to
multiple collected items. No required function prefix is absent in either source.
The pinned official parser stores the first whitespace-delimited name token, so
its historical reporting labels are not always literal native CLI selectors.
An ambiguous label must not silently select just one native parameter.

This diagnoses invoking reported labels as direct selectors; it does not establish
passing test behavior or permit rewriting output names to obtain scores. Preserve
original missing statuses and exact required reporting identities. A future author
probe may execute their complete test files and use unchanged official parsing,
with separate native report events to check every underlying collected item for
ambiguous labels. This includes additional tests and must remain distinct from
original selected-label grade01. Do not drop obligations, substitute cases or
claim independent model evidence from exposed author grading.

한국어: 실제 항목은 존재하지만 Requests의 매개변수 내부 ::와 pytest의 공백에서
잘린 역사적 보고 이름 때문에 직접 선택이 실패했다. 잘린 이름 하나는 여러 실제
항목을 가리키므로 임의로 하나만 고르면 안 된다. 수집 진단이며 테스트 통과나
모델 효율 증거는 아니고 원래 실패를 그대로 보존한다.
