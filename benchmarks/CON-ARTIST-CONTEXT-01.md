# Read-only audit context candidate

Revision `d442b3b` adds a deterministic context collector to remove repeated
instruction/configuration discovery and manual source slicing when explicit
Python paths are already known. The [preceding transfer](results/httpx-queryparams-01/README.md)
still used more tokens and repeated discovery despite a reuse instruction.
That result remains intact; no model efficiency benefit is yet measured for
the new tool. This is a development implementation record, not a benchmark win.

## Implemented workflow

[Interface and limitations](../skills/con-artist/references/python-context.md).
One invocation returns complete selected files or qualified definition excerpts
with original line numbers, ancestor instruction contents and checked paths,
common pytest configuration files and static conftest indexes. The collector
does not import code, resolve a fixture graph, choose a fault or run tests.

Conftest decorators, top-level imports/plugin settings and definition locations
remain visible. Inspect relevant autouse fixtures/hooks and unresolved dependencies
before execution. Definition excerpts are navigation, never a substitute for
executing real modules with their compilation context. Dynamic configuration,
outside-root host instructions and concurrent filesystem changes are not resolved.

Limits are enforced before emitting stdout: 1–8 selectors, 32 path components,
256 KB per regular UTF-8 file, 2 MB total reads and 100,000 output characters.
Traversal, Git internals, symlinks, missing/ambiguous symbols, oversized content
and unsupported conftest syntax fail explicitly. This is not a concurrency-safe
filesystem sandbox or an automatic authorization to publish source/configuration.

## Actual checkout exercise

On the unchanged HTTPX source at
`26d48e0634e6ee9cdc0533996db289ce4b430177`, execute:

```sh
python3 -B skills/con-artist/scripts/context.py --root /path/to/disposable/httpx \
  tests/models/test_queryparams.py httpx/_urls.py:QueryParams.get_list
```

Observed result: `collected`; eight ancestor instruction paths checked, none
present; full `pyproject.toml`; 18 definitions indexed from `tests/conftest.py`,
including the `clean_environ` autouse decorator; the full selected test and
`QueryParams.get_list` at lines 526–535. Relevant fixture bodies still require
inspection; this is not complete preparation for every audit.

Returned original source hashes:

- `tests/models/test_queryparams.py`:
  `d9e25e70996674484714fcac794a6a26db11b74a494b98990807754114d1be1a`
- `httpx/_urls.py`:
  `757f7d551d4348e1e9828f40abb3f360ee0529dc6a2a3c32369f20adff1d1cdd`

The upstream checkout remains clean. This was an author CLI exercise, not a fresh
model session. No token/time or percentage saving is inferred from output length,
the number of returned paths or a shorter hypothetical workflow.

## Verification and next gate

Ten new tests execute the CLI and exercise nested instructions, exact decorated
and async spans, source preservation, nonexecution of import-time failures,
conditional plugin/hook visibility, symlink/traversal rejection, ambiguous symbols,
read/output limits and explicit syntax failure. They do not assert a performance
claim or merely match skill wording. Catalog, schema and language sync checks pass.
Full local regression: 291 tests pass in 49.624 seconds, including bundle/resource
checks. This does not verify current hosted CI, remote installation or model cost.

Next behavioral evaluation must freeze resources and criteria, inspect whether
the model actually replaces repeated discovery with this call, and retain any
additional reads, scope changes and failed attempts. New-tool availability alone
does not prove adoption; adoption alone does not prove whole-task savings. Preserve
the earlier unfavorable comparisons and do not change featured charts.
