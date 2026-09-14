I’ll trace `display_label`’s current consumers and local Git history, then assess whether the fallback is still needed. I won’t modify any files.

I recommend **keeping the `name` fallback for now**.

- **Current necessity:** [`partner_label()`](project/consumer.py#L3) passes only `{'name': 'Ada'}` and documents API v1 support through December 2027. I verified it currently returns `'Ada'`. Removing the fallback would return `None` with `.get('display_name')`, or raise `KeyError` with direct indexing.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration”) introduced both the fallback and that consumer. The earlier commit `9e7cfdb` supported only `display_name` for internal v2 payloads. That original scope does not establish that today’s fallback is unnecessary.

Remove it after supported v1 callers are migrated or their payloads are normalized before calling `display_label`. Also account for its current handling of empty `display_name` values, which fall back to `name`.

All inspection stayed within this project. No files were modified; originals were preserved.
