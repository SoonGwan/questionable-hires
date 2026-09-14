I’ll use the necromancer skill to trace `display_label` through its current consumers and Git history, without changing any files.

**Keep the fallback for now.** Removing it breaks a current consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) passes `{'name': 'Ada'}` to [`display_label`](project/labels.py#L1). An in-memory check returned `'Ada'` today; removing the fallback returned `None`, or raised `KeyError` when requiring `display_name`. The consumer also documents API v1 support through December 2027.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration”) replaced direct `display_name` access with the fallback and added that consumer. Its patch establishes migration compatibility as the original purpose; the current caller and reproduced failure establish necessity today.

Preserve support for name-only payloads. The smallest next step toward removal is migrating or normalizing the partner input first. Also account for the existing fallback on empty or otherwise falsy `display_name` values.

No files were changed; all originals and existing user changes were preserved.
