# Con Artist: reusable integrity observations

## Evidence and change

Checkpoint 04's [Con Artist commands](results/bundle-contract-04/persistence-test--skill--1/commands.json)
end with a separate Python block hashing both original files and checking removal
of the owned audit directory. The helper had already checked original bytes and
permission bits in its finally block and exited its temporary-directory context,
but its JSON did not expose that outcome. This is a demonstrated duplicate check,
not proof that every extra command or the entire token overhead comes from it.

The helper now includes `integrity` on returned observations, after original
verification and an explicit absence check for the owned scratch path. It reports
the number of selected files, unchanged selected bytes/modes, and confirmed owned
scratch removal. The default interface explains when to reuse that evidence and
when it is insufficient: unselected files, added files and later commands remain
outside its claim. Existing observed/incomplete and per-check exit semantics stay
unchanged. No additional subprocess, original-file scan or per-file digest output
is introduced; the original verification already runs once in finally.

This also applies to an early return caused by a failed precheck. Successful
cleanup does not turn incomplete test evidence into a completed audit. Changed
originals raise an error and are not restored. Cleanup failure cannot produce
a successful integrity result.

## Author validation, not model performance

Two newly added result-contract tests first failed with missing `integrity`
against the previous implementation; 66 focused tests ran in 12.631s with those
two errors. After implementation, the same 66 tests passed in 12.568s. An
additional cleanup-failure test then exercises real native audit checks with only
the temporary-directory exit deliberately prevented from removing scratch.

The new tests independently inspect unchanged original bytes/modes and absent
scratch; verify failed precheck remains incomplete; deliberately modify an
original and confirm an error without restoration; and leave scratch present to
confirm no successful result escapes. Existing tests continue covering permission
changes, timeouts, native pass/fail probes, import provenance and batch reuse.

No model benchmark was rerun for this change. Removing a reason for duplicate
work is the hypothesis; adoption, net token impact and runtime impact are still
unmeasured. Prior checkpoint costs and featured chart provenance remain intact.

Final local verification: all 397 repository tests passed in 65.252s, including
the cleanup-failure control. Skill validation, repository link/metadata validation,
featured-language synchronization check and diff whitespace check passed.
