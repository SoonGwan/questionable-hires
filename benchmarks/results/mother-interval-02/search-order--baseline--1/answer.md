I’ll inspect Search and the local test setup, then add a rerunnable test with controlled request completion order without changing production code.

Search assigns each response when it completes, so a slow earlier query appears able to overwrite a completed newer result. I’ll test both orders with gated responses. The normal-order test will assert the display only after both requests finish; the reversed-order test will check that the latest result survives the older response.

Reproduced a stale-response bug in actual `Search`:

- Normal completion: passes; latest result remains after both requests finish.
- Reversed completion: fails; older `"ca"` overwrites completed `"cat"`.

The test controls overlapping responses, bounds waits, and cleans up owned tasks. Production files are unchanged.

Rerun: `python3 -B -m unittest -v test_search_overlap.py`

[Test](project/test_search_overlap.py) · [Captured controls and assertions](project/search_qa_results.txt)
