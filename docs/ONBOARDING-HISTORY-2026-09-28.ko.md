# README의 과거 비교 근거 — 2026-09-28

온보딩을 정리하며 README `d195a37e`의 근거를 보존했습니다. 아래 내용은 “최근”이라는 표현을 포함해 해당 리비전 당시의 기록이며, 별도로 유지하는 최신 결과 주장이 아닙니다. 측정 자원·불리한 결과·한계는 각 원본 보고서에 연결돼 있습니다. 측정값이나 그래프는 변경하지 않았습니다. [English](ONBOARDING-HISTORY-2026-09-28.md) · [현재 판단 목록](../benchmarks/CURRENT-CANDIDATE-STATUS.md) · [도구 계약](HELPERS.ko.md).

## 도구별 개발과 비용

테스트 사기 감별사는 새 검사를 실제 요구 계약에 연결하고, 객체 동일성은 명시된
요구가 있을 때 검사하도록 보완했습니다. [Assertion-contract01](../benchmarks/ASSERTION-CONTRACT-01-REVIEW.md)
(2026-09-27, `33530f98`)은 품질을 지켰지만 무스킬 대비 **합계 토큰36.43% 증가**,
시간12.01% 감소였습니다. 토큰·시간 동시 개선은 입증되지 않았습니다.
이후 [네이티브 단일 비교 안내](../benchmarks/NATIVE-SINGLE-MODULE-ROUTE-02.md)는 로컬에서
검증됐습니다. [native-split02 비용 기록](../benchmarks/NATIVE-SPLIT-02-COSTS.json)
(2026-09-27, `6c099d68`)은 합계 토큰이 무스킬보다43.05% 많고 이전 버전보다
9.35% 적습니다. [원본 범위별 검토](../benchmarks/NATIVE-SPLIT-02-REVIEW.md)는
바인딩 출력 누락·평가 문구·보존 증거의 한계를 유지합니다.

