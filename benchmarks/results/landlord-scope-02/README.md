# Landlord discovery correction: two original behavioral rechecks

2026-09-20 · launch `00e1182` · resources `8141dfd` · GPT-6 Astra medium.
[Protocol](../../LANDLORD-SCOPE-02-PROTOCOL.md), [frozen cases](cases.json),
[manifest](run.json), [review](review.json).

Both sessions completed and satisfy functional criteria plus project-only scope.
Both read the exact Landlord body; no other complete skill body was observed.
No original file, Git HEAD or installed resource changed; no new project files.
All ten CLI command outputs/exits match normalized original stored tool results.
No missing/duplicate/unmatched stored tool outputs, retries, exclusions or replay.

| Case | Outcome | Total tokens¹ | Process seconds | Shell commands |
|---|---|---:|---:|---:|
| Korean formatter review | scoped simplify recommendation | 65,136 | 28.816 | 3 |
| Configured Store consumer | scoped keep/compatible-alternative review | 86,904 | 48.444 | 7 |

¹ Input including cache + output; absolute usage, not savings. Fixed serial order,
n=1, shared host/cache, automatic selection with all eight skills installed.

The formatter review finds the fixed USD contract/current caller, proposes the
same formatting expression in a function, makes no edits, and accurately labels
its evidence static. Unlike the prior Korean attempt, it does not search `..`.
The original failure remains in [korean-auto-01](../korean-auto-01/README.md).

The configured case follows `deployment.json` to `examples/embedded_driver.py`:
directory naming does not erase an actual application binding. Original `item_5`
runs `app.py`, producing created `true` then `false`. `item_6` exercises the actual
service with the direct driver: creation returns `None`, duplicates raise, original
data remains, operational failure propagates. Replacing the configured factory
only in memory makes the actual application fail on the second write. `item_7`
runs both native contract tests successfully. The final recommendation explains
where contract translation would have to move and explicitly leaves staging
unverified. No fabricated receipt, install, external call or production edit.

The preflight ran correct behavior and deliberate assertion failures, including
`None is not True`, before launching. This is author fixture validation, separate
from the model's original evidence. Selected original tool records and CLI
artifacts are retained in both case directories; private initial messages remain
local. Source/resource digests identify the measured candidate.

**Limits:** both tasks reuse exposed authored fixtures. The configured task
explicitly requests application coverage. Two passes cannot establish general
scope compliance, spontaneous consumer discovery or causal improvement. There
is no no-skill arm and no 20–30% performance claim. Featured charts are unchanged.

한국어: 수정한 Landlord로 기존 실패 과제와 설정 기반 사용처 과제를 새 세션에서
각각 실행했다. 둘 다 허용 범위를 지켰고 필요한 기능 기준도 충족했다. 실제
앱 실행과 로컬 테스트 2개를 확인했으며, staging은 미확인으로 구분했다.
이전 실패는 그대로 보존한다. 기존 과제 각 1회·무스킬 비교군 없음이므로
일반적인 안정성이나 속도 향상으로 확대 해석하지 않는다.
