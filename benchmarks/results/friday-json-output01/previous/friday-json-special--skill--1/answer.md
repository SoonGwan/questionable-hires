I’ll use the Friday skill to run the helper once, preserve its stdout, and prepare and validate the JSON handoff locally.

The helper exited 0 and saved a complete matrix, including the reader failure `no such table: absent`. Its stdout contains bare `Infinity` and `-Infinity`, so I’ll convert only those numeric values to tags and verify that every other field is preserved.

Handoff ready. Helper ran exactly once and exited **0**; the specified Node consumer exited **0**.

Preserved original stdout verbatim in `native.json`. Created `report.json`, converting only numeric ±Infinity to single-key `float_special` objects. Verified all other fields and observations unchanged.

The `missing` reader remains failed: `no such table: absent`. A complete matrix does not establish release safety. Nothing was deployed.
