# Friday representative-sequence adoption 01 — 2026-09-14

[Protocol](FRIDAY-SEQUENCE-MODEL-01-PROTOCOL.md), launch `70225a0`, resources
`b2925c9`; [both original cells and separate replay](results/friday-sequence-model-01/).
Two exposed authored cases, skill-only n=1, shared host/cache. Both completed.

| Case | Previous skill tokens | New tokens | Change | Previous seconds | New seconds | Change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | 90,287 | 73,060 | −19.08% | 63.636 | 65.347 | +2.69% |
| Gap | 94,930 | 93,445 | −1.56% | 82.585 | 72.019 | −12.79% |

Previous values are [ack screen 01](FRIDAY-ACK-01-REVIEW.md), not contemporary
randomized controls. These descriptive differences do not isolate the guidance,
prove baseline superiority or establish all-eight/general performance gains.
Input includes cached tokens once, plus output; no dollar conversion.

## What changed in actual behavior

Both read the new entry and actual project sources, and use the real application
entrypoints with committed writes and independent read connections. No helper
guide or SQL-only matrix substitutes for application behavior.

Control uses a representative sequence instead of the previous large nested
value/version product. It performs 16 acknowledged writes (2 initial, 12 mixed,
2 post-down). All current records are reread after each acknowledgment; its 127
counted value checks comprise 104 mixed and 23 old-only checks. The previous
skill had 70 writes, 2,510 mixed checks and 100 counted old-only checks (plus an
uncounted initial assertion). Counts describe different programs, not equal work.
New control retains six accounts at down instead of 32 while exercising old/new
inserts/updates, same-value updates, cross-version changes, zero/negative and
signed-64-bit boundaries. It verifies actual before/after-down rows, old writes
after down, schema/trigger removal and integrity. No control defect is invented;
production evidence remains unknown. Fewer distinct payload combinations are not
proof of identical general coverage, but the explicit local obligations remain.

Gap uses six mixed writes and two post-down writes, recording both fresh readers
for all known keys after each mixed acknowledgment. It captures stale values in
both directions, null after old insert, and loss of an acknowledged new update
after down, while showing compatible inserts and latest old-written values.
It preserves the important reconciliation warning: copying the new column would
destroy a newer old-written value. Observations record failures rather than
asserting every expected mismatch; this is evidence inspection, not a green
native suite claiming compatibility. Both identify the correct local conclusion
without certifying production readiness.

Both preserve the six supplied files and remove disposable project-local DBs.
Gap retains its script and JSON evidence; control adds no project file. Both use
project-local discovery; empty AGENTS search output/exit 1 is not a SQL failure.
Source rereads and different output/extra checks remain. No decisive output gap
was observed in reviewed verification commands.

## Reconciliation

`replay_friday_ack_01.py --profile sequence-01` selects this run and frozen revision
explicitly; the default old profile remains separate. Raw CLI/redacted events,
terminal usage, original fixture bytes, installed resource hashes/modes and
before/after manifests reconcile. The exact retained programs run in separate
project-local copies with 30-second bounds. Both exit 0 without stderr and their
**complete stdout equals the original**, without normalization. Original/copied
file inventories remain unchanged; replay never replaces measured transcripts.

The new instruction has observed representative-sequence behavior and lower
recorded tokens on these two attempts, but control time increased. Preserve this
adverse value and the earlier writer screen's unfavorable baseline comparison.
Historical/featured graphs stay unchanged. Broader/independent evidence is still
required; adding more instructions just to chase this exposed screen is not the
next justified step.
