# Correct-probe reuse: less executed work, small local saving

[Protocol](CON-ARTIST-PROBE-REUSE-PROTOCOL.md) committed as `c0fbb81` before
execution. Two cases, three serial repetitions per version, no retries/exclusions.
Python 3.9.6 / Clang 21.0.0 on the shared local host. This is author-executed helper
timing, **not a model benchmark**.

Timing-boundary deviation: the runner includes the small recipe's `deepcopy`
immediately before `audit_batch` inside each measured interval, in both versions.
Fixture copying and verification remain outside. Retain these measurements as
collected; no rerun was used to remove the deviation or improve the result.

Reproduce from a checkout retaining the pinned history:

```sh
python3 -B benchmarks/con_artist_probe_screen.py
```

The [runner](con_artist_probe_screen.py) executes trusted helper source from Git;
no dependencies, model calls or external services are required. Do not use Python
`-O`: assertions verify the observations. Source archive users without that Git
history can run the [current example](../examples/con-artist.md) but cannot
reproduce this historical version comparison from the archive alone.

Previous `5f68ac78324641e536dadc65b49fdb3798354d3e`, helper SHA-256
`8dda0b041544d5080c7d0e47f4148609e648b324071556948c02bdc293b1d842`.
Candidate `91fdde380c2da2f21d466f03b50a315b97d8f0e4`, helper SHA-256
`a1384c402a975b7be3f5797593c167ec85db1c17b6904d4e4cf656f44fef9a75`.
Fixture files and recipe come from `e7fb780`, not mutable working files.

## All observations, in execution order

Times rounded to nine decimal places; bytes are indented JSON serialization,
not tokenizer counts. Every row has two observed audits with both intended
mutant assertion failures, unchanged original bytes/modes and no leftover copies.

| Probe case | Repeat | Version | Seconds | Child checks | JSON bytes |
| --- | --- | --- | ---: | ---: | ---: |
| Identical | 1 | Previous | 0.265156291 | 7 | 3102 |
| Identical | 1 | Candidate | 0.222737125 | 6 | 3070 |
| Identical | 2 | Candidate | 0.224337250 | 6 | 3070 |
| Identical | 2 | Previous | 0.257729625 | 7 | 3102 |
| Identical | 3 | Previous | 0.260410292 | 7 | 3102 |
| Identical | 3 | Candidate | 0.221851667 | 6 | 3070 |
| Different | 1 | Candidate | 0.256437792 | 7 | 3102 |
| Different | 1 | Previous | 0.281872959 | 7 | 3102 |
| Different | 2 | Previous | 0.279740750 | 7 | 3102 |
| Different | 2 | Candidate | 0.259150208 | 7 | 3102 |
| Different | 3 | Candidate | 0.256307750 | 7 | 3102 |
| Different | 3 | Previous | 0.254846541 | 7 | 3102 |

## Interpretation

Identical-probe mean: 0.261098736 → 0.222975347 seconds, about **38 ms less**
(−14.60%). Each candidate run removes one redundant correct-code child process;
both mutants still execute their own tests and probes. Reused results point
directly to the original successful observation, never another reference.
Output saves only 32 bytes in this deliberately quiet example.

Different-probe mean: 0.272153417 → 0.257298583 seconds (−5.46%), with unchanged
seven executions and 3102 output bytes. The final candidate sample is slower
than its corresponding predecessor sample. There is no removed work in this
control; its timing variation is a reason not to attribute the entire
identical-probe time difference causally to reuse.

All correct checks pass; original weak tests survive both faults; stronger probes
fail on the actual missing/duplicated records. No timeout or output truncation is
accepted. These checks establish the local execution-count reduction and guard
against reusing a different probe, not model adoption, end-to-end token savings,
statistical superiority or suitability for nondeterministic workloads.
