I’ll read the Con Artist instructions and recipe, invoke the helper once with the specified interpreter, and review only the evidence it returns.

The single helper invocation exited **2**, returning **incomplete**: project preservation failed because `notes.txt` changed. The authorized fixture effect does not override that failure.

| Code | Native unittest outcome | Exact-value probe |
|---|---|---|
| Original (`1`) | 1 test passed; exit 0 | Passed; exit 0 |
| Mutant `2` | 1 test passed; exit 0 | Exit 1: `AssertionError: 2` |
| Mutant `3` | 1 test passed; exit 0 | Exit 1: `AssertionError: 3` |
| Mutant `4` | **Unrun** | **Unrun** |

The failing probes checked `service.value() == 1`. Native passing tests did not print assertion values. No returned execution timed out or had truncated output.

Each executed check verified copied `service.py` imports under its project-local disposable directory. Reported SHA-256 prefixes were `5d080563…` (original), `d3fe3723…` (`2`), and `86508686…` (`3`). These establish copied module provenance, not code-object identity.

For mutant `3`, both correct-code checks referenced mutant `2`’s original observations; neither baseline executed again. Six checks executed total.

Selected original bytes/modes and owned-copy cleanup were verified for both audits. The first whole-project inventory, including Git metadata, passed; the second reported only `notes.txt` changed. Thus whole-project preservation failed and the batch cannot be called successful.

No retry, separate tests, repair, restoration, report, or harness was created.
