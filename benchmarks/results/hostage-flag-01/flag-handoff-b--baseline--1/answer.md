I’ll compare the requirements, parser, caller, and existing tests, fix any contract defects, then retain and inspect the native unittest output with its command and exit status.

`flags.py` and `worker.py` already match the contract, so I’ll leave production code unchanged. I’ll extend the tests for all accepted spellings, normalization, both defaults, invalid values, caller behavior, and mapping preservation.

No contract defects found; production code remains unchanged. Added 11 unittest tests, preserving both existing tests.

Inspected retained native evidence: `python3 -B -m unittest discover -v` ran **13 tests, all passed**, exit **0**.

New evidence files:
- `verification/unittest-h0v70lhq/command.txt`
- `verification/unittest-h0v70lhq/native-output.txt`
- `verification/unittest-h0v70lhq/exit-code.txt`

Earlier evidence and unrelated notes remain untouched.