테스트 사기 감별사는 파일 전체를 다시 보내는 대신 [정확히 일치하는 부분 수정](../skills/con-artist/references/python-audit-probes.md#improve-existing-tests-at-their-native-paths)도
받습니다. 기존 테스트와 강화한 테스트의 정상·결함 코드 검사는 그대로 유지합니다.
큰 네이티브 배치 출력은 [보관한 검사별 기록을 나눠 검토](../skills/con-artist/references/native-unittest-batch.md)해
출력 복구를 위한 재실행 없이 원본 증거를 유지합니다.

**전체 작업의 비용 개선은 아직 입증되지 않았습니다.** [integration07 비용](../benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md)(2026-09-28, `1be35120`)은 합계 토큰+1.67%, 실행 시간−9.63%이며 동시 감소는2/8입니다. [원본 검토](../benchmarks/ALL-EIGHT-CURRENT-07-REVIEW.md)에 검사량 차이와 출력 복구를 남겼으며, 한정된 결과는 유지됐지만 품질 우위는 입증되지 않았습니다. 노출된 개발 과제로 독립 검증이 아닙니다. 불리한 [과거 integration06](../benchmarks/ALL-EIGHT-CURRENT-06-REVIEW.md)도 보존합니다.

[integration05](../benchmarks/ALL-EIGHT-CURRENT-05-COSTS.md)
(2026-09-27, `75183f2f`)의 노출된 개발 과제8개 비교는 합계 토큰18.54%, 시간9.06%
증가였습니다. [원본의 명시된 과제 검토](../benchmarks/ALL-EIGHT-CURRENT-05-REVIEW.md)는
범위·평가 조건·보존 증거의 한계를 유지합니다.
[실행기 선택 후보](../benchmarks/NATIVE-INTERPRETER-ROUTE-01.md)(2026-09-27, `e918d02d`)는
측정한 대조에서 실패한 실행 재시도를 피했지만6회 비용은 혼재하며 합계 토큰·시간
동시 절감은 없습니다.
[날짜별 근거와 한계](../benchmarks/CURRENT-CANDIDATE-STATUS.md)에 불리한 개발·모델 설정
비교도 보존합니다. Receipt 직접 도구 availability01(2026-09-27, `b081240e`)도
두 모델이 CLI를 계속 사용했고 두 비용을 함께 줄인 과제가 없어 채택하지 않습니다.
supplied-tool routing01(2026-09-27, `44c4ff5e`)도 MCP 호출이 호스트 승인 정책에
차단돼 CLI 복구 전 비용이 늘었으므로 채택하지 않고 안내를 복원했습니다.
model-choice01(2026-09-27, `6701069f`) 설정은 채택하지 않으며
토큰·시간 동시 절감의 근거가 아닙니다.
설정 비교도 혼재합니다. [apps01](../benchmarks/ALL-EIGHT-APPS-01-REVIEW.md)(2026-09-27,
`6701069f`)은 토큰9.49% 감소·시간0.52% 증가이며,
[namespaces01](../benchmarks/ALL-EIGHT-NAMESPACES-01-REVIEW.md)(2026-09-27, `0333a084`)은
합계 토큰12.73%·시간2.73% 감소지만 동시 절감5/8이고 추가 검사가 불균등합니다.
둘 다 기본 채택하지 않으며 전체8개 역할의 개선 근거가 아닙니다.

[도구별 개발 이력과 불리한 결과](../docs/DEVELOPMENT-NOTES.ko.md)
(2026-09-14, `17ede49` 기록)를 별도로 모았습니다. Hostage의 토큰 증가·원본 테스트
출력 누락, Friday의 실제 쓰기 비교에서 합계 토큰 7.01% 증가도 그대로 보존합니다.
유용한 동작이 낮은 비용이나 완전한 증거를 뜻하지는 않습니다. 과거 결과를 현재
스킬의 성능으로 해석하기 전에 [현재 검증 현황](../benchmarks/CURRENT-CANDIDATE-STATUS.md)을 확인하세요.

위의 스킬 요청을 그대로 사용하면 필요한 경우 도구를 선택할 수 있습니다. 작은 작업이나 이미 증거를 확보한 작업은 직접 처리하는 편이 더 저렴할 수 있습니다. 전원 설치가 모든 작업에 8명을 전부 투입하라는 뜻은 아닙니다.


## 이전 팀 전체 비교와 선택 검증


[이전 후보 개발 결과](../benchmarks/results/mother-in-law-fast-2026-09-12/README.md)

**팀 전체 통합 실험 08(2026-09-14): 일반적인 효율 향상은 아직 미입증입니다.**
[9개 과제 검토](../benchmarks/BUNDLE-CONTRACT-08-REVIEW.md)는 리소스 `ecff8a8`에서
새 세션 18개를 실행했고 **총 토큰 0.58% 감소, 실행 시간 합계 15.08% 감소**를
기록했습니다. 과제 3개는 두 비용이 모두 늘었고, 6개는 토큰이 늘었습니다.
추가 작업량 차이와 원본 테스트 출력 누락 2건(스킬 미적용 검색 QA, 스킬 적용 폼)도
공개합니다. 별도 네이티브 대조군 22개는 예상대로 동작했지만 원본 출력 누락을
채우지는 않습니다.
이미 사용한 작성자 제작 과제·조건별 1회·공유 실행 환경이므로 일반적인 20–30%
개선이나 이후 수정본의 성과를 증명하지 않습니다. 합계 비율은 과거 그래프의
과제별 비율 평균과 다릅니다. [통합 실험 07](../benchmarks/BUNDLE-CONTRACT-07-REVIEW.md),
[통합 실험 05](../benchmarks/BUNDLE-CONTRACT-05-REVIEW.md),
[통합 실험 06](../benchmarks/BUNDLE-CONTRACT-06-REVIEW.md),
[이전 불리한 결과](../benchmarks/BUNDLE-CURRENT-02-REVIEW.md)도 그대로 보존합니다.

<details>
<summary>과거 팀 전체 실험 — 초기 스킬 파일로 실행한 72개 세션</summary>

현재는 **개발 프리뷰**입니다. 최초 반복 실험은 GPT-6 Astra / medium으로 **72회**를 측정했습니다. 작은 synthetic 과제 8개 × 스킬 없음·일반 지침·해당 스킬 3조건 × 3반복이며, 각 실행은 새로운 프로세스·대화·Git fixture를 사용했습니다. 이전 n=1 결과는 이 반복 실험에 포함하지 않았습니다.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-dark.svg">
  <img src="../benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-light.svg" alt="Baseline/control/skill: tokens 100/111.9/111.5%, time 100/125.1/117.6%, implementation LOC 100/100/100%. Strict success 19/24, 16/24, 18/24." width="100%">
</picture>

스킬 없음=100%일 때 일반 지침은 **토큰 111.9% / 시간 125.1%**, 해당 스킬은 **토큰 111.5% / 시간 117.6%**였습니다. 두 구현 과제의 변경 LOC는 동일했습니다. LOC가 적다고 더 좋은 것은 아니며, 이번 실험에서 자원 절감은 없었습니다.

엄격한 증거·범위 기준의 성공은 **스킬 없음 19/24, 일반 지침 16/24, 스킬 18/24**였습니다. 핵심 수정·진단은 대체로 같았습니다. 일반 지침 3회는 감사 중 기존 테스트를 수정했고, 스킬 4회는 거부된 패치의 대상이 로그에 없어 범위 준수를 확인할 수 없었습니다. 타임아웃은 없었습니다. 저자가 직접 채점한 소형 synthetic 실험이며, 우월성이나 일반적인 안전성을 증명하지 않습니다. 구독 사용량을 달러 청구로 환산하지 않았습니다.

[최초 반복 실험·평가기준·원시 증거](../benchmarks/REPORT-2026-09-11.md) · [재현 방법](../benchmarks/README.md) · [기존 n=1 결과](../benchmarks/REPORT.md)

</details>

과거 자동 선택 시험 8회에서는 과제에 맞는 스킬 파일을 읽는 것을 확인했습니다. 당시 로컬 플러그인의 설치·캐시 비교·제거 시험도 통과했습니다. 이는 이후 모든 수정본의 검증이 아닙니다. 자세한 범위와 날짜는 [설치 검증 기록](../docs/INSTALLATION-TEST.md)에 있습니다.

최근 근거는 위 그래프와 별도로 봐주세요.

- [최근 자동 감사의 실제 기록](../benchmarks/results/probe-adoption-01/README.md): 두 조건의 명령·출력·답변·사용량을 확인할 수 있습니다. 토큰 증가와 도우미 미사용, 가린 정보와 출력 누락도 그대로 설명합니다.
- [모델 사용량 없이 두 결함 감사 실행하기](../examples/con-artist.md#try-the-helper-without-model-usage): 실제로 실행할 수 있는 도우미 예제이며, 모델의 속도 향상을 증명하는 비교는 아닙니다.

- [자동 선택과 스킬 없음 비교](../benchmarks/CURRENT-SELECTION-01.md): 두 과제에서 적절한 스킬을 선택했지만 둘 다 토큰이 늘었고, 시간 결과는 혼재했습니다. 실제 수행한 작업량도 다릅니다.
- [관련 없는 요청](../benchmarks/ROUTING-NEGATIVE-01.md)과 [예제 폴더의 실제 소비자](../benchmarks/LANDLORD-CONFIGURED-01.md): 좁은 선택 범위 검증이며 일반적인 정확도·효율 점수가 아닙니다.
- [이전 버전·수정본의 실제 기록 열기](../benchmarks/results/landlord-compact-01/README.md): 비공개 로그 없이 명령·출력·답변·사용량을 확인할 수 있습니다. 이 비교의 불리한 결과도 그대로 남겼습니다.

예를 들어 `con-artist`는 저장을 제거한 복사본에서도 기존 테스트가 통과하는 것을 확인하고, 저장된 데이터 자체를 검사하면 실패한다는 것을 보여줬습니다. 기본 모델도 이 문제를 찾았습니다. [세 조건을 직접 비교하기 →](../examples/con-artist.md)

