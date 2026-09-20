I’ll use the con-artist skill to trace the collector binding, run a correct-code baseline, and test one cache-reuse fault in a disposable project-local copy. I’ll leave the four tests and all original files unchanged, then remove the copy.



The tests load `skills/con-artist/scripts/context.py` directly; the similarly named file under `.agents` is not exercised. The stale-context test rewrites a file between two `collect` calls and checks its symbol and hash. I’ll make the copied collector retain its cache per root across calls, which should expose stale data without causing unrelated roots to collide.



The existing tests **detect the cross-invocation cache-reuse fault**.

The tests directly load `skills/con-artist/scripts/context.py`. In-process tracing verified each copied module’s path, `collect` binding, and source hash. The baseline implementation was byte-identical to the original.

The isolated mutation replaced the invocation-local cache with a persistent dictionary keyed by resolved root. Subsequent calls therefore reused cached source, hash, AST, and definition spans.

Both copies ran:

```sh
python3 -B -m unittest discover -s tests -p test_context_line_index.py -v
```

Each child used its copy’s `.test-tmp` as `TMPDIR`; all four tests remained unchanged.

- **Baseline:** all four tests passed, exit 0.
- **Mutant:** three passed; `test_no_stale_spans_after_new_invocation` failed, exit 1.
- **Detecting assertion:** `tests/test_context_line_index.py:86` expected `('old', 'changed')` but received `('old', 'old')`.

Tracing confirmed the mutant skipped rereading the rewritten file and returned the old excerpt and identical hash. The hash assertion at line 87 cannot be credited as an independent detection because the preceding assertion failed. Both runs emitted launcher diagnostics; the mutant’s failure was a concrete assertion mismatch.

This establishes protection against stale snapshots after a same-root, line-selector rewrite. These four tests do not establish freshness for changed excerpt text independently of symbol/hash, refreshed ancestor context, or other selector lifecycle paths.

All disposable copies and instrumentation were removed. Original contents and modes—including notes and caches—were verified unchanged. No fix, test edit, harness, or report was retained.
