I’ll use the necromancer skill to trace `display_label`, check its current consumer, and inspect the relevant Git history without changing any files.

**Keep the fallback for now.** Removing it breaks an existing consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) calls `display_label({'name': 'Ada'})`. A read-only verification returned `'Ada'` today and `None` with an in-memory replacement using only `payload.get('display_name')`. Requiring `payload['display_name']` would instead raise `KeyError`.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24`, “Keep API v1 partners working during migration,” replaced direct `display_name` indexing with the [current fallback](project/labels.py#L2) and introduced that consumer. This establishes migration compatibility as its purpose; the current call establishes that compatibility is still needed. The [consumer comment](project/consumer.py#L3) also states support through December 2027.

Preserve name-only payloads returning their `name`. The smallest next step toward removal is to migrate this consumer and establish that supported API v1 inputs no longer need that behavior.

No files were changed; originals and existing user changes were preserved.
