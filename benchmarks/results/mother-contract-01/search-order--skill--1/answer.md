I’ll use the mother-in-law skill to inspect the search contract and existing tests, then add and run a deterministic regression against the actual Search without changing production code.

The contract requires the latest query’s result to remain visible, but Search currently assigns every response to the displayed result. I’ll test a single query and both overlapping completion orders. The tests will observe intermediate display state without imposing an unspecified policy, and assert that the latest result owns the final state.

Reproduced a stale-response failure against actual `Search`:

- Start `ca`, then `cat`, with both requests pending.
- Normal completion: final result is `cat result` — passes.
- Reversed completion: `cat result` appears, then older response overwrites it with `ca result` — assertion fails.

Saved rerunnable coverage in [test_search.py](project/test_search.py) with [controlled_fetch.py](project/controlled_fetch.py). Run from project root:

```sh
python3 -m unittest -v test_search
```

Result: **3 passed, 1 failed**, including a deliberate assertion-control check. Behavior-dependent waits and owned-task cleanup are bounded to one second.

Tested the component layer. Production files and existing user changes remain untouched.
