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
