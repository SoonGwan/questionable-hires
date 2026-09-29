# Roadmap / 앞으로 할 일

Status date: **2026-09-29**. The repository is public. The owner authorized
publishing0.2.0 now with its documented limitations; GitHub Actions remains disabled
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

## Delivery and further research / 배포와 후속 연구

- [ ] Demonstrate better outcomes at lower whole-task tokens and faster completion
  across all eight roles. Integration07 still records tokens+1.67%, time−9.63%,
  only2/8 pairs lower both; [all costs and limits](../benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md).
- [ ] Obtain an authorized independent model execution environment and complete
  the remaining selected-case preparation without altering frozen grades.
- [x] Verify candidate local tests, archive installation and bilingual documentation;
  [2026-09-29 source-specific results](../benchmarks/RELEASE-020-CANDIDATE-20260929.md)
  retain initial failures and distinguish source-archive skips.
- [x] Push candidate [PR #2](https://github.com/SoonGwan/questionable-hires/pull/2);
  prepare the0.2.0 release draft and verify all four uploaded downloads.
- [ ] Complete the authorized merge, versioned preview publication and public checks.
- [ ] Confirm the final hosted revision and its responsive/localized interactions.
- [ ] Broaden automatic-selection and realistic interaction evaluation before
  generalizing beyond the already measured tasks.

한국어: 전체 품질·토큰·시간 개선은 미입증입니다. 승인 가능한 독립 검증 환경,
남은 평가 준비·머지·정식 릴리스·최종 공개 배포 확인이 필요합니다. 후보 소스 검사·
설치·문서와 PR·릴리스 초안의 다운로드 검증은 완료했습니다. 현재 필요한 조건에 과거 비공개 전환 승인이나 원격 CI 결제 문제를
다시 포함하지 않습니다.

[Earlier roadmap](ROADMAP-HISTORY-2026-09-29.md) preserves historical checklists,
source revisions and counts. [Candidate decision index](../benchmarks/CURRENT-CANDIDATE-STATUS.md)
retains both favorable and adverse evidence. More passing examples alone do not
establish stronger real-world performance.
