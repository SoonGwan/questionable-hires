Every refresh must invoke its supplied fetch(key), even while another
refresh is pending. No duplicate suppression, serialization or automatic cancellation.
Each call returns its own exact fetched object or propagates its own exception.
Only the latest-started refresh owns pending and may publish value. Earlier success,
failure or cancellation cannot clear pending while the latest is unresolved.
Latest settlement clears pending even if older calls remain running. Keep the prior
value during loading and on failure/cancellation. Instances are independent.
Synchronous fetch failure also clears its owning pending state. Retry is allowed.
All callbacks here are cooperative asyncio callbacks; no network or threads.
