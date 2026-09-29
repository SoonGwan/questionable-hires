# Git capture memory01 — isolated prototypes, 2026-09-28

**Do not adopt either prototype.** Native capture can use less Python allocation
while preserving decoded output, but both alternatives are slower here and add
workspace writes. Ordinary Necromancer code, installation and hosted downloads
remain unchanged. No model experiment or whole-task improvement is claimed.

This investigates the still-open full-Git-output allocation limit documented in
[compact transport01](HISTORY-COMPACT-OUTPUT-01.md). Existing patch/current-line
optimizations operate after capture; they do not remove `subprocess.run`'s full
captured stdout. A small current file can have a large removed historical body.
Simply truncating stdout would lose late selected evidence and was not proposed.

## Actual native observations

The [reproducible probe](history_capture_memory.py) creates an owned Git repository
with a225-character Unicode/CRLF patch, a16,800,204-character removed-history patch,
invalid UTF-8 historical content, and a missing revision. It runs actual Git with
the collector's normal flags and20-second command timeout. Only the author fixture
is mutated; its temporary directory is removed after collection.

The existing helper is measured from parent `cfa7e920`; its source hash is retained.
First prototype source is committed as `33a27e75` and the exact script hash is in
[the first observations](results/history-capture-memory-01/native.json). Both
stdout/stderr go to temporary files and are decoded directly from read-only memory
maps, avoiding a full captured bytes object before decoding. Four alternating
pairs/case plus a separate traced call/arm preserve actual decoded strings, exits,
and UTF-8 error positions/reasons. The large patch's traced peak falls33,730,433→
16,812,453 bytes, but median time increases0.106911→0.152648 seconds. Smaller cases
also take longer. These initial adverse observations are retained unchanged.

Inspection of this runtime's Python `Popen._communicate`/`_wait` shows that without
pipes the timed wait uses increasing sleep intervals. A second prototype keeps
stderr as a pipe, so EOF can wake the selector; stdout alone uses a temporary file.
This does not prove that polling accounts for all timing differences. It also
retains the existing unbounded stderr capture.

The [second comparison](results/history-capture-memory-01/stdout-spooled.json)
retains all three implementations, using all six execution-order permutations for
each same authored case, plus one separately traced call/arm/case. These reused
inputs are development evidence, not independent validation.

| Case | Current peak bytes | Stdout-spooled peak bytes | Current median s | Stdout-spooled median s |
| --- | ---: | ---: | ---: | ---: |
| Small Unicode/CRLF | 91,540 | 79,156 | 0.013039 | 0.017079 |
| Large removed history | 33,730,546 | 16,807,981 | 0.106070 | 0.116685 |
| Invalid UTF-8 | 91,540 | 79,156 | 0.014047 | 0.017685 |
| Missing revision | 91,436 | 79,052 | 0.013216 | 0.013788 |

All decoded output or error observations match across all arms. CR bytes and
Korean text are preserved. Invalid historical UTF-8 raises `UnicodeDecodeError`;
the missing revision returns128 and matching stderr. The large-case Python peak
falls50.17%, while time increases10.01%; all smaller cases also slow down. Full
three-arm observations and each timing sample remain in the linked JSON.

## Scope and decision

Tracemalloc covers newly allocated Python memory during each wrapper call. It
excludes previously constructed fixtures/results, native allocations, mapped page
RSS, Git child memory and disk usage. Timings run separately without tracing on a
shared host/cache. Both alternatives still allocate the full decoded text; neither
is a whole-process memory cap or streaming evidence selector. No token saving can
be derived from equal output strings or Python heap measurements.

The prototypes deliberately create temporary files inside the author-owned repo.
The existing collector does not require workspace writes. Changing that contract
would break read-only/project-scope assumptions; moving writes outside a permitted
root would not repair it. Whole-collector output equivalence, interruption/timeout
cleanup, concurrent children and alternate platforms were not validated. Do not
install these prototypes or describe the original full-output limit as fixed.

The measured tradeoff rejects this mechanism for ordinary adoption. Do not repeat
these same captures to seek a favorable timing pair. A future change needs both a
compatible resource contract and measured end-to-end benefit; the all-eight
quality/token/time objective remains unmet.

한국어: Git 출력 전체를 메모리에 담는 문제를 실제 변경 이력으로 검사했다.
임시 파일과 메모리 매핑을 쓴 시제품은 약16.8MB 출력에서 Python 할당 피크를
약50% 줄였으나, 대기 방식을 보완한 후보도 약10% 느렸다. 작은 입력도 느려졌다.
한글·CRLF·오류 출력은 같았지만 작업 폴더 쓰기가 새로 필요하고 전체 프로세스
메모리나 타임아웃 정리를 검증한 것은 아니다. 두 시제품 모두 기본 스킬에
반영하지 않는다. 이는 네이티브 자원 비교이며 모델 토큰 절감 실험이 아니다.
