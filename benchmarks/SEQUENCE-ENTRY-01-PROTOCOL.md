# Sequence entry verification pilot 01 — frozen before model execution

2026-09-21. One extracted real repository issue, two fresh serial sessions:
no-skill baseline followed by Receipt, n=1. GPT-6 Astra medium, 360 seconds/cell.
Use the existing `run.py`, `--arms baseline skill --seed 0 --repeats 1 --jobs 1
--persist-session`, frozen `sequence-entry-case-01.json`, and Receipt resources
extracted from `9f0cd19`. The output directory is newly reserved exactly once.
No replacements/retries/exclusions; retain failed work and stop on account limits.

## Inputs and provenance

`sequence_entry_case.py --freeze` extracted implementation bytes from `8804ee4`
and `ec4a538`, test bytes from `87513cb`. The JSON contains their hashes. The actual
source/tests are unchanged; project history, task instructions, notes and selected
test list are authored for this pilot. This is **not** an untouched external repo,
held-out issue, or a claim that its new fixture commits are original commits.
No test-selection change may occur after launch. Model-visible instructions
disclose all scored obligations, including same-process dynamic import identity,
preserving Git state and removing comparison scratch without a retained harness.

The eight selected native tests exercise real early return, exception, cancellation,
overlap cleanup, cooperative setup, timeout cleanup and healthy/stale controls.
Exact prepared-project preflight observes four async-wait errors before, eight
passes after, actual loaded copy paths, unchanged originals and removed copies.
Those errors are behavior-specific timeout propagation, not failed test discovery
or import setup. Full native evidence is required; exit codes alone are insufficient.
No new test instrumentation is supplied to the model as an answer. The author
bootstrap used for preflight is not a project input. A model may use suitable
native setup or optional Receipt support; helper adoption is not a pass condition.

## Review and cost

Review all five frozen criteria from original native outputs, loaded paths,
revision identities, fixed-file hashes, before/after project snapshots and modes.
Retain any repairs, additional checks, capture omissions and differing work.
Preserve the raw CLI output privately until privacy and original-session review;
do not publish initial system instructions. Check exact skill exposure and reconcile
recorded response input/output/cache counters before publishing cost claims.

Report each arm's success, input+output tokens (cached input once), process wall
time and recorded response count. A lower time with more tokens is mixed, not a
combined efficiency win. No single-pair result, favorable or adverse, establishes
general superiority or a 20–30% gain. This is a support-adoption/cost diagnostic
on a known issue, not a new candidate-selection contest. Do not repeatedly retune
this task, promote its numbers into the featured chart, or erase an adverse result.

한국어: 실제 저장소에서 추출한 한 이슈를 무스킬·Receipt 두 새 세션으로 비교한다.
코드와 테스트는 그대로지만 이력·지시문은 이 비교를 위해 작성했음을 공개한다.
정상·결함·로드 경로·보존 조건과 전체 비용을 함께 검토하고, 불리한 결과와 복구
비용도 남긴다. 한 쌍의 결과를 전체 우위나 대표 그래프로 승격하지 않는다.
