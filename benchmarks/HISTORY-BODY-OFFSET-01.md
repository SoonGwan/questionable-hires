# History body offset01 — local allocation correction, 2026-09-27

Candidate on parent `d8e39d5f`; exact old/new source hashes in the
[author profile](results/history-body-offset-01/profile.json).
The prior [patch-streaming checkpoint](HISTORY-PATCH-MEMORY-01.md) removes the
whole line list but still copies the complete patch body before iterating it.
This change uses its starting offset in the original string instead. Full-tail
validation,selected rows/order,omission markers,budgets and fallback behavior stay.
CLI and existing one-argument iteration remain compatible; no new skill guidance.

The new native regression [fails before](results/history-body-offset-01/before.txt):
2,717,506bytes is above600,000. It passes after. A valid40,000old/new-row patch
produces exactly the same selected excerpt; malformed extra tail still rejects.
CR/LF/Unicode and chunk boundaries are covered. [Checkout49](results/history-body-offset-01/after.txt)
and [Git-free49](results/history-body-offset-01/git-free.txt) pass without skips.
The first archive omitted the scratch benchmarks directory and had5 setup errors;
[original failure](results/history-body-offset-01/git-free-first.txt.gz) retained and
archive corrected. Those setup errors are not defect reproduction or passing tests.

Author traced peak: **2,717,506→259,653bytes**,about90.45% less. Input allocated
before tracing;this is only allocations inside excerpt selection,not total RSS,
Git/subprocess memory or a total cap. Full input/Git output still exists; unusually
long rows can exceed nominal chunk size. Existing input/source bounds are unchanged.

Ten alternating untraced author pairs: median0.031413→0.031115s,less than0.3ms.
No repeatable speedup or model whole-task token/time claim. One synthetic large
sparse patch on one Python3.11.6 host,not independent workflow validation. Outputs
compare exactly every time. No model reruns or featured chart changes.

[Owned installation](results/history-body-offset-01/installed.json) copies all8
skills/51files,checks byte/mode parity,and exercises the actual installed CLI on
a40,000-line native Git commit. Current line20000 and selected new-row19999 are
correct;prefix truncation remains explicit. Owned copies removed. Skill metadata
validator passes;these are local install/functionality controls,not remote release.

한국어: history-body-offset01(2026-09-27,부모`d8e39d5f`)은 큰 패치 본문 전체의
불필요한 복사를 제거했다. 같은 선택 결과·잘못된 꼬리 거부를 유지하며 로컬 추가
할당2.72MB→0.26MB,저장소·Git 없는 복사본49개 검사가 통과했다. 실제 격리
설치8개 스킬·51개 파일과 설치된 Git 조회를 확인했다. 시간 차이는1ms 미만이며
모델 전체 토큰·시간 개선이나 전체8개 역할 목표 달성으로 해석하지 않는다.
