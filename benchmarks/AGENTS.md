# Benchmark authoring and evidence

- Before freezing a new QA fixture, exercise the supplied test support through
  both a passing check and a deliberate failing assertion. Verify that failure
  output preserves the relevant actual/expected values, rather than reporting a
  support-code exception. Nominal green tests alone are not a harness preflight.
- Define input, payload and failure contracts before calling a fixture clean.
  Do not count a reasonable finding under an underspecified contract as an
  agent false positive merely because the author did not intend it.
- Preserve frozen fixtures, criteria and every scheduled cell. If a fixture
  defect is discovered during execution, disclose the effect on interpretation;
  correct a future version, not the input underlying an already reported run.
- Separate original model evidence, author replay and resource arithmetic.
  Lower recorded cost with unequal work or invalid controls is not by itself an
  accepted performance win. Keep existing featured results tied to their actual
  source revision and obey the repository's localization/chart synchronization rule.
