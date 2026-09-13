# Necromancer multi-decision development screen 01

The `d5c7150` entrypoint consolidation remains behaviorally unverified: its
[single-decision attempt](NECROMANCER-ENTRY-01.md) timed out before captured work.
Gate 05's increased history cost remains preserved. No new skill code is added
for this screen. Test the existing candidate on a different, multi-decision task
before treating another helper or instruction change as necessary.

Generate the existing `history_region_cases.py` fixture unchanged into
`necromancer-regions-cases.json`, SHA-256
`d78934def2ca030ed9f7d329d93bd9a6a6c437c9788b821b2cab35f117141806`.
This authored development task is previously exposed, not a new holdout. The
supported consumer and explicit contract differentiate three decisions: preserve
code fallback and negative rejection, but permit removing private display-name
fallback while preserving caller normalization. Cite the introducing commits and
later normalization; current need must not be inferred solely from old messages.

Prelaunch: 26 history-helper/transfer tests passed in 6.744s, including real Git
history, unchanged native tests and proposed-behavior controls through actual
render. Removing code fallback or negative rejection fails; removing redundant
private display fallback passes. No model performance follows from author tests.

Freeze at this protocol's commit; two fresh serial Astra medium cells, baseline
and skill once, seed 20260914, 240 seconds each. No resource/task edits or author
test workloads during timing. Preserve every attempt and original output. No
replacement of the earlier timeout or retries/exclusions for better percentages.
Stop scheduling on account limits. Runtime connection retries remain recorded.

Review current consumer binding, actual variants and native outcomes, all three
decisions and provenance, worktree preservation, extra searches/artifacts and
capture gaps. Helpers are optional; invocation count is not a quality score.
Record input+output tokens (cached input once), process time and unequal work.
A complete turn or a correct recommendation without required verification is
not full acceptance. Missing output cannot be filled by author replay.

One exposed task at n=1 cannot establish broad efficiency, causality, all-eight
improvement or real-production transfer. No automatic featured-chart changes.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/necromancer-regions-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 \
  --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/necromancer-regions-01
```
