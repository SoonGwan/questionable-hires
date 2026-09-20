# Friday output candidate 01 — 2026-09-21

**Not adopted or model-performance validated.** Base resource `75f6b4f`;
`friday_output_candidate.py` changes only the API collection example and adjacent
reporting guidance in `skills/friday/references/sqlite-matrix.md`. Entrypoint,
helper, SQL coverage, assertion guards and permission boundaries remain unchanged.

## Observation, not a claimed saving

The retained [screen03 Friday execution](results/all-eight-current-03/current/view-contract--skill--1/commands.json)
prints the full matrix before checking it, followed by ten identified check/contract
outcomes. Its third command's output contains a 2,134-character first JSON line
and 976 subsequent characters, excluding the separating newline. The JSON includes
reader provenance absent from the subsequent summary; it is **not all redundant**.
Both full rows/columns and BLOB bytes were actually checked. Do not remove those
checks, rewrite this original output or subtract characters from recorded tokens.

The guide currently demonstrates printing the entire matrix in its assertion API
example. The candidate keeps the native result for assertions, asks for identified
outcomes and decisive mismatches afterward, and retains raw formatting for requested
observations or unresolved diagnostics. Required provenance and incomplete/unrun
checks must remain visible. This is not permission to emit an unsupported “PASS.”
It neither forces a summary on observation-only work nor adds a new reporting helper.

Two local tests pass: exact isolated guide transformation with invalid-input
rejection, and actual SQLite before/after BLOB assertions without serialization.
The latter deliberately supplies a stale expected value and verifies that the native
failure retains phase, check, expected bytes and observed bytes. The result remains
unchanged. These are author checks, not evidence the model follows the candidate.

## Required next comparison

Use two different authored SQL-only release tasks: a contract review requiring
complete ordered values/columns and write survival, and an observation task requiring
raw observations plus reader provenance. Include a real incompatible transition and
an inactive-reader error whose contractual status is explicit. Preflight passing and
failing native controls, then freeze all model-visible obligations and review criteria.

Compare contemporary baseline/original/candidate in six fresh sessions, with the
same model/settings/time limits and no changes to helper or main skill body. Review
raw evidence, assertions, actual phase/check coverage, provenance, unchanged files,
incomplete/unrun handling and total token/time costs. Preserve every result. A smaller
printout with missing evidence is not a win. Do not reuse the exposed view task, select
only the cheaper mode, or extrapolate a local character difference into a 20–30% gain.
Reject the candidate if it hides requested output or adds cost without useful benefit.

한국어: 전체 JSON 출력과 계약 검증 결과가 함께 출력되는 실행을 확인했다.
검증용 예제에서 전체 출력의 자동 반복을 없애는 후보를 별도로 만들었지만,
원본 JSON에만 있는 출처 정보까지 불필요하다고 판단하지 않는다. 검증과 원본
출력 요청 두 종류를 새 과제로 비교해야 하며, 현재는 성능 개선을 입증하지 않았다.
