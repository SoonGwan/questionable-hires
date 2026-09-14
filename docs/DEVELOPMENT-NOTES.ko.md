# 개발 검증 기록 — 2026-09-14

`17ede49`의 README에서 옮긴 과거 기록입니다. 아래 스킬 버전·측정값·한계는
그대로이며 상대 링크만 새 위치에 맞췄습니다. ‘최신’ 등의 표현은 이 기록
당시를 뜻합니다. 현재 상태는 [검증 현황](../benchmarks/CURRENT-CANDIDATE-STATUS.md)을
확인하세요. [설치·사용 안내로](../README.ko.md) · [English](DEVELOPMENT-NOTES.md)

[구조 관리인·범위 협상가의 탐색 지침 검증](../benchmarks/DISCOVERY-ROUTING-01-REVIEW.md)은
아직 절감 효과를 입증하지 못했습니다. 파일 내보내기는 스킬 비용이 늘었고,
Store 검토는 연결 오류 후 시간 초과됐습니다. 모든 시도와 사용량 누락을 그대로 남겼습니다.

- **범위 협상가(`hostage-negotiator`):** 프로젝트에 동등한 테스트 도구가 없을 때 [비동기 호출 제어 도구](../skills/hostage-negotiator/references/async-callback.md)로 반복적인 시작·완료 신호 코드를 대체할 수 있습니다. 앱 동작 검증과 태스크 정리는 테스트가 담당합니다. [모델의 실제 사용](../benchmarks/HOSTAGE-CALL-MODEL-01-REVIEW.md)은 확인했지만 기준 실행 시간 초과와 원본 테스트 출력 누락 때문에 효율 비교는 인정하지 않습니다. 별도 재실행에서 구현 통과·결함 대조군 검출을 확인했으며, 이는 원본 누락을 대신하지 않습니다.
  [복사 확인 모델 실험](../benchmarks/HOSTAGE-COPY-CHECK-MODEL-01-REVIEW.md)에서 바이트 비교는 채택했지만 구현 전체 읽기는 남았습니다. 원본 테스트 43개 통과와 별도 결함 재실행 12개의 예상 결과를 확인했으며, 효율 향상을 입증하지는 못했습니다.
  선택형 [작업 종료 감지 대기](../benchmarks/HOSTAGE-ENTRY-WAIT-MODEL-01-REVIEW.md)를 새 모델도 채택했습니다. 마지막 원본 테스트 45개 통과, 별도 재실행에서 누락된 콜백 8건을 약 0.10초에 검출했습니다. 첫 테스트 출력 누락은 남아 있으며 모델 전체 효율 향상을 주장하지 않습니다.
  [Python 작업 종료 감지 대기](../benchmarks/HOSTAGE-PYTHON-ENTRY-WAIT-01.md)도 지원합니다. [Python 채택 실험 01](../benchmarks/HOSTAGE-PYTHON-ENTRY-MODEL-01-REVIEW.md)에서는 중복 반환값의 과잉 검증을 발견했습니다. 지침 수정 후 [키별 가져오기 실험 01](../benchmarks/HOSTAGE-KEYED-IMPORT-01-REVIEW.md)은 정상 대체 반환값을 허용하고 중복·복구 결함을 잡았지만, 테스트의 부차적 진단 오류가 남았고 비용 절감도 입증하지 못했습니다(118,971토큰·103.161초). 과제의 명시적 계약 설명 때문에 스킬만의 효과는 분리할 수 없습니다.
  [의존 단계 안내](../benchmarks/HOSTAGE-DEPENDENT-PHASES-01.md)와 [최종 검사 묶기](../benchmarks/HOSTAGE-FINAL-BATCH-01.md)를 [새 모델 실험 01](../benchmarks/HOSTAGE-FINAL-BATCH-MODEL-01-REVIEW.md)에서도 채택했습니다. 95,992토큰·94.261초·명령 4회이며 별도 결함 실행의 추가 오류도 사라졌습니다. 원본은 10개 통과 요약 중 5개 테스트 이름이 누락됐습니다. 이전 단일 실행 대비 토큰 19.31%·시간 8.63% 감소는 작업량·캐시·출력 누락 차이 때문에 일반적인 개선으로 주장하지 않습니다.
  [JavaScript Promise 호출 제어 도구](../skills/hostage-negotiator/assets/controlled_call.mjs)도 독립 ES 모듈로 사용할 수 있습니다. [네이티브 검증](../benchmarks/HOSTAGE-JAVASCRIPT-CALL-01.md)에서 동일성과 결함 검출을 확인했습니다. [모델 비교](../benchmarks/HOSTAGE-JAVASCRIPT-PANEL-01-REVIEW.md)에서 도구 사용과 회귀 테스트 통과는 확인했지만, 작성자 제작 과제 1개에서 기본 실행보다 **토큰 93.51%, 시간 11.32% 증가**했습니다. 효율 향상이나 브라우저 검증을 주장하지 않습니다.
  현재 모듈에는 등록한 작업의 대기 시간과 호출 정리를 관리하는 선택형 [테스트 정리 래퍼](../benchmarks/HOSTAGE-JAVASCRIPT-SCOPE-01.md)도 있습니다. 이를 실제로 사용한 [새 개발용 비교](../benchmarks/HOSTAGE-JAVASCRIPT-SCOPE-MODEL-01-REVIEW.md)에서 회귀 검증을 유지했고 **전체 토큰은 10.80% 증가, 시간은 6.70% 감소**했습니다. 직접 작성한 테스트는 줄었지만 복사한 도구까지 합하면 코드가 더 많습니다. 일반적인 효율 개선을 주장하지 않으며, 앞의 비교 수치는 래퍼 추가 전 결과입니다.
  이후 [사용법을 먼저 읽는 방식도 실측](../benchmarks/HOSTAGE-JAVASCRIPT-USAGE-MODEL-01-REVIEW.md)했습니다. 실제 읽기는 줄었지만 새 비교에서도 **토큰 30.82% 증가 / 시간 6.75% 감소**였습니다. 이미 개선에 사용한 과제 한 개의 결과이며 전체 효율 개선은 아직 입증되지 않았습니다.
  [두 단계 미리보기 작업](../benchmarks/HOSTAGE-JAVASCRIPT-PREVIEW-01-REVIEW.md)에서는 **토큰 14.22% 증가 / 시간 31.46% 감소**였지만, 추가로 넣은 상태 내용 덮어쓰기 결함을 스킬 테스트 54개가 모두 놓쳤습니다. 기본 실행은 이를 잡아냈습니다. 시간만으로 개선 성공을 주장하지 않으며 회귀 검증을 보강해야 합니다.
  보강한 지침을 사용한 [새 모델 테스트도 해당 결함을 검출](../benchmarks/HOSTAGE-STATE-CONTENTS-MODEL-01-REVIEW.md)했고 정상적인 내부 수정은 허용했습니다. 스킬 단독 실행은 171,403토큰 / 130.943초였으며, 동작 보강의 증거이지 새로운 효율 비교는 아닙니다.
  [출력 누락 대응 지침](../benchmarks/HOSTAGE-MISSING-EVIDENCE-01.md)을 [인수인계 조건 3개](../benchmarks/HOSTAGE-EVIDENCE-01-REVIEW.md)로 확인했습니다. 입력 일치와 정확한 코드 복구 뒤 기존 보고서를 재사용했지만, 보고서 없는 실행은 새 테스트를 요청하고도 원본 결과 출력이 누락됐습니다. 별도 재검증은 그 누락을 채우지 않으며 모델이 본 출력과 기록의 차이는 미확인입니다. 효율·전체 채택 성공은 주장하지 않습니다. [수집기 표시](../benchmarks/HOSTAGE-VERIFICATION-DELIVERY-01.md)는 자동 채점이 아닌 검토 후보입니다.
  [문서별 발행 과제](../benchmarks/HOSTAGE-KEYED-PUBLISH-01-REVIEW.md)에서도 도구 재사용과 단독 테스트 종료 상태를 확인했지만, 토큰 25.25%·시간 7.64% 증가 및 원본 출력 일부 누락으로 효율 개선은 인정하지 않습니다. 별도 대조군 검증은 정확성을 뒷받침하며 원본 누락을 대신하지 않습니다.
  최신 [단일 파일 안내](../benchmarks/HOSTAGE-SINGLE-READ-01.md)는 [새 모델 실험](../benchmarks/HOSTAGE-SINGLE-READ-MODEL-01-REVIEW.md)에서 실제로 사용됐고 필요한 검증도 유지됐습니다. 토큰 6.42% 증가·시간 7.50% 감소를 기록했지만, 하위 테스트 구성·추가 검증량 차이와 원본 개별 출력 일부 누락으로 일반적인 효율 향상은 주장하지 않습니다.
