I’ll use the necromancer skill to trace `display_label`, its current consumer, and the relevant Git history. I’ll keep the review inside this project and leave all files unchanged.

**Keep the fallback.** Removing it would break the current consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) passes `{'name': 'Ada'}` to [`display_label`](project/labels.py#L2). Execution confirmed it returns `'Ada'`; removing the fallback would return `None` with `.get('display_name')`, or raise `KeyError` with direct indexing.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration”) replaced direct `display_name` indexing with the current fallback. This establishes migration intent; the current consumer demonstrates why it remains necessary.
- **Removal condition:** Name-only payloads must still produce their labels. The consumer documents v1 support through December 2027, though that comment alone isn’t proof of the contract. Before removal, migrate or normalize this consumer’s input and verify that supported callers no longer depend on the fallback.

No files were modified; the existing untracked `.agents/` directory was preserved.
