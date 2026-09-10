I’ll use the exorcist skill to trace the retry path, run local experiments, and assess which safeguards cover the reproduced behavior. I’ll keep this investigative and leave production code unchanged.

The worker uses the job identifier as the provider’s idempotency key, and the project states that retries retain that identifier. I’ll test a failure after sending but before acknowledgment: that should trigger another send call, while the provider should suppress a second delivery. The project has no production logs or provider traces.

The duplicate-email report **did not reproduce under this project’s retry contract**.

| Local experiment | Send calls | Modeled deliveries |
|---|---:|---:|
| Normal processing | 1 | 1 |
| Acknowledgment fails after sending; same job retried with a new worker | 2 | 1 |
| Same body with different keys—a contract-breaking control | 2 | 2 |

The worker sends before acknowledging, so an acknowledgment failure can cause another send attempt. Its safeguard is passing the stable job identifier as `idempotency_key`; the provider suppresses repeat delivery for that key. The experiment confirms that repeated calls do not necessarily mean repeated emails.

This establishes protection for sequential retries against the same local provider instance. It does not establish production behavior: the model uses an in-memory dictionary, and no production logs or provider traces are available.

No code correction is supported by these results. The next decisive evidence would be a reported duplicate’s logical job identifier, both attempts’ idempotency keys, and provider delivery records, to determine whether the stable-key contract or provider suppression failed.

Production code was unchanged; all local assertions passed.