- **테스트 사기 감별사(`con-artist`):** 임시 복사본에서 Python 결함 주입, 복사본 import 검증, 테스트별 종료 상태, 로그 메모리·시간 제한을 처리합니다. [사용법과 한계](../skills/con-artist/references/python-audit.md). 샌드박스가 아니므로 신뢰할 수 있는 테스트만 실행해야 합니다.
  [네이티브 안내 분리](../benchmarks/CON-ARTIST-PROBE-ROUTING-01.md)는 [후속 모델 실험](../benchmarks/CON-ARTIST-PROBE-ROUTING-MODEL-01-REVIEW.md)에서 실제로 사용됐고 네 단계 검증도 유지됐습니다. 96,455토큰·46.178초로 이전 스킬 실행보다 토큰 3.42%·시간 6.35% 낮았지만 이전 기본 실행보다 토큰은 11.96% 많았습니다. 작업량·단일 표본·공유 캐시 차이 때문에 인과적 개선이나 기본 실행 대비 우월성은 주장하지 않습니다.
  [SQLite 적용 실험 01](../benchmarks/CON-ARTIST-SQLITE-01-REVIEW.md)은 모듈 간 함수 연결과 기존 테스트 준비 코드를 통해 실제 디스크 커밋을 검증했습니다. 스킬은 네 단계 출력을 확보했지만 토큰 15.92% 증가·시간 28.65% 감소였습니다. 기본 실행의 원본 정상 테스트 출력 누락은 별도 재검증으로 채우지 않습니다. 도구 활용은 확인했지만 일반적인 효율 향상은 미입증입니다.
  [기본 안내 후보 01](../benchmarks/CON-ARTIST-CORE-GUIDE-01.md)은 기본 문서 크기를 27.81%, 상세 문서까지 합치면 9.27% 줄였고 도구·패키징 테스트 88개가 통과했습니다. [이후 모델 실험](../benchmarks/CON-ARTIST-CORE-GUIDE-MODEL-01-REVIEW.md)은 73,679토큰·35.540초로 네 단계 검증을 수행했지만 프로젝트 코드와 안내를 읽은 기록이 없습니다. 안내 채택은 미확인이며 낮아진 기록만으로 수정 효과를 인정하지 않습니다.
  [실행기 종료 후 정리](../benchmarks/CON-ARTIST-PIPE-EXIT-01.md)를 개선해 자식 프로세스의 출력 파이프 때문에 완료된 검사를 중단하던 문제를 해결했습니다. 실제 결함 생존·검출 검사는 통과했습니다. 남은 그룹 구성원은 종료하므로 백그라운드 실행기는 지원하지 않으며, 모델 작업 전체의 절감 효과는 아직 미측정입니다.
  [완료된 checkpoint 06](../benchmarks/BUNDLE-CONTRACT-06-REVIEW.md#persistence-audit--skill)에서는 모델이 도우미를 실제 사용해 네 가지 감사 검증 출력을 확보했습니다. 노출된 단일 과제에서 토큰·시간 기록은 줄었지만, baseline의 추가 수정·출력 누락으로 작업량이 다릅니다. 원본·리소스 대조는 완료했으며 파이프 수정 자체의 절감 효과는 분리 측정하지 않았습니다.
  필요한 경우 [읽기 전용 맥락 수집기](../skills/con-artist/references/python-context.md)에 정의 이름이나 오류 추적에 나온 `file.py:123`을 지정해 해당 함수·클래스 본문, 상위 경로의 지침·설정, conftest 색인을 한 번에 모을 수 있습니다. 프로젝트 코드를 import하지 않으며, 색인은 탐색을 돕는 자료이지 테스트 동작이나 모든 의존성을 검증한 결과가 아닙니다.
  [물리적 줄 번호 처리](../benchmarks/CON-ARTIST-PHYSICAL-LINES-01.md)를 고쳐 문자열 속 유니코드 구분 문자 때문에 코드가 잘리거나 줄 번호가 밀리는 문제를 해결했습니다. 로컬 소스 무결성 검증은 통과했으며 모델 비용 효과는 아직 미측정입니다.
- **레거시 고고학자(`necromancer`):** 선택한 코드 줄의 현재 상태와 Git 이력을 모으고, 미커밋 변경·얕은 이력의 한계를 표시합니다. [사용법과 한계](../skills/necromancer/references/focused-history.md). 과거 코드를 지금도 유지해야 하는지는 별도로 판단합니다.
  [Git 줄 경계 처리](../benchmarks/NECROMANCER-PHYSICAL-LINES-01.md)를 고쳐 현재 코드·줄별 이력·변경 발췌에서 문자열 속 구분 문자와 CR을 그대로 보존합니다. 실제 Git 검증은 통과했으며 모델 비용 효과는 아직 미측정입니다.
  [세 가지 판단을 요구한 개발 실험](../benchmarks/results/necromancer-regions-01/README.md)에서 두 방식 모두 판단을 맞혔고, 스킬은 토큰 15.85%·시간 18.56% 감소를 기록했습니다. 추가 검증량 차이와 이미 노출된 단일 과제 때문에 일반화할 수 없으며, 선택형 이력 수집 도구는 사용하지 않았습니다.
- **배포 생존 담당(`friday`):** 메모리 SQLite에서 마이그레이션·롤백 단계별 읽기 쿼리 검사를 재사용합니다. [사용법과 한계](../skills/friday/references/sqlite-matrix.md). 유리했던 [스키마 경량화 비교 02](../benchmarks/FRIDAY-COMPACT-MODEL-02-REVIEW.md)의 결과가 [실제 쓰기 비교 01](../benchmarks/FRIDAY-ACK-01-REVIEW.md)(2026-09-14)에서는 이어지지 않았습니다. 합계 토큰 7.01% 증가·시간 0.29% 감소이며 검증량 차이와 기본 실행의 범위 이탈도 있습니다. 일반적인 효율 개선은 미입증입니다. 쿼리 성공이 배포 준비 완료를 뜻하지 않으며, 다른 DB 엔진의 동작은 별도로 확인해야 합니다. [대표 시퀀스 확인 01](../benchmarks/FRIDAY-SEQUENCE-MODEL-01-REVIEW.md)은 이전 스킬보다 검증량·토큰이 줄었지만 정상 사례 시간은 2.69% 늘었습니다. 새로운 기본 실행 비교나 일반적인 개선 주장은 아닙니다.
  [쿼리 선언 분석 재사용](../benchmarks/FRIDAY-READER-SNAPSHOT-01.md)으로 같은 파일을 여러 번 읽고 분석하지 않습니다. 단계별 SQL 검사는 그대로 실행하며, 모델 비용 효과는 아직 미측정입니다.
  [짧은 기본 안내](../benchmarks/FRIDAY-CORE-GUIDE-01.md)를 [새 모델 실험 01](../benchmarks/FRIDAY-CORE-GUIDE-MODEL-01-REVIEW.md)에서도 사용했습니다. 한 번의 API 결과로 열·값까지 검증했고 89,545토큰·54.127초를 사용했습니다. 체크포인트 07 대비 토큰은 18.13% 감소했지만 시간은 19.88% 증가했으며, 작업량 차이·단일 실행 때문에 일반적 효율 개선으로 주장하지 않습니다.
  최신 [실행 결과 재사용 안내](../benchmarks/FRIDAY-RESULT-REUSE-01.md)는 기존 Python API를 기본 문서에 배치했습니다. [새 모델 실험](../benchmarks/FRIDAY-RESULT-REUSE-MODEL-01-REVIEW.md)에서도 한 번의 실행 결과로 값 비교까지 마쳤지만, 토큰 39.28%, 시간 2.04% 증가와 검증량 차이로 효율 향상을 입증하지는 못했습니다. 실행 코드는 `e3bc342` 그대로입니다.
  [빈 단계 항목 생략 지원](../benchmarks/FRIDAY-PHASE-DEFAULTS-01.md)으로 재현된 API 입력 오류를 없애고 검증 조건은 유지했습니다. [새 단일 과제 실험](../benchmarks/FRIDAY-PHASE-DEFAULTS-MODEL-01-REVIEW.md)에서도 첫 실행에 성공했지만 SQL 중복 실행과 함께 토큰 67.14%, 시간 3.12% 증가를 기록했습니다. 사용성 오류 수정이며 효율 향상의 증거는 아닙니다.
  이후 [두 과제 인터페이스 실험](../benchmarks/FRIDAY-INTERFACE-MODEL-01-REVIEW.md)은 API 오류 수정·재실행을 포함해 전체 토큰 68.56%, 시간 8.41% 증가를 기록했습니다. 필요한 문서만 읽는 동작은 확인했지만 효율 개선은 아니며, 모든 시도를 보존했습니다.
  [고정 쿼리 선언 참조](../benchmarks/FRIDAY-LITERAL-READERS-01.md)는 Python 파일을 실행하거나 별도 추출 코드를 작성하지 않고 쿼리를 읽습니다. 동적 모듈은 거부하며, 파일·해시·줄 번호가 실제 실행 경로까지 증명하지는 않습니다. [단일 과제 실험](../benchmarks/FRIDAY-LITERAL-MODEL-01-REVIEW.md)에서 실제 사용을 확인했고 토큰은 10.07% 증가, 시간은 24.73% 감소했습니다. 추가 검증량이 달라 일반적 절감 효과로 주장하지 않습니다.
- **수정 검증관(`receipt`):** 현재 테스트와 지원 파일을 고정해 커밋된 수정 또는 미커밋 Python 수정을 비교합니다. 일반적인 `src/` 패키지도 설치 없이 지원하며 해시·각각의 출력·버전 식별 정보를 남깁니다. [사용법과 한계](../skills/receipt/references/existing-fix.md). [소스 구조 모델 검사](../benchmarks/results/receipt-src-model-01/README.md)에서는 도구가 실제 사용되고 기록상 비용도 줄었지만, 작업량 차이·출력 일부 누락·단일 과제라는 한계가 있어 전반적인 효율 개선은 아직 미입증입니다.
  [테스트 실행기 종료 후 정리](../benchmarks/RECEIPT-PIPE-EXIT-01.md)를 개선해 자식 프로세스의 출력 파이프 때문에 완료된 검사를 timeout으로 처리하고 수정 후 비교를 건너뛰던 문제를 해결했습니다. 남은 그룹 구성원은 종료하므로 백그라운드 실행기는 지원하지 않으며, 모델 작업 전체의 비용 효과는 아직 미측정입니다.
- **가설 퇴마사(`exorcist`):** 진단 명령의 프로세스 실행 시간과 수집 로그 크기를 제한합니다. [사용법과 한계](../skills/exorcist/references/bounded-probe.md). [첫 모델 검사](../benchmarks/EXORCIST-PROBE-RUNNER-01.md)에서 도구는 정상 사용했지만 비용은 줄지 않았습니다.
  [명령 종료 후 정리](../benchmarks/EXORCIST-PIPE-EXIT-01.md)를 개선해 남은 자식 프로세스가 출력 파이프를 열어 둬도 즉시 그룹 정리를 시작합니다. 버퍼에 남은 출력과 직접 실행한 명령의 종료 상태는 보존하며, 백그라운드 작업을 남기는 실행기는 지원하지 않습니다. 로컬 검사는 통과했지만 모델 작업 전체의 절감 효과는 아직 미측정입니다.
- **클릭 꼬투리 QA(`mother-in-law`):** 응답 순서를 제어해 정상 동작·오류 복구·오래된 응답을 검사하고, 필요하면 같은 실행의 JSON 증거를 남깁니다. 화면 유지가 요구된 경우 정상·역순 응답 중 표시 상태도 검사합니다. [3개 과제 개발 실험](../benchmarks/results/mother-retention-model-01/README.md)에서 새 옵션 사용과 토큰 1.58%·시간 52.77% 감소를 관찰했지만, 추가 검증량 차이와 조건별 1회 실행 때문에 일반화할 수 없습니다. [이후 작업 유형별 비교](../benchmarks/results/mother-routing-01/README.md)는 토큰이 늘고 생성된 프로젝트 테스트의 중간 상태 assertion 누락도 확인돼 개선 성공으로 인정하지 않았습니다. [지원 인터페이스와 한계](../skills/mother-in-law/SKILL.md). 지원 형태에 맞는 UI 없는 Python 컴포넌트용이며 기존 프로젝트 테스트를 우선합니다. 비동기 시간 제한은 동기 블로킹 코드를 중단하거나 브라우저 동작을 검증하지 않습니다.

이어진 [QA 중간 상태 검증 실험](../benchmarks/results/mother-interval-01/README.md)에서는 누락됐던 검증을 실제로 추가했습니다. 생성된 테스트를 변경 없이 별도로 재실행해 일시적인 오류는 잡고 정상 수정은 통과하는 것도 확인했습니다. 다만 **토큰 9.32%·시간 10.58% 증가**로 비용 목표는 미달입니다. 스킬 실행 두 건의 원래 출력은 일부 누락됐으며, 별도 재실행으로 그 기록을 대체하지 않습니다. 특정 오류 검증의 진전이지 효율 개선 성공은 아닙니다.

[후속 작업량 비교](../benchmarks/results/mother-interval-02/README.md)에서는 이런 추가 테스트를 줄였고, 별도 재실행에서 필수 오류 검증도 유지했습니다. **기록상 토큰 14.54% 감소·시간 83.52% 증가**였습니다. 연결 재시도·원래 테스트 출력 한 건 누락·조건별 1회 실행 때문에 종합 효율 개선으로 인정하지 않았으며, 별도 재실행으로 모델 증거 누락을 채우지 않습니다.

