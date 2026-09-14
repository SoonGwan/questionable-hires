I’ll use the con-artist skill to trace the exception checks and run a narrow mutation in a disposable project copy, leaving the original source and tests unchanged.

Both exception tests use the default transport setting and expect `RuntimeError` through the real client call—before a response and after a completed response. I’ll change only the copied constructor default to `False` to check whether those assertions detect swallowed exceptions.

Coverage is adequate for the targeted fault; no stronger test is needed.

In an isolated project copy, I changed only `ASGITransport`’s `raise_app_exceptions` default from `True` to `False`.

Using the specified interpreter and pytest arguments `-q -s tests/test_asgi.py`:

- Baseline: **24 passed**, exit 0.
- Mutant: **4 failed, 20 passed**, exit 1.
- `test_asgi_exc` and `test_asgi_exc_after_response` each failed on asyncio and trio with **`DID NOT RAISE RuntimeError`**.

These assertions detect swallowed application exceptions both before and after response completion. Copied imports and client dispatch bindings were verified in each test process.

An initial diagnostic-plugin setup warning was corrected before collecting these results; it was not counted as mutation evidence. Original files remained unchanged, and disposable copies were removed.
