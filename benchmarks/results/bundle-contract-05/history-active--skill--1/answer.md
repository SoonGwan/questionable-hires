I’ll use the necromancer skill to check `display_label`, its current consumers, and the relevant Git history. I’ll keep the review inside this project and leave all files unchanged.

**Keep the `name` fallback for now.** Removing it breaks the current consumer.

- **Current necessity:** [consumer.py:5](project/consumer.py#L5) calls `display_label({'name': 'Ada'})`. In-memory verification returned `'Ada'` today; removing the fallback returned `None` with `.get('display_name')`, or raised `KeyError` with direct indexing.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24`, “Keep API v1 partners working during migration” (January 2, 2026), replaced direct `display_name` indexing with the fallback and added that consumer. This establishes migration compatibility as its purpose.
- **Supporting documentation:** The consumer says API v1 remains supported through December 2027. The executable caller, independently of that comment, demonstrates the present dependency.

The condition to preserve is that name-only partner payloads produce their label. Before removing the fallback, migrate or normalize the current consumer’s input and confirm that supported callers no longer require name-only compatibility.

No files were modified; originals and the existing untracked `.agents/` directory were preserved.
