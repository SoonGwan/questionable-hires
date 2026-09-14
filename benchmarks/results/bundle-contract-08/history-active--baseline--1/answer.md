I’ll inspect `display_label`, its current consumers, and the local Git history, then recommend whether the fallback can be removed without changing any files.

**I recommend keeping the fallback for now.** A current consumer still requires it.

- **Current necessity:** [consumer.py:5](project/consumer.py#L5) calls `display_label({'name': 'Ada'})`. Its comment states that Partner API v1 remains supported through December 2027.
- **Historical intent:** Commit `d5fc972` (“Keep API v1 partners working during migration”) introduced both this consumer and the fallback. The preceding commit, `9e7cfdb`, accepted only `display_name`. This explains why compatibility was added; the existing consumer demonstrates why it remains necessary.
- **Verification:** Running the current consumer returned `'Ada'`. For that same payload, removing the fallback would return `None` with `.get('display_name')`, or raise `KeyError` with `['display_name']`.

Remove it after migrating or retiring consumers that supply only `name`, consistent with the documented support commitment.

No files were modified; the working tree remains clean.
