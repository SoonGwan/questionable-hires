# Rendered interaction QA

Use real browser input and inspect rendered state. Record submitted operations and
the relevant result, error, input, and focus. Mocked state alone does not prove UI
behavior; a disabled button does not prove server idempotency.

Launch a shared browser once. Cover the nearest normal case and each applicable
stale completion once:

1. older success after newer success;
2. older failure after newer success when error or recovery state is visible;
3. older completion after a documented invalidating action such as clear or
   navigation.

Control responses directly. Omit inapplicable classes without manufacturing
parallel state. On launch failure, retain one diagnostic and mark dependent cases
unrun; lower-layer checks do not replace browser evidence. Keep detailed evidence
in files and print one compact status per case plus the evidence path. When that
stdout includes every case, outcome, and cleanup status, use it for the report;
do not reopen the detailed evidence merely to repeat it. Inspect the file only for
missing or ambiguous output. Avoid duplicate logs and screenshots.
