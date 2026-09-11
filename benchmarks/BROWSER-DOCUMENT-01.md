# Full-document departure and fresh return

Author-side browser check, local Chrome 152.0.7977.83. Run the existing
`benchmarks/browser/input-check.mjs` with the installed Chrome executable path.
All six fill/keyboard and guard variants completed successfully, including prior
ordering, clearing, recovery and same-document disposal assertions.

After starting an unresolved search request through real input, the workflow
clicks a local link to `away.html`. It verifies the destination document and lack
of the search fixture there; the old document handle can no longer execute.
It then navigates freshly to the original configured URL, observes an empty
request inventory and result, and submits/completes a new request successfully.
No page errors are observed. Network requests remain blocked by the existing
context route; no backend, purchases or external services are involved.

This checks full-document departure and a **fresh navigation back**, not browser
Back/Forward Cache restoration. It does not settle a request in the destroyed
document, prove server cancellation, or test persistent/shared-worker state.
Those require different fixtures. It is not model-driven QA or efficiency evidence.
Existing in-process watchdog limitations remain unchanged.
