I’ll use the exorcist skill to trace the retry path, test competing explanations locally, and assess the safeguards without modifying production code.

The worker uses the job identifier as its idempotency key, and the local provider stores only one delivery per key. I’ll simulate acknowledgment failing after delivery, then retry the same job. I’ll also check whether changing the identifier or losing provider state defeats that safeguard.

The report was **not reproduced under the project’s stated contract**.

- Normal processing: 1 send call, 1 modeled delivery.
- Acknowledgment failure after delivery, followed by retry with a fresh worker: 2 send calls, **1 delivery**.
- Another 100 retries: 102 total send calls, **still 1 delivery**.

The safeguard works: [worker.py](project/worker.py#L3) passes the stable job identifier as the idempotency key; [provider.py](project/provider.py#L5) suppresses repeated deliveries for that key. Retrying a send does not itself duplicate delivery.

Controls produced two delivery records when the identifier changed or provider state was replaced. These demonstrate safeguard boundaries, not evidence that either caused the reported incident. The model’s state is instance-local; it does not establish real provider persistence or concurrency guarantees.

No code correction is supported by these results. The next decisive evidence would be the alleged duplicate attempts’ job IDs, idempotency keys, and provider delivery records. Those traces are unavailable in this project.

No files were changed; all experiments ran locally.
