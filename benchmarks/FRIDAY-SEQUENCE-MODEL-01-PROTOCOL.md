# Friday sequence guidance adoption 01 — 2026-09-14

Resources `b2925c9`. Two fresh explicit-Friday Astra medium sessions on unchanged
`friday-ack-cases.json` SHA-256
`4e746de6d34b5b5d06955546e8cdc77d14042a2f98e2b45465ac4aba99d133b4`.
One repeat per case, serial, seed20260911, 240 seconds/cell. No favorable retries.
No author tests or resource/task changes during timing. No supplied author probe,
previous answer or intended witness list in model prompts. Freeze before launch.

Preflight at candidate: 54 Friday tests pass, including native actual-caller
commit/independent-read controls, compact-sequence positive plus five intended
sync/recovery/cross-record failures, interior branches and state changes. These
are author controls; model adoption remains untested. Runtime helpers unchanged.

Review actual entry/project reads, actual application.write/read and migration
execution, both versions' updates/inserts, fresh cross-version visibility after
acknowledgment and latest values after documented down. Control must not acquire
invented defects; gap must retain stale/null/lost-update findings. Respect missing
production evidence, original files and project-local scope. Do not require a
particular operation/read count or helper; reduced coverage cannot be a win.

Inspect repeated values, cross-version transitions, distinct-row need and retained
data, not just operation totals. Reconcile raw events/usage, frozen resources and
original inventories, then replay actual retained programs separately unchanged.
Do not fill missing original output using replay. Preserve errors/timeouts/unknown
usage and all unfavorable results. No broad efficiency claim from exposed n=1,
shared host/cache or unequal work. Prior skill costs: control 90,287 tokens /
63.636s, gap 94,930 / 82.585s. Earlier no-skill costs are historical comparisons,
not contemporary randomized controls for this instruction change.

Publish both reviewed outcomes and EN/KO limitations. Historical/featured charts
stay unchanged. This is an adoption screen, not confirmation of all-eight gains.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-ack-cases.json --output benchmarks/local-runs/friday-sequence-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
