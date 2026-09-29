# 0.2.0 development preview / 개발 프리뷰

Published on **2026-09-29**. This development preview combines the bilingual landing page, complete
downloadable skill resources and accumulated helper correctness fixes. It remains
a development preview; the whole-team performance objective is not achieved.

한국어: **2026-09-29 게시한 개발 프리뷰**입니다. 한영 랜딩, 전체 스킬 다운로드와 보조
도구의 누적 정확성 수정을 묶었습니다. 개발 프리뷰이며 전체 성능 목표는 미달입니다.

## What changes / 변경 사항

- Responsive Korean/English pages preserve profile, chart and evidence-table state
  when changing language. Localized OG cards, canonical URLs, hreflang and sitemap
  are generated together from the configured public origin.
- Read-only source helpers handle supported UTF-8 signatures and complete decorator
  ranges. Context index selection can skip constructing discarded full-source output.
- Test helpers retain returned observations through failed cleanup/preservation
  checks, reject invalid recipes and preserve original project state within their
  documented limits. Optional controlled callbacks support realistic async sequences.
- Installation and downloadable archives include all 8 skills and 52 skill resources.
  Existing destinations are not overwritten; personal changes require a backup.
  Distribution modes are normalized to 0644/0755, preserving the owner-executable
  flag while removing checkout write-permission differences.

한국어: 언어 전환 상태 유지, 반응형 그래프·근거 표, 언어별 공유·검색 정보를
제공합니다. 지원하는 UTF-8 소스 발췌와 실패 시 테스트 근거 보존을 개선했으며,
선택형 비동기 호출 제어를 지원합니다. 스킬8개·리소스52개를 제공하고 기존 설치를
덮어쓰지 않습니다. 배포 권한은 실행 비트에 따라0644/0755로 통일합니다. 자세한 조건은 [한국어 도구 안내](HELPERS.ko.md)를 따릅니다.

## Evidence and release conditions / 검증과 출시 조건

Integration07 (2026-09-28, `1be35120`) records 592,783→602,679 total tokens
(**+1.67%**) and 494.990→447.302 CLI seconds (**−9.63%**). Only 2/8 pairs improve
both. The measured tasks are exposed development cases with one session per arm,
shared host/cache and unequal checks. This is not a measurement of every later
helper fix, repeated-sample confirmation or independent quality superiority.

The featured Mother confirmation stays frozen at its own source: 5/5 reviewed
targets in both arms, normalized tokens 93.2% and elapsed 71.3%. It measures one
role on different cases; these percentages must not replace integration07.

한국어: integration07의 합계 토큰은1.67% 늘고 시간은9.63% 줄었습니다. 두 비용이
같이 줄어든 역할은2/8입니다. 이미 노출된 개발 과제·조건별1회·검사량 차이라는
한계가 있습니다. 대표 Mother 실험의93.2%·71.3%는 별도 사례의 정규화 비율이며
전체8개 결과를 대신하지 않습니다. 후속 로컬 수정도 새 모델 측정으로 간주하지 않습니다.

[Release gates](RELEASE-READINESS.md) · [Full cost table](../benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md) ·
[Decision index](../benchmarks/CURRENT-CANDIDATE-STATUS.md) · [Install](INSTALL.md).

[PR #2](https://github.com/SoonGwan/questionable-hires/pull/2) ·
[Versioned release](https://github.com/SoonGwan/questionable-hires/releases/tag/v0.2.0).
[Dated candidate validation](../benchmarks/RELEASE-020-CANDIDATE-20260929.md)
records exact tested sources, retained failures and four verified draft assets.
The owner subsequently authorized merging, publishing and deploying this preview
with the existing limitations. Publication does not establish the performance goal.

한국어: 후보 검증 문서는 당시의 초안 상태와 실제 검사 결과를 보존합니다.
이후 사용자가 현재 한계를 유지한 머지·릴리스·랜딩 배포를 승인했습니다.
게시 여부와 전체 성능 목표 달성 여부는 별개입니다.

[Completed publication and hosted checks / 게시·배포 확인](RELEASE-DELIVERY-2026-09-29.md).
