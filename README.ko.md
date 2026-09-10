<p align="center"><img src="assets/team.svg" alt="Questionable Hires — 이상한데 아직 회사 다님" width="100%"></p>

<p align="center"><img src="assets/team-characters.png" alt="하찮은 낙서 캐릭터로 그린 Questionable Hires 8명." width="100%"></p>

# Questionable Hires

**이걸 뽑네. 근데 일을 하네.**

영수증 집착남, 코드 건물주, 레거시 무당까지. 채용 과정은 의문인데 맡기는 일은 분명한 개발자 스킬 8개입니다. GPT-6 Astra를 염두에 두고 만들었습니다.

[English](README.md) · [실제 실행 예시](examples/README.md) · [비교 결과](benchmarks/REPORT.md) · [설치 가이드](docs/INSTALL.md)

## 이런 일을 시킵니다

| 스킬 | 한마디 | 맡기는 일 |
| --- | --- | --- |
| `necromancer` | 전임자는 퇴사했다. 이유는 퇴사하지 못했다. | 현재 호출부와 Git 이력으로 이상한 코드의 이유 추적 |
| `receipt` | 고쳤다고? 영수증은? | 수정 전 실패와 수정 후 통과를 실제 실행으로 확인 |
| `landlord` | 이 추상화 월세 누가 냄? | 구조의 실제 소비자와 유지 비용 검토 |
| `mother-in-law` | 저장 누르고 또 누르면? | 중복 동작·응답 순서·빈 결과 같은 사용자 흐름 검증 |
| `exorcist` | 캐시 탓이라는 귀신부터 쫓겠습니다. | 추측을 구분 가능한 실험으로 바꾸는 원인 분석 |
| `hostage-negotiator` | 버튼부터 풀어주세요. | 작은 요청이 불필요한 리팩터링으로 커지는 것 방지 |
| `con-artist` | 테스트가 mock을 칭찬하고 있습니다. | 실제 동작을 망가뜨려도 통과하는 테스트 확인 |
| `friday` | 월요일의 내가 복구할 수 있음? | 배포 중 버전 호환성과 롤백 가능성 검토 |

## 진짜 작동하나요?

현재는 **개발 프리뷰**입니다. GPT-6 Astra / medium으로 **신규 72회**를 측정했습니다. 작은 synthetic 과제 8개 × 스킬 없음·일반 지침·해당 스킬 3조건 × 3반복이며, 각 실행은 새로운 프로세스·대화·Git fixture를 사용했습니다. 기존 n=1 결과는 새 측정에 포함하지 않았습니다.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-dark.svg">
  <img src="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-light.svg" alt="Baseline/control/skill: tokens 100/111.9/111.5%, time 100/125.1/117.6%, implementation LOC 100/100/100%. Strict success 19/24, 16/24, 18/24." width="100%">
</picture>

스킬 없음=100%일 때 일반 지침은 **토큰 111.9% / 시간 125.1%**, 해당 스킬은 **토큰 111.5% / 시간 117.6%**였습니다. 두 구현 과제의 변경 LOC는 동일했습니다. LOC가 적다고 더 좋은 것은 아니며, 이번 실험에서 자원 절감은 없었습니다.

엄격한 증거·범위 기준의 성공은 **스킬 없음 19/24, 일반 지침 16/24, 스킬 18/24**였습니다. 핵심 수정·진단은 대체로 같았습니다. 일반 지침 3회는 감사 중 기존 테스트를 수정했고, 스킬 4회는 거부된 패치의 대상이 로그에 없어 범위 준수를 확인할 수 없었습니다. 타임아웃은 없었습니다. 저자가 직접 채점한 소형 synthetic 실험이며, 우월성이나 일반적인 안전성을 증명하지 않습니다. 구독 사용량을 달러 청구로 환산하지 않았습니다.

[신규 보고서·평가기준·원시 증거](benchmarks/REPORT-2026-09-11.md) · [재현 방법](benchmarks/README.md) · [기존 n=1 결과](benchmarks/REPORT.md)

8개 스킬을 함께 설치한 자동 선택 시험도 8회 진행해 각 과제에 맞는 스킬 파일을 읽는 것을 확인했습니다. 로컬 플러그인의 실제 설치·캐시 비교·제거 시험도 통과했습니다. 자세한 범위는 [설치 검증 기록](docs/INSTALLATION-TEST.md)에 있습니다.

예를 들어 `con-artist`는 저장을 제거한 복사본에서도 기존 테스트가 통과하는 것을 확인하고, 저장된 데이터 자체를 검사하면 실패한다는 것을 보여줬습니다. 기본 모델도 이 문제를 찾았습니다. [세 조건을 직접 비교하기 →](examples/con-artist.md)

## 설치

Python 3.8 이상과 Git이 필요합니다. 현재 private 레포이므로 접근 권한이 있어야 합니다.

```sh
git clone https://github.com/SoonGwan/questionable-hires.git
cd questionable-hires
python3 scripts/install.py --dest /내/프로젝트/.agents/skills --skill necromancer
```

실제 프로젝트 경로로 바꿔주세요. `--skill necromancer`를 빼면 8개 전부 설치합니다. `--dry-run`으로 미리 확인할 수 있으며 기존 스킬 폴더는 덮어쓰지 않습니다.

Codex CLI나 IDE의 새 대화에서:

```text
$necromancer 이 호환성 분기 지워도 됨?
$receipt 이 수정으로 진짜 중복 저장이 막히는지 확인해줘.
$friday 이 배포 롤백 가능한지 봐줘.
```

모델 선택이나 권한 설정은 변경하지 않습니다. 상시 실행 훅, 별도 백그라운드 프로세스, 텔레메트리도 없습니다. 업데이트·제거 방법은 [설치 가이드](docs/INSTALL.md)에 있습니다.

## 같이 채용하기

웃긴 캐릭터마다 실제 개발 판단이 달라져야 합니다. 새로운 스킬에는 구체적인 문제, 출력할 근거, 종료 조건, 그리고 정상 코드를 건드리지 않아야 하는 사례가 필요합니다.

[기여 가이드](CONTRIBUTING.md) · [평가 실행 방법](benchmarks/README.md) · [개발 현황](docs/ROADMAP.md) · [MIT 라이선스](LICENSE)

캐릭터와 실용적인 개발 습관을 연결하는 방식은 [Ponytail](https://github.com/DietrichGebert/ponytail)에서 영감을 받았습니다.
