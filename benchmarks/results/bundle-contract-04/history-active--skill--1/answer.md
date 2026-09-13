I’ll use the necromancer skill to check `display_label`, its current consumers, and the relevant Git history. I’ll keep the review inside this project and leave all files unchanged.


**Keep the fallback for now.** Removing it breaks the current consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) passes `{'name': 'Ada'}` to [`display_label`](project/labels.py#L1). Execution returned `'Ada'`; an in-memory simulation using only `payload.get('display_name')` returned `None`. Direct indexing would instead raise `KeyError`.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration,” January 2, 2026) introduced both the fallback and this consumer. This establishes the migration rationale.
- **Supporting context:** [`consumer.py:3`](project/consumer.py#L3) documents v1 support through December 2027. The executable consumer—not that comment alone—demonstrates the present dependency.

Name-only payloads must continue producing a label. Before removal, migrate the consumer or provide equivalent normalization, with evidence that supported v1 inputs no longer require this behavior.

No files were changed; originals and existing user changes were preserved.
