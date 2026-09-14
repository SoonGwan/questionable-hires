# Friday acknowledged-writer screen 01 — 2026-09-14

[Protocol](FRIDAY-ACK-01-PROTOCOL.md), launch `76c251c`, resources `f15f3ae`.
[Four cells and author replay](results/friday-ack-01/). Related authored fixtures,
two cases, n=1/arm, serial Astra medium; all four executions complete.

| Case | Baseline tokens | Skill tokens | Change | Baseline seconds | Skill seconds | Change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | 86,888 | 90,287 | +3.91% | 78.005 | 63.636 | −18.42% |
| Gap | 86,202 | 94,930 | +10.13% | 68.645 | 82.585 | +20.31% |
| Sum | 173,090 | 185,217 | +7.01% | 146.650 | 146.221 | −0.29% |

Tokens count input including cache once plus output. Sum is a ratio of totals,
not a mean of case ratios. Shared host/cache, n=1 and different generated work
prevent causal claims. **Both cases cost more tokens; no efficiency win is
established.** The earlier favorable schema pair does not generalize here.

## Behavioral evidence

All four inspect supplied source and use actual application.write/read, not a
replacement SQL writer. The entrypoint commits/closes before acknowledgment and
reads open independent connections. Both controls find no local contract defect
and leave production configuration/restore evidence unknown. Both gap executions
demonstrate stale old/new reads, null after old insert and lost acknowledged new
updates after documented down, while preserving compatible new inserts and old
post-rollback behavior. No clean-case false positive was observed in these two
control attempts; this is not a general false-positive rate.

Control baseline performs 24 mixed writes / 280 mixed reads; skill performs 70
total writes (2 before up, 66 mixed, 2 after down), 2,510 mixed reads and 100
old-only checks. Skill retains 32 accounts through down versus baseline 11.
Both expand integer boundaries and reread source. Skill's nested operation/value
loops plus checking every accumulated row after every write create much more
verification work. This is not proof those checks are unnecessary or the cause
of model-token differences: native execution, source review and output differ.
The witness selection should be audited against actual branches/dependencies
before shortening it. All-row reads remain important where cross-row side
effects or an explicit contract require them.

Gap baseline executes nine mixed writes and checks the affected key; skill uses
two pre-up writes and eight mixed writes, checking every known key and adding
storage observations. Both retain project-local scripts, JSON and SQLite files.
Skill gives a useful distinction: alternating versions make either column stale,
so blindly copying either one cannot restore latest acknowledged values without
write-order evidence. This observation is not a new measured success advantage.
No helper guide or matrix is needed for these application-writer checks.

The gap baseline runs `find .. -name AGENTS.md`, exceeding the requested
project-only discovery boundary. Its empty output shows no matching instruction
file, not a permitted search. Do not count every cell as fully scope-compliant.
Skill AGENTS searches with no match exit 1; these are not SQL failures. Gap
baseline mkdir is legitimately empty. Supplied files are unchanged in all four.
The task requires a disposable project-local DB but does not explicitly require
end-of-task deletion: retained gap artifacts are disclosed, not retroactively
scored as a cleanup failure. Controls remove their temporary DBs.

## Separate verification

`replay_friday_ack_01.py` reconciles raw CLI/redacted events, terminal usage,
fixture source bytes, installed resource SHA-256/modes and before/after manifests.
All four original programs execute unchanged in copied projects with 30-second
bounds and exit 0 without stderr. Control complete stdout matches exactly. Gap
JSON observations match after excluding only generated directory names (skill
database field, baseline trailing Results path). Original SQLite version remains
compared. Complete measured project inventories, including retained binary DB
hashes, are saved and unchanged. Export omits binary DB content; its digest and
the program/results remain available for inspection and recreation.

Replay is separate author evidence and never repairs original output. No decisive
verification-output gap was observed in the reviewed programs/results. All adverse
costs remain. Historical/featured charts stay tied to their original experiments.
