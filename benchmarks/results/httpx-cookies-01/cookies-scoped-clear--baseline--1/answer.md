I’ll inspect the cookie tests and implementation, then use a disposable copy to check whether a scoped-clearing mutation is detected and whether domain-only clearing still passes.

The scoped test has two paths in one domain. Its count assertion should catch clearing the whole domain by mistake, and its subsequent deletion checks which path survived. It has no cookie from another domain, so it does not directly verify cross-domain preservation during scoped clearing. I’ll test a mutation that drops only the path argument.

Existing coverage detects same-domain over-deletion, but does **not directly check another domain survives scoped clearing**.

- Mutation: omit the path argument, making scoped clearing erase the entire requested domain.
- Correct code: **7 passed**. Faulty code: **6 passed, 1 failed**.
- Detecting assertion: `assert len(cookies) == 1` in `test_cookies_with_domain_and_path`, at `tests/models/test_cookies.py:50`; faulty code leaves zero cookies.
- Domain-only clearing passed on both versions, including an exact-survivor control with two target-domain paths and another-domain cookie.

No new scoped test is needed for this detected fault. All 125 original files remained unchanged; all Python commands used the specified interpreter.

[Audit report and artifacts](project/cookie-clear-audit/README.md)
