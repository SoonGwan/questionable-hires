# urllib3 history01 — reviewed 2026-09-21

**Do not adopt the section-read candidate as an efficiency improvement.** Prior
and baseline meet5/5; candidate meets4/5 because it reads non-ancestor history.
Resource prior`92afe96`, candidate`f53cb65`, launch`6cf747f`.
[Frozen protocol](URLLIB3-HISTORY-01-PROTOCOL.md): one author-inspected new-project
task, prior→baseline→current, Astra medium, n=1, serial360s. All three complete;
no timeout, limit, retry or exclusion. Setup failures and capture limits remain
included. This is not an independent holdout or all-eight result.

| Arm | Input | Cached subset | Output | Total tokens | Seconds | Recorded responses | Criteria |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Prior | 253,720 | 219,520 | 4,086 | 257,806 | 150.375 | 8 | 5/5 |
| Baseline | 173,258 | 144,768 | 3,459 | 176,717 | 124.648 | 7 | 5/5 |
| Candidate | 242,303 | 206,976 | 4,312 | 246,615 | 157.228 | 8 | 4/5 |

Candidate versus prior: tokens−4.34%, time+4.56%; versus baseline:
tokens+39.55%, time+26.14%. Cached input is already part of input. These are
observed whole-task costs, including repair/extra work—not causal savings or
dollar estimates. Fixed order/shared cache and unequal work limit interpretation.

## Original outcomes and scope

[Prior answer](results/urllib3-history-01/prior/urllib3-retry-history--skill--1/answer.md),
[baseline answer](results/urllib3-history-01/baseline/urllib3-retry-history--baseline--1/answer.md),
[candidate answer](results/urllib3-history-01/current/urllib3-retry-history--skill--1/answer.md).
Each directory retains CLI commands, events, metadata, licensed selected source,
original tool records, response usage and exact-body exposure observations.

| Frozen obligation | Original evidence / outcome |
| --- | --- |
|15 actual outputs with local bindings and independent A/B variants | Prior`item_8`, baseline`item_7`, candidate`item_9`; all pass. AST matching in skill arms, checked exact-source replacement in baseline. |
| Separate compatibility conclusions and current test/doc contract | All reject A for bypassing method restriction and B for zero-budget header behavior. AND-contract test and parameter docs inspected. |
| Caller meaning, including zero-budget forced status | All inspect `connectionpool.py`; explain that `increment()` can raise before another request. No HTTP execution claimed. |
| Fallback introduction and helper extraction from ancestors | All identify `b6d45c4e702f66e819373c79122944204ebe7e72`, predecessor `is_forced_retry`, and `f37a48942be19c019fa9834f9796f354dd1ef2c1`; inspect relevant before/after code/tests. All distinguish later naming/extraction from introduction. |
| Preserve original state and requested scope | All158 original files match bytes/modes, HEAD and resources unchanged, no scratch. Prior/baseline pass; candidate fails ancestor-only restriction as detailed below. |

All arms record the same matrices for cases1–5:
current`[False, False, True, True, True]`, A-only`[True, False, True, True, True]`,
B-only`[False, True, True, True, True]`. No predicate calls raise after startup
repair. No replay substitutes for these original observations.

Candidate`item_2` runs `git log --oneline --all --ancestry-path HEAD..HEAD`.
Despite the empty-looking range, `--all` includes other refs; the output contains
later commits, including `66bdbf85a94f1c41b031e04a578661aea562cfe8`, verified not
an ancestor of pinned HEAD. The original stored output also retains that commit.
Correct final ancestor citations do not erase this explicitly forbidden history
inspection. [Scope/capture supplement](results/urllib3-history-01/capture-and-scope-supplement.json).

Both skill bodies are injected initially and reread; no helper/reference is used.
Baseline has no exact candidate-body match, not proof of absent provider catalogs.
Both skill versions already read selected file ranges; candidate also rereads
some caller/blame/test regions and emits a large unrelated history list. This
does not isolate an effect of the new sentence.

## Setup and preparation defects

All three first import attempts fail because upstream omits generated
`urllib3._version`. Each then supplies only version metadata in memory: prior
uses`2.2.3`, baseline/candidate use`0.0.0`. No disk/runtime dependency changes.
The predicate under review does not consult that version; these repaired calls
retain valid observed behavior, but the setup/repair costs are inseparable from
the recorded totals. Candidate's failure is in original`item_6` prefix, omitted
from the CLI suffix. Do not report a clean initial setup.

