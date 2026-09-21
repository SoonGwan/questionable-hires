# Packaging specifier audit: author preparation

2026-09-21. [Selection committed before execution](../../PACKAGING-SPECIFIER-01-SELECTION.md)
at `8b591ff`; existing audit helper from resource `c8fd471`, no skill edits.

Source: [packaging 24.2 upstream tests](https://github.com/pypa/packaging/blob/d8e3b31b734926ebbcaff654279f6855a73e052f/tests/test_specifiers.py),
commit `d8e3b31b734926ebbcaff654279f6855a73e052f`. The complete `src/packaging`
directory, original specifier tests and their version-test dependency, test
initializer, pyproject and all three license files were copied without edits.
The fresh import explicitly resolves the local 24.2 package, not the installed
26.3 dependency needed by the preflight environment. Upstream clone is clean.

## Actual native observations

Python 3.11.16, pytest 8.3.4, pretend 1.0.9; complete dependency versions and
source/helper/script hashes are retained. The native pytest selector is the
whole `tests/test_specifiers.py` with `-x -q --tb=short -p no:cacheprovider`.
No test is selected or removed after observing its result. Fail-fast mutant
runs establish first detection, not complete mutated-suite coverage.

| Request / observation | Result |
| --- | --- |
| Single: correct source | 806 passed, exit 0 |
| Single: compatible comparator mutation | 1 failed / 376 passed, exit 1 |
| Multiple: correct source | 806 passed, exit 0 |
| Multiple: compatible comparator mutation | 1 failed / 376 passed, exit 1 |
| Multiple: equality comparator mutation | 1 failed / 311 passed, exit 1 |
| Multiple: inequality comparator mutation | 1 failed / 338 passed, exit 1 |

Failures are actual `assert version in spec` observations: respectively `1`
against `~=1.0`, `2.0` against `==2`, and `2.1` against `!=2`. They are not import
or support exceptions. Local package paths and test-to-Specifier binding are
checked within the actual native pytest processes. Correct baselines are reused
only within the multiple-fault batch and explicitly reference the first check.
The first mutation is independently executed again for the single control.

All checks retain complete bounded output (`output_truncated:false`), with no
timeouts. Final source inventory matches original bytes/modes and all owned
scratch is removed. The report's successful-baseline reuse is one observation,
not two additional native executions. No model, latency-saving or token-saving
claim follows from these six author test processes.

## Retained evidence and reproduction

- `single.json` and `multiple.json`: all native output, exits, provenance and
  preservation/cleanup reports, including explicit reuse references.
- `summary.json`: all supplied file digests/modes, exact mutations and recipe,
  fresh-import record and interpreter identity.
- `capture.json`: pre-redaction report hashes, author/helper script hashes and
  installed dependency versions. Export replaces private workspace paths only.
- `author-preflight.py`: byte-for-byte original author script. To reproduce its
  existing layout, place it at `benchmarks/local-runs/preflight_packaging_specifier.py`
  and put the clean pinned clone at `benchmarks/local-runs/packaging-specifier-upstream-24.2`.
  Use a Python 3.11 environment with the recorded dependencies and the pinned
  helper revision. Its output directory must be absent; it refuses overwrite.
  Native timing and private paths can differ. This is a retained preparation
  script, not the eventual model scheduler.

The forthcoming four-cell model comparison still needs a committed exporter,
explicit task criteria, source/runtime/resource manifests and one-attempt runner
controls. No model call has run for this task. It is author-selected real-source
transfer with correlated single/multiple requests, not independent generalization
or a replacement for the adverse all-eight screen. Do not change the skill after
seeing these cases and continue calling them unexposed validation.

한국어: 사전에 정한 원본 테스트806개가 통과하고, 선언한3개 결함은 모두 실제
단언 실패로 검출됐다. 로컬 원본 모듈 연결·파일 보존·임시 복사본 정리도 확인했다.
이는 작성자의 준비 검사이며 모델 비용이나 일반 성능 개선 결과가 아니다.
