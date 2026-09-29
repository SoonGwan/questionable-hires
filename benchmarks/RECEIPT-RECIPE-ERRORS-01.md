# Receipt recipe errors01 — 2026-09-28

Native correctness/usability change from parent `e2bed7ff`, not a model trial.
[Exact source hashes, commands and exits](results/receipt-recipe-errors-01/summary.json)
identify the measured resources. No frozen benchmark or performance claim changes.

Previously, an unknown option such as `guard_trees` produced the same generic
required-fields error as a missing `tests` field. More seriously, standard JSON
decoding silently kept the last duplicate key: a second `tests` field replaced
the first selection without warning. No malformed input should silently redefine
the requested comparison.

The CLI now rejects duplicate keys, including nested objects and equivalent
escaped spellings, for both stdin and recipe files. Missing and unknown top-level
keys are identified together; a non-object has a specific error. Key names are
escaped and each list/name diagnostic is bounded to 240 characters plus an
ellipsis. Values are not dumped. Python callers also receive explicit schema
errors, but a Python dict has already lost duplicate-key information.

Invalid recipes still exit 2 with no result JSON. They do not launch a comparison;
normal comparison, native exit interpretation, output format, source preservation
and cleanup remain covered by existing controls. The object decoder cannot detect
duplicate selections already overwritten before input is serialized.

## Execution evidence

The same seven regression methods run against the parent and changed resources
in a fresh extracted source archive, without repository history. Test fixtures
for existing comparisons create their own disposable Git projects. The new error
controls deliberately use a non-Git source directory: errors must identify the
recipe fault before trying Git or native tests, with directory contents intact.

| Original native process | Methods | Result |
| --- | ---: | --- |
| [Before regression](results/receipt-recipe-errors-01/before.txt) | 7 | Exit1,9 assertion failures including subtests |
| [After regression](results/receipt-recipe-errors-01/after.txt) | 7 | Pass |
| [Existing Python helper](results/receipt-recipe-errors-01/helper.txt) | 50 | Pass |
| [Whole-tree guard](results/receipt-recipe-errors-01/tree-guard.txt) | 9 | Pass |
| [Selected-file replacement](results/receipt-recipe-errors-01/selected-read.txt) | 1 | Pass |
| [Native Node comparison](results/receipt-recipe-errors-01/node.txt) | 9 | Pass, Node24.16.0 |
| [Isolated stream prototype compatibility](results/receipt-recipe-errors-01/stream-candidate.txt) | 3 | Pass; prototype remains unadopted |

Total **79 distinct after methods** across these processes. A prior working-tree
run of the same regression/helper methods is not added again. Public logs replace
temporary archive path prefixes; no model sessions or private prompts are involved.

Adopt this input correction. It provides enough information to repair common
recipe mistakes without guessing, but no model has been measured doing so here.
Do not translate fewer diagnostic ambiguities into token or wall-time savings.
The all-eight whole-task objective remains unmet; earlier mixed/adverse results
remain in the dated decision index. Both README capability descriptions and both
runtime-specific recipe guides describe the changed contract.

## Delivery

Source **`9db5a8ec`** is installed on the owner's Mac and served by the public
landing. The old Receipt resource inventory exactly matched parent `e2bed7ff`
before replacement; its complete directory is retained outside skill discovery
under `~/.agents/skill-backups/questionable-hires/20260928-recipe-errors-9db5a8ec/receipt`.
The staged replacement and the old backup were checked by bytes/modes. All eight
installed skills now match the source; the other seven were not replaced.
[Delivery inventories](results/receipt-recipe-errors-01/personal-delivery.json)
and [eight actual installed checks](results/receipt-recipe-errors-01/installed-checks.txt)
cover the seven invalid-input methods and one real native before-fail/after-pass
comparison with both output formats. These repeat native methods, not additional
independent model evidence. The recorded successful replacement did not exercise
the rollback path.

Eighteen landing checks passed, including generated snapshot packaging. Public
HTTPS [health, both languages and both download files](results/receipt-recipe-errors-01/hosted-delivery.json)
were fetched after deployment. Health identifies `9db5a8ec`; the downloaded
archive/checksum match the generated files exactly. Archive SHA-256:
`572f1daa90f910b0502606175ebe09ffe81fdacf36863585db2bb73e8caf3b2f`.
The featured chart, model metrics and page design did not change in this release.
These are release checks, not a new responsive-browser or efficiency measurement.

한국어: 잘못된 옵션을 알려주지 않던 오류와 JSON 중복 키가 앞의 비교 조건을
조용히 덮어쓰던 동작을 고쳤다. 중첩·이스케이프된 중복 키도 실행 전에 거부하며,
누락·알 수 없는 키를 함께 알려준다. 같은 회귀 검사7개가 수정 전 실패하고 수정
후 통과했다. 기존 Python·Node 비교와 원본 보존을 포함한79개 검사도 통과했다.
실제 모델 토큰·시간을 새로 측정하지 않았으며 전체8개 성능 목표 달성은 아니다.
수정은 Mac 설치본과 공개 다운로드에 반영했고 이전 Receipt 폴더를 백업했다.
전체8개 설치본이 소스와 일치하며 실제 설치 경로의8개 검사, 랜딩18개 검사,
공개 양언어·배포 식별·다운로드 바이트 일치를 확인했다.
