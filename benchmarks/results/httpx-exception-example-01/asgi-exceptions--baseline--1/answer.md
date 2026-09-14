I’ll inspect the ASGI tests and transport, then run a narrow mutation in a disposable copy to check whether the tests catch broken default exception propagation.

Both exception tests omit `raise_app_exceptions` and expect `RuntimeError`: one raises before a response, the other after the response completes. I’ll change only the constructor default from `True` to `False` in the mutation copy and run the unchanged test file against both copies.

Coverage is adequate for the targeted fault. No stronger test is needed.

- Baseline: **24 passed**.
- Isolated mutation: changed only the `ASGITransport` constructor default from `raise_app_exceptions=True` to `False`.
- Mutant: **4 failed, 20 passed**. `test_asgi_exc` and `test_asgi_exc_after_response` each failed on asyncio and trio with **DID NOT RAISE RuntimeError**.

This demonstrates protection of default exception propagation both before and after response completion.

Used the specified interpreter; installed nothing. Original files remained unchanged, verified by hashes. Copies, logs, and mutation diff are in asgi-audit-4y14a2b2.

Export note: the local-directory link was removed because this export contains selected source excerpts, not that complete retained directory. Original command output and the full diff remain available.
