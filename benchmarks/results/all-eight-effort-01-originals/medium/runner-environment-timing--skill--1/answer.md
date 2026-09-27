I’ll use the exorcist skill to compare the actual unittest path with the standalone command and identify where the retry setting takes effect. I’ll keep existing files unchanged and run only local Python probes.

I’ll use the existing unittest runner for the comparison, since its import and `setUp` order may explain the difference.

The discrepancy is deterministic import timing.

[test_worker.py](project/test_worker.py#L4) imports `worker` before `setUp`. At import, [worker.py](project/worker.py#L3) reads the absent environment variable and sets `RETRIES=2`. Changing the environment afterward does not update that integer.

Local evidence using the actual test:

| Command | Result |
|---|---|
| `env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker` | Fails: `3 != 1` |
| `env REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker` | Passes: one attempt |

An observation subclass calling the original `setUp` and inherited test confirmed:

```text
before setUp: env=None, worker.RETRIES=2
after setUp:  env='0', worker.RETRIES=2
after cleanup: env=None, worker.RETRIES=2
```

The standalone callback also recorded exactly one attempt when `REQUEST_RETRIES=0` was set before import.

`patch.dict` correctly changes and restores the environment; it cannot recompute an already initialized module variable. No intermittent cache problem is needed to explain this reproduction. Startup configuration matches the stated application behavior; whether live changes should work remains unspecified.

No files were changed, dependencies installed, or external services accessed.
