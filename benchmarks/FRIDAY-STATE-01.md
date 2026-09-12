# Friday changed-state transfer: correct decisions, still higher cost

[Frozen protocol](FRIDAY-STATE-PROTOCOL.md), source `05b6b03`, Friday `4362342`,
canonical-workspace runner `fd8d578`. Actual order: compatible skill, gap skill,
gap baseline, compatible baseline. Four fresh Astra medium sessions, one per
case/arm, serial, seed 20260911, 240 seconds. All completed without retries,
timeouts or capture flags. Raw captures: `benchmarks/local-runs/friday-state-01`.

| Case | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Truncating old reader | 65,973 / 53.933 | 70,314 / 56.254 |
| Compatible old reader | 65,535 / 47.740 | 70,715 / 53.916 |
| Sum | 131,508 / 101.673 | 141,029 / 110.170 |

Skill costs +7.2% total tokens and +8.4% elapsed time. Total input includes cache;
output is added once. No stable or causal estimate from two related tasks, one
sample each and shared host/cache. Neither a performance win nor broad acceptance.

All arms execute actual old/new functions with separate SQLite connections,
observe original whole data and recheck after committed fractional writes. Gap
arms correctly locate the first fractional commit as the compatibility break,
demonstrate old readers returning 10 from retained 10.5 after rollback, and explain
that delaying fractional writes solves coexistence but requires a fraction-capable
rollback artifact as well. The compatible arms correctly find no local blocker.
All distinguish application/data evidence from unknown staging operation.

Both skill runs use temporary on-disk databases and reopen old connections for
rollback. Baselines use shared-memory databases; gap baseline also opens a fresh
old connection, compatible baseline stops invoking the candidate but retains its
old reader connection. Thus execution depth/storage is not identical. No optional
SQL helper/reference is opened; no history lookup is needed or performed.

All four also enumerate the complete permitted numeric domain. Gap arms each
check 2,001 candidate half-step writes and 1,001 old whole writes, besides phase
witnesses. Compatible baseline reports 10,014 read assertions; compatible skill
reports 10,013 with fresh rollback readers for each candidate value. The finite
domain in the author fixture invites enumeration in both arms; it is not evidence
that the skill uniquely caused this work. A next candidate can target selection
by actual conversion branches and representation boundaries, preserving changed-
state checks rather than equating every numeric value with a new failure mode.

Original commands/outputs/answers and diffs were inspected. Twenty original file
instances are unchanged; all diffs empty. Eight installed resource instances match
frozen Git bytes and remain unchanged before/after. No model patch is attempted,
so zero rejections says nothing about whether canonical paths fixed patch behavior.
Compatible skill searches `..` for AGENTS.md despite the project-only restriction:
an observed scope violation even with no external content returned. Remaining
captured commands are project-scoped. Do not convert final preservation into a
claim that all attempted actions respected scope. No author replay is credited as
model evidence. State-change detection works here; efficiency remains unmet.
