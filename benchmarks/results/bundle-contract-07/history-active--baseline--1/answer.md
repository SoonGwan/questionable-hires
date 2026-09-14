I’ll trace `display_label` and its current consumers, then check the local history for why the fallback was added. I won’t modify any files.

**Keep the fallback for now.** A current consumer still requires it.

- **Current necessity:** [`partner_label()`](project/consumer.py#L3) passes `{'name': 'Ada'}` without `display_name`. Its comment states that Partner API v1 remains supported through December 2027.
- **Historical intent:** Commit `d5fc972` (“Keep API v1 partners working during migration”) introduced both this consumer and the fallback in [`labels.py`](project/labels.py#L2). Earlier commit `9e7cfdb` used only `payload['display_name']` for internal v2 payloads. That earlier design does not establish that today’s fallback is unnecessary.
- **Verification:** Running the current consumer returned `'Ada'`. Without the fallback, direct indexing raises `KeyError`; using `.get()` returns `None`.

Remove it only after migrating the name-only consumer and confirming the v1 support obligation has ended or changed. All originals were preserved; no files were modified.
