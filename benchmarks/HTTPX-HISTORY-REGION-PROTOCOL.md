# Real-checkout region-first transfer

One new development review on HTTPX checkout `26d48e0634e6ee9cdc0533996db289ce4b430177`.
This checkout is shallow; missing historical origin must not be invented. The
current Necromancer entrypoint is `18a2070`, collector `ae99bac`. Freeze this
protocol commit before execution. Two fresh Astra medium sessions, skill then
baseline, serial, one repeat, 360-second timeout, no retries/exclusions. Use
`run.run_cell` with `project_source` to preserve the actual checkout and its Git
history, not a synthetic subset. No earlier answers or author oracle supplied.

## Identical task

Review whether the `if not text` early return in `LineDecoder.decode` in
`httpx/_decoders.py` can be removed. The adjacent comment says empty text does not
occur in practice because other internals filter it. Establish current necessity
through the actual Response line-iteration path, comparing current and proposed
behavior with an ordinary input control. Explain what local Git evidence does
and does not establish about the historical reason. Do not modify original source
or tests, use network access, or install dependencies. Temporary diagnostic
artifacts must stay inside the project. Use the preinstalled interpreter
`/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python` for Python commands. The existing
`tests/test_decoders.py` cannot currently collect because `chardet` is missing;
report that limitation and use available local facilities for behavioral checks.

## Frozen assessment

Inspect actual current/proposed public Response behavior, an ordinary control,
surrounding state transformations and caller logic, preservation of original
files, and accurate shallow-history uncertainty. The author has verified a
reachable difference using in-memory AST substitution; do not give its input or
expected outcome to model sessions. Runtime evidence must be in original logs.
Do not require a helper, full suite, particular mutation technique, or a longer
answer. Count token/time costs and failed actions even if the conclusion is right.
Compare necessary context collection and duplicate reads, not command count alone.
One pair cannot demonstrate broad superiority or isolate wording causally.
