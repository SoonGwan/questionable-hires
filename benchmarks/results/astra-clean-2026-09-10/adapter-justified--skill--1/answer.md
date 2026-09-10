I’ll use the landlord skill to inspect the adapter, its consumers, and project conventions, then recommend whether to keep, simplify, or remove it. I won’t edit files.

**Keep the adapter.** Its compatibility boundary pays for itself even with one consumer.

- [requirements.md](project/requirements.md#L1) establishes a current need: both provider schemas remain in production, migration is independent of invoice releases, and schema handling belongs in the adapter.
- [adapter.py](project/adapter.py#L1) confines that compatibility obligation to one small function. Inlining it into [invoice.py](project/invoice.py#L3) would make invoice code responsible for provider schema changes.

No unnecessary dependencies or configuration surfaces are present. Keep it as-is; revisit the fallback when v1 is retired.

Static review only; no files edited.
