<p align="center"><img src="assets/team.svg" alt="Questionable Hires — 이상한데 아직 회사 다님" width="100%"></p>

<p align="center"><img src="assets/team-characters.png" alt="하찮은 낙서 캐릭터로 그린 Questionable Hires 8명." width="100%"></p>

# Questionable Hires

**이걸 뽑네. 근데 일을 하네.**

레거시 고고학자, 수정 검증관, 테스트 사기 감별사까지. 채용 과정은
의문인데 맡기는 일은 분명한 개발자 스킬 8개입니다. GPT-6 Astra를
염두에 두고 만들었습니다.

[English](README.md) · [실제 실행 예시](examples/README.md) · [현재 비교 근거](benchmarks/CURRENT-CANDIDATE-STATUS.md) · [설치 가이드](docs/INSTALL.md)

## 이런 일을 시킵니다

| 한국어 별칭 · 코드명 | 한마디 | 맡기는 일 |
| --- | --- | --- |
| 레거시 고고학자 · `necromancer` | 전임자는 퇴사했다. 이유는 Git에 남았다. | 현재 호출부와 Git 이력으로 이상한 코드의 이유 추적 |
| 수정 검증관 · `receipt` | 고쳤다고? 전후 증거부터. | 수정 전 실패와 수정 후 통과를 실제 실행으로 확인 |
| 구조 관리인 · `landlord` | 이 추상화 유지비는 누가 냄? | 구조의 실제 소비자와 유지 비용 검토 |
| 클릭 꼬투리 QA · `mother-in-law` | 저장 누르고 또 누르면? | 중복 동작·응답 순서·빈 결과 같은 사용자 흐름 검증 |
| 가설 퇴마사 · `exorcist` | 캐시 탓이라는 귀신부터 잡자. | 추측을 구분 가능한 실험으로 바꾸는 원인 분석 |
| 범위 협상가 · `hostage-negotiator` | 버튼 하나만 고치기로 했잖아요. | 작은 요청이 불필요한 리팩터링으로 커지는 것 방지 |
| 테스트 사기 감별사 · `con-artist` | 테스트가 mock한테 속고 있습니다. | 실제 동작을 망가뜨려도 통과하는 테스트 확인 |
| 배포 생존 담당 · `friday` | 월요일의 내가 복구할 수 있음? | 배포 중 버전 호환성과 롤백 가능성 검토 |

## 진짜 작동하나요?

**최신 사전 고정 확인 실험:** 클릭 꼬투리 QA(`mother-in-law`)와 스킬 미적용 조건
모두 검토 대상 **5/5**를 충족했고 오탐은 없었습니다. 실행 전에 커밋한
새 과제 5개에서 스킬의 정규화 총 토큰은 **93.2%**, 실행 시간은
**71.3%**였습니다. 과제·조건별 새 세션 1회 결과이며 팀 전체나 반복
표본의 우월성을 뜻하지 않습니다.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-dark.svg">
  <img src="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-light.svg" alt="새 과제 5개의 사전 고정 확인 실험. 두 조건 모두 5개 기준을 충족했고, 스킬은 정규화 토큰 93.2%, 실행 시간 71.3%를 사용했습니다." width="100%">
</picture>

[과제·원시 수치·방법·한계 확인](benchmarks/results/mother-in-law-confirmation-2026-09-12/README.md) ·
[이전 후보 개발 결과](benchmarks/results/mother-in-law-fast-2026-09-12/README.md)

팀 전체의 최신 통합 검증은 아직 비용 절감 목표를 충족하지 못했습니다.
자세한 불리한 결과와 남은 과제도 [현재 후보 상태](benchmarks/CURRENT-CANDIDATE-STATUS.md)에
그대로 보존합니다.

<details>
<summary>과거 팀 전체 실험 — 초기 스킬 파일로 실행한 72개 세션</summary>

현재는 **개발 프리뷰**입니다. 최초 반복 실험은 GPT-6 Astra / medium으로 **72회**를 측정했습니다. 작은 synthetic 과제 8개 × 스킬 없음·일반 지침·해당 스킬 3조건 × 3반복이며, 각 실행은 새로운 프로세스·대화·Git fixture를 사용했습니다. 이전 n=1 결과는 이 반복 실험에 포함하지 않았습니다.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-dark.svg">
  <img src="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-light.svg" alt="Baseline/control/skill: tokens 100/111.9/111.5%, time 100/125.1/117.6%, implementation LOC 100/100/100%. Strict success 19/24, 16/24, 18/24." width="100%">
