# Existing fix with native Node tests

Use only when the project already uses `node --test` and lacks adequate isolated
before/after comparison. This mode reuses the same bounded copying, preservation
and foreground process supervision as the Python comparison; it does not replace
npm scripts, Jest/Vitest, build steps or custom loaders. Native workflow remains
necessary for unsupported setup. No package installation is performed.

Requires Python 3.9+/POSIX for the collector and Node synchronous `registerHooks`;
native behavior is verified on Node 24.16.0. Select the project's Node executable
with `--node` (default `node` on PATH). Missing hooks produce incomplete provenance,
not a passing regression. Do not upgrade a project merely to use this helper.

Adapt paths/revisions in one invocation:

```sh
python3 /path/to/receipt/scripts/compare.py --source . --node /path/to/node --spec - <<'JSON'
{"fixed":["regression.test.mjs"],"vary":["app.mjs"],"before":"HEAD^","after":"HEAD","imports":["app.mjs"],"runner":"node","tests":["regression.test.mjs"]}
JSON
```

`fixed` includes current tests, package configuration and required local support;
explicit directories are expanded, including hidden files. `vary` lists existing
implementation files in both versions. For an uncommitted fix use
`"after":{"working_tree":true}`: current bytes/modes, not staged content. Tests
are fixed selected `.js`/`.cjs`/`.mjs` files, never flags, globs or varying files.
`imports` names selected JS **paths**, not package/module specifiers; select the
actual affected modules whose loading must be observed. No early application
imports are added. Native tests load their own modules normally, including static
ESM import, dynamic import and CommonJS require in the verified paths.

Each command is `node --test --test-reporter=tap --import <observer> <test paths>`
from its respective copy. Child temp defaults point inside that copy. The observer
records selected module URL, PID and returned source SHA-256 in the native process;
`copied_loads` retains these records. No matching record, hash mismatch, malformed
record or truncated output leaves `provenance_ready=false`: check 7, CLI 2, no after
execution. Native status is separately retained in `native_exit_code`. A timeout
also stops the comparison. Tests and assertions can already have run before a
missing-load result is detected; this is not a pre-execution security gate.

**A load is not evaluation or dispatch.** Initialization may throw after loading;
a loaded module may not exercise the affected function. Records require at least
one load per selected path, not coverage in every test worker. Later hooks/reassignment
can change behavior. Check the actual native test identities/counts/skips and
defect-specific failure before, success after. CLI 0 means observations collected,
not proof of the fix. A setup error, empty or skipped test is not that evidence.
This is trusted-test observation, not tamper-proof attestation or a sandbox.

Nonempty `NODE_OPTIONS`, `NODE_PATH` or `NODE_COMPILE_CACHE` is rejected rather
than silently discarded. Python `invocation`, `import_roots`, `module_bindings`
are unsupported in this mode. Package maps/custom transformations, inherited
preloads, other Node versions and runtime-required flags need project-native
verification; do not remove required configuration to fit this helper.

Inspect `originals` and `comparison_copies_removed`; do not add a duplicate guard.
Optional `watch` checks extra selected originals without executing/copying them.
Use `guard_tree:true` only for requested whole-project preservation with all reads
authorized. Copies under `.receipt-*` inside `--source` are cleaned on exit;
changed originals abort without restoration. Git identity, working-tree hashes,
shared 20 MB copy budget, selected path restrictions and bounded tree checks apply.
Default deadline is 30 seconds/check (`--timeout` up to 300), retaining the last
12,000 output characters. Remaining process-group members are killed even after
normal exit; no persistent background work. Cleanup may wait five more seconds.
See [resource and preservation limits](comparison-details.md) when those boundaries
matter. None of these checks establishes model token/time savings.
