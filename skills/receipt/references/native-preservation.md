# Preserve originals around a project-native comparison

Python 3.9+/POSIX. Use this optional API only when native project setup is required and an adequate
preservation check is missing. Existing `compare.py` already supplies a guard;
do not wrap it in another guard. This API reuses that bounded inventory without
changing the project's runner, environment or startup hooks.

Load `scripts/preserve.py` by its actual installed path using `importlib.util`:

```python
spec = importlib.util.spec_from_file_location("receipt_preserve", helper_path)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
```

Place the existing native comparison and its cleanup inside
`with support.preserved_tree(project_root) as preservation:`. Remove all owned
copies inside that block, including failure paths, then inspect/print the report
after normal context exit. Loading the module or entering an empty block does
not execute tests. Run orchestration with bytecode writing disabled (`python -B`)
so importing support does not add cache files to the tree being preserved.

The guard performs exactly one bounded inventory before and one after the block.
It starts with `unchanged: null`; successful comparison produces `unchanged: true`,
entry/byte counts and a digest. It includes Git/ignored entries, root/directory
modes, regular-file bytes/modes and symlink text. It does not follow link targets.
Use only with authorized whole-root reads. Limits are 10,000 entries and 20 MB
streamed per inventory; special files and overflow fail closed.

Changed or retained entries raise without restoring anything. Caller exceptions
still propagate when preservation passes; if both workflow and preservation
fail, the preservation error retains the original exception as its context.
Unknown/failed preservation is not a success report. An unchanged report says
nothing about test success: native commands/exits/assertions, identical inputs,
revision identity and same-process import evidence remain the caller's job.
This API neither copies revisions nor runs/supervises subprocesses nor cleans up.

Not a sandbox or an atomic snapshot. No protection against outside-root effects,
concurrent/restored changes, timestamps, ownership, ACLs/xattrs or changes outside
the context interval. Do not broaden access or waive required checks to use it.
