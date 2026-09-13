I’ll use the con-artist skill to trace the clearing assertions, run one isolated mutation, and check domain-only clearing on both versions. I’ll leave the original source and tests unchanged.

The path test checks that one cookie remains, then deletes the cookie at the other path and checks that the jar is empty. I’ll mutate `clear` to ignore the path, making it clear the whole requested domain. This should trigger the existing length assertion. The domain-only control will also check exactly which cookie survives.

Existing coverage **detects the scoped-clearing fault**. In an isolated copy, I removed forwarding of `path`, causing `clear(domain=..., path=...)` to clear the entire domain.

- Correct code: **7 passed**.
- Mutated code: **6 passed, 1 failed**. `test_cookies_with_domain_and_path` detects it at `tests/models/test_cookies.py:50`: `assert len(cookies) == 1` observes **0**.
- Domain-only control: **passed on both versions**, including an exact assertion that both target-domain cookies disappeared and the different-domain cookie survived.

Scope limitation: the existing path test contains only one domain, so this demonstrates protection against losing the sibling path, not different-domain preservation during path-scoped clearing.

Used the specified interpreter and audit helper with pytest arguments `-v tests/models/test_cookies.py`. Copied imports were verified, disposable copies removed, and originals remained unchanged. No new tests are needed for the detected fault.