</picture>

스킬 없음=100%일 때 일반 지침은 **토큰 111.9% / 시간 125.1%**, 해당 스킬은 **토큰 111.5% / 시간 117.6%**였습니다. 두 구현 과제의 변경 LOC는 동일했습니다. LOC가 적다고 더 좋은 것은 아니며, 이번 실험에서 자원 절감은 없었습니다.

엄격한 증거·범위 기준의 성공은 **스킬 없음 19/24, 일반 지침 16/24, 스킬 18/24**였습니다. 핵심 수정·진단은 대체로 같았습니다. 일반 지침 3회는 감사 중 기존 테스트를 수정했고, 스킬 4회는 거부된 패치의 대상이 로그에 없어 범위 준수를 확인할 수 없었습니다. 타임아웃은 없었습니다. 저자가 직접 채점한 소형 synthetic 실험이며, 우월성이나 일반적인 안전성을 증명하지 않습니다. 구독 사용량을 달러 청구로 환산하지 않았습니다.

[최초 반복 실험·평가기준·원시 증거](benchmarks/REPORT-2026-09-11.md) · [재현 방법](benchmarks/README.md) · [기존 n=1 결과](benchmarks/REPORT.md)

</details>

과거 자동 선택 시험 8회에서는 과제에 맞는 스킬 파일을 읽는 것을 확인했습니다. 당시 로컬 플러그인의 설치·캐시 비교·제거 시험도 통과했습니다. 이는 이후 모든 수정본의 검증이 아닙니다. 자세한 범위와 날짜는 [설치 검증 기록](docs/INSTALLATION-TEST.md)에 있습니다.

최근 근거는 위 그래프와 별도로 봐주세요.

