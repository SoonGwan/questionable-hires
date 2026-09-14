# Receipt native invocation adoption 01 — reviewed 2026-09-14

Launch `b2c7703`, resources `bc3b225`; [protocol](RECEIPT-NATIVE-MODEL-01-PROTOCOL.md),
[two original sessions](results/receipt-native-model-01/),
[previous ledger screen](RECEIPT-LEDGER-01-REVIEW.md).
Unchanged correlated ledger tasks, explicit skill, Astra medium, serial n=1,
seed20260911, no retries. Both completed; frozen fixture/resources and current
project bytes reconcile. The comparison below is descriptive, not causal.

## Adapters removed; token parity with baseline not achieved

| Case | New skill tokens / seconds | Change vs prior skill | Change vs prior baseline |
| --- | ---: | --- | --- |
| a: complete fix | 80,212 / 44.893 | −39.09% / −37.93% | +14.65% / −25.53% |
| b: incomplete fix | 81,055 / 41.633 | −10.19% / −39.46% | +14.70% / −41.43% |
| Sum | 161,267 / 86.526 | **−27.34% / −38.67%** | **+14.67% / −34.14%** |

Prior skill sum: 221,949 tokens / 141.093s. Prior baseline sum: 140,630 /
131.371s. New a usage: input 79,424 + output 788, cached input 67,584;
b: input 80,076 + output 979, cached input 67,584. Cached input is counted once,
reasoning output (8 / 76) is already included. Three shell calls per new case.

Both select `invocation: module` and `guard_tree: true` through the ordinary CLI.
Neither replaces internal functions, writes a harness or constructs custom hash
code. Both still search helper implementation with `rg`, adding source-reading
work; a also repeats historical source reads. Full entry/guide, project instructions,
requirements, current tests and schema are present in the captured reads.

Case a unnecessarily selects `--python python3`, whereas b uses the already
resolved default interpreter. Original a output contains two xcodebuild diagnostics
per phase. No environment-cleanliness claim or interpreter-overhead estimate is
made. The complete native result remains present despite those diagnostics.

This is a real observed adoption change on these tasks, not a broad 20–30% win:
the large reduction is against the previously expensive skill adapters, while
tokens remain above baseline. No contemporary baseline; exposed correlated cases,
n=1, shared host/cache, different runs and unequal provenance/extra work prevent
causal attribution or an all-eight efficacy claim. Historical/featured graphs
remain unchanged.

## Original correctness and scope evidence

Each phase runs the actual command `python -B -m unittest -v checks.test_delivery`
with the same five current tests and schema, actual SQLite transactions and fresh
balance connections. Three same-process import checks (ledger, implementation,
test module) complete; `provenance_ready` is true. Both HEAD^ runs show two native
retry assertion failures and three controls. Complete HEAD passes five. Partial
HEAD still fails with `(False, 250)` and `(False, -100)` instead of `(False, 125)`
and `(False, -50)`. Both final diagnoses are correct; helper CLI 0 is not confused
with a complete fix. Native/check exit values agree, without timeouts/truncation.

Before revision: `721139585aea166e10dd4e06fd6f35152e7fdc61`; complete after:
`547b2e89c7f99e13192ddc2ccb90f623a8234307`; partial after:
`562854580f33f36e06a2ee05755eb8d7737608d8`. Current test hash:
`4571e36668f830a1b7f80d00eedd7f0452909774d68962efe84e35eafb693021`.

Original guards report 81 unchanged entries: a 44,660 file bytes, b 44,607.
Owned comparison copies are removed; normal test cleanup and absence of retained
databases/harness/report are consistent with the actual suite and retained files.
Original notes/cache/project bytes and installed resource hashes/modes match.
Guards cover the comparison interval, not later Git commands. The shell records
all four child exits as zero but does not itself propagate every failed child;
its final printf status alone is not the evidence. No decisive original capture
gap was observed; empty automated diagnostics alone do not establish that.

## Separate replay with preserved differences

`python3 -B benchmarks/replay_receipt_ledger_01.py --profile native-01` executes
each complete original shell program unchanged in a disposable copy, restores
only that copy's index from verified pre-collector bytes/mode/hash, and reconciles
original raw/events/usage/resources. Original retained workspaces are untouched.
[Replay report](results/receipt-native-model-01/author-replay.json) keeps all output.

Both replays exit 0. Case b's complete helper object matches after normalizing
only temporary paths and native durations. Case a differs only because its four
original xcodebuild diagnostic lines do not recur; all other fields, including
native test content, source identities and whole-tree digest, match. The full
object equality flag stays false rather than deleting those original warnings.

Both replay copies' `.git/index` changes during subsequent Git review, outside
the helper interval; those changed paths are retained in the report. Neither
outer shell checks whole-tree equality after Git review. Therefore do not present
the complete replay as leaving all metadata unchanged. Captured index restoration
establishes the matching comparison snapshot, not equivalence of later Git stat
refresh behavior in a different physical copy. Binary index artifacts remain local.

The next optimization target is remaining instruction/source-reading overhead,
with task coverage/provenance preserved. Do not claim completion of the broad
objective or promote this small screen into the featured benchmark.
