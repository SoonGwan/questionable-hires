# Hostage input-contract pilot 01 — reviewed 2026-09-21

**Candidate not adopted.** Six fresh sessions completed at launch `4fb980f`, with
original resources `6516f5e` and the isolated paragraph candidate from `563d68a`.
Two authored related tasks, n=1 per condition, GPT-6 Astra medium, serial shared
host/cache. [Frozen protocol](../../HOSTAGE-INPUT-01-PROTOCOL.md),
[inputs](../../hostage-input-cases-01.json), [all outcomes](comparison.json),
[actual schedule](schedule.json). No retries, exclusions, timeout or account limit.

## Original model outcomes and cost

| Contract | Condition | Total tokens | Seconds | Responses | Final native tests |
|---|---|---:|---:|---:|---:|
| Opaque passthrough | Baseline | 84,950 | 72.709 | 5 | 6 |
| Opaque passthrough | Original | 77,335 | 71.201 | 4 | 7 |
| Opaque passthrough | Candidate | 97,884 | 76.322 | 5 | 4 |
| Normalized value | Candidate | 79,555 | 78.264 | 4 | 6 |
| Normalized value | Original | 129,636 | 87.159 | 6 | 7 |
| Normalized value | Baseline | 83,597 | 82.658 | 5 | 7 |

All six meet the five reviewed criteria. All implement the focused `try/finally`
cleanup, retain the existing success method/assertions, test their actual argument
contract, and cover delivery errors/cancellation, pending duplicates, retry and
independent instances. Test counts are method counts, not scenario counts; candidate
opaque groups multiple settlement scenarios into subtests. No method-count advantage
is claimed. Before-fix native failures were also observed in opaque baseline,
opaque candidate and normalized original; the task did not require before evidence.

The only changed originals are `sender.py` and `test_sender.py`. Protected files
and all original modes are preserved; HEAD and retained pre-collector index match
the original, installed skills are unchanged and no scratch remains. Normalized
original additionally copies `controlled_call.py`, byte-identical to its installed
asset, as permitted local support. No other extra file is present. This is a
material difference in work, not proof that the candidate paragraph caused savings.

Summed costs: baseline **168,547 tokens / 155.367s**, original **206,971 / 158.360s**,
candidate **177,439 / 154.586s**. Candidate versus original: **−14.27% tokens /
−2.38% time**. Candidate versus baseline: **+5.28% tokens / −0.50% time**. Cache is
counted once in input; original response/cumulative/CLI counters reconcile. Wall
time is not helper latency or price. There is no broad whole-task resource win.

The aggregate hides opposite token directions versus original: opaque **+26.57%**,
normalized **−38.63%**. All conditions already discriminate the explicit contracts;
the candidate supplies no observed additional detection. One favorable normalized
pair with different support construction does not justify shipping the candidate.
Retain original production instructions; do not tune or rerun these exposed cases
to seek a favorable replacement. This is not evidence that every future use of
the candidate is worse, nor general superiority of either condition.

## Separate author replay, not original model evidence

`check_hostage_input_output.py` copies each final project, executes its unchanged
generated tests on Python3.11 and intercepts callback arguments without changing
the retained source. Original model commands used the available Python3.9 runtime.
Source hashes/modes and all native outputs are in each `author-replay.json`.

- All six healthy copies pass.
- All three opaque suites reject copied arguments through actual identity assertions.
- All three normalized suites reject missing normalization through actual value assertions.
- All three normalized suites accept equivalent reconstructed normalized strings.

These 15 author runs are not added to model token/time totals or called fresh model
results. In opaque baseline/original and normalized baseline, deliberate argument
faults also cause bounded entry-wait timeout errors after callback assertions fire.
Those additional errors are retained, not hidden; direct contract assertion failures
are independently present. No author process deadline expires. The candidate's
mutation runs have no such extra errors, but this small set does not establish
exhaustive cleanup or coverage superiority.

The author harness's normalized-string reconstruction was changed from an encoding
round-trip to `''.join(list(value))` before any normalized artifact replay, avoiding
an unnecessary encoding restriction. Earlier opaque runs do not execute that branch.
Two harness checks exercise healthy/failing/equivalent native controls and reject
unknown contracts/symlinks. No frozen model input or model attempt was changed.

## Evidence integrity and limitations

All corresponding original stored shell outputs and exits match emitted CLI
capture; no replay was used to repair original transcripts. Private complete
sessions stay local. Reviewed tool records, usage/exposure summaries, CLI records,
source hashes and final artifacts are exported, not private initial instructions.
Exact original/candidate entry body exposure occurs in initial messages and later
tool output for skill cells; baseline matches are unobserved, not global absence
proof. A publication scan caught local interpreter paths in author tracebacks;
exported paths were masked before committing, original local evidence retained.

Authored explicit contracts, related tasks, one cell per condition, fixed order,
shared host/cache and unblinded review limit interpretation. This is neither a
release approval nor achievement of the eight-skill 20–30% efficiency objective.
Featured charts remain tied to their historical resource.

한국어: 여섯 실행 모두 요구사항을 충족했고 복사·정규화 결함을 구별했다. 후보는
기존 대비 합계 토큰 14.27%가 줄었지만 원본 전달 과제에서는 26.57% 늘었고,
무스킬 대비 합계 토큰도 5.28% 늘었다. 추가 검증 능력은 관찰되지 않아 후보를
채택하지 않는다. 단회 결과를 일반화하지 않으며, 개발자 재검증 15회와 원래
모델 결과를 구분하고 모든 오류·비용·산출물을 보존한다.
