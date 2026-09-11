# Scoped discovery with a configured-consumer countercase

Compare predecessor `0143ef2` with discovery candidate `51ce19e`. The changed
opening paragraph reuses supplied paths and follows unresolved live bindings
before broad text search. It must not hide configured consumers outside the
initial source root. No new skill edit is permitted during the screen.

Use exactly two authored development tasks:

- `packaging_review_cases.py`: unchanged actual packaging snapshot `436e409`.
  Reusing this exposed case tests the new search mechanism; it is not independent
  confirmation or a rerun of an unchanged candidate for a better score.
- `configured_consumer_cases.py`: source fallback, application loader, external
  adapter path and input records connected by local JSON configuration. The
  ordinary unit test covers strings; the configured pipeline includes null.
  Directory naming is not proof of obsolescence.

Freeze both generators, `packaging_cases.py` and this protocol at one commit;
combine the generated cases without changing their prompts/files/criteria.
Record the combined JSON digest and export full skill trees from both revisions
with file modes and SHA-256 inventories before launching. Criteria and this
protocol are not supplied to the evaluated model.

Run four fresh serial Astra medium sessions, one per task/version, 240 seconds
per cell, seed 20260911. Fixed order: configured/predecessor,
configured/candidate, packaging/candidate, packaging/predecessor. Use `run.py`
with `--arms skill --jobs 1 --repeats 1`, the combined `--cases-file`, the
selected `--case`, frozen `--skills-root`, and a new `--output` for each cell.
No retries/exclusions. Stop scheduling on account limits or incomplete
orchestration, retaining all attempted outputs and resource costs.

Author preflight for the configured case verifies one unit test passes both
original and fallback-removed implementations. The actual app returns
`["A", "unknown"]` originally; removing only the None guard in memory causes
AttributeError through the configured adapter. Original files remain identical.
The packaging preflight and its limits are recorded in
[its protocol](NECROMANCER-PACKAGING-REVIEW-PROTOCOL.md).

Accept behavior only when the configured live adapter is identified and its
actual application failure is reproduced, and packaging cleanup remains protected
with the relevant original tests. A static guess, green string-only test or
unexplained setup failure cannot replace that evidence. Search scope/volume and
commands show adoption, not correctness or token savings. Inspect tool outputs,
answers, diffs and installed-resource manifests; reject missing consumers even
if the run is faster.

Compare total input-plus-output tokens and process wall time, retaining cached
input once and recording unequal work. Prior packaging results remain visible.
One repeat, two exposed tasks, shared host/cache and packaged skill text in the
packaging fixture prevent broad or causal superiority claims. Do not publish a
headline gain or update the original comparison chart from this screen alone.
