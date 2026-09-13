# Receipt source-layout support

Native author validation from `fd51ca2`, not a model timing result. Inspection
of the retained bundle boundary-fix pair showed both arms already used four
shell commands; skipping its before/after checks would not be an efficiency
improvement. A separate practical limitation was that Receipt's copied Python
environment added only the copy root to import lookup, not regular `src/` layouts.

The optional ordered `import_roots` recipe field now prepends selected directories
inside each comparison copy before its root. It neither installs the package nor
inherits `PYTHONPATH`, rewrites project configuration or changes source files.
The result records the ordered roots. Package initializers/support remain frozen
current `fixed` inputs; changed implementation files remain revision-specific
`vary` inputs. Existing root-layout recipes keep their previous behavior.

The native regression creates a real two-commit `src/sample` package, with a
relative initializer import and the same current unittest boundary assertion.
Before implementation it failed because the recipe field was unsupported
(44 tests, one error, 15.572 seconds). After implementation the same suite passed
(44 tests, 15.708 seconds): the historical comparison reaches an actual
`AssertionError: False is not true`; the fixed comparison executes and passes.
Both processes report copied imports, original inputs remain unchanged and owned
comparison directories are removed. No dependency installation is used.

Additional CLI coverage reverses two selected roots containing the same package.
Native outcomes must change with lookup order, and recorded order must match.
This is deliberately a counterexample to treating CLI 0 or copied-module location
alone as proof of the intended fix: choosing another copied implementation can
make both variants pass. The same assertion and correct implementation identity
still matter. Path validation rejects nonlists, nonstrings, roots outside the
project, noncanonical paths, duplicates, files, empty/unselected/missing directories
and symlinks before test execution.

Final verification: all 412 repository tests passed in 67.079 seconds, including
the native CLI ordering check and prior import-exit correction. Skill validation,
metadata/documentation links, featured synchronization and whitespace checks pass.

This supports regular pure-Python source packages, not editable-install metadata,
build hooks, compiled extensions or every namespace-package setup. Native project
isolation remains necessary when those are part of the contract. No whole-session
token/time reduction, independent model adoption or all-eight improvement is yet
established. Frozen benchmark results and featured/localized charts are unchanged.
