# Configuration audit01: native success, no efficiency promotion

Reviewed2026-09-21. Selection`e004fdf`, scheduler`c852644`, launch`106c012`,
fixed Con Artist resource`e1e1ef8`.
[Protocol](CONFIG-LAYERS-01-PROTOCOL.md), [all four cells](results/config-layers-01/README.md),
[measurements/artifact checks](results/config-layers-01/measurements.json).
All scheduled cells completed without timeout or limit stop; no retries or
replacements. These are two correlated authored requests, n=1 per arm/request,
on a shared host/cache, not independent validation or a generalization estimate.

| Request | Baseline tokens | Current tokens | Difference | Baseline seconds | Current seconds | Difference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Single fault | 67,803 | 70,958 | +4.65% | 69.089 | 70.653 | +2.26% |
| Four faults | 76,983 | 77,279 | +0.38% | 87.664 | 86.541 | −1.28% |

Tokens are original input including cache once plus output; time is process
wall time. Both original usage profiles and actual Astra/medium contexts were
collected for every cell. All have four recorded responses and three shell
commands. No dollar estimate, confidence interval or causal saving is inferred.

## Behavioral review

All four demonstrate the native checks, stronger-assertion sensitivity and
scope/preservation obligations. However, **multiple/current misreports reuse**,
so it is not an unqualified complete-task pass: the task explicitly requires
labeling reused correct observations. Final files alone were not used to
establish native correctness; functional evidence does not erase reporting errors.

- Both single arms execute four native processes: original correct4pass,
  original reversed-priority4pass, augmented correct5pass, augmented fault
  5methods/1failure. The regression expects override retries5 and observes
  environment retries4 under the fault. Existing assertions remain unchanged.
- Both multiple arms execute11 native processes. One original correct baseline
  is reused for four isolated faults. Reverse priority, truthiness and input
  aliasing survive the original four methods; accepting `None` fails the actual
  `None` versus3 assertion. Each survivor receives a distinct five-method
  strengthened suite, passing correct code and failing that fault once. Neither
  arm adds a redundant stronger check for the already-detected `None` fault.
- Multiple/baseline explicitly labels its single original correct observation as
  reused across the four comparisons. Multiple/current performs the same one
  baseline plus four faults but ends with “no observations reused.” Its11-process,
  50-method count is correct; the reuse description contradicts the recorded
  workflow and fails the request's reuse-disclosure requirement. Preserve this
  reporting defect rather than treating the final summary as authoritative.
- Added priority checks expose4 versus5. Truthiness checks cover false/zero/empty
  values in both environment and override layers. The current arm combines six
  fields into one expected mapping; baseline uses two calls/assertions. Input
  preservation checks expose mutated defaults5 versus original3 while inspecting
  all three mappings. These are equivalent scoped obligations, not identical work.
- Baseline multiple verifies copy-local source and each executing test's global
  binding in `TextTestResult.startTest`. Current multiple checks module/code
  paths and binding through its own `sitecustomize` in the native unittest
  process. Single baseline uses `unittest.main`; single current executes the
  native unittest module through `runpy`. Actual captured provenance agrees.

Both current arms read the complete skill body at original line16. Neither
reads a supporting guide or invokes the shipped helper. Both use custom native
harnesses, as do baseline arms. Therefore the author-helper9-check preflight
versus model11-check result is not a measured optimization or justification to
force one combined stronger assertion. The new returning-probe cache is unused.
Baseline full-body exposure is unobserved in the inspected records, not proof of
absence of every possible hidden context.

## Original output reconciliation

Every original tool call has a recorded output; no duplicate/unmatched call IDs.
For the three non-truncated sessions, original line30 contains the complete
native output. CLI item4 omits a leading initial correct run, so its aggregate
alone is incomplete; the original is an exact equal-exit suffix match.

Multiple/baseline original line30 has a911-token stored-output omission, while
CLI item4 retains all later phases but omits the initial correct phase. The
[capture review](results/config-layers-01/capture-review.json) joins the wholly
retained initial correct phase to the CLI suffix and verifies matching retained
head/tail text after path normalization. Truncation cuts through one workspace
path, so that exact partial path is normalized against recorded metadata before
comparison. The combined record has all11 native counts/exits, four genuine
assertion failures and final cleanup evidence. No process was replayed to fill
the gap. The original diagnostic still reports the unresolved truncated match;
this reviewed reconciliation supplements it rather than rewriting that record.

All four final source/test bytes and modes match inputs; no extra files remain.
Installed skill digests match the pinned tree and before/after manifests. Git
HEAD and before-model/pre-collector index byte/mode identities match in every
cell. In-model inventories confirm file preservation and owned cleanup. These
observations do not establish an atomic filesystem snapshot or exclude every
transient change. No outside-project command was observed.

## Decision

No accepted cost improvement: current costs more tokens on both requests and
only the multiple request is slightly faster. Do not promote the pair, change
featured charts, force helper adoption or retry it until favorable. The scoped
functional success is shared by baseline; current also has the reuse-reporting
defect above, not a quality advantage.
Another tiny explicit-mutation task is unlikely to answer the unresolved
operating-range question by itself. Further changes need a distinct observed
workflow mechanism, not another generic read-less/group-more instruction.

Capture-time `quality_review: Pending...` fields in `measurements.json` describe
the export stage; this report is the subsequent review. No frozen measurement
or native output was edited. Hosted CI remains a separate unresolved release
condition; these local model sessions do not establish hosted test success.

한국어:4회 모두 실제 결함 검증을 수행했지만 다중 스킬 세션은 정상 결과를 비교에
재사용하고도 재사용하지 않았다고 잘못 보고했다. 단일 과제는 토큰4.65%·시간2.26%
증가했고, 다중은 토큰0.38% 증가·시간1.28% 감소였다. 양쪽 모두 자체 검사 코드를
사용해 제공 도구의 실행 절감 효과는 실측되지 않았다. 잘린 저장 출력은 다른
원본 조각과 대조했으며 재실행으로 채우지 않았다. 대표 그래프나 전체 성능 향상
주장으로 채택하지 않고 불리한 결과도 보존한다.
