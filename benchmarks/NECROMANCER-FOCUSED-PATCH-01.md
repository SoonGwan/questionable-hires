# Focused patch evidence: local regression, not model performance

A synthetic Git history changes a large early section and a selected late line
in one commit. The previous collector's 12,000-character prefix omits the selected
line's before/after patch. The candidate returns 332 characters containing that
patch and the commit metadata, with one explicitly omitted hunk and no truncation.
Both versions were executed against the same regression design.

Complete hunks overlapping attributed historical lines are retained before the
cap, for unambiguous single-file patches. Omitted hunks are not proven semantically
unrelated; native Git remains necessary when surrounding changes matter. Combined,
multi-file, ambiguous and unmatched patches fall back to full capped output.

An initial fixture with repeated separator lines produced one large Git hunk and
still failed after filtering. Unique stable separators exercise the distinct-hunk
case. The single-large-hunk limitation remains, is documented, and is not counted
as fixed. This synthetic output-size reduction is not a typical-repository token
estimate or equal information content: surrounding changes are deliberately omitted.

Fourteen collector tests pass, including multiple selected hunks, unmatched and
combined-diff fallback, rename, shallow history and read-only behavior. Full suite:
131 tests pass in 12.401 seconds; repository and skill validators pass. No model
session, efficiency acceptance or broad completion claim is made.
