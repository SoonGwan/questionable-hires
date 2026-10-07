# English-first onboarding — 2026-10-08

The canonical README was already English, with Korean in `README.ko.md`. Both now
introduce the executable Con Artist example before the benchmark section. Existing
English artwork and localized chart labels are retained; no chart or measured
performance value has been changed.

The website root now serves complete English HTML without JavaScript. Fresh visitors
start in English; explicit locale paths, `?lang=ko|en`, and saved language preferences
still take precedence. `/ko/` continues to serve Korean. The app script URL includes
a source hash so cached browser-language detection does not override the new default.

The actual helper ran locally on its trusted sample recipe. Both lost-write and
duplicate-write mutations produced the expected observations: original tests passed
on correct and faulty copies, while stronger probes passed on correct code and failed
on both faulty copies. Original files were not changed. No model provider was used;
this is not new model performance evidence.

The frozen featured benchmark and adverse whole-team measurements are unchanged.
Featured-source synchronization and generated-file checks pass. The local landing
suite passes **19 tests**. These checks validate onboarding and static output, not
whole-team quality or token savings.

The [Show HN introduction and publication status](SHOW-HN.md) distinguish the runnable
helper from model measurements. Publication is blocked by Hacker News's temporary
Show HN restriction observed on the owner's signed-in account.

## 한국어

기존 영어 README를 유지하고 양쪽 README에 실제 실행 가능한 Con Artist 예시를
앞쪽에 추가했습니다. 사이트 첫 방문과 JavaScript 없는 루트는 영어로 시작하며
언어별 경로·URL 설정·저장된 선택은 유지합니다. 기존 그림과 한영 차트도 보존합니다.

샘플의 저장 누락·중복 저장 두 결함을 실제 실행으로 확인했고 원본 파일은 유지했습니다.
모델 호출이나 새로운 성능 측정이 아닙니다. 기존 대표·불리한 실험 수치는 그대로이며
대표 근거 동기화·생성 파일 검사와 로컬 랜딩 검사19개가 통과했습니다.
HN은 현재 계정에 표시된 Show HN 임시 제한 때문에 게시되지 않았습니다.
