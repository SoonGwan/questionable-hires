# Select patch hunks without copying omitted bodies — 2026-09-21

Parent`c96730d`. Necromancer already groups selected ranges and deduplicates
attributed commits; no redundant Git process was removed. The observed mechanism
was instead `focused_patch` splitting/copying every hunk, even when almost all
were omitted. This differs from the earlier
[numbered-excerpt line iteration](HISTORY-PATCH-MEMORY-01.md) optimization.

The revised selector scans header positions in the original string and slices
only retained hunks. Exact returned text, omitted-hunk counts, ambiguous-input
fallbacks and the no-match return remain unchanged. No discovery, scope, CLI,
Git query, selected lines or evidence budget is broadened or shortened.

## Local allocation and timing observations

[All samples and helper identity](results/history-hunk-selection-01.json).
Reproduce with the existing benchmark utility:

```sh
python3 -B benchmarks/history_patch_memory.py --hunks
```

Python3.11.16 on the shared local host; ten alternating timing pairs. Allocation
tracing is separate from timing. Inputs are allocated **before** tracing; these
are allocations inside the selection function, not total memory, RSS, Git time,
model tokens or full developer-task performance. The original implementation is
retained as a history-independent test oracle.

| Authored input | Eager peak bytes | Revised peak bytes | Eager median seconds | Revised median seconds |
| --- | ---: | ---: | ---: | ---: |
| 2,000 hunks, first/last selected | 8,341,537 | 12,768 | .034381 | .029496 |
| 2,000 hunks, all selected | 20,608,735 | 12,279,966 | .035198 | .030700 |
| 2,000 hunks, none match | 8,330,374 | 2,126 | .033857 | .029155 |
| One large hunk | 4,000,843 | 2,000,506 | .006616 | .005595 |
| Tiny hunk | 1,732 | 2,121 | .000001875 | .000001875 |

The first three inputs contain4,049,823 characters. The all-selected internal
parser stress control exceeds the public collector's100-selected-line bound;
it is not a permitted full CLI workload. The other cases cover sparse selection,
unchanged no-match fallback, a long row and a tiny control. The tiny case uses
more intermediate memory; it is not hidden by averaging into the large cases.
All five outputs and omission counts compare exactly. No statistical or broad
speedup claim follows from these small shared-host samples.

## Regression controls

Before editing runtime code, the equivalence method passed and the new sparse
allocation control failed: revised8,341,537bytes was not below half the original
peak, because both implementations still copied everything. After the edit,
both pass. Controls include selection boundaries, no targets, duplicate targets,
zero-length hunks, leading whitespace, malformed/ambiguous text, Unicode/CR rows,
missing/duplicate file markers and large/small inputs. As before, this function
selects evidence rather than validating arbitrary Git patches for application.

Python3.11.16: all56 history tests pass in18.326s, including native Git controls.
Python3.9.6: both new tests pass in0.330s. Repository/link validation, featured
synchronization and whitespace checks pass. These checks are not a complete
current release matrix or hosted CI result. Entry instructions and frozen model
measurements/charts are unchanged; whole-task efficiency remains unproven.

한국어: 선택하지 않은 패치 구간까지 복사하던 중간 할당을 없앴다. 반환 근거와
생략 개수는 동일하며 큰 희소 선택 예제의 함수 내부 메모리·실행 시간은 줄었다.
작은 입력의 메모리 증가는 함께 공개한다. 입력 문자열·Git·전체 프로세스 메모리와
모델 토큰·시간은 이 측정 범위가 아니며 전체 스킬 개선율로 환산하지 않는다.
