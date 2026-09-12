I’ll use the mother-in-law skill to test normal and reversed response order with a deterministic local harness, without changing production code.

The project has a Python search state object and no browser harness. It uses a generation check to reject stale responses. I’ll test that state boundary by holding two requests open and completing them in both orders.

No stale-result defect reproduced. Both deterministic tests passed:

- Start older, then newer; complete older first: older result is ignored, then newer result appears.
- Complete newer first, then older: newer result remains.

Added [test_search.py](project/test_search.py), using controlled futures without sleeps or external services.

Production code is unchanged. Tested `Search.result`; no browser journey was exercised because this project has no browser harness.
