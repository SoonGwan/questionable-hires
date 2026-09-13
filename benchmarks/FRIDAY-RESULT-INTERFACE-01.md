# Friday: explicit observation schema and reusable JSON output

The [all-eight gate](BUNDLE-CONTRACT-03-REVIEW.md#rolling-schema--friday-reviewed)
records reading both the matrix reference and the helper implementation before
using the API. Source review may be justified; the trace does not establish why
it happened or that this change will eliminate it. Inspection found a concrete
interface gap: the reference called the API result the same dictionary as CLI
output but did not distinguish native tuple/BLOB values or specify result keys.

`matrix` continues returning its existing native SQLite row tuples and bytes.
New public `format_result(result)` serializes already-collected observations using
the same JSON representation as the CLI, including `{"blob_hex": "..."}` values.
The CLI now uses this function itself. No SQL rerun, connection, result mutation,
new recipe option, input-budget change or exception-to-success conversion occurs.
Unknown non-JSON/non-bytes values raise TypeError instead of being stringified.

The reference contains an executable runpy/API/output example and the exact
phase/check success, error, truncation and incomplete-result shapes. It identifies
native/API versus serialized/CLI types and their different invalid-input reporting.
This avoids asking callers to recover output details or copy serialization from
implementation. It does not prohibit source review, expand the helper to other
engines, or treat a successful SELECT as correctness/rollout safety.

## Author checks

Three new regressions execute real SQLite or the literal documented Python block:

- A query returns integer, float, NULL, Korean text, nonempty BLOB and empty BLOB.
  Plain json.dumps on the native result raises TypeError; the public formatter
  retains all values in CLI JSON shape. Output equals actual CLI stdout exactly.
  Native results are unchanged, and formatting opens no connection. An invalid
  reader remains failed without rows even though overall execution completes.
- A partially applied migration preserves complete=false, its migration_error,
  empty checks and absent later phase through formatting. An unsupported object
  is rejected, not silently converted into a claimed observation.
- The documented API example executes against BLOB data and emits valid JSON.

Focused suite: **19 tests pass (0.097s)**. These establish interface behavior,
not model adoption, token savings or a real-project performance improvement.
No entrypoint, selection policy or UI change. Skill-creator's principle applied
is making reusable deterministic output handling public and documenting only
the interface needed by its consumers. Current all-eight acceptance remains
unmet; previous measured resources/results and featured charts are unchanged.

Full suite: **373 tests pass (52.887s)**. The catalog initially mistook dictionary
lookup followed by a call in the fenced Python example for a Markdown link.
After the full run, the example was restated using named function bindings;
its actual execution suite passes **19 tests (0.096s)** and packaging passes
**12 tests (2.951s)**. Catalog/local-link, featured and whitespace checks pass.
No resource edits overlapped either test run. This formatting correction does
not change helper behavior, but the final example was checked after the full run.
