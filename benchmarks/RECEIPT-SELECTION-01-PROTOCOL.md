# Receipt selection 01: frozen development comparison

2026-09-15. [Native preflight and task definition](RECEIPT-SELECTION-01-PREFLIGHT.md).
No outcome assumptions or model evidence at freeze time.

One authored allocation scenario has two matched support conditions: an adequate
existing native comparison command is present or absent. This is **not two
independent real-world projects**. Each gets baseline (no skill), original Receipt
at `6cf9fb1`, and candidate at `ca3da48`. Only entry/reference tool-selection
guidance differs between skills; executable helpers and other resources match.

Six fresh sessions, Astra `gpt-6-astra`, medium, one repeat, serial, 360 seconds per
session. Fixed order: present baseline/original/candidate, then absent candidate/
original/baseline. Reversing order does not eliminate host/cache/time confounding;
original is always in the middle. No statistical superiority or all-eight claim.

## Scoring before execution

All four explicit task criteria are necessary for full-task success:

1. Same five native tests/current assertions against the actual parent and latest
   allocation implementation, changing no other compared source.
2. Actual defect-specific before/after values and passing controls, preserving
   each test process's exit. Setup errors do not reproduce the defect.
3. Full revision identities and copy-local allocation imports in the native test
   process, not a separate import-only check.
4. Original files/modes/resources preserved; project-local owned scratch removed;
   no production edits, installs, network, external discovery or commits.

Tool choice is descriptive, **not a fifth required criterion**. An adequate native
solution when support is absent or helper solution when present is not automatically
wrong. Record command/resource reads and duplicate work, but judge equal-work cost
and actual obligations. A cheaper incomplete task is not an accepted win.

Keep every scheduled original attempt. No retries for unfavorable results,
timeouts or missing observation; inspect the original live handle/stored streams.
Stop on detected quota limits. Preparation runs native positive/negative controls,
checks fixture identity and snapshots immutable resources without model calls.
Execution rejects changed inputs and a second invocation. The start marker does
not prove liveness; process/tool handles do. Do not alter frozen tasks mid-run.

## Evidence and interpretation

Record original outputs, total input plus output tokens (cached input included
once), wall seconds, per-criterion outcomes, original bytes/modes/resources and
cleanup. Inspect matching persisted initial context for actual skill injection;
disable requests alone do not establish removal. Inspect stored tool responses
when CLI captures are incomplete. Redact local paths and exclude private full
instructions before publishing original evidence.

No feature-graph promotion from this paired development probe. Even a favorable
result requires transfer to other developer tasks and real-source workflows; an
unfavorable result stays visible. This follows task-specific evaluation rather
than broad claims from a small test in [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

Run `python3 -B benchmarks/run_receipt_selection_01.py` to prepare. Review snapshots
and commit this protocol/runner, then run the same command with `--execute` once.

한국어: 같은 업무 과제에서 기존 도구 유무를 나누고 무스킬·수정 전·수정 후를
각각 1회 비교한다. 도구 선택을 정답으로 강제하지 않는다. 네 가지 검증·보존
요구사항을 모두 충족한 작업의 전체 토큰·시간을 비교하고 모든 실패도 보존한다.
작성된 소규모 개발 실험이므로 실제 프로젝트 전반의 성과나 대표 그래프로 확대하지 않는다.
