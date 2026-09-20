I’ll attempt the supplied patch unchanged and capture its exit and output. If it fails, I’ll inspect the requirements and current code, adapt only `options.py`, then run the specified tests.

`git apply requested.patch` failed with exit 1: `error: patch failed: options.py:1` and `error: options.py: patch does not apply`. The current code uses `or 100`, which replaces explicit zero with the default. I’ll apply the patch’s intended `None` check to the current code.

Updated only `options.py`: missing/`None` defaults to 100; zero and positive integers are preserved without changing input.

Initial `git apply requested.patch` exited **1**:
```text
error: patch failed: options.py:1
error: options.py: patch does not apply
```
The adapted edit applied successfully before testing.

`python3 -B -m unittest discover -v`: **4 tests, all passed; test-process exit 0**.

Preserved the patch, existing tests, other original files, HEAD, and runner-generated log.
