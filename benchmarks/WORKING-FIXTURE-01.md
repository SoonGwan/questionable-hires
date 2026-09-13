# Preserve uncommitted starting state without crediting it to the model

The authored fixture runner now accepts optional `working_files`, a mapping of
canonical project-relative paths to text. After deterministic history commits,
it writes these files without committing or staging them. This enables a task
that starts with an already-present uncommitted fix and current regression tests.
It does not change any existing fixture or allow dirty external source checkouts.

Before the model starts, an isolated temporary Git index records a commitless
tree of the initial contents, including explicit ignored working inputs. The
normal index remains unchanged and HEAD retains the fixture history. The temporary
index is removed; tree/blob objects remain in the owned synthetic repository.
No extra preparation cost enters model-process timing.

- `base_commit` remains the actual historical commit.
- `initial_tree` identifies the prepared Git content used as the diff reference,
  not a commit or user-created revision.
- `initial_working_files` records hashes for explicit working inputs.
- `initial.diff` shows their initial tracked/untracked/ignored changes relative
  to the base. The exporter preserves this artifact.
- `changes.diff` measures final content against the initial tree, not against
  old HEAD. Existing user-like modifications are not counted as model edits.

All paths are validated before repository creation; traversal, noncanonical
paths, Git/skill internals and non-text inputs are rejected. `working_files`
is only supported by authored fixture preparation, not `project_source` copying.
This is benchmark setup, not a new general worktree-management skill or sandbox.

## Actual regression checks

The starting-state execution test fails on predecessor `75c8718`: the old runner
launches with `VALUE = "old"` instead of the requested uncommitted `"fixed"`.
With this change, a real Git fixture plus stub model process verifies dirty
content, a clean staging area, unchanged commit count and an empty model diff
when the stub makes no changes. Export retains the nonempty initial diff.

Adding an ignored initial file first exposed a false deletion in the final diff.
The reporting step now includes present explicit working inputs with intent-to-add
even when ignored; unchanged ignored inputs no longer appear deleted. A separate
stub intentionally changes the initial dirty source and deletes that ignored
file: both real changes remain in the final diff, relative to the user-like input,
not old HEAD. These tests run real Git/export operations but **no model account**.

Existing clean fixtures retain their previous base-commit diff behavior. Frozen
old runs are neither regenerated nor rescored. Future uncommitted-fix tasks must
freeze their working input alongside historical input and evaluate preservation
against that combined state. This harness capability is not skill performance
evidence and does not change featured or localized benchmark charts.
