# Necromancer: preserve selected evidence under Git presentation settings

This is an author-run regression check, not a model benchmark or a token/time
improvement claim. The predecessor is `45b11cd`; no frozen experiment is changed.

## Demonstrated failure

The real-Git fixture commits two separated edits: a large unrelated hunk and a
small selected change at line 181. With default presentation, the collector
returns the selected before/after lines and reports one omitted hunk. With either
`color.ui=always` or `diff.noprefix=true`, the predecessor instead misses the
single-file patch marker and falls back to the capped beginning of the large
patch. The selected change is beyond that prefix. These are user settings, not
missing history or an ambiguous source change.

The new regression was run before the implementation change: both setting
subtests failed on actual returned evidence. Other proposed presentation settings
did not fail on the installed Git and were removed from this targeted regression;
they are not claimed as demonstrated bugs.

## Scoped correction

The existing `git show` command now specifies `--no-color`, `--src-prefix=a/`
and `--dst-prefix=b/`. It does not add a Git process or rewrite configuration.
The regression requires the entire returned commit evidence to match default
presentation, including the actual before/after change and omitted-hunk count,
and checks that repository configuration bytes remain unchanged.

The focused suite passes all 23 tests on the default Python and Python 3.11.
The complete local suite passes 333 tests in 46.148 seconds; catalog/link and
featured-localization checks pass as well.
Existing rename, dirty/shallow-history, truncation, numbered-excerpt and no-write
checks remain in that suite. This only establishes the tested helper behavior;
it does not prove all Git presentation options are normalized or that a model
needs fewer tokens/time to finish a real development task. Featured images and
both localized landing-page results remain unchanged.
