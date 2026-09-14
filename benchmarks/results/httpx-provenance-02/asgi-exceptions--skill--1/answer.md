I’ll use the con-artist skill to trace the exception-propagation checks and run one narrow mutation in a disposable project copy, leaving existing files untouched.

Two tests expect `RuntimeError` with the default transport settings: one before a response and one after the response body is sent. They call the real ASGI transport through `AsyncClient`. I’ll change only the copied constructor default from `True` to `False` to check whether those assertions detect swallowed exceptions.

Coverage is adequate for the targeted fault. No stronger test is needed.

Using the specified interpreter and the skill’s isolated audit helper, I ran `pytest -q tests/test_asgi.py`:

- **Baseline:** 24 passed, exit 0.
- **Mutation:** changed only the copied `ASGITransport` default from `raise_app_exceptions=True` to `False`.
- **Result:** 4 failed, 20 passed, exit 1. Both `test_asgi_exc` and `test_asgi_exc_after_response` failed on asyncio and trio with **`DID NOT RAISE RuntimeError`**.

These assertions detect swallowed application exceptions both before and after a completed response. The runner verified imports from each isolated copy. Original file bytes and modes remained unchanged, and disposable copies were removed.
