I’ll use the con-artist skill to trace the assertions, run the baseline and one isolated masking fault, and check the normal URL controls. I’ll inspect imports in each check process and remove the disposable copies afterward.

The auth test directly checks for `example-username:[secure]`; the URL suite also checks representations with ordinary URL components. I’ll replace only the password-masking assignment with `pass` in the disposable copy, then run the unchanged tests and both normal controls.

The existing tests **detect the masking fault**.

Both isolated copies ran with the supplied interpreter and unchanged arguments:

```text
-m pytest -q -p no:cacheprovider tests/models/test_url.py tests/client/test_auth.py::test_auth_hidden_url
```

- Correct code: **91 passed**, exit 0.
- Masking assignment replaced with `pass`: **90 passed, 1 failed**, exit 1.
- Detecting assertion: `tests/client/test_auth.py:307`, `assert expected == repr(httpx.URL(url))`. It expected `example-username:[secure]` and received `example-username:example-password`.

Username-only and no-userinfo controls passed on both versions. Captured password-case representations preserved the username, scheme, host, port, path, query, and fragment; only masking differed.

Each check process verified copied implementation paths, hashes, and URL/parser bindings. The URL suite alone survived this fault; the auth assertion caught it. This establishes protection against this specific masking omission, not every representation defect.

Disposable copies were removed. Original source, tests, configuration, and warning policy were preserved. No network, installations, retained artifacts, fixes, commits, or publication.
