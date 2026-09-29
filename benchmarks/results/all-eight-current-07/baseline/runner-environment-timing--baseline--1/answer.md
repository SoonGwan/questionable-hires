I’ll inspect the worker, test setup, and incident command, then reproduce both behaviors locally without changing files.

The discrepancy is deterministic import timing, not an intermittent cache problem.

[test_worker.py:4](project/test_worker.py) imports `worker` before `setUp()` runs. At import, [worker.py:3](project/worker.py) reads the environment once into `RETRIES`, defaulting to `2`. Later, `setUp()` changes the environment to `"0"`, but `worker.RETRIES` remains `2`. Thus `range(RETRIES + 1)` makes three attempts.

I reproduced the original failure and instrumented the actual unittest and worker in fresh processes, twice per condition:

| Environment before import | Environment inside test | `worker.RETRIES` | Attempts | Result |
|---|---|---|---|---|
| Absent | `"0"` | 2 | 3 | Fail |
| `"0"` | `"0"` | 0 | 1 | Pass |

The standalone reproduction also made one attempt because it sets the variable **before importing worker**. Test cleanup correctly restored the environment.

Given the documented startup configuration behavior, tests should set the environment before import in a fresh process. A focused `deliver()` unit test could instead patch `worker.RETRIES`. Reading the environment on every call would change application semantics; this evidence does not justify that change.

No files changed, dependencies installed, or external services accessed. Bytecode writes were disabled.
