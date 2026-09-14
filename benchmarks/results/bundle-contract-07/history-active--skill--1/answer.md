I’ll use the necromancer skill to trace `display_label`, its current consumer, and the relevant Git history, without changing any files.

**Keep the fallback for now.** Removing it breaks the current consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) passes `{'name': 'Ada'}`. Execution confirmed it returns `'Ada'`; removing the fallback yields `None` with `.get('display_name')`, or `KeyError` with indexing.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration”) replaced direct `display_name` indexing with the fallback and introduced that consumer. The patch supports the migration rationale; the current executable consumer establishes today’s dependency.
- **Behavior to preserve:** [`display_label`](project/labels.py#L2) uses `name` when `display_name` is missing or falsy. The consumer also documents v1 support through December 2027, though that comment alone does not prove necessity.

The smallest prerequisite for removal is migrating the consumer to provide `display_name` while preserving supported v1 inputs through normalization elsewhere.

No files changed; existing user changes were preserved.