Post-run author diagnostics explain why the15 original preflight tests were green:
[startup diagnostic](results/urllib3-history-01/startup-diagnostic.json) confirms
both full-checkout and copied-package direct imports fail, while the copied native
unittest selector passes. [Instrumented trace](results/urllib3-history-01/startup-trace.json)
shows unittest retrying the test-module import: the first attempt leaves
`urllib3.util`/`urllib3.util.retry` cached even though package initialization fails;
the second imports those cached submodules and runs the actual assertion.
Requiring the root package too produces the expected import error. Thus the
preflight's behavior assertions remain genuine, but did not prove cold package
bootstrap. Replaying the unmodified preflight after the model sessions also passes;
that replay is not a new model result. Future preparation must check the public
entrypoint in a separate clean process. The task01 inputs are not repaired in place.

The frozen hash list also mistakenly includes the unused Slugify loader rather
than `preflight_urllib3_history_01.py`. Runtime imports the correct urllib3 loader;
its bytes before and after execution match launch`6cf747f`, SHA256
`281d8dfdb95fb49bc6421acacc9068d3cc17e2cb46c28bdb334e3e776f9c6271`.
This supplementary check does not retroactively fix the manifest omission.
[Scope and counter accounting](results/urllib3-history-01/scope-and-costs.json).

## Capture limitations

- Prior: stored combined output at line28 truncates5,267 characters from CLI
  `item_3` (marker1,348 tokens); the other nested output remains available. The
  retained text includes fallback/helper patches; later outputs retain parent
  evidence and accompanying tests. `item_9` CLI is only a205-character suffix of
  the14,594-character original. Keep the partial record, not a reconstructed full
  model-visible message.
- Baseline: nine shell outputs match exactly; `item_9` CLI is a41-character
  suffix of the6,641-character original.
- Candidate: four exact matches; `item_6` CLI omits1,890 original prefix
  characters, including the first failed import. `item_7` CLI is empty although
  original output retains4,677 characters. `item_2` stored output truncates13,291
  CLI characters (marker3,323 tokens); no claim the model saw that middle.

Original successful probe outputs are exact-matched in all arms. Automatic
capture reports retain unresolved entries; supplements do not overwrite them.
Private full rollouts stay local, mode0600; no private initial instructions are
exported. Evidence pattern scan has no findings, but is not exhaustive assurance.

## Decision

Withdraw the unproven section-read sentence, restore prior entrypoint wording and
both README descriptions, and stop tuning/repeating this ticket for favorable
numbers. This does not prove the sentence caused the scope violation. It means
the candidate failed its acceptance conditions, with setup/capture confounders
also disclosed. Add the demonstrated cold-import preflight rule and regression
controls; do not add a universal skill instruction for this particular package.
Featured data/images remain unchanged and the all-eight efficiency goal remains
unmet. The next useful work is reliable preparation/another substantive bottleneck,
not promoting a−4.34% subset statistic.

Local follow-up validation: the two synthetic package-bootstrap regression tests
pass on Python3.9 (0.154s) and3.11 (0.165s), including missing/valid metadata and
strict root-import controls. Skill quick validation, build13 (2.938s), standalone
archive4 (1.072s), repository links, bilingual featured sync and whitespace checks
pass after wording restoration. Necromancer resources match`92afe96` exactly.
These are local checks; no new full-suite or model run is claimed after withdrawal.

한국어: 이전·무스킬은5/5, 수정본은 조상 외 이력 조회 때문에4/5다. 수정본은
이전 대비 토큰4.34% 감소/시간4.56% 증가, 무스킬 대비 토큰39.55%/시간26.14%
증가했다. 세 실행 모두 생성 버전 모듈 누락을 복구했고 비용에 포함했다.
사전 테스트는 import 재시도의 하위 모듈 캐시 덕분에 통과했음을 재현했다.
후보 문구는 철회하고 이 준비 취약점을 회귀 검사로 남긴다. 큰 성능 향상은 아직
입증하지 못했으며 불리한 기록과 그래프의 기존 측정 기준을 보존한다.
