# Receipt: choose isolation by missing work, not language support

2026-09-15, parent `6cf9fb1`. Guidance revision; model impact unmeasured.

The [reviewed HTTPX comparison](results/httpx-json-01/README.md) showed that all
three conditions met the same requirements, but current Receipt used 47.7% more
tokens than baseline and the shorter candidate used 74.0% more. Both skill
sessions inspected helper implementation before invoking its Python API. That
single-task result does not prove helper use caused the whole cost gap, nor that
native comparison will always be cheaper.

The shipped guide nevertheless instructed supported Python tasks to use the
helper. This is too broad a selection rule: language support does not establish
that replacing a project's adequate comparison or creating another wrapper helps.

## Narrow change

- The existing-fix entry now states the required comparison outcome directly:
  isolated versions, unchanged current assertions/inputs, compatible runtime and
  loaded-code identity. It retains the prohibition on reversing user patches.
- Reuse adequate project-native comparison facilities. The helper remains available
  when it supplies missing copying, in-process import checks and cleanup.
- The reference permits native isolation for supported projects too; it remains
  necessary when the helper does not support the required runtime/layout.
- Existing CLI examples, runtime/guard limits and evidence requirements are retained.
  Implementation inspection remains appropriate for concrete trust, adaptation or
  diagnosis questions. No blanket prohibition on reading code; no new mandatory tool.

Only `skills/receipt/SKILL.md` and `references/existing-fix.md` change. Metadata,
helper code, other roles, frozen observations and featured charts are unchanged.
The text is longer, not a claimed prompt compression. Its purpose is to avoid an
unjustified workflow requirement, not claim measured token savings.

## Verification and next evidence

Existing native Receipt checks exercise the literal committed/uncommitted CLI
examples, actual before failures/after passes, pytest loading, native startup,
source/resource preservation and cleanup. Installation and documentation checks
also ran: Receipt **102 tests passed in 36.425 seconds**, installation-related
**21 passed in 2.610 seconds**, plus skill/repository validation, featured-language
synchronization and whitespace checks. These establish retained functionality, **not that
a model chooses the right path or uses fewer tokens after this revision**.

The earlier HTTPX baseline proves native facilities can satisfy that particular
task; it did not use this revised skill and is not evidence of this revision's
performance. Do not rerun the same ticket for a favorable replacement result.
Next evaluation should include a different project/task with an existing adequate
comparison path and a case where missing setup makes the helper useful, at equal
obligations and with all attempts retained. The full eight-role goal remains open.

한국어: Python 지원 여부만으로 도우미 사용을 지시하던 부분을 수정했다. 같은
검증 요구사항을 충족하는 기존 프로젝트 절차는 재사용하고, 필요한 준비 작업을
대체할 때 도우미를 선택한다. 복사 격리·같은 테스트·출처·원본 보존 기준은 유지한다.
문구는 오히려 늘었고 아직 모델 성능 개선 수치는 없다. 새 과제에서 올바른 도구
선택과 전체 토큰·시간을 확인해야 한다.
