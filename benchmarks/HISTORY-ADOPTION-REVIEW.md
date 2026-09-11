# Collector adoption check before another model benchmark

Current collector 6318b91 has a measured local process improvement; main entrypoint
8454059 is unchanged. The existing bulk-history and real HTTPX region reviews were
inspected before selecting a next model task.

- HISTORY-BULK-01: neither skill session loads the helper reference or invokes
  trace.py. Native Git resolves the question. The normalized case reads excessive
  current/history text, but a faster unused helper cannot explain its costs.
- HTTPX-HISTORY-REGION-01: neither arm invokes trace.py. The positive skill pair
  uses focused native reading and actual behavior; baseline repairs a failed probe.
  Shallow history prevents origin attribution. Faster parsing cannot restore absent
  parent history or establish the historical reason.

Therefore neither exposed workload is a useful confirmation of the latest helper
optimization. Do not rerun either merely to obtain a favorable timing, force helper
use into their user prompts, or present helper timing as model performance.

Before a new model run, establish a representative workload that actually benefits
from repeated current-text/status/attribution/patch collection. It must ask for a
real decision across multiple relevant regions, preserve caller/contract checks,
and allow the model to choose native Git. Preflight must prove available history
and a meaningful active-versus-obsolete distinction, not just a large file. Report
non-adoption honestly. Keep any resulting test set below ten tasks as requested.

The immediate engineering question is whether multiple region requests repeat
identical repository identity/status and commit-patch retrieval. Inspect existing
collector interfaces and real repeated-use costs before adding a batch API; do not
add a new resource or mandatory workflow solely on speculation. The current
single-region helper remains valid, optional, and unchanged in this review.

## Repeated-region inspection on the actual repository

At e68272d with a clean worktree, imported current trace.py and instrumented only
its Git wrapper in memory. Queried trace.py ranges 91:102, 108:115 and 118:128,
all within selected_patch_excerpt. Each reports available history and two commits.
Fifteen Git calls comprise eight distinct argument tuples: rev-parse and status
three times each, three different blames, and six show calls for three distinct
commit/path requests. Repeated show outputs have the same lengths (4,535 three
times and 3,602 twice). Summed observed Git-call wall time is 0.224984 seconds.
No source edits or state cache were introduced.

The existing range interface queried 91:128 in six Git calls: identity, status,
one blame and three shows. It returned 38 current lines, three commits, zero omitted
commits, 22,783 serialized JSON characters and 0.085400 summed Git seconds. The
comparison used max_commits=5 for this combined query versus default three per
separate query; only three commits were actually returned. These are one-off local
observations, not a balanced benchmark or equivalent output: the combined request
adds seven intervening current lines and may include additional patch context.

This demonstrates repeated work but does not yet justify a new batch API or stale-
state cache. Nearby regions in the same behavior can already fit the 100-line
interface. Widely separated regions, irrelevant intervening code or excessive
attributed commits may invalidate that approach. Assess output and behavioral
context before combining; never widen a range just to reduce the command counter.
No model token benefit or adoption is measured. Next improve/evaluate use of the
existing range mechanism where context is genuinely shared, not mandatory batching.

Follow-up at 49ba7cc used default max_commits=3 for both separate and combined
queries. All selected current-line records and complete blame rows match exactly;
every separately returned commit ID is present in the combined result, with zero
omitted commits. Serialized JSON characters total 35,059 separately versus 22,783
combined (about 35% less). Patch excerpts are not asserted byte-identical: the wider
query may include additional relevant hunks/context. These are characters, not
model tokens. This remains a local single-function observation, not agent adoption.

The optional collector reference now explains when nearby regions may share a
bounded range, requiring relevant intervening context and inspection of omission/
truncation. Distant/unrelated regions remain separate. The main entrypoint, helper,
automatic routing and character are unchanged; no mandatory batching or new API.
Repository validation and diff checks pass. No model rerun or new performance
acceptance claim accompanies this conditional usage change.
