# Changelog / 변경 기록

## 0.2.0 — 2026-09-29 development preview / 개발 프리뷰

The owner authorized publishing this development preview with its measured
limitations. A version number is not evidence that all eight skills improve
quality, tokens and time. See [release status](docs/RELEASE-READINESS.md).

- Added a Korean/English responsive landing page, interactive benchmark charts,
  downloadable evidence and skill archives, localized social cards and search metadata.
- Receipt preserves returned test evidence on execution/cleanup failures, supports
  multiple historical comparisons and records optional typed assertion arguments.
- Con Artist improves isolated test auditing and bounded source collection,
  including UTF-8 BOMs and multiline decorator ranges. Large index-only reads can
  avoid allocating full source while preserving exact output.
- Added Python/JavaScript controlled-call support and more reliable asynchronous
  cleanup. Helpers remain optional and do not replace application assertions.
- Friday emits valid JSON for non-finite SQLite values. Installer/build/archive
  handling rejects linked inputs and preserves existing destinations on failure.
- Normalized standalone archive permissions so Git source exports and clones
  generate identical downloads for identical contents/executable flags.
- Reorganized bilingual onboarding and retained adverse model results. Integration07
  (2026-09-28, resource `1be35120`) uses **1.67% more total tokens** and **9.63% less
  CLI time**; only **2/8** pairs reduce both. No general savings claim is supported.

한국어: 한영 반응형 랜딩·실험 그래프·근거와 스킬 다운로드·공유 메타데이터를
추가했습니다. 실제 테스트 근거 보존, 소스 발췌, 비동기 작업 정리, JSON 출력과
설치 안전성을 개선했습니다. 소스 압축본과 체크아웃의 권한 차이가 다운로드
해시를 바꾸지 않도록 배포 권한을 통일했습니다. 전체8개 품질·비용 목표는 미달이며 integration07은
합계 토큰1.67% 증가·시간9.63% 감소, 두 비용 동시 감소2/8입니다. 사용자가 이 한계를 유지한 개발 프리뷰 게시를 승인했습니다.
버전 변경만으로 성능 목표 달성을 주장하지 않습니다.

[Current candidate notes / 후보 설명](docs/RELEASE-0.2.0.md) ·
[Detailed helper contracts / 보조 도구](docs/HELPERS.md) ·
[한국어 보조 도구](docs/HELPERS.ko.md) ·
[Dated evidence / 날짜별 근거](benchmarks/CURRENT-CANDIDATE-STATUS.md).

## 0.1.0 — development preview / 개발 프리뷰

Eight focused skills, local installation and plugin metadata, deterministic
fixtures, worked examples, original artwork, Korean onboarding and an MIT license.
This was a source development version; it was not a published GitHub Release.

스킬8개·설치 도구·플러그인 정보·검증 예제·캐릭터·한국어 안내를 제공한 초기
개발 버전입니다. GitHub Release 게시와는 구분합니다.

[Preserved earlier changelog](CHANGELOG-HISTORY-2026-09-29.md) retains dated
development notes and their historical test counts. Those counts are not current
validation results.
