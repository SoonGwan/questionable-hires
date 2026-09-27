# Landlord check grouping01 review — 2026-09-28

Previous resource `cc7591ed`, candidate/execution `849e06dc`.
[Frozen protocol](LANDLORD-CHECK-GROUP-01-PROTOCOL.md),
[all attempts and counters](results/landlord-check-group-01/comparison.json),
[original grouping](results/landlord-check-group-01/tool-groups.json),
[preservation and outcome review](results/landlord-check-group-01/original-review.json).

**Do not adopt the added instruction.** Costs decrease in this pair, but both
versions already execute their native checks together. The additional instruction
has not demonstrated an incremental scheduling capability. Do not repeat this
unchanged candidate or label this pair an all-eight or no-skill improvement.

| Matching-skill arm | Whole-task tokens | CLI seconds | Model responses |
| --- | ---: | ---: | ---: |
| Previous | 78,325 | 39.876 | 5 |
| Candidate | 62,781 | 33.974 | 4 |

Tokens **−19.85%**, time **−14.80%**. Original per-response counters reconcile
with final CLI totals; cached input is included once. Both scheduled sessions
completed without limit, timeout, replacement or retry. Actual Astra/medium and
retained-rule host execution are verified. This is an exposed synthetic task,
one fixed-order pair on a shared host/cache, not independent validation.

## What actually changed

Both original sessions use `Promise.allSettled` to execute the same two independent
native processes: the complete documented local test group and a direct-Backend
probe. Each process has its own output and successful exit. Neither waits for an
extra model response between those checks. Original call inputs and line hashes
are retained in `tool-groups.json`; shell count alone could not show this.

The candidate instead combines its second file inventory and line-numbered source
read in one tool interaction. The previous session separates those into two.
The initial discovery globs also differ before the skill body is read. Existing
Landlord guidance already says to batch known definitions and consumer regions.
Therefore the observed improvement cannot establish that the new native-check
instruction caused a useful behavioral change. A favorable total is insufficient
reason to accumulate another rule in the shipped skill.

## Outcomes and preservation

Both run `python3 -B -m unittest -v test_contract`: two native test methods pass.
The first uses three key subcases and checks literal creation/duplicate booleans
and retention of the original stored value; the second checks operational-error
propagation. Both separate probes show direct wiring returning `{'created': None}`,
raising `Duplicate` on repetition, preserving the original value and propagating
`OSError('offline')`. Their actual assertions and outputs were reviewed, not only
the exits. No native-output recovery or author rerun was necessary.

Both recommend keeping the translation boundary and explain compatible inlining:
the policy must move into `service.save`, coupling it to the driver's signaling.
Both distinguish unavailable staging evidence and do not manufacture a receipt.
No implementation edit, dependency installation or external service call appears
in the original commands.

All initial project bytes/modes equal the final captured inventory. Installed skill
resources and captured before-model/before-collector index bytes/modes match.
These are boundary observations, not proof about every transient action or all Git
metadata. Original command discovery stays inside the project. No private initial
instructions or session files are published; known-pattern path/credential scans
are a limited export check, not a universal privacy guarantee.

Before timing, the existing native preflight, seven inherited scheduling controls,
the Store fixture check and candidate frontmatter validation passed. Frozen hashes
and the sole changed file (`landlord/SKILL.md`) were checked. These native checks
are distinct from the model observations. Ordinary skills, personal installation,
hosted download, featured benchmark and both README cost claims remain unchanged.

한국어: 기존/후보 한 쌍에서 토큰19.85%·시간14.80% 감소했지만, 기존 버전도 이미
두 검사를 같은 도구 호출에서 실행했다. 차이는 탐색·소스 읽기를 묶은 구간이므로
추가 지침의 효과로 단정할 수 없다. 두 버전의 실제 검사·추천·파일 보존은 확인했지만
기본 스킬에는 지침을 추가하지 않는다. 노출된 단일 과제 결과이며 전체8개 효율
개선의 증거가 아니다. 유리한 수치만으로 대표 차트나 설치 파일을 바꾸지 않는다.
