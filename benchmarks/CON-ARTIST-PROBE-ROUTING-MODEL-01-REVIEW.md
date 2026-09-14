# Focused native-probe routing screen 01 — 2026-09-14

Launch `bcc6713`, resources `708c7a8`; [frozen protocol](CON-ARTIST-PROBE-ROUTING-MODEL-01-PROTOCOL.md).
One scheduled session completes at **96,455 tokens / 46.178s**, four recorded
shell calls, no timeout/retry. All usage known; input includes cached input once
plus output. No author tests or edits during timing. [Export](results/con-artist-probe-routing-model-01/run.json)
preserves original captured events/commands, hashes and retained project.

## Routing adopted, required audit retained

The model reads SKILL.md, all five actual project files, the common audit guide
and the focused native-probe guide. It does **not** read the advanced guide,
implementation or context collector. The complete project-source contents are
present in captured read outputs. This establishes the intended routing for this
session, unlike the earlier [unverified-read screen](CON-ARTIST-CORE-GUIDE-MODEL-01-REVIEW.md).
Broad filename discovery still lists installed skill resources unnecessarily.

One helper invocation uses the actual receipt tests, endpoint/writer aliases and
native fixture. Both test methods' imported `accept` and that function's `_record`
binding are asserted in each check process. The stronger native test invokes the
existing binary-upload test, opens a fresh SQLite connection, selects all ordered
rows and asserts old-row preservation plus the exact new binary payload. The
fault only removes commit; acknowledgment and closing stay unchanged.

All original native test names/counts and summaries are captured: correct-existing
two pass, faulty-existing two pass, correct-probe one pass, faulty-probe one fails
with the intended missing committed row AssertionError. Four exits are 0/0/0/1;
no timeouts/truncation, copied import hashes present, all five selected originals'
bytes/modes preserved and owned scratch removed. No artifact or repair is retained.
No decisive original capture gap is observed in this screen.

## Separate replay and cost limitations

[Author replay](results/con-artist-probe-routing-model-01/author-replay.json)
reconciles raw usage/events, frozen resource bytes/modes and complete unchanged
project inventories. The actual captured JSON body is replayed unchanged using
frozen helper files in a project-local disposable copy with a 40-second outer
bound. Both original and author outputs verify native counts 2/2/1/1, exits
0/0/0/1, both binding messages, intended row failure and integrity. AST-decoded
binary literals in the fixture/probe are hex 00ff6e6577. Retained files stay intact.

The replay helper now has explicit `sqlite-01` (default) and `probe-routing-01`
profiles; the old profile was rerun locally against both historical cells and
retained its outcomes. Old published evidence was not overwritten. These author
checks do not fill the earlier SQLite baseline's missing positive-control output.

Compared with [SQLite skill 01](CON-ARTIST-SQLITE-01-REVIEW.md)'s 99,868 tokens /
49.308s, recorded costs fall **3.42% tokens / 6.35% time**. This is descriptive,
not a causal split-guide gain: exposed n=1 task, shared host/cache, different
generated checks and output. This session combines discovery/entry in one call,
omits the previous extra native TestCase.fail identity check and prints no separate
row list on success (the native assertion still executes). These differences matter.

Relative to the earlier baseline's 86,152 tokens it still uses **11.96% more**;
the earlier baseline also has an original capture gap. Do not call this all-axis
baseline superiority, an all-eight gain, or a 48.57% model improvement from the
document-byte metric. Featured/historical graphs remain unchanged. Stop this
adoption screen here; more repetitions until favorable would not isolate causality.
Further work must target demonstrated overhead or genuinely different developer
workflows rather than shrink required verification.
