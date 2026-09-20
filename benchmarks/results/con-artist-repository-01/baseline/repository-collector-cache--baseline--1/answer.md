I’ll trace which collector the tests actually load, run an unchanged baseline in a disposable copy, then inject a cross-call cache-reuse fault into a second copy and check the assertion results. I’ll remove both copies afterward and preserve the original files.

The tests load `skills/con-artist/scripts/context.py` directly by file path. `collect()` currently creates a fresh cache for each call; that cache stores source text, hashes, parsed trees, and line spans.

I’ll change only the copied collector to reuse one cache across calls, keyed by relative path. This should exercise both stale data after an edit and collisions between projects containing `module.py`. The freshness test checks symbols before hashes, so a symbol failure will prevent its hash assertion from running.

The baseline passed all four tests, and the binding check confirmed it loaded the byte-identical copied collector. The native launcher also left files in the copy’s temporary directory, which tripped my extra cleanup check after the tests passed. The copy was removed and the originals verified unchanged. I’ll rerun both cases and remove the whole disposable directory, including those launcher files.

The existing suite **detects the injected cross-invocation cache-reuse fault**.

Tests directly load `skills/con-artist/scripts/context.py`. I verified the copied module path, `collect` code filename, and SHA-256 identity. Both runs used the required native command, unchanged tests, and copy-local `TMPDIR`.

The mutation replaced `collect()`’s fresh cache with a module-level shared dictionary keyed by relative path.

| Test | Baseline | Mutant |
|---|---|---|
| All-line resolution parity | Pass | Pass |
| Eight selectors / one span walk | Pass | Pass |
| Equal-span ambiguity | Pass | Pass |
| Freshness after another invocation | Pass | **Fail** |

The detecting assertion was at `tests/test_context_line_index.py:86`:

```python
self.assertEqual((before['symbol'], after['symbol']), ('old', 'changed'))
```

Actual result: `('f0', 'f0')`. The earlier eight-selector test populated `module.py`; the shared cache then reused that other project’s context for both freshness-test calls.

Coverage limits:

- The subsequent hash-inequality assertion passed on baseline but was **not reached** in the mutant run.
- No assertion checks excerpt contents, despite the eight-selector test’s name.
- Requested lines are checked within one invocation, not after edits.
- Named-selection freshness and ambiguity across calls lack explicit coverage.
- Cross-project contamination is detected through test ordering rather than a dedicated assertion.

All disposable copies were removed, including after the initial cleanup-check failure. All 57 original entries retained their contents and modes, including owner notes/cache. No fix, test changes, harness, or report remains.