- [최근 자동 감사의 실제 기록](benchmarks/results/probe-adoption-01/README.md): 두 조건의 명령·출력·답변·사용량을 확인할 수 있습니다. 토큰 증가와 도우미 미사용, 가린 정보와 출력 누락도 그대로 설명합니다.
- [모델 사용량 없이 두 결함 감사 실행하기](examples/con-artist.md#try-the-helper-without-model-usage): 실제로 실행할 수 있는 도우미 예제이며, 모델의 속도 향상을 증명하는 비교는 아닙니다.

- [자동 선택과 스킬 없음 비교](benchmarks/CURRENT-SELECTION-01.md): 두 과제에서 적절한 스킬을 선택했지만 둘 다 토큰이 늘었고, 시간 결과는 혼재했습니다. 실제 수행한 작업량도 다릅니다.
- [관련 없는 요청](benchmarks/ROUTING-NEGATIVE-01.md)과 [예제 폴더의 실제 소비자](benchmarks/LANDLORD-CONFIGURED-01.md): 좁은 선택 범위 검증이며 일반적인 정확도·효율 점수가 아닙니다.
- [이전 버전·수정본의 실제 기록 열기](benchmarks/results/landlord-compact-01/README.md): 비공개 로그 없이 명령·출력·답변·사용량을 확인할 수 있습니다. 이 비교의 불리한 결과도 그대로 남겼습니다.

예를 들어 `con-artist`는 저장을 제거한 복사본에서도 기존 테스트가 통과하는 것을 확인하고, 저장된 데이터 자체를 검사하면 실패한다는 것을 보여줬습니다. 기본 모델도 이 문제를 찾았습니다. [세 조건을 직접 비교하기 →](examples/con-artist.md)

## 설치

Python 3.8 이상과 Git이 필요합니다. 현재 private 레포이므로 접근 권한이 있어야 합니다.

```sh
git clone https://github.com/SoonGwan/questionable-hires.git
cd questionable-hires
python3 scripts/install.py --dest /내/프로젝트/.agents/skills --skill necromancer
```

실제 프로젝트 경로로 바꿔주세요. `--skill necromancer`를 빼면 8개 전부 설치합니다. `--dry-run`으로 미리 확인할 수 있으며 기존 스킬 폴더는 덮어쓰지 않습니다.

신뢰할 수 있는 소스에서 설치하세요. 소스의 심볼릭 링크 파일·폴더는 쓰기 전에
거부합니다. 실패하거나 취소하면 이번 실행이 만든 폴더만 정리를 시도합니다.
정리도 실패할 수 있으므로 재시도 전에 남은 불완전한 폴더를 확인하고,
기존 파일과 개인 수정본은 보존하세요.

Codex CLI나 IDE의 새 대화에서:

```text
$necromancer 이 호환성 분기 지워도 됨?
$receipt 이 수정으로 진짜 중복 저장이 막히는지 확인해줘.
$friday 이 배포 롤백 가능한지 봐줘.
```

모델 선택이나 권한 설정은 변경하지 않습니다. 상시 실행 훅, 별도 백그라운드 프로세스, 텔레메트리도 없습니다. 업데이트·제거 방법은 [설치 가이드](docs/INSTALL.md)에 있습니다.

### 도구도 들고 출근합니다

설치본에는 필요한 경우에만 로컬에서 실행하는 보조 도구 다섯 개가 포함됩니다. 도구 실행에는 **Python 3.9 이상**, Con Artist·Receipt·Exorcist에는 POSIX 환경도 필요합니다. 의존성을 자동 설치하거나 백그라운드에서 실행하지 않습니다.

- **테스트 사기 감별사(`con-artist`):** 임시 복사본에서 Python 결함 주입, 복사본 import 검증, 테스트별 종료 상태, 로그 메모리·시간 제한을 처리합니다. [사용법과 한계](skills/con-artist/references/python-audit.md). 샌드박스가 아니므로 신뢰할 수 있는 테스트만 실행해야 합니다.
- **레거시 고고학자(`necromancer`):** 선택한 코드 줄의 현재 상태와 Git 이력을 모으고, 미커밋 변경·얕은 이력의 한계를 표시합니다. [사용법과 한계](skills/necromancer/references/focused-history.md). 과거 코드를 지금도 유지해야 하는지는 별도로 판단합니다.
- **배포 생존 담당(`friday`):** 메모리 SQLite에서 마이그레이션·롤백 단계별 읽기 쿼리 검사를 재사용합니다. [사용법과 한계](skills/friday/references/sqlite-matrix.md). 쿼리 성공이 배포 준비 완료를 뜻하지 않으며, 다른 DB 엔진의 동작은 별도로 확인해야 합니다.
- **수정 검증관(`receipt`):** 현재 테스트를 고정한 채 두 커밋의 Python 구현을 비교하고, 각각의 출력과 커밋 ID를 남깁니다. [사용법과 한계](skills/receipt/references/existing-fix.md). [첫 모델 검사](benchmarks/RECEIPT-HELPER-01.md)는 직전 표본보다 빠르지만 토큰은 늘었습니다. 비용 개선이 입증된 것은 아닙니다.
- **가설 퇴마사(`exorcist`):** 진단 명령의 프로세스 실행 시간과 수집 로그 크기를 제한합니다. [사용법과 한계](skills/exorcist/references/bounded-probe.md). [첫 모델 검사](benchmarks/EXORCIST-PROBE-RUNNER-01.md)에서 도구는 정상 사용했지만 비용은 줄지 않았습니다.

위의 스킬 요청을 그대로 사용하면 필요한 경우 도구를 선택할 수 있습니다. 작은 작업이나 이미 증거를 확보한 작업은 직접 처리하는 편이 더 저렴할 수 있습니다. 전원 설치가 모든 작업에 8명을 전부 투입하라는 뜻은 아닙니다.

## 같이 채용하기

웃긴 캐릭터마다 실제 개발 판단이 달라져야 합니다. 새로운 스킬에는 구체적인 문제, 출력할 근거, 종료 조건, 그리고 정상 코드를 건드리지 않아야 하는 사례가 필요합니다.

[기여 가이드](CONTRIBUTING.md) · [평가 실행 방법](benchmarks/README.md) · [공개 준비와 남은 검증](docs/RELEASE-READINESS.md) · [개발 현황](docs/ROADMAP.md) · [MIT 라이선스](LICENSE)

캐릭터와 실용적인 개발 습관을 연결하는 방식은 [Ponytail](https://github.com/DietrichGebert/ponytail)에서 영감을 받았습니다.
