I’ll use the exorcist workflow to compare the test’s effective retry setting with the standalone run, then reproduce the difference through the actual worker. I’ll keep the project files unchanged and use only local Python commands.

The code points to an import-time setting: `worker.RETRIES` is read when `test_worker` imports `worker`, before `setUp` changes `os.environ`. I’ll verify the values at those two points in fresh processes and run the existing failing test.

The discrepancy is deterministic. [test_worker.py](project/test_worker.py#L4) imports `worker` before `setUp` sets `REQUEST_RETRIES=0`. At import, [worker.py](project/worker.py#L3) reads the absent variable and fixes `RETRIES` at its default of 2. Changing the environment afterward does not change that value.

With `REQUEST_RETRIES` absent, the existing unittest failed with **3 calls instead of 1**. A probe using the actual `setUp` confirmed `REQUEST_RETRIES=0` while `worker.RETRIES=2`, followed by three calls through `worker.deliver`. In a fresh process with `REQUEST_RETRIES=0` set *before* import, the same worker made one call. This supports import timing, not an intermittent cache problem. `setUp` patches the environment, but it cannot change a value already read at import.

No existing files were modified.
