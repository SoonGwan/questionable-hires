# Receipt: verify an already-present uncommitted fix

Predecessor `9dfce8f` only accepts committed implementation revisions. A real CLI
regression for an explicit current-file snapshot fails there with exit 2,
`Invalid revision`. The candidate adds `"after":{"working_tree":true}` while
keeping `before` a Git commit expression. This is a new supported workflow, not
evidence of a faster model session or a repair of previous benchmark scores.

The existing bounded read already captures selected current file bytes and modes.
The new variant reuses that snapshot rather than resolving an after commit or
reading staged contents. Tests/support remain identical in both isolated copies.
`revisions.after` is null and `working_tree_after` records selected implementation
SHA-256 hashes and modes. It does not invent a commit identity. Existing revision
strings, CLI recipe fields, file/layout limits, import checks, cleanup and original
integrity behavior remain in place. No new mandatory resource or current-bug
procedure is added; retrospective verification remains an optional mode.

## Executed behavioral checks

- Real CLI with three distinct states: committed implementation, different staged
  implementation, and uncommitted current implementation with an additional marker.
  The fixed regression fails on the requested before commit and passes on the
  frozen current bytes; using HEAD or staged contents cannot pass that assertion.
  Copied import evidence is captured. Output hashes/modes match the current file.
- Every file byte in the fixture, including Git index and metadata, is identical
  before/after; original executable permission is preserved and temporary copies
  are removed. The helper creates no commit or stash and never reverses the
  working patch.
- A separate fault injection changes the original working implementation between
  checks. The after check still executes the initially frozen version and passes;
  final integrity detection raises, leaves the changed original untouched and
  removes owned copies. This does not claim an atomic snapshot under concurrency.
- Invalid/false/numeric/extra-field selectors and a working-tree `before` are
  rejected before any test process is launched. No string revision is reserved
  as a magic working-tree name.

This can remove the need to hand-build comparison copies or create a temporary
commit for a supported uncommitted-fix verification. The amount of developer/model
work saved has **not** been measured. It cannot replace a user requirement to run
a regression before making the original edit, handle added/deleted implementation
layouts, establish all repository side effects, or prove broad 20–30% gains.
Earlier adverse comparisons and featured/localized charts are unchanged.
