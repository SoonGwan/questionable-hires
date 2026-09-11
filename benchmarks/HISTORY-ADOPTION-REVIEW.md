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
