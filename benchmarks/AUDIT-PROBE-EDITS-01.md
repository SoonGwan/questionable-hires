# Small test edits without resending a whole file

2026-09-21, parent resource`23f06d2`. This is a new optional input form for
Con Artist's existing native four-check workflow, not a model-performance result.

Previously, changing an assertion at an existing native path required sending
the entire proposed file through `probe_replacements`. `probe_edits` now accepts
one exact `old`/`new` UTF-8 fragment per selected existing non-target file. The
old fragment must occur exactly once; ambiguous/missing matches fail before any
native execution. Other bytes remain unchanged, including line endings and modes.
The source project is never edited. This removes unchanged file contents from
the request when a localized edit is enough; it does not remove necessary source
reading, assertion design or any of the four native checks. Tiny files can be
shorter to send in full; keep the existing replacement interface.

Edited files are materialized into the existing replacement map. Complete result
bytes count toward the20 MB combined input limit before allocating replacements;
batch cache identity also uses those resulting bytes. Equivalent full-file and
edit forms reuse the same correct-code observation, while changed output runs
again. Mutant checks still execute. Shared batch roots do not accept fault-specific
edits; they belong in individual entries. New files, full replacements and edits
can coexist only on distinct permitted paths. There is no fuzzy matching,
automatic production repair, semantic patching or multi-edit sequencing.

## Local validation

Seven new tests exercise actual native four-check runs, unchanged source/modes,
fresh copies/cleanup, CLI module invocation, malformed/ambiguous/colliding inputs
rejected before execution, full-result budget accounting, CRLF/Unicode preservation,
materialized-byte cache equivalence and native pytest fixture/assertion rewriting.
Correct original/stronger suites pass; the original suite misses an omitted write;
the stronger suite fails on actual `[]` versus `['item']`, not setup errors.

- Python3.11.16: all128 audit checks pass,23.520s, no skips.
- Python3.9.6: new group has6 passes/1 explicit pytest-dependency skip,1.124s.
  The skip is not pytest compatibility evidence on that interpreter.

These durations are not speed comparisons. The seven author-side tests are not
fresh model sessions, automatic adoption or a20–30% efficiency result. No graph
values or frozen measurements change. Both README languages and the existing
mode-specific references describe the capability; the top-level skill body and
automatic discovery policy remain unchanged. Following `skill-creator`, detail
stays in the relevant existing-test guide rather than a new universal workflow.

한국어: 기존 테스트 파일의 작은 수정은 전체 파일 대신 한 번만 일치하는 교체
구간으로 전달할 수 있다. 정상·결함 코드의 기존/강화 검사, 원본 보존과 재사용
조건은 유지된다. 입력 형식 개선이며 모델의 채택·토큰·시간 개선은 아직 미측정이다.
