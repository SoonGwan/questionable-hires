I’ll trace `display_label` and its current consumers, then check the local history for why the fallback was added. I won’t modify any files.

**I recommend keeping the fallback for now.**

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) calls `display_label({'name': 'Ada'})`. Its comment states that Partner API v1 remains supported through December 2027. Removing the fallback would break this existing consumer.
- **Historical intent:** Commit `d5fc972` (“Keep API v1 partners working during migration”) introduced both the fallback and this consumer. Earlier commit `9e7cfdb` used only `payload['display_name']` for internal v2 payloads. That original scope explains the earlier implementation; it does not establish that the fallback is unnecessary today.
- **Verification:** The current consumer returns `'Ada'`. For its payload, direct `display_name` access raises `KeyError`; using `.get('display_name')` alone returns `None`.

Remove the fallback after migrating this consumer and ending or otherwise accommodating v1 support. No files were modified; the working tree remains clean.
