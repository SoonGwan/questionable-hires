# Current candidate: completion is not established

Mother-in-law now clarifies cancellation-resistant cleanup after an [author fault
check](INTERACTION-CLEANUP-01.md) of the retained screen-05 test. The test hangs
despite a bounded dispatch wait; a process deadline contains it. This instruction
revision has no new model measurement and adds no cross-skill helper dependency.

Latest combined snapshot: `c11103c`, [FAST-REGRESSION-05](FAST-REGRESSION-05.md).
All nine task criteria pass; 628,256 tokens / 337.371 seconds, down 8.1% / 8.8%
from screen 04 and 9.3% / 4.4% from screen 02. No rejected patches. Most skills
are unchanged, verification depth varies, and the diagnosis artifact loses its
local timeout; these are not causal or broad improvement claims. The historical
snapshot discussion below remains evidence history, not the latest gate.

Subsequent Exorcist revision `8ec7a57` has a [targeted termination check](EXORCIST-BOUNDED-01.md),
not a combined screen: the model's retained probe now terminates on missing dispatch
and cancellation stalls in author fault checks. Its single model sample costs
26.1% more tokens and 24.6% more time than screen 05's diagnosis case. This is an
explicit reliability/cost tradeoff, not completion of the efficiency objective.

An optional Exorcist foreground probe runner now factors out repeatedly generated
process-deadline plumbing. It reuses existing bounded runners when available and
is not a sandbox. Eight subprocess-backed tests cover statuses, deadlines after
closed output, inherited descendant pipes, large Unicode logs, argument handling
and CLI timeout distinctions; the full suite passes 116 tests. Author application
to the actual unbounded screen-05 probe returns normally on the original behavior
and terminates missing dispatch at the configured 0.5-second deadline (0.507 seconds,
CLI 124, child -9). No model session covers this new helper or routing yet. The
helper's local termination evidence is not evidence of token/time improvement.
Its [first model adoption check](EXORCIST-PROBE-RUNNER-01.md) now records correct
wrapper usage but full-source reading and an extra result artifact: 89,674 tokens /
52.353 seconds, 4.2% more tokens and essentially unchanged time versus the preceding
bounded-instruction sample. No helper efficiency win is established.

The subsequent Exorcist entrypoint exposes the minimal optional runner invocation
directly and makes a separate result file unnecessary. `--help` now documents
statuses, output limits and process-group effects without source inspection.
Detailed reference and inspection remain available; execution semantics are
unchanged and all eight runner checks pass. This interface revision has no model
measurement yet; fewer discovery steps are a hypothesis, not a claimed saving.

That interface's [runtime-setup transfer check](EXORCIST-INTERFACE-TRANSFER-01.md)
now records 116,325 tokens / 90.214 seconds, up 67.4% / 68.3% against the earlier
same-case sample. The diagnosis is correct, but the model reads full runner source,
wraps already bounded child experiments, and repairs an initially misplaced runtime
observation. These costs are retained; direct invocation guidance alone has not
established cheaper tool selection.

The next Exorcist revision removes the universal direct-runner suggestion and
routes to its interface only for an uncovered asynchronous wait/cancellation
path. Already bounded experiment children are explicitly excluded from redundant
wrapping. Helper behavior and diagnostic evidence requirements are unchanged.
This is a routing candidate motivated by the adverse transfer trace, not measured
efficiency recovery; no additional model run has evaluated this revision yet.

Its subsequent [conditional-route check](EXORCIST-CONDITIONAL-01.md) avoids helper
source/reference reads and redundant wrapping while preserving the setup diagnosis:
88,482 tokens / 61.371 seconds. This is lower than the latest adverse sample but
still 27.3% more tokens / 14.5% more time than the earlier setup-routing sample.
No stable efficiency recovery or new combined gate is established.

