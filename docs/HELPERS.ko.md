# 선택형 보조 도구

[English](HELPERS.md) · [역할 선택](CHOOSE-A-HIRE.ko.md) · [처음으로](../README.ko.md)


먼저 일반 스킬 요청으로 시작하세요. 프로젝트에 동등한 도구가 없을 때만 보조
도구를 선택하면 됩니다. Python 도구에는 **Python 3.9 이상**, 테스트 사기 감별사의
결함 주입 실행기·수정 검증관·가설 퇴마사에는 POSIX도 필요합니다. 범위 협상가의
독립 JavaScript 모듈은 **Python 없이** JavaScript 환경에서 사용할 수 있으며,
네이티브 검증에는 Node.js를 사용합니다. 의존성 자동 설치나 상시 실행은 없습니다.

| 스킬 | 선택형 도구와 적용 범위 |
| --- | --- |
| 범위 협상가 | [Python 호출 제어·선택적 작업 정리](../skills/hostage-negotiator/assets/controlled_call.py)(진입 대기를 취소해도 아직 전달하지 않은 호출을 보존하며, 종료를 다시 요청해도 진행 중인 비동기 정리에 취소를 재전송하지 않음) 또는 [JavaScript 호출·정리](../skills/hostage-negotiator/assets/controlled_call.mjs), 출력 누락에 대비한 선택적 [테스트 증거 보존](../skills/hostage-negotiator/references/native-evidence.md). 성공한 편집과 테스트를 같은 도구 호출에서 실행하되 각각의 결과를 보존할 수 있습니다. 앱 검증은 테스트가 담당하며 증거 보존 방법은 브라우저 검증이나 실행 시간 제한을 제공하지 않습니다. |
| 테스트 사기 감별사 | 선택 파일 교체 확인과 배치 내 반복 테스트 선택·강화 검사의 정상 결과 재사용(저장 한도 적용, 네이티브 강화 검사는 기존 선택이 달라도 자체 실행 인자가 같으면 재사용)을 지원하는 [Python 테스트 결함 감사](../skills/con-artist/references/python-audit.md), 크기 제한이 있는 선택형 프로젝트 전체 변경 확인, 같은 이름의 정의 선택과 전체 출력 크기 제한을 지원하는 [읽기 전용 맥락 수집](../skills/con-artist/references/python-context.md). 선택한 FIFO·소켓 등 특수 파일은 복사에서 조용히 제외하지 않고 거부합니다. 중첩 변형·검사 필드를 포함한 JSON 레시피 중복 키는 네이티브 실행 전에 거부합니다. 복사·실행·정리·최종 보호 검사 실패 시 반환된 검사와 이전 배치 근거를 불완전 결과로 보존하고 후속 변형은 중단하며, 반환되지 않은 결과나 확인하지 못한 보호 항목(임시 복사본 조회 실패 포함)은 추정하지 않습니다. [import 해시는 청크 단위로 계산](../benchmarks/AUDIT-IMPORT-HASH-01.md)하며 로컬 할당 절감은 모델 비용 개선 근거가 아닙니다. 빈 테스트나 지정한 하위 모듈의 부모 패키지가 import 캐시에 없는 경우는 성공이 아닌 검증 불완전으로 처리합니다. 선택형 [네이티브 unittest 배치 예제](../skills/con-artist/references/native-unittest-batch.md)는 실행 관찰 코드를 추가한 `python -B -m unittest`와 정상 결과 재사용을 안내하며, 기본값은 기존 내부 실행 방식입니다. 신뢰하는 테스트만 실행하며 샌드박스나 동시 변경을 격리하는 스냅샷이 아닙니다. |
| 레거시 고고학자 | [이름별 Python 발췌](../skills/necromancer/references/python-regions.md)는 크기 제한이 있는 로컬 파일이나 Git/stdin 소스를 실행하지 않고 읽으며 모델 비용 절감은 미입증입니다. [관련 Git 이력 수집](../skills/necromancer/references/focused-history.md). 다른 참조로 범위를 넓히지 않고 지정한 커밋과 조상 이력을 조회하는 명령을 안내합니다. [같은 리비전의 완전한 패치 구간은 재사용](../benchmarks/SAME-REVISION-HUNKS-01.md)하며, 과거 이유가 유지·삭제 결론을 정하지는 않습니다. [작성자 제작 이력 비교](../benchmarks/ANCESTRY-SCOPE-01.md)에서 범위는 지켰지만 비용 개선은 입증하지 못했습니다. [로컬 패치 선택 할당 보완](../benchmarks/HISTORY-BODY-OFFSET-01.md)은 본문 전체 복사를 제거하며 모델 비용 개선의 근거는 아닙니다. |
| 배포 생존 담당 | [SQLite 호환성 확인](../skills/friday/references/sqlite-matrix.md). 실제로 연 소스 파일의 식별자를 검사해 파일 교체를 확인합니다. CLI JSON 중복 키는 소스 읽기·SQL 실행 전에 거부합니다. 무한대 등 비유한 결과 숫자는 명시적인 JSON 태그로 전달하고 네이티브 API의 float 값은 유지합니다. [JSON output01](../benchmarks/FRIDAY-JSON-OUTPUT-01-REVIEW.md)(2026-09-28, `371b4b1e`→`c9b30fc6`)의 명시적 CLI 인계2개에서는 토큰·시간 감소를 관찰했으며 일반·전체8개 절감률은 아닙니다. 파일 시스템 격리나 운영 배포·다른 DB 엔진의 안전성을 증명하지 않습니다. |
| 수정 검증관 | [Python](../skills/receipt/references/existing-fix.md) 또는 [Node 기본 테스트](../skills/receipt/references/node-comparison.md)를 격리해 전후 결과·소스 출처를 확인하고, 용량 제한이 있는 프로젝트 전체 변경 감지를 선택할 수 있습니다. unittest에서는 여러 과거 버전을 비교할 때 현재 버전 검사를 한 번만 실행해 공유할 수 있습니다. CLI 입력의 중복 키는 거부하고 누락·알 수 없는 키를 실행 전에 알려줍니다. 복사·실행·정리·최종 보존 검사 실패 시 반환된 실행 근거를 불완전 상태와 CLI 종료값 2로 남기며, 반환되지 않은 결과나 확인하지 못한 정리 상태는 추정하지 않습니다. 선택 파일을 여는 순간 감지한 교체는 거부하지만 원자적 스냅샷은 아닙니다. 두 unittest 실행 방식의 검사 완료와 종료값 일치를 기록하며, 결과가 없으면 비교를 중단합니다. 선택적으로 현재 스레드의 `assertEqual`/`assertIsNot` 기본 값·표준 pathlib 인자를 용량 제한과 `v:3` 형식으로 관찰하며, 관찰이 불가능하면 원래 실행 결과를 보존하고 비교를 중단합니다. Node 로딩 기록만으로 기능 실행·테스트 범위가 입증되지는 않으며 일반적인 모델 효율 향상은 아직 입증되지 않았습니다. |
| 가설 퇴마사 | [시간·출력 제한 진단 실행](../skills/exorcist/references/bounded-probe.md). 백그라운드 서비스용이 아닙니다. |
| 클릭 꼬투리 QA | [응답 순서 제어 검증](../skills/mother-in-law/SKILL.md). 네이티브 테스트용 요청 제어는 진입 대기를 취소해도 아직 전달하지 않은 요청을 보존합니다. 지원 인터페이스에 맞는 UI 없는 Python 컴포넌트용이며 기존 테스트가 우선이고 브라우저 검증은 아닙니다. |
| 구조 관리인 | [구조 검토 지침](../skills/landlord/SKILL.md). 별도 실행 도구는 포함하지 않습니다. |

날짜별 모델 비용과 채택하지 않은 후보는 [현재 판단 목록](../benchmarks/CURRENT-CANDIDATE-STATUS.md)에서 확인하세요. 로컬 도구의 동작 개선이 전체 모델 비용 절감을 뜻하지는 않습니다.
