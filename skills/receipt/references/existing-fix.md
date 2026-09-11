# Receipt for a fix that already exists

First determine whether available before/after evidence already establishes the
same input, assertion, implementation revisions and relevant failure. Reuse it
when valid; do not recreate history just because Receipt was invoked.

If comparison is needed, use isolated local copies without reversing patches in
the user's working tree. Freeze the regression assertion and inputs across both
versions: vary the affected implementation, **not each revision's historical test
suite**. Old tests may never have checked the reported boundary. Keep required
dependencies/configuration comparable and identify the actual loaded revision.

Run the same regression through the project's documented runtime and command.
Capture each exit status independently of later printing. Confirm that before
fails for the reported behavior, not an import/compiler/setup error, and after
passes. If an old interface cannot run the same check, name that limitation;
two different checks do not establish the claimed before/after result.

Verification does not authorize production edits, installations, external
services or publication. Preserve user changes. Return the decisive command,
revisions, behavior and limits; no separate report or complete history survey is
required. Stop after the scoped comparison, not after unrelated regression work.
