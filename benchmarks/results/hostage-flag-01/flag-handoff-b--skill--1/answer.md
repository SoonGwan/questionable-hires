I’ll use the hostage-negotiator skill to check the contract, make only necessary fixes, and extend the native tests. I’ll retain and inspect the test output, exact command, and exit status in fresh project-local files.



`flags.py` and `worker.py` already satisfy the contract, so production code can stay unchanged. I’ll add tests for all accepted spellings, normalization, defaults, invalid values, caller behavior, and mapping preservation on both success and error paths.



No contract defects found; production code remains unchanged. Added six native tests covering the requested cases and mapping preservation, retaining both existing tests.

Ran `python3 -B -m unittest discover -v`: inspected native evidence confirms **8 tests passed**, exit **0**. Diff checks passed.

Fresh retained evidence:
- `.test-evidence.wE1EgE/argv.txt`
- `.test-evidence.wE1EgE/output.txt`
- `.test-evidence.wE1EgE/exit.txt`

Earlier evidence and unrelated notes were preserved.
