# 공개 전환 직전 체크리스트 / Public launch

현재 상태: **공개 버튼만 누르면 된다고 확정할 수는 없다.** 설치 후보를 만드는
자동화는 준비되어 있지만, 아래 두 가지는 별도 해결이 필요하다.

1. GitHub Actions가 결제/사용 한도 사유로 실행 전 차단된 상태였다.
   계정 소유자가 해결한 뒤, 공개할 정확한 커밋에서 검증 성공을 확인한다.
2. 원본 Git 이력에는 작성자 로컬 경로와 계정 폴더 식별자가 남아 있다.
   [분류 결과](../benchmarks/PUBLIC-PATH-CLASSIFICATION-01.md)를 보고 공개 허용,
   별도 공개용 저장소 또는 승인된 이력 정리 중 방식을 결정한다.
   가린 사본을 추가했다고 원본 이력이 지워진 것은 아니다.

## 준비 순서

- [배포 상태](RELEASE-READINESS.md)의 검증·개인정보 조건을 확인한다.
- Actions → **Prepare release candidate** → 대상 브랜치 → **Run workflow**.
  전체 검증과 설치 후보 생성이 모두 성공해야 한다.
- 결과의 커밋 번호가 공개할 커밋과 일치하는지 확인한다. 그 후 코드가 바뀌면
  새 커밋으로 다시 검증한다. 후보 파일은14일 안에 내려받는다.
- 모든 조건이 해결된 뒤에만 소유자가 GitHub 저장소의 visibility를 Public으로
  변경한다. 이 문서나 후보 워크플로우는 그 변경을 실행하지 않는다.
- 공개 후 인증 없는 새 환경에서 설치 경로를 확인한다:
  `npx skills add SoonGwan/questionable-hires`.
  이는 공개 전 private 인증 설치와 별개인 최종 확인이다.

별도 저장소를 택하면 위 설치 주소와 두 언어 README의 주소도 실제 공개 위치로
함께 바꿔야 한다. GitHub Release 게시, npm 패키지 게시, 저장소 공개 전환은
서로 다른 작업이다. 설치 후보 생성만으로 어느 것도 수행되지 않는다.

## 발표 문구

8개 개발 스킬과 검증 가능한 사용 예시를 제공하는 **개발 프리뷰**로 소개한다.
모든 작업에서20–30% 향상, 완벽한 안전성, 전체 품질 우위를 주장하지 않는다.
벤치마크 원본·불리한 결과·제약을 유지하고, 새 모델 측정이 없으면 그래프의
숫자를 바꾸지 않는다.

English: candidate preparation is automated, publication is not. Resolve hosted
CI and the owner's history/privacy disposition, validate the exact source commit,
then have the owner change visibility. Verify anonymous installation afterward.
The available evidence supports a development preview, not broad performance
superiority. A standalone artifact excludes history; making the repository public
does not. Do not mistake a local pass or a sanitized copy for either release gate.
