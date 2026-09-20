# Existing fix with native Node tests

Use when the project already runs `node --test` and lacks adequate isolated
comparison. Requires Python 3.9+/POSIX and Node synchronous `registerHooks`
(verified on 24.16.0). This does not replace npm scripts, Jest/Vitest, builds or
custom loaders. Nonempty `NODE_OPTIONS`, `NODE_PATH`, `NODE_COMPILE_CACHE` and
Python invocation/import options reject. Use project-native setup for unsupported
requirements; do not remove configuration, upgrade or install merely to fit this.

## Execute and reuse the evidence

Adapt paths/revisions and the project Node executable (default: node on PATH):

```sh
python3 /path/to/receipt/scripts/compare.py --source . --node /path/to/node --spec - <<'JSON'
{"fixed":["regression.test.mjs"],"vary":["app.mjs"],"before":"HEAD^","after":"HEAD","imports":["app.mjs"],"runner":"node","tests":["regression.test.mjs"]}
JSON
```

- `fixed`: current tests/configuration/support, files or explicit directories;
  `vary`: implementation files present in both versions. No root, symlink, Git
  internals, empty directories or overlaps; shared copy budget 20 MB.
- `tests`: fixed selected JS paths (.js/.cjs/.mjs), not flags/globs. `imports`:
  selected JS paths to observe, not package specifiers.
- Uncommitted after: `"after":{"working_tree":true}` freezes bytes/modes, not the
  index. Results already identify full commits or working-tree hashes.
- `watch:["notes.txt"]` checks extra originals without copying them. For requested
  whole-project preservation with authorized whole-root reads, add `"guard_tree":true`.
  `tree_guard` covers bytes/modes, entries and link text including .git/HEAD/index
  around tests/cleanup, not other commands or concurrent/restored changes.
  Limits: 10,000 entries/20 MB per inventory.

The helper owns copying, execution, preservation and removal of its project-local
.receipt-* copies. `preserve.py` belongs to a different native workflow, not another
prerequisite/wrapper here. This recipe needs no implementation read; inspect source
for a concrete trust, adaptation or error question. Reuse reported identities and
guard results. Use default compact JSON; `--pretty` is for requested human formatting.

## Judge results

Inspect actual assertions, identities/counts/skips and `native_exit_code`: defect
failure before, success after. CLI 0 only means observations collected.
Missing/mismatched/malformed/truncated provenance or timeout is incomplete; check
7 (CLI 2) or timeout stops further comparison. Setup errors and skipped tests are not proof.
Inspect `originals`, optional `tree_guard` and `comparison_copies_removed` too.

Native execution adds `--test-reporter=tap --import <observer>` to `node --test`.
`copied_loads` retains URL/PID/source hashes without pre-importing the application.
Loading is not evaluation, dispatch or every-worker coverage; retain actual
test-bound observations when required. Trusted tests only, not a sandbox or
tamper-proof attestation. Changed originals abort without restoration.

Default: 30 seconds/check, last 12,000 output characters; cleanup can wait five
more seconds. Remaining process-group members are killed even after normal exit;
persistent background work is unsupported. For unresolved boundary questions read
[preservation limits](comparison-details.md#preservation-guards); for overflow,
timeout or cleanup errors read [process limits](comparison-details.md#resource-and-process-boundaries).
These are conditional diagnostics; Python startup sections do not apply.
