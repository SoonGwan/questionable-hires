# Path-discovery candidate: mixed costs, not adopted

2026-09-21 KST · launch `e9a59c6` · original resources `6592959` · GPT-6 Astra medium.
[Frozen protocol](../../CON-ARTIST-DISCOVERY-01-PROTOCOL.md), [manifest](run.json),
[reviewed comparison](comparison.json).

Six scheduled sessions completed without timeouts, account limits, replacements
or exclusions. Two requests differ only in whether relevant paths are supplied:
**one authored filesystem-publication project with a disclosure control**, not
two independent projects or a held-out set. Serial fixed/reversed arm order,
shared host/cache, n=1 and differing extra work limit interpretation.

The isolated candidate changes only discovery guidance: direct known-path reads;
otherwise inventory project filenames/hidden instructions before speculative
filename synonyms. Runtime/support files and metadata remain unchanged. The
production skill is **not** updated from this candidate.

| Paths | Arm | Total tokens¹ | Seconds | Recorded responses |
|---|---|---:|---:|---:|
| Unknown | baseline | 68,234 | 83.307 | 4 |
| Unknown | original | 74,911 | 75.193 | 4 |
| Unknown | candidate | 96,793 | 103.109 | 5 |
| Known | candidate | 74,467 | 73.144 | 4 |
| Known | original | 102,660 | 113.005 | 5 |
| Known | baseline | 69,775 | 81.784 | 4 |

¹ Input including cached input once, plus output; all per-response/cumulative/CLI
counters reconcile. No dollar estimate, latency attribution or causal savings.

Candidate versus original: **unknown +29.21% tokens / +37.13% time**;
known −27.46% / −35.27%. Summed tasks −3.55% / −6.35% do **not** override the
frozen failed unknown-path gate. Candidate versus no-skill baseline across both
requests is **+24.09% tokens / +6.76% time**. All arms meet the five final task
criteria in both requests; this includes repairs, not first-attempt success.

## Reviewed actual behavior

All final audits execute the two existing success tests on correct code and an
isolated omission of `staged.replace(destination)`. Acknowledgment and pending-file
cleanup remain. Existing tests survive; the same stronger native assertion passes
correct code and fails faulty code specifically at old-versus-published full bytes.
Each uses an actual tested entrypoint, a different preexisting destination, literal
expected UTF-8 JSON with Unicode routes, final LF and documented formatting, a
fresh file read and pending-file cleanup. Same-process traces establish copied
test entrypoint and writer binding; these are not separate import-only checks.

- **Unknown baseline:** inventory, source read, then five native runs. It adds an
  original-workspace baseline before four copied comparisons. Its stronger payload
  uses version7 and an extra Unicode label; other arms use version3. A discovered
  trace module observes actual bridge/writer calls and destination bytes.
- **Unknown original:** inventory and skill read in one interaction, then another
  directory listing/source read/hidden instruction search. Four native comparisons;
  child-only PYTHONPATH loads sitecustomize tracing. No repair.
- **Unknown candidate:** hidden inventory and skill/instruction read, then source
  read. No speculative synonyms, but the first four-phase comparison's startup
  tracing does not load. The model notices the missing evidence and repeats all
  four phases with an explicit observational import in disposable test modules.
  Existing method bodies/assertions remain unchanged; the import itself is an
  instrumentation change. The second comparison verifies actual copied paths,
  caller/writer frames, call counts and cleanup. **All eight runs and repair costs
  remain included.** Missing first tracing is not blamed on CLI omission.
- **Known candidate:** combined paths/skill/source read, then another inventory
  and AGENTS search. Four native comparisons with working child-only PYTHONPATH
  tracing, no repair. The extra inventory means the candidate did not eliminate
  all repeated discovery even in its favorable request.
- **Known original:** inventory/source read followed by another inventory and
  numbered reread. Its first stronger test source has an escaping-induced
  SyntaxError in both copies. These are setup failures, not mutation detection.
  The model repairs/compiles the added test, then reruns only the two stronger
  comparisons successfully. **All six native runs, including setup errors, remain
  in cost.** A cheaper candidate here is not isolated evidence for its search rule.
- **Known baseline:** inventory/source read, listing/numbered reread, four native
  comparisons. Its discovered trace module records actual call and pending
  write/replace/unlink counts; replacement appears only in correct code.

None uses the shipped collector/audit helper. All final original project bytes,
0644 file modes, owner notes, Git HEAD and installed resources remain unchanged;
owned scratch is removed and no additional project files remain. These observations
were checked against commands and retained project/metadata, not just final claims.

## Capture and provenance

Five CLI outputs omit prefixes. Each was correlated with its matching original
stored tool result, reviewed without rerunning the model or reconstruction:

| Cell | CLI item | Original tool-record line |
|---|---|---:|
| unknown baseline | item_4 | 30 |
| unknown candidate | item_5 / item_7 | 32 / 43 |
| known candidate | item_4 | 33 |
| known baseline | item_5 | 33 |

Known candidate omits phase/command headers only; others omit earlier native
results. Remaining command outputs/exits match in order. Selected original tool
records, usage profiles and exposure observations accompany each cell. Private
full rollouts and initial instruction text are excluded; paths are redacted.
All four skill sessions have exact installed entry-body exposure in initial
injected messages, followed by a tool reread. Baseline exact bodies are unobserved,
not proof of all context absence. Pattern scanning found no configured privacy
matches; this is not a general privacy guarantee.

## Decision

Do not adopt or retune this discovery candidate on these exposed tasks. Do not
promote a favorable subtotal or rewrite featured graphs. The full objective of
better whole-task efficiency across all eight hires remains unmet. Any next
implementation must address concrete work, not add another generic inventory rule.
This screen exposes fragile custom test-source/tracing setup as repair costs;
investigate reusable support or a distinct real workflow before further model
measurement. Do not suppress required provenance or test failures to lower cost.

한국어: 6개 세션 모두 최종 감사·원본 보존 조건을 충족했지만 후보는 미채택이다.
경로 미상에서 기존 스킬 대비 토큰 +29.21%·시간 +37.13%로 사전 조건을 실패했다.
경로 제공에서는 −27.46%·−35.27%였으나 기존 스킬의 테스트 문법 오류 복구가
포함돼 탐색 규칙만의 효과가 아니다. 후보도 미상 과제에서 추적 미작동을 고치며
검증을 반복했다. 양쪽 복구 비용을 모두 보존했다. 후보 합계는 무스킬보다
토큰 +24.09%·시간 +6.76%로, 전체 성능 향상이 아니다. 같은 과제를 유리할 때까지
재실행하지 않으며 배포용 지침·대표 그래프를 바꾸지 않는다.