Latest combined snapshot reviewed: `d54da1d`, in [FAST-REGRESSION-04](FAST-REGRESSION-04.md). All nine task-specific criteria pass; the previous parent-directory search does not recur, but two rejected patches retain attempted-scope uncertainty. Total tokens fall 6.8% and time 8.3% versus screen 03; versus screen 02 tokens fall 1.3% while time rises 4.8%. The objective remains better developer outcomes with similar or lower token/time cost across the eight skills. Neither a short instruction file, a green synthetic task, nor a favorable individual sample establishes that objective.

| Skill | Current instruction revision | Available behavioral evidence | Important remaining gap |
| --- | --- | --- | --- |
| Necromancer | Instructions `8346bc7`, collector `fa3fab7` | [Collector review](NECROMANCER-TOOL-01.md) plus native-Git active compatibility pass in FAST-REGRESSION-03 | No repeatable collector efficiency advantage; obsolete/public-contract coverage remains limited |
| Receipt | `e00c751` | [Mode routing](RECEIPT-ROUTING-01.md): common fix skips history reference; historical comparison freezes current assertions | Two samples use fewer tokens but more aggregate time than prior samples; dirty-tree/old-interface transfer and latest full-team gate remain open |
| Landlord | `925758f` | [HTTPX follow-up](HTTPX-DESIGN-02.md) preserves contracts/findings without repeated nonexistent-path reads | Lower cost than previous skill, still 3.0% more tokens than earlier baseline; differing test depth and single samples limit conclusions |
| Mother-in-law | `8312d1f` | [Focused follow-up](MOTHER-FOCUSED-01.md): broken/protected flows distinguished, bounded waits and in-scope discovery observed | Combined cost not improved; rendered browser interactions and recovery unverified |
| Exorcist | `a060148` | [Conditional setup follow-up](EXORCIST-RUNNER-01.md): skips unused pytest setup but inspects meaningful unittest environment timing | Latest HTTPX cost rises about 20.0% tokens / 51.9% time versus preceding skill, with rejected-patch confound; broad/repeatable efficiency unproven |
| Hostage Negotiator | `4c327a9` | [Transfer](HOSTAGE-TRANSFER-01.md) and [bounded-wait follow-up](HOSTAGE-TRANSFER-02.md): preserved tests, scoped discovery and terminating duplicate-fault regression | Latest tokens lower but time higher; one authored workload does not establish efficiency or broader scope handling |
| Con Artist | Instructions `a772b0d`, helper/reference `941ea50` | Local bounded-memory checks, real HTTPX compatibility, [routing follow-up](HTTPX-ROUTING-01.md) and [conditional probe mechanics](CON-ARTIST-CONDITIONAL.md) | Conditional scheduling and directory-selection guidance lack model efficiency evidence; prior routing costs more; no broad claim |
| Friday | Helper `580ac16`, routing `4ac4ffe`; subsequent local byte-budget/temp-storage correction | [Matrix follow-up](FRIDAY-MATRIX-01.md): rollout/rollback and post-up data checks; tested optional SQLite mechanics | Both new samples cost more than baseline; follow-up uses native SQL, not helper; non-rolling plans and representative runtime context unverified |

The historical pre-helper screen [FAST-REGRESSION-02](FAST-REGRESSION-02.md) had essentially unchanged aggregate costs. [FAST-REGRESSION-03](FAST-REGRESSION-03.md) records adverse aggregate costs and a scope violation. [FAST-REGRESSION-04](FAST-REGRESSION-04.md) now covers the subsequent instruction/helper changes together, including the conditional mutation probe and SQLite matrix routes. All skill resources match their frozen snapshot. These single screens have no contemporaneous baseline. The specific Receipt missing-runtime case has not been rerun to isolate its documented-runner correction.

Receipt's later `e00c751` mode-routing revision has two targeted checks only; it is not part of the `d54da1d` combined snapshot above.

