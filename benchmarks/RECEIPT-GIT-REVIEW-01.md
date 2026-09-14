# Receipt Git review preservation — 2026-09-14

Parent `65c2340`. Candidate guidance, tested with native Git 2.50.1
(Apple Git-155); not a model benchmark or a performance win.

## Observed reason

The [native-mode author replay](RECEIPT-NATIVE-MODEL-01-REVIEW.md) retained
`.git/index` changes during Git review after the helper's preservation interval.
The helper's unchanged result never covered those later operations. Do not
reinterpret those frozen runs as whole-session metadata preservation.

Two new tests in `tests/test_receipt_git_review.py` use disposable actual Git
repositories, staged owner work, unstaged tests and an untracked owner file.
An unchanged implementation receives an older timestamp, making cached index
stat information stale without changing its bytes or relying on a sleep.

The first proposed prefix, `git --no-optional-locks`, failed both author tests:
the index still changed. Individual native commands showed status preserving it
but `diff --check` changing it. Adding command-local
`-c diff.autoRefreshIndex=false` makes the combined review preserve the index
and full tree inventory. No persistent Git configuration is changed by the
proposed review command. The fixtures explicitly configure ordinary refresh on
and disable fsmonitor/untracked cache to isolate this mechanism.

The final tests establish:

- Whitespace, unstaged diff, staged diff and untracked-inclusive status outputs
  exactly match ordinary review. Actual staged, unstaged and untracked changes
  remain visible. The ordinary-review adverse control changes the index.
- Literal native unittest before/after comparison still reproduces the boundary
  assertion failure and then passes. Owned copies are removed, and the full
  source inventory remains equal after the proposed follow-up Git review.

Validation: 2 new tests / 0.732s, 13 native invocation tests / 6.251s,
12 build tests / 3.281s, all passing. The guide grows 295 bytes from 6,953 to
7,248. Entry instructions, runtime, output and examples are unchanged.

## Scope and evidence

The new paragraph applies only when verification must preserve Git metadata.
It suppresses these refresh mechanisms, not arbitrary command, driver, hook or
submodule effects, and cannot make a mutating command read-only. Tree inventory
covers entry names/types, bytes/modes and link text, not timestamps/ownership,
transient effects or concurrent operations. This is a local operational test,
not a claim of all-version behavior, model adoption, lower token cost or a broad
20–30% improvement. Model results, charts and featured pointer are unchanged.

Git documents the optional status refresh in
[git-status](https://git-scm.com/docs/git-status#_background_refresh), and the
separate default-enabled diff refresh in
[git-diff](https://git-scm.com/docs/git-diff#Documentation/git-diff.txt-diffautoRefreshIndex).
The candidate uses both controls because the native test demonstrated that the
first alone was insufficient here.

## 한국어

기존 재실행에서 비교 후 Git 조회가 인덱스를 바꾼 문제가 있었다. 실제 임시
저장소로 확인한 결과 `--no-optional-locks`만으로는 부족했고, 명령별로
`-c diff.autoRefreshIndex=false`도 지정해야 이번 환경의 갱신을 막았다.
기본 조회와 출력은 동일하고 스테이징·미스테이징·미추적 변경은 모두 보였다.
실제 전후 테스트와 뒤이은 조회까지 파일 내용·권한 등 전체 목록이 유지됐다.

관련 테스트 27개가 통과했다. 안내는 295바이트 늘었고 영구 설정·실행 코드는
변경하지 않았다. 모든 Git 부작용을 막는 기능이나 모델 성능 개선 실측은
아니다. 첫 제안의 실패와 기존 재실행의 변경 기록도 그대로 보존한다.
