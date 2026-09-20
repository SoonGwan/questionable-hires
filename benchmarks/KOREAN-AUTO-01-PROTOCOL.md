# Korean automatic-selection screen 01

2026-09-20. Resource revision `2990f44`, all eight skills installed. Ten fresh
GPT-6 Astra medium sessions, serial, one per task, 240-second limit. Fixed order:
the eight main-suite roles, then plain label and README typo controls. No explicit
skill name in any task; `run.py` uses its auto arm without adding a skill request.
Its project-only/no-external-services/no-delegation wrapper remains in English.

This checks deployment behavior in Korean, **not token/time improvement**. There
is no no-skill arm. The eight positive projects and functional criteria are reused
from `cases.json`; only the user request is translated, with a common explicit
project-scope restriction. This is not a new held-out real-project evaluation.
Two negative controls are ordinary text edits without audit/redesign cues.

## Before execution

`test_korean_auto_cases.py` verifies unchanged positive source/history/criteria,
eight distinct expected roles, two negatives and absence of skill names in tasks.
Actual native controls exercise legacy fallback removal failure, eligibility
before/fixed boundaries, existing formatter outputs, deterministic forward/reverse
async completion, surviving missing-write mutation plus stronger failure, and
SQLite reader compatibility through up/down. Async cleanup is bounded/owned;
SQLite is in-memory. These author checks are not injected into model projects.

Preparation records hashes, snapshots every committed resource, executes those
controls and makes no model calls. Commit the inputs before one `--execute` launch.
Reject changed inputs/resources and an existing execution marker; the marker
alone is not evidence of a live process. Keep timeouts/errors and stop on quota.
No favorable replacement, source edits during execution, or hidden retry.

## What is reviewed

Record separately:

1. Catalog exposure and actual body exposure for **each** of the eight skills,
   from persisted initial context and original tool responses. Announcing a role
   or merely listing its filename does not establish a body read. Disable flags
   alone do not establish removal of other instructions. Never publish private
   full initial messages or unrelated catalog names.
2. Selected role(s), timing, and unnecessary activation on the two negative
   controls. Expected primary roles are author metadata, not model-visible hints.
   Adjacent roles are not automatic failures: judge whether they serve the actual
   request. No-body/direct completion is recorded rather than silently discarded.
3. Actual functional delivery against the unchanged criteria, scope, changed
   files and native evidence. Routing success is not task success; finishing the
   task does not establish correct routing or broader performance.
4. Total input plus output tokens and wall time as absolute observations only.
   Shared host/cache, one sample, translated exposed tasks and no paired baseline
   prevent efficiency or population precision/recall claims.

Do not force a skill to activate, disable implicit invocation, or broaden every
description to pass this set. Change descriptions only for evidenced ambiguity,
then use independently phrased controls. Existing performance charts stay frozen.
Implicit selection is based on matching descriptions; see the [official skill
documentation](https://learn.chatgpt.com/docs/build-skills).

한국어: 설치한 8개 스킬을 이름 없이 한국어로 요청했을 때 실제 선택·작업 완료와
단순 수정에서의 불필요한 활성화를 확인한다. 기존 작성 과제의 한국어 요청 8개와
일반 수정 2개이며, 성능 비교나 새로운 실프로젝트 표본이 아니다. 선택과 기능
성공을 구분하고 초기 문맥·실제 본문 읽기·실행 결과를 원본으로 확인한다.
