# Output recurrence is not the demonstrated bundle bottleneck

Read-only audit of existing paired-02 original logs (nine tasks, eight skills),
plus two recent Landlord pairs. No new model sessions or edited skill criteria.
`inspect_output_reuse.py` counts completed command outputs once, preserving exact
line text. It rejects ambiguous completed IDs and malformed capture, ignores
started events, and counts only recurrence from earlier commands, not repetition
inside one output. CLI reports counts/IDs without raw command or output contents.

Paired 02 totals: baseline 35 commands / 13,261 output characters; skill 43 commands
/ 48,473 characters. With minimum exact-line lengths 20, 40 and 80, recurring
characters are respectively baseline 364/321/0 and skill 201/179/0. These thresholds
are a sensitivity check, not a tuned waste score. Short boilerplate may recur;
line-number prefixes, context changes and formatting hide semantic re-reading.
Zero exact recurrence does not mean no repeat work.

Separately compare each installed resource's stripped UTF-8 text against completed
command output, after verifying its bytes against the original metadata SHA-256.
Full resource matches total 29,411 characters in skill outputs: Receipt 1,304;
Necromancer 3,600; Hostage 2,371; Con Artist 3,266; Friday 5,566; Exorcist 9,272;
Mother-in-law 2,016 in each of two cases. Landlord has no exact full-resource match
under this method; do not interpret that as proof it did not load its instructions.
Matches include first-use instructions, optional references and helper source, not
merely repetition. This is text composition, not causal attribution of token costs.

Recent Landlord auth outputs contain 55,421 baseline / 63,052 skill characters;
at minimum length 80, baseline recurrence is 0 and skill 424 (five lines in the
known repeated test region). The check-scope pair contains 5,382 / 8,872 output
characters with zero exact long-line recurrence, despite both rereading files with
line numbers. Both pairs therefore illustrate why this heuristic needs original
command inspection rather than automatic wasted-read scoring.

Reproduce recurrence inspection by passing original JSONL paths to:

```sh
python3 -B benchmarks/inspect_output_reuse.py --minimum-length 80 PATH_TO_ORIGINAL_JSONL
```

Historical capture gaps, unknown rejected patch targets and unequal verification
remain as documented in the original reports. No missing output is reconstructed.
Characters are not tokens; context replay, model work and time are not allocated
per command by these logs. The audit does not imply deleting all matched resources
would retain behavior or save the same amount of session cost.

Action: do not add a universal no-reread rule. Inspect first-use information and
conditional resource routing per skill, preserving decision-changing contracts and
trust/adaptation inspection. Existing Exorcist routing attempts already show mixed
adoption, so another blanket efficiency sentence is not a demonstrated mechanism.
The whole-bundle performance objective remains unmet.
