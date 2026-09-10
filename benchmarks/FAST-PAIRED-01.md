# Three-case paired development check

Frozen skills from `1c16bc8`, run revision `88ca967`, Astra medium, serial, one sample per arm/task. Cases and criteria were unchanged. The preselected seed happened to schedule all three skill cells before baseline cells; temporal/cache effects are not controlled by that order. Local raw evidence: `local-runs/fast-paired-01`. All six processes completed without timeout, with no reruns or exclusions.

| Task | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| boundary-fix | 79,799 | 101,916 | 25.535 | 39.411 |
| search-diagnosis | 63,993 | 84,379 | 42.117 | 44.103 |
| persistence-test | 80,188 | 86,228 | 44.416 | 44.919 |

Tokens are input plus output, cached input already included. Skill token overhead was respectively 27.7%, 31.9%, and 7.5%; wall time was higher in each sample. These observations do not establish stable effect sizes.

Answers, commands and diffs were inspected. Both boundary runs used the same new age-18 assertion before/after and preserved 17/19 behavior. Both diagnostic runs exercised real search/transport code with cache-free stubs and demonstrated stale completion. The skill explicitly explained why no-cache cannot solve ordering and limited production claims; baseline demonstrated the mechanism but omitted that explicit safeguard explanation and production uncertainty in its answer. Both audits showed the original test surviving missing append and the stronger contents check passing correct code/failing the mutant; the skill explicitly verified copied imports. Both audits left original source/tests unchanged.

There is no demonstrated across-the-board efficiency win. In particular, baseline already delivered Receipt's core regression behavior. Six shell calls in that skill sample versus five baseline calls include an additional skill read; repeated file discovery also remains. This does not prove any single instruction caused the entire difference.

Next candidate: compress Receipt's duplicated workflow and delivery instructions, explicitly reuse applicable before evidence, retain unchanged-assertion verification, relevant project checks, identifiable exit status, isolation, user scope and honest limits. Remove the unproven generic discovery sentence from this skill. This is a candidate change, not a measured improvement. Do not rerun unchanged candidates until a favorable number appears, or weaken criteria to erase the adverse result.

## Compressed Receipt follow-up

Revision `d794b67`, one fresh skill session on the unchanged boundary task: 83,254 total tokens, 29.031 seconds. [Retained evidence](results/fast-receipt-2026-09-11/run.json) includes commands, answer, diff, final files and usage; local originals remain in `local-runs/fast-receipt-02`.

The actual trace shows the new age-18 assertion failing with exit 1 before the comparison change, then the unchanged three-test suite passing with exit 0. Only the comparison and focused regression test changed. No timeout occurred. Shell command count fell from six in the immediately preceding skill sample to five; the skill read was combined with initial inspection. Early guessed-path discovery still occurred.

Observed total tokens were 18.3% lower and elapsed time 26.3% lower than the preceding skill sample. Against the preceding baseline they remained 4.3% and 13.7% higher, respectively. These are temporally separated single samples, not a controlled causal estimate, stable speedup, or general superiority claim. Preserve both earlier results.

The compressed instructions retained this task's core behavior. Their new reuse-of-before-evidence branch, existing-fix isolation and unavailable-runtime handling are not exercised by this case; those remain behavioral validation gaps. Do not infer that every Receipt workflow improved from this easy boundary example.
