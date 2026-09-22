# Public development preview / 공개 개발 프리뷰

2026-09-22: 소유자가 기존 이력의 경로·폴더 식별자 검토 후 공개 전환과 CI
제거를 승인했다. GitHub Actions 자동 검증·후보 생성 버튼은 제공하지 않는다.
계정 결제/한도 변경이나 Git 이력 재작성은 하지 않는다.

## Local validation / 로컬 검증

Python3.9+의 별도 개발 환경에서 의존성을 설치하고 저장소 루트에서 실행한다:

```sh
python3 -m pip install -r requirements-dev.txt
python3 -B scripts/validate.py
python3 -B scripts/sync_featured_benchmark.py --check
python3 -B -m unittest discover -s tests -v
git diff --check
```

각 명령의 성공을 확인한다. 설치 묶음이 필요하면
[로컬 아카이브 빌드·설치 안내](STANDALONE-ARCHIVE.md)를 따른다.
자동 CI가 없으므로 변경을 게시하기 전에 관리자가 이 검사를 실행해야 한다.
로컬 통과를 원격 CI 통과로 표현하지 않는다.

## Installation / 설치

```sh
npx skills add SoonGwan/questionable-hires
```

지원 환경과 개별 스킬 선택은 [설치 안내](INSTALL.md)를 참고한다.
저장소 공개는 npm 패키지 발행이나 GitHub Release 생성을 뜻하지 않는다.

## Scope / 공개 범위

기존 Git 이력을 유지한다. 검토한 로컬 사용자 경로와 계정 폴더 UUID는
개발 환경 정보이며 해당 UUID가 인증정보로 사용된 흔적은 발견하지 못했다.
이는 모든 종류의 비밀정보가 없다는 보증은 아니다.

8개 개발 스킬과 검증 가능한 예시를 제공하는 **개발 프리뷰**다. 모든 작업에서
20–30% 향상이나 완벽한 안전성을 주장하지 않는다. 불리한 결과와 한계를
보존하며 실제 새 측정이 없으면 그래프 수치를 변경하지 않는다.

English: the owner authorized public visibility with existing history and removal
of CI. Maintainers run the local checks above before publishing changes. Prior
hosted failures remain historical evidence, not current release gates. Public
availability is separate from npm publication, GitHub Releases and performance
superiority; this project remains a development preview.
