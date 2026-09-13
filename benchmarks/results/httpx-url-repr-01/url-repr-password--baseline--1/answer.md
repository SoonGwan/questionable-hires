I’ll inspect the URL masking code and existing assertions, then run the requested tests on disposable baseline and faulty copies, checking import provenance and normal URL controls in each process.

The auth test already asserts the exact masked representation. The URL suite also checks ordinary components, including port, path, query, and fragment. I’ll introduce one fault that leaves the password visible, then run both unchanged test selections and check username-only and no-userinfo controls on each copy.

Covered for the isolated password-masking fault.

Using the supplied interpreter and `pytest -q -p no:cacheprovider` with both requested test selections:

| Check | Result |
|---|---|
| Correct copy | 91 passed |
| Faulty copy: masking assignment replaced with a no-op | 1 failed, 90 passed |
| Username-only and no-userinfo controls | Passed on both copies |

The detecting assertion is [tests/client/test_auth.py:307](project/tests/client/test_auth.py#L307):
`assert expected == repr(httpx.URL(url))`

It expected `URL('http://example-username:[secure]@example.org/')`; faulty behavior exposed `example-password`.

This demonstrates protection for nonempty-password masking while preserving the username, scheme, host, and `/`. Existing URL assertions and additional normal controls verified ordinary components, including port, path, query, and fragment. This single mutation does not establish exhaustive coverage of credential edge cases.

Each check process inspected and verified copied import paths, implementation source, and SHA-256. No network was used. Disposable copies were removed; all 125 original files remained byte-identical. No tests, configuration, warning policy, or production code were changed.
