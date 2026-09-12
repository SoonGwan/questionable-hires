# Browser clearing regression

Author-side check on local Chrome 152.0.7977.83, using the existing installed
Playwright dependency. No model session, dependency install or external page.

```sh
node benchmarks/browser/input-check.mjs '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

The extended workflow completed successfully in six fresh contexts: fill and
keyboard input, each against unguarded, fully guarded and view-disposal-mutated
variants. Earlier assertions for response ordering, focus, recovery and
same-document view disposal still execute before the added sequence.

The new sequence enters a nonempty query, clears it via fill or select-all plus
Backspace, completes the empty query with an empty result, then completes the
older query. Captured input records assert browser-trusted events and an actual
empty query submission. Empty results initially render empty in every variant.
The two unguarded variants then show `pre-clear result`; the four request-guarded
variants remain empty, including those whose separate view-disposal guard is
disabled. Input focus remains on the search field. No page errors are observed.

This is a deliberate synthetic browser regression, not browser-model QA or a
performance comparison. Completion is emitted only after browser cleanup. The
existing workflow watchdog remains an in-process timer, not OS containment.
Full-document navigation, a real backend and model-driven browser use remain
outside this check. No original model benchmark result is rescored.
