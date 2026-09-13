# Disposable component observations

Use only when captured observations, not standalone project tests, are requested
and no adequate existing runner applies. The helper requires a zero-argument
constructor, async `run(query, fetch)` and state storing fetched payload directly.
By default it checks sequential normal success and reversed overlapping completion,
not loading retention. The opt-in mode below adds normal/reversed overlap with an
already displayed result. Repeated identical overlapping queries remain unsupported.
Use project-specific checks
from the outset for unsupported requirements; never adapt production to the tool.

Run the installed skill's [script](../scripts/sequence_probe.py) directly without
reading or duplicating its implementation:

```sh
python3 -B SCRIPT --root . --source FILE --class-name CLASS [--boundary QUERY]
```

Defaults: method `run`, state `result`, queries `old`/`new`, timeout 5 seconds.
Use `--method`, `--state`, `--old`, `--new` for matching supported interfaces;
old/new queries must differ. An optional `--boundary QUERY` also must differ
from them; an empty boundary query is allowed. No production behavior is inferred
merely from the attribute names.

Add `--retain-while-pending` only when the product requires preserving the
displayed result until the latest request succeeds. It seeds `seed result` through
an actual completed call using the old query, then starts old/new requests on that
same instance. Two additional isolated cases complete them in normal and reversed
order. Checkpoints verify the seed, display after each fetch entry, display after
the first completion and final latest ownership. Failure evidence includes phase,
query, actual state and expected state. No state is assigned directly by the probe.
The seed reuses a query but overlapping old/new keys must still differ.
This is a success-path display contract, not loading-error, cancellation, debounce,
rendered-UI or general state-machine coverage. Do not enable it when clearing or
displaying intermediate results is permitted. Default behavior is unchanged.

Exit 1 means a checked behavior failed, 0 means targeted checks passed, and 2
warrants inspection. `--error-state ATTRIBUTE` requires JSON-serializable state
where falsy means clear and truthy means displayed. It checks errors on success,
current failure, recovery and stale failure. Failure output retains the failing
checkpoint. The tested layer is the local async component, not rendered UI.

If retained evidence is requested, use `--output NEW.json` for the same execution's
JSON. Existing files are refused. Missing console output requires inspecting that
file or marking verification incomplete; final prose is not execution evidence.
`--timeout` bounds cooperative async waits (at most 30 seconds), not blocking
imports or callbacks. Keep test cases isolated and preserve original files.
