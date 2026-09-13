# Con Artist: explicit copied source roots

## Reproduced compatibility gap

The audit bootstrap previously prepended only the disposable copy root and
removed inherited PYTHONPATH. A selected regular package under `src/audit_sample`
therefore failed with `No module named 'audit_sample'` before any native test,
even though its implementation and test were copied. Adding an `import_roots`
recipe was initially rejected as an unknown field. This is an author-created
layout regression, not a new organic repository benchmark or model observation.

The new optional `import_roots` list prepends selected copy-relative directories
in explicit order, before the copy root, for imports/prechecks/tests/probes.
Default behavior stays root-only. Roots must contain selected files; missing,
non-directory, duplicate normalized, symlink, absolute and traversal paths are
rejected. No dependency installation or original-source path is introduced.
Copied import provenance remains required. Ordered roots join the baseline
identity and are shared in batch mode, preventing reuse across changed resolution.

Instructions route this detail from the common interface to the advanced
reference only when the project has an evidenced source path. This follows
progressive disclosure rather than adding src-layout steps to every audit.
Editable-install hooks, metadata/build steps, compiled artifacts and namespace
validation remain outside this feature; a source path is not a substitute for
those runtime contracts.

## Native evidence

The first 69-test focused run failed once on the unsupported recipe field in
11.217s, after observing the root-only import failure. After implementation,
69 passed in 12.380s. Two additional order/cache and CLI-batch tests brought the
focused suite to **71 passing tests in 11.740s**.

- Existing acknowledgment test passes on correct and missing-write code.
- The same exact-record probe passes correct code and fails faulty code with
  `AssertionError: ['kept']`; all four checks report copied src module paths.
- Reversing two roots containing same-named packages loads the other package,
  fails the actual acknowledgment assertion and does not reuse the old baseline.
- The real CLI batch with src imports retains native mutant failures and reuses
  only identical successful correct-test/probe observations.
- Invalid root recipes are rejected before execute; originals and owned-copy
  cleanup are independently checked by the regression suite.

No timed model session ran during this change. The gain established here is
supported project layout without custom import orchestration, not a measured
token/time reduction. Previous unfavorable model evidence and featured graphs
remain unchanged. Broader real-developer and all-eight performance claims remain
unproven.

Final validation: **401 repository tests passed in 54.367s**. Skill validation,
repository links/metadata, featured-language synchronization and diff whitespace
checks passed. These are local compatibility/regression checks, not model costs.
