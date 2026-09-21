# Optional Python source collection

For a design review with known Python definitions not yet read, run the installed
skill's helper directly; reading its implementation first is not necessary:

```sh
python3 -B /path/to/landlord/scripts/context.py --root /authorized/project \
  --max-output 12000 service.py:Store.save callers.py:save_record
```

Supply 1–8 project-relative files, `file:qualified.definition` or `file:line`
selectors. Named/line selections retain complete definitions, decorators and line
numbers. Use `--all-matches` for every same-name leaf definition (for example,
overloads); it does not choose the runtime implementation. Ambiguous parents fail.
For unknown names use project search or an unqualified file: large Python files
return an index only when smaller than full source. An index is not reviewed code.
`--full` reads complete selected files; it does not override explicit selectors.

The output also includes complete selected-path ancestor instructions and pytest
configuration inside the root, and ancestor conftest indexes. Host instructions
still apply; parent-root instructions are not discovered. Excerpts do not resolve
imports, enclosing conditions, globals, assignments, dependencies or runtime
bindings. Inspect these where they change the review. Collection is not consumer
coverage or execution evidence; use native tests for runtime questions.

`--max-output` limits complete JSON characters including its final newline, not
tokens. Choose room within the enclosing tool response; the example is not a
token-fit guarantee. Default100000; range1–100000. Output never silently drops
instructions or cuts source: over-limit context exits2 with no stdout. Narrow
selectors or use project tools on failure. Python3.9+, UTF-8 regular files only;
256KB/file,2MB input. No imports, subprocesses or writes; symlinks/traversal/Git
internals refused. Stable files are required; this is not an atomic snapshot or
sandbox. Source/configuration may be private. Reuse unchanged context rather than
collecting it again; direct native reads remain appropriate for simpler cases.
