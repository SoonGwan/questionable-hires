# Current candidate: completion is not established

Latest combined snapshot reviewed: `9683528`, in [FAST-REGRESSION-03](FAST-REGRESSION-03.md). All nine task-specific criteria pass, but search QA violates the project boundary; total tokens rise 5.9% and elapsed time 14.3% versus the previous single screen. The objective remains better developer outcomes with similar or lower token/time cost across the eight skills. Neither a short instruction file, a green synthetic task, nor a favorable individual sample establishes that objective.

| Skill | Current instruction revision | Available behavioral evidence | Important remaining gap |
| --- | --- | --- | --- |
| Necromancer | Instructions `8346bc7`, collector `fa3fab7` | [Collector review](NECROMANCER-TOOL-01.md) plus native-Git active compatibility pass in FAST-REGRESSION-03 | No repeatable collector efficiency advantage; obsolete/public-contract coverage remains limited |
| Receipt | `4d9b380` | Boundary/existing-fix evidence plus [changed-test history check](RECEIPT-FROZEN-01.md) using frozen assertions | Dirty-tree and old-interface limits unverified; no paired cost evidence for latest change; missing-runtime runner correction not specifically retested |
| Landlord | `925758f` | [HTTPX follow-up](HTTPX-DESIGN-02.md) preserves contracts/findings without repeated nonexistent-path reads | Lower cost than previous skill, still 3.0% more tokens than earlier baseline; differing test depth and single samples limit conclusions |
| Mother-in-law | `8312d1f` | [Focused follow-up](MOTHER-FOCUSED-01.md): broken/protected flows distinguished, bounded waits and in-scope discovery observed | Combined cost not improved; rendered browser interactions and recovery unverified |
| Exorcist | `a060148` | [Conditional setup follow-up](EXORCIST-RUNNER-01.md): skips unused pytest setup but inspects meaningful unittest environment timing | Latest HTTPX cost rises about 20.0% tokens / 51.9% time versus preceding skill, with rejected-patch confound; broad/repeatable efficiency unproven |
| Hostage Negotiator | `4c327a9` | [Transfer](HOSTAGE-TRANSFER-01.md) and [bounded-wait follow-up](HOSTAGE-TRANSFER-02.md): preserved tests, scoped discovery and terminating duplicate-fault regression | Latest tokens lower but time higher; one authored workload does not establish efficiency or broader scope handling |
| Con Artist | Instructions `a772b0d`, helper `9683528`, usage reference `c8cdbbc` | Local bounded-memory checks, real HTTPX compatibility and [scoped routing follow-up](HTTPX-ROUTING-01.md) with original/resource integrity checks | Latest directory-selection guidance unmeasured; routing avoids parent/source reads but costs more; no broad efficiency claim |
| Friday | Helper `580ac16`, routing `4ac4ffe`; subsequent local byte-budget/temp-storage correction | [Matrix follow-up](FRIDAY-MATRIX-01.md): rollout/rollback and post-up data checks; tested optional SQLite mechanics | Both new samples cost more than baseline; follow-up uses native SQL, not helper; non-rolling plans and representative runtime context unverified |

The historical pre-helper screen [FAST-REGRESSION-02](FAST-REGRESSION-02.md) had essentially unchanged aggregate costs. The later [FAST-REGRESSION-03](FAST-REGRESSION-03.md) includes the streaming audit helper and records adverse aggregate costs and a scope violation. Subsequent Receipt, Landlord, Mother-in-law and Con Artist instruction/reference changes have targeted evidence only, not another current-snapshot combined screen. The specific Receipt missing-runtime case has not been rerun to isolate its documented-runner correction.

## What the evidence permits

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
