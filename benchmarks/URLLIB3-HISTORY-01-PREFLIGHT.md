# urllib3 history preparation — 2026-09-21

**Post-run qualification:** [The subsequent model comparison](URLLIB3-HISTORY-01.md)
found missing generated version metadata. The native assertions below genuinely
run, but unittest's import retry reuses cached submodules after package startup
fails. They do **not** establish a successful cold root-package import. Both
the original evidence and later instrumented diagnostics are retained.

**Author controls only; no model sessions or efficiency claim.** Prepares a
different upstream project for the [section-read candidate](NECROMANCER-SECTION-READ-01.md)
`f53cb65`, after the adverse [Slugify history result](SLUGIFY-HISTORY-01.md).
Repository history search found no earlier urllib3/is_retry benchmark. This
source was inspected by the author, so it is development evidence, not a blind
holdout. Model-visible task, criteria and schedule must be frozen separately.

## Provenance and boundaries

Full clone of [urllib3 2.2.3](https://github.com/urllib3/urllib3/tree/2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df),
revision `2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df`,4,188 ancestors.
The original checkout is clean and unchanged. The script verifies revision,
nonshallow state, selected tracked source bytes and modes against Git blobs;
copies only the complete `src/urllib3` tree, `test/test_retry.py` and MIT license
to owned project-local scratch. It does not adapt upstream code to another runtime.
The existing Python3.11 environment suffices; no dependency installation was made.

[Script](preflight_urllib3_history_01.py) /
[retained observations and license](results/urllib3-history-01-preflight.json).
Fifteen independent unittest processes execute author-written compatibility
assertions, not the upstream pytest suite. Same-process imports verify the actual
copied `urllib3.util.retry` module and `Retry` binding. No HTTP requests are sent,
no historical code is executed and no model is called.

## Two independent proposed changes

A moves the method-allowlist guard below the forced-status early return, leaving
both checks and the header fallback otherwise intact. B removes only `self.total`
from the Retry-After fallback condition; it does not change `increment()` or the
forced-status path. Each is applied separately to a clean current source copy.

All cases explicitly allow GET. Other unspecified Retry arguments use defaults.

| Configuration and call | Current | A: forced status first | B: omit fallback total |
| --- | --- | --- | --- |
| total3, forced500, POST500 | False | True (assertion failure) | False |
| total0, no forced statuses, GET429 with Retry-After | False | False | True (assertion failure) |
| total3, forced500, GET500 | True | True | True |
| total3, no forced statuses, GET429 with Retry-After | True | True | True |
| total0, forced500, GET500 | True | True | True |

Both negative controls fail with `AssertionError: True is not False`, not a setup
exception. The remaining13 controls pass. Scratch is removed and source identity
rechecked. First execution passes without repair. Output creation is exclusive.
Four offline identity tests pass on Python3.9 (0.008s) and3.11 (0.006s): original
bytes accepted; changed content/mode/revision, dirty/shallow state, same-content
symlink and missing required source rejected. Repository/link, featured sync and
whitespace checks pass. These validate preparation gates, not model decisions.

The last row matters: `is_retry()` is a decision predicate, **not** an observation
of an actual HTTP retry. Its connection-pool caller checks `increment()` and
handles `MaxRetryError` before sleeping or requesting again. The model task must
ask for that distinction; do not score predicate-only probes as live-network
coverage or invent a universal “zero total means is_retry is false” contract.

## Historical controls

- `b6d45c4e702f66e819373c79122944204ebe7e72` introduces the Retry-After fallback
  (with total/header/status guards) and renames `is_forced_retry` to `is_retry`.
  Its parent already applies the method whitelist before forced statuses.
  This is not the first-ever method-policy introduction.
- `f37a48942be19c019fa9834f9796f354dd1ef2c1` extracts the existing inline method
  check to `_is_method_retryable` and reuses it for read errors. Attribution to
  this refactor is not introduction of the earlier method restriction.

Both commits are verified ancestors; parent/child source hashes and relevant
patches are retained. The current source later moves to `src/`, is formatted,
typed and renames whitelist to allowed_methods. A blame line alone therefore
does not establish the semantic introduction. The425-line upstream retry test
file contains both relevant and unrelated methods: it is not artificially padded.

한국어: 새 프로젝트의 원본 코드로15개 정상·변경 대조를 확인했다. 두 변경은
각각 실제 반환값을 바꾸며, 정상 결과를 유지하는 대조도 함께 남겼다. 판단 함수가
참이라고 실제 HTTP 재시도가 일어나는 것은 아니라는 호출부 경계도 평가에 포함할
예정이다. 사전 검증일 뿐 수정 스킬의 토큰·시간 개선 수치는 아직 없다.
