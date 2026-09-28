# Roadmap / 앞으로 할 일

Status date: **2026-09-29**. The repository is public. The owner authorized
publication after the requested work is complete; GitHub Actions remains disabled
by request. See [release readiness](RELEASE-READINESS.md) for the actual gates.

## Delivered capabilities / 제공 중인 기능

- Eight focused skills, UI metadata, Python installer and local plugin bundle.
- English/Korean onboarding and a responsive bilingual website with interactive
  experiments, raw evidence downloads, OG cards and search metadata.
- Standalone skill downloads with per-file hashes and permissions; installation
  refuses existing destinations and preserves personal changes.
- Native helper correctness fixes and retained original model comparisons,
  including unsuccessful optimization candidates and their limitations.

한국어: 스킬8개·설치 도구·플러그인, 한영 안내·반응형 랜딩·실험과 근거 다운로드·
공유 정보를 제공합니다. 원본 모델 비교와 불리한 결과도 보존합니다. 현재 기능과
과거 측정값을 동일한 성능 보증으로 해석하지 않습니다.

## Remaining release work / 남은 출시 작업

- [ ] Demonstrate better outcomes at lower whole-task tokens and faster completion
  across all eight roles. Integration07 still records tokens+1.67%, time−9.63%,
  only2/8 pairs lower both; [all costs and limits](../benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md).
- [ ] Obtain an authorized independent model execution environment and complete
  the remaining selected-case preparation without altering frozen grades.
- [ ] Verify the exact candidate's local tests, archive installation and bilingual
  documentation; link the dated results instead of reusing older test totals.
- [ ] Push the candidate, review its PR and merge only after the requested gates
  are met; publish a versioned release and verify its actual downloadable artifacts.
- [ ] Confirm the final hosted revision and its responsive/localized interactions.
- [ ] Broaden automatic-selection and realistic interaction evaluation before
  generalizing beyond the already measured tasks.

한국어: 전체 품질·토큰·시간 개선은 미입증입니다. 승인 가능한 독립 검증 환경,
남은 평가 준비, 최종 소스·설치·문서 확인 후 PR·머지·버전 릴리스·공개 배포 확인이
필요합니다. 현재 필요한 조건에 과거 비공개 전환 승인이나 원격 CI 결제 문제를
다시 포함하지 않습니다.

[Earlier roadmap](ROADMAP-HISTORY-2026-09-29.md) preserves historical checklists,
source revisions and counts. [Candidate decision index](../benchmarks/CURRENT-CANDIDATE-STATUS.md)
retains both favorable and adverse evidence. More passing examples alone do not
establish stronger real-world performance.
