I’ll use the exorcist skill to test the cache suspicion against request completion order, exercising the actual search code locally and leaving production files unchanged.

The code sends `Cache-Control: no-cache`, but each completed search writes directly to the same result field. I’ll hold two requests at a recording request dependency, then release them in normal and reversed order. This will show whether an older response can overwrite the newer result without a cache.

Local evidence supports a completion-order race: `Search.run` overwrites the result whenever a request finishes.

The experiment exercised actual `Search` and transport, recording `Cache-Control: no-cache` on both requests:

- Normal completion (`old → new`): final result was `new`.
- Reversed completion (`new → old`): the older result overwrote `new`.

No cache was involved. The header does not guard against out-of-order result writes. Production incidents remain unconfirmed; request completion and result-update traces would establish whether this mechanism occurs there.

Rerun [the experiment](project/experiments/search_completion_probe.py):

```sh
python3 -B experiments/search_completion_probe.py
```

Passed with bounded waits and owned-task cleanup. Production file hashes stayed unchanged; existing user files were preserved.
