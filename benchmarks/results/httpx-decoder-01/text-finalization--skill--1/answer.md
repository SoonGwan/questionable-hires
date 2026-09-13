I’ll use the con-artist skill to trace the finalization checks and run one isolated mutation, leaving the original source and tests unchanged.

The streaming test checks only ASCII. The UTF-8 autodetection test reads the response before iterating text, and its input ends with a complete sequence. I’ll change the isolated copy’s flush call from `final=True` to `final=False` to test whether the suite notices a missing replacement character at end-of-stream.

All 40 existing checks pass with both correct and faulty finalization, so the mutation survives. I’m checking a focused assertion for the trailing replacement character, with a valid euro sign split across chunks as the control, through both streaming APIs. The interpreter lacks `coverage`, so I used pytest directly with the repository’s configuration.

Coverage is missing: `tests/test_decoders.py` does not detect lost UTF-8 finalization output.

One isolated mutation changed `TextDecoder.flush()` from `decode(b"", True)` to `decode(b"", False)`, leaving an incomplete sequence buffered at EOF.

| Checks | Correct | Faulty |
|---|---:|---:|
| Existing decoder tests | 40 passed | 40 passed |
| Focused assertions | 6 passed | 3 failed, 3 passed |

The focused checks exercised synchronous streaming and asynchronous streaming under asyncio and trio:

- Incomplete `[b"prefix ", b"\xe2", b"\x82"]`: assert decoded output equals `"prefix \ufffd"`. Faulty behavior returned `"prefix "`.
- Valid split control, adding `b"\xac"`: assert output equals `"prefix €"`. Passed everywhere.

The existing streaming assertion covers ASCII; the autodetection test uses complete sequences and reads the response first.

Commands run in each isolated copy:
```sh
/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python -m pytest -q tests/test_decoders.py
/tmp/qh-httpx-preflight.3Slnqw/venv/bin/python -m pytest -q tests/test_utf8_eof_audit.py
```

`coverage` was unavailable; pytest retained the repository configuration. Imports and caller bindings were verified inside each test process. All 130 original files remain unchanged; disposable copies and assertions are under `utf8-audit-6h_00o1s/`.
