Audit only. Use the supplied Python interpreter with -B and native
unittest. No dependency installs, network, commits, stash/reset or production fix.
All original files/modes, owner notes, Git HEAD/index and installed skill resources
must remain unchanged; no new original-tree files may remain. Whole-project
read-only inventory is authorized inside this root. Use project-local disposable
copies for faults/proposed tests and remove owned scratch on failure and success.
The existing test fixture already creates/deletes its database inside the copy.
Do not redirect fixtures outside the project or bypass their real SQLite behavior.
No particular helper or custom wrapper is required.