Receipt now also includes an optional frozen-test Python history comparison helper.
Seven local behavioral checks cover current dirty assertions, original preservation,
CLI observations, invalid inputs, missing history, import provenance, timeout cleanup
and bounded output. This replaces repeatedly authored snapshot plumbing when appropriate;
Its [first model check](RECEIPT-HELPER-01.md) uses the helper correctly and preserves
both original files: 86,814 tokens / 32.841 seconds, versus the previous routed
sample's 68,978 / 65.039. This mixed single-sample result is not a token-efficiency
win and is outside the combined snapshot above.

After that measurement, Receipt's historical reference was reduced from 389 to
232 whitespace-delimited words by removing entrypoint duplication, retaining
frozen assertions, comparable dependencies, actual revisions, native-runner fallback
and helper evidence limits. Its recipe no longer repeats the measured fixture's
filenames. No model efficiency measurement covers this reference revision yet.
Two additional local checks exercise package-relative imports with fixed data and
distinguish incompatible-interface errors from assertion failures; the complete
local suite passes 107 tests. These are mechanics checks, not unseen model transfer.

The compact reference subsequently received one [package/data development pair](RECEIPT-PACKAGE-01.md):
Receipt 68,515 tokens / 28.750 seconds versus baseline 80,126 / 31.064, with actual
old/current execution only in the Receipt arm. Both verify current behavior;
baseline adds other current-input checks. This favorable single pair has unequal
verification scope and does not establish a general speedup or isolate compression.
All seven original files are preserved in both arms. Local suite now passes 108 tests.

## What the evidence permits

- [Capture investigation](CAPTURE-DIAGNOSTICS.md) adds per-run evidence diagnostics and a subprocess-backed preservation test. Known missing output is already absent in the CLI stream; rejected-patch root cause remains unknown. These runner checks neither establish a skill speedup nor invalidate adverse costs.
- [Paired development checks](FAST-PAIRED-01.md) showed higher skill token/time costs before the latest compression. These adverse results remain part of the record.
- [Con Artist follow-ups](FAST-ITERATION-01.md) include a favorable latest-baseline comparison, but a less favorable earlier-baseline comparison. They are temporally separated single samples.
- [State-review checks](FAST-STATE-REVIEWS-01.md) show mixed efficiency, not a universal compression benefit.
- [HTTPX check](HTTPX-COMPRESSED-01.md) demonstrates a real coverage gap and original-file preservation, not a baseline win or complete scope compliance.
- [Tool-backed HTTPX comparison](HTTPX-TOOL-01.md) and [two further tasks](HTTPX-TOOL-TRANSFER-01.md) show lower observed wall time in all three single pairs, with a token regression on exception propagation and scope/coverage-depth caveats. They do not establish all-skill superiority.
- Local validation establishes package/fixture mechanics; it does not measure skill quality. No new superiority chart or broad performance claim is warranted.

## Resumed direction: preserve the concept, own workload selection

The user resumed the objective and explicitly asked the agent to improve performance while preserving the concept. Representative-workload selection is no longer treated as a prerequisite for progress: start with the already scoped Python audits and pinned HTTPX repository, clearly label their coverage limits, and do not imply they represent all eight skills. Keep all character names, taglines and visual identity. The first structural change is an optional tested audit helper, not another mandatory checklist or a new character.

## Workload and acceptance discipline

The current small fixtures expose correctness branches but do not establish which real development workload should drive optimization. Continuing to tune solely on their repeated outputs risks overfitting and spending more than the skills could save.

Use representative in-scope repository work before expanding task content. Keep the development set below ten tasks, freeze acceptance criteria and resource priorities before model execution, and retain successful, adverse and incomplete outcomes. Do not replace easy or unfavorable tasks solely to improve a score. Distinguish the fixed regression screen from new workload evidence.

No numerical definition of "huge improvement" has been agreed. A target must name the relevant workload and outcome/cost tradeoff; the existing request rules out selling higher token cost as improvement without justification. Until those choices and stronger evidence exist, this is an experimental candidate collection, not a completed performance-upgrade claim.
