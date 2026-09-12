# Runtime-first routing: one targeted development observation

Candidate `5f1dc34` changes only Friday's execution-path paragraph: application
writers, transactions and connection behavior use actual runtime facilities;
the optional SQL reader matrix reference is read for the SQL-only path. Character,
release scope, helper and reference are unchanged. Eleven Friday/fixture tests
and repository/skill validators pass; these are not model-quality tests.

One fresh Astra medium skill session on the existing writer-gap case, serial,
no retry. Raw ignored evidence: `local-runs/friday-routing-01`. No new baseline or
control; the compatible-control path has not been rechecked with this candidate.

| Observation | Total tokens, cache included | Seconds |
| --- | ---: | ---: |
| Current skill | 70,307 | 50.112 |
| Preceding skill | 70,811 | 53.713 |
| Earlier baseline | 80,937 | 47.410 |

The model does not read the matrix reference or helper source. It runs actual
version functions against project-local temporary database files, with separate
old/new connections and committed writes. It demonstrates both stale-update
directions, null values after old insert, new-insert/update rollback loss, ordinary
new insertion, immediate rollback, and both writer orders. No production or
restore readiness claim. The generated experiment removes its databases afterward.

The preceding skill used in-memory single-connection probes; this run uses file
backing and separate connections. Both use five shell commands. Costs are about
-0.7% tokens / -6.7% time versus preceding skill, and -13.1% tokens / +5.7% time
versus earlier baseline. Different runtime depth and separated single samples
prevent causal attribution or an efficiency acceptance claim.

Original commands/output were inspected, not replayed as if they were model
evidence. All five original files are unchanged; all four installed resources
match candidate blobs and before/after inventories. No timeout, rejected patch
or capture flags. One discovery command exits 1 because no AGENTS file is found,
not because the behavioral checks fail. Snapshot equality and clean diagnostics
cannot prove absence of transient edits or guarantee complete output.

Retain as observed routing improvement with mixed costs. Do not add a universal
transaction checklist, force file-backed databases, or rerun this exposed task
until a favorable result appears. Broader current-candidate confirmation remains
necessary; the full objective is unmet.
