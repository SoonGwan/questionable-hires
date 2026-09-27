I’ll read the Con Artist skill and recipe, run the helper exactly once with the specified interpreter, and review the returned evidence.



The single helper invocation exited **2**: `Audit not established: Project tree changed during audit; not restored (1 paths): notes.txt`.

- No native original/mutant outcomes, assertion values, copied-import identities, or baseline references were returned. Baseline reuse and which mutations executed or remain unrun are therefore unavailable—not inferred from source.
- Before/after inventories verified that only `notes.txt` changed, from `original\n` to `changed!\n`. All other bytes/modes and Git metadata remained unchanged; Git status now reflects the authorized note change.
- No owned `.con-artist-*` copies remain. Cleanup was independently verified, although the helper returned no integrity report.

The preservation failure prevents a successful-audit conclusion. The note was left unchanged afterward; no rerun, repair, restoration, report, or harness was created.
