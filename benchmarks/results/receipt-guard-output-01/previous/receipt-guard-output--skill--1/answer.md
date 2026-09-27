I’ll read the Receipt skill, inspect the recipe and helper interface, then run the comparison exactly once with the specified Python interpreter. I’ll report the returned evidence and any gaps without repairing or restoring anything.


Ran exactly once with unchanged `recipe.json`:

```sh
<TEMP> -B .agents/skills/receipt/scripts/compare.py --source . --spec recipe.json
```

CLI exit: **2**. Returned:
> Comparison not established: Selected originals changed; not restored: notes.txt

- **Unavailable:** before/after results, native test exits, actual assertion values, imported code identity and whole-tree preservation result. No execution outcomes inferred from source.
- **Preservation failed:** `notes.txt` changed from `original\n` to `changed!\n`; the authorized side effect remains untouched. Checked remaining project files, Git index and HEAD retained their hashes and modes.
- **Cleanup:** no `.receipt-*` copies remained; the CLI returned no structured cleanup field.

No repair, restoration, repeat comparison, separate test execution or new report/harness.
