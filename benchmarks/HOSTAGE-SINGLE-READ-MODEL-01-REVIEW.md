# Hostage single-read screen — reviewed, mixed cost evidence

[Protocol](HOSTAGE-SINGLE-READ-MODEL-01-PROTOCOL.md), launch `69ceece`, resource
`6d733b9`. Both scheduled sessions completed, no timeout/account-limit/error
events, exclusions or author retries. No resource/input edits or author test
workloads during model timing. One exposed authored task, n=1 per arm.

| Arm | Tokens (cached input included) | Seconds | Shell calls |
| --- | --- | --- | --- |
| Baseline | 87,216 | 88.793 | 4 |
| Skill | 92,819 | 82.136 | 5 |

**+6.42% tokens / −7.50% time**: mixed evidence, not an accepted overall cost win
or a general 20–30% improvement. Shared host/cache, n=1 and unequal checks limit
inference. Earlier adverse screens are not a controlled old/new comparison.

## Actual route and scoped implementation

Skill batches project, entrypoint and self-contained asset in one read command;
it does not open the compatibility redirect. Copies exact resource asset and uses
ControlledCall in retained regressions. This observes the intended one-file
interface, not proof of causal savings. A project-only `find` instruction sweep
still accompanies discovery. Baseline uses custom entry/release gates.

Both produce identical Publisher implementations: exact-ID set owned per instance,
duplicate return before state mutation, finally cleanup. All original tests and
other supplied files remain byte-identical. Only Publisher and new regression
file change, plus skill's copied support. No unrelated effects or scope violation.

Baseline retains seven new test methods (nine including originals), covering six
concurrent non-normalized IDs including Unicode distinctions. Skill retains five
new methods (seven including originals), grouping success/failure/cancellation and
four cross-key cases as subtests. These are fewer method names, not missing those
required transitions. Both exercise duplicate noninterference, cross-key/instance
concurrency, exact callback argument/result/error identity and all required retries.
Async tasks register cleanup before entry waits and waits are bounded. Extra
normalization witnesses and test organization differ; do not equate workloads.

## Original evidence

Both run unittest alone: exit 0 and passing count/summary are captured (baseline
9 in 0.041s; skill 7 in 0.050s). Final reported counts match. Individual verbose
headers are partial: baseline has none, skill only its last full header. Collector
flags both. These summaries support total pass observations, not complete native
per-test transcripts. No claim that collection is repaired. Copy output is empty
legitimately; final Git checks support scoped changes.

## Separate replay and reconciliation

[Exports](results/hostage-single-read-model-01/) retain both attempts and
[author replay](results/hostage-single-read-model-01/author-replay.json).
The keyed replay utility now accepts explicit resource and expected method counts
(old defaults remain unchanged). New run uses `--resource 69ceece --skill-tests 7`.
This checks discovery, not a reduced acceptance criterion.

Eight isolated native controls using unchanged retained tests match:

- Baseline final: 9 pass, 0.040s; skill final: 7 pass, 0.049s.
- Originals: each rejects the actual duplicate callback with AssertionError.
- Global busy: bounded cross-key timeouts (baseline one, skill four subtest errors).
- Missing cleanup: baseline five retry-result failures; skill seven bounded
  retry/entry subtest errors. Do not describe these timeouts as value assertions.

Twenty-second subprocess bounds apply. All snapshots/tests remain unchanged;
raw terminal usage, sanitized events, resource hashes and exact reviewed inventories
reconcile. Copied asset matches frozen bytes. Replay does not fill original header
gaps or establish why they happened. Featured and historical results stay fixed.

The simplified route is adopted with retained required coverage, but whole-task
efficiency remains unproven. Next evidence should broaden across the skill bundle
or unseen task structure, not rerun this exposed pair until a favorable ratio.
