# Three nearby decisions, one supported behavior

Freeze all current resources and history_region_cases.py at this commit. Generate
one case using the committed builder. Run baseline/skill, one repeat, serial,
Astra medium, seed 20260911, timeout 240 seconds. No retries, exclusions or helper
mandate. Both arms receive the same task and original repository files/history.

Author preflight uses actual Git history and in-memory replacements through the
actual consumer binding. Current tests pass; removing only code fallback fails;
removing only private name fallback passes because the public caller normalizes;
removing negative guard fails. Four existing tests run in every variant. Original
files stay unchanged. Three introducing commits and later normalization are present.

Inspect each historical/current decision, actual executed checks, resource identity,
scope and capture. Do not score a helper invocation or range merging as correctness.
If native Git is sufficient, non-adoption is valid and cannot support collector
speedup claims. If ranges are merged, inspect omitted commits and patch coverage;
the declarations/root history must not displace decisive introducing commits.

Report input + output tokens (cached input once), process wall time and actual
commands for both arms. Unequal verification, failed probes and incomplete capture
remain visible. This small authored transfer is not independent held-out evidence
or whole-bundle acceptance. Do not rerun it just to improve its score.
