# Recorded skill re-exposure — 2026-09-21

Post-run analysis, not a new model experiment or performance improvement.
Earlier six-session [context audit](CONTEXT-EXPOSURE-01.md) already established
initial injection. This analysis extends coverage to screen03's complete16 cells
and the three packaging design sessions without exporting private initial text.

Reproduce:

```sh
python3 -B benchmarks/analyze_skill_reloads.py benchmarks/results/all-eight-current-03
python3 -B benchmarks/analyze_skill_reloads.py benchmarks/results/packaging-design-01
```

The analyzer checks target resource hash against measured metadata, validates
exposure ordering, retains source artifact hashes, and distinguishes initial
injection from tool-only first exposure. Missing audits fail instead of becoming
zero exposure. Exact-content absence is not proof that nothing was read.

| Original cohort | Initial target body exposed | Later full-body tool output |
| --- | ---: | ---: |
| Screen03 skill |8/8|7/8|
| Screen03 baseline |0/8|0/8|
| Packaging candidate/prior |2/2|2/2|
| Packaging baseline |0/1|0/1|

Screen03 Landlord is the exception with initial exposure only. The other seven
roles have both initial injection and tool-output re-exposure. All screen03 skill
pairs nevertheless use more tokens, including Landlord. Thus duplicate full-body
output is neither necessary nor sufficient to explain the full input-cost gap.
Packaging both skill arms also reread their entries despite initial injection.

[Official skills guidance](https://learn.chatgpt.com/docs/build-skills) describes
loading full instructions once a skill is selected, with explicit `$skill` and
implicit selection supported. It does not quantify reread costs or establish
that this benchmark's observed calls are unnecessary. The runner explicitly
requests the named skill and supplies its path; that is part of the measured
workflow, not grounds to erase its cost retrospectively.

Do not subtract skill-body bytes from tokens, subtract whole combined calls,
disable required instruction reading, or rewrite historical charts. Tool calls
often also read project evidence. Host requirements, provenance/trust questions
and resource changes may justify a file read. A changed invocation or instruction
would need a separate frozen comparison, keeping the current protocol as a
control; a harness-only difference would not establish a better shipped skill.

Three analyzer tests pass: initial versus first tool exposure, invalid resource/
ordering rejection and all16 original screen cells. No private text is emitted.
The next optimization still needs actual workflow evidence, not a generic
"never reread" rule. Production skills and frozen model results are unchanged.
