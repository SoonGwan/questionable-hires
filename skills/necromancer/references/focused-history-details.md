# History collector: API and exact boundaries

Use the [main interface](focused-history.md) for routine CLI collection and
interpretation. This reference covers integration, encoding and excerpt mechanics.

## Python integration

`trace_ranges(repo, filename, [(12, 24), (180, 192)], max_commits=3)` returns the
native evidence dictionary. The original single-range `trace()` API remains
supported. Multiple disjoint ranges appear in `ranges`; a single merged range
retains the original result shape. JSON compact/pretty choices do not change the
native result. The collector has no persistent result cache.

## Source reads and line boundaries

Non-regular sources (including named pipes) and known oversized current files
are rejected before opening or running Git. The read stops at
2 MB plus one detection byte; growth beyond the limit is rejected before Git
collection. This bounds that read, not total memory or Git output, and does not
provide a snapshot of concurrently edited files.

Source and Git output must decode as UTF-8. Embedded Unicode separators and CR
characters remain source content, including CR in CRLF files. Current text,
blame rows and numbered excerpts all count LF-delimited lines, not language-parser
lines.

## Focused patch selection

For an unambiguous single-file patch, complete hunks overlapping attributed
historical lines are retained; `omitted_hunks` counts excluded hunks. Commit
metadata and nearby hunk context remain. Ambiguous, multi-file or combined patches,
or no matching hunk, fall back to full capped output.

When a selected hunk exceeds the cap, `selected_patch_excerpt` can preserve
attributed lines and up to three neighboring patch rows with explicit old/new
line numbers and omission markers. The prefix shrinks to 4,000 characters and
the excerpt uses at most 8,000; `truncated` remains true. Ambiguous parses or
selected rows exceeding the allowance retain the ordinary capped fallback.

The parser validates the complete patch but retains numbered-row data only near
selected locations. The helper still captures full Git output and patch text
internally: excerpting reduces displayed output, not subprocess-memory use.

Patch collection disables terminal colors and fixes `a/` and `b/` prefixes for
that command only. User/repository configuration is not changed.

At shallow cutoffs, commit metadata remains but apparent whole-file additions
are suppressed; genuine roots in complete histories retain patches. This does
not recover missing parents or prove original intent.
