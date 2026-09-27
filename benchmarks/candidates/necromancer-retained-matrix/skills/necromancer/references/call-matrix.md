# Native Python call matrix

Optional for repeated caller/input comparisons, not a replacement for requested
or project-required tests. Python3.9+, standard library. Read this interface;
loading the full helper source is unnecessary unless adapting it. Load by path:

```python
import importlib.util, json
spec = importlib.util.spec_from_file_location("call_matrix", "/actual/skill/path/scripts/call_matrix.py")
matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix)
```

Bind a real supported project caller. Build `cases` as a list of
`(input, {"return": expected_value})` or `(input, {"raises": ValueError})` entries
from the documented contract. Then `report = matrix.observe(caller, cases)`;
print the report with `json.dumps(report)`. For multi-argument callers, use a
small wrapper that unpacks the explicit input. Do not substitute a reimplementation
of the caller. Native process0 means observations collected, not all cases passing.

The report includes attempted/evaluated/unrun/ungraded counts, matches/mismatches,
input mutations and actual/expected examples. `complete` must be true, `unrun`
and `ungraded` zero before treating it as complete evidence. Mismatches in a
proposed removal can support rejecting it; don't invent an expected mismatch
count to make collection succeed. Expected valid behavior still needs assertions.
Examples default3, selectable1..8; omitted mismatch examples are counted. Avoid
printing every passing row when the summary and decisive actual/expected examples
settle the decision. When specific actual values are requested, call `observe(caller, cases, retain=True)`
and print `report['observations']` after completion checks. The ordered list records
one encoded actual outcome per evaluated case during the first callback execution,
including matches and exact exception classes. Do not rerun the same cases merely
to print values already retained. Opt-in reports use version3; default reports
remain version2 without this list. Unsupported actual-return encoding retains
only the evaluated prefix; incomplete output is not all-case evidence. Returning
more rows can increase output cost, so use retention for a concrete evidence need.
Example limits do not waive requested observations or required tests.

Each input is deep-copied before the actual call; mutations count as disagreement.
Run each alternative independently, keeping real source bindings/imports/compiler
settings and restoring replacements in finally. The helper does not load source,
patch functions, resolve callers, or establish historical provenance for you.

Limits:1..256 cases, bounded primitive None/bool/int/str/list/tuple/dict values;
integers256bits, strings256characters, containers16entries, nesting4. Floats,
Decimal and arbitrary objects are unsupported: unsupported input/expectation
fails before calls; unsupported actual return yields incomplete report with prior
observations retained. Use a suitable native probe for unsupported evidence rather
than changing a contract to fit this representation. Exceptions compare exact
types; messages and subclass contracts need separate checks. Equality is Python
value equality, not necessarily type identity. Unexpected failures and BaseException
interruptions can still propagate. Callback execution is unsandboxed and lacks
an internal deadline; use the project's interpreter and a bounded native process.
No installation, network, source writes or external state cleanup is performed.
