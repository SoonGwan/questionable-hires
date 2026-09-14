# Checkpoint 09 history/schema review — 2026-09-14

Partial review of launch `3a7d972`, resources `9071a1c`;
[whole-run intake](BUNDLE-CONTRACT-09-INTAKE.md). These two skill pairs use more
tokens and time. Correct conclusions do not convert them into efficiency wins.

## History: relevant evidence, not a helper-reading regression

Both arms read current labels.py and consumer.py, inspect the compatibility patch
`d5fc9729e83eca829c17b3981abfb70be9df1f24`, and distinguish historical intention
from the current name-only partner caller. Both correctly recommend retaining
the fallback while API v1 support remains in the supplied contract.

Both observe the current caller returning Ada. Skill replaces the consumer's
bound display_label in memory and observes None without fallback. Baseline
evaluates the same name-only payload directly and additionally observes the empty
display_name fallback. Direct-index KeyError is a source-based inference in their
answers, not a captured direct-index execution. Baseline reads the initial patch
too; skill uses blame plus the compatibility patch. Both make three shell calls.
Skill reads its entry only, not the optional history collector or reference.

Baseline: 63,725 tokens / 26.243s. Skill: 67,142 / 33.129s. Additional entry context
is observable, but this n=1 comparison cannot isolate the token/time cause. There
is no observed repeated helper-source reading to fix in this pair. Do not add a
blanket prohibition on history or remove current-caller evidence to reduce cost.

## Schema: native SQL route adopted; cost still higher

Both read the actual release procedure, three migration files and two literal
reader queries. Both execute four states and all eight old/new reader outcomes:
initial, up, up after committed update/insert, and down retaining those writes.
The old query fails after up and new query fails after down, with actual missing
column errors. Updated Unicode values, an untouched row and an inserted row
survive down in the observed outputs. Both correctly block the stated rollout
and old-binary-first rollback, distinguish data survival from compatibility, and
leave actual application writers and staging unverified.

Baseline additionally asserts an explicit expected three-row list and runs an
integrity PRAGMA. Skill compares ordered before-down and after-down lists; actual
captured values support its narrower data-survival statement. Neither executes
application writer code or independent database connections. Both use native
in-memory SQLite, create no retained harness, and preserve all six supplied files.

Skill reads only its entry, chooses native SQLite, and never loads the optional
matrix guide or helper. It uses four shell calls versus baseline three; entry
and project reads are separate. A claim that matrix adoption caused this overhead
would contradict the trace. Baseline: 65,363 tokens / 50.518s; skill: 70,118 /
69.323s. Unequal witnesses and shared-host timing prevent attributing this to a
particular paragraph or predicting savings from another wording change.

## Separate witness replay and limits

[Replay script](replay_bundle_contract_09_readonly.py) extracts each original
Python witness literally (three heredocs and one `-c` argument), runs it in a
disposable project-local copy with bytecode disabled and a 20-second deadline,
and records the [four results and sources](results/bundle-contract-09-readonly-controls/author-replay.json).
All four exit 0; their full stdout is contained in the respective original
capture without normalizing versions or values. No timeout or stderr. Copy and
retained project inventories remain unchanged, and all original file bytes match
the frozen cases. No unrelated retained artifacts were added.

This replays Python witnesses, **not the entire shell, Git history, model reasoning
or independent fault controls**. Original captured patches supply the history
evidence; replay does not recreate it. Printed successful reader observations are
not equivalent to assertions on every column/row or production readiness. Later
failure-control work, remaining pair review and whole-run publication remain due.
No skill edits, new model runs or graph changes are justified by this review alone.

## 한국어

이력·스키마 과제는 두 모델 모두 근거 있는 결론을 냈지만 스킬 비용이 더 컸다.
이력은 양쪽 모두 3번 조회했고 스킬은 현재 호출자를 실제로 연결해 확인했다.
스키마 스킬은 도우미를 읽지 않고 직접 SQLite를 실행했다. 따라서 이번 증가를
도우미 남용으로 설명하거나 필요한 증거를 줄이는 수정은 하지 않는다.

원본 Python 검증 코드 4개를 별도 복사본에서 그대로 실행했고 출력은 원본
캡처에 모두 포함됐다. 파일은 보존됐다. 이는 Python 검증의 재현이지 전체
세션·Git 이력·별도 결함 대조군의 재현은 아니다. 스키마의 실제 애플리케이션
쓰기와 운영 준비도도 미확인이다. 나머지 검토와 전체 결과 공개는 계속 필요하다.
