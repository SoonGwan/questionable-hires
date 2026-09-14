I’ll use the hostage-negotiator skill to check the contract, make only necessary fixes, and extend the native tests. I’ll retain each verification run’s output, command, and exit code, then inspect that evidence before reporting results.

`read_flag` incorrectly treats every nonempty string as true. Its missing/`None` handling and `worker_options` already match the contract. I’ll fix string parsing and add coverage for the required inputs, caller behavior, and mapping preservation, keeping both existing tests.

Fixed `read_flag` string parsing to match the contract. Preserved valid default handling, `worker.py`, and existing tests. Added coverage for spellings, whitespace/case, defaults, invalid inputs, caller behavior, and mapping preservation.

Inspected retained native evidence: `python3 -B -m unittest discover -v` ran **8 tests, all passed**, exit **0**. Diff check passed.

New evidence files:
- `.test-evidence.lDnty2/argv.txt`
- `.test-evidence.lDnty2/output.txt`
- `.test-evidence.lDnty2/exit.txt`

Earlier evidence and unrelated notes remain untouched.
