# Current paired regression — execution in progress

Follow the [frozen 18-cell protocol](FAST-PAIRED-02-PROTOCOL.md), resources and
unchanged cases at `eca8921`, scheduling commit `594d0c6`. This report is partial,
not an aggregate or completed gate. Raw ignored evidence is under
`local-runs/fast-paired-02`; inspect individual metadata/run.json for current
completion. Do not restart an observed or running cell.

## First two completed pairs

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| history-active | 62,835 | 68,852 | 24.247 | 31.132 |
| boundary-fix | 79,233 | 83,442 | 29.915 | 32.267 |

Tokens count input including cache plus output. These partial observations do
not establish the direction or size of the full comparison.

Both history reviews correctly retain the active name fallback and execute the
actual caller. Skill additionally inspects/cites its introducing commit and checks
None/empty display values. Baseline never inspects history and omits the historical
citation required by the unchanged criteria. Note that the neutral task requests
a recommendation with evidence without explicitly requiring a Git citation; the
rubric's historical-evidence requirement makes these unequal-work results
unsuitable for claiming equivalent-outcome speedup.

Both boundary runs produce identical implementation and regression-test diffs:
age 18 changes from rejected to accepted; 17/19 assertions remain. Original logs
show the new age-18 assertion failing before the fix, then all three passing
afterward. Skill is costlier despite the same core outcome. One empty-output
diagnostic is retained for skill; its actual test outcomes are present separately.

The first four cells complete without timeout or patch rejection. Their installed
resource inventories match before/after and frozen Git blobs. Full scope review,
remaining pairs and combined interpretation are pending; no blanket success claim
or final integrity audit follows from these preliminary checks.
