# Landing page / 랜딩페이지

A bilingual design preview using the approved character artwork and Wanted
Montage semantic colors. Large editorial typography, a selectable employee
profile, restrained motion and a separate dark evidence section.

승인된 캐릭터와 Wanted Montage 컬러로 만든 한국어·영어 디자인 프리뷰입니다.
큰 타이포그래피, 직원별 프로필 선택, 절제된 모션과 검증 기록 섹션으로 구성했습니다.

## Preview / 미리보기

Run from the repository root / 저장소 루트에서 실행:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

- 한국어: http://localhost:4173/landing/?lang=ko
- English: http://localhost:4173/landing/?lang=en

KO / EN switches all UI copy, employee descriptions, prompts, image descriptions,
metadata and copy feedback. An explicit `lang` URL takes priority over a saved
preference; otherwise the browser language determines the initial language.
Selection persists when switching languages. Language storage is optional.

KO / EN으로 전체 문구와 업무 설명·요청 예시·대체 텍스트·메타데이터·복사 결과가
바뀝니다. URL의 `lang`이 저장된 언어보다 우선하며, 둘 다 없으면 브라우저 언어를
사용합니다. 언어 전환 시 선택한 직원은 유지됩니다.

## Implementation / 구현

No build step, runtime dependencies, external fonts or analytics. Motion uses
CSS, the Web Animations API and IntersectionObserver; reduced-motion preferences
are respected, including a preference change while the page is open.

`content.js` holds the parallel language dictionaries and employee copy.
`app.js` handles language, selection and clipboard behavior. `style.css` holds
layout and motion. Evidence links use the decision index and canonical
`benchmarks/featured.json`; no benchmark figures are maintained independently.

빌드나 외부 런타임 의존성이 없습니다. `content.js`에 언어별 문구를 모았으며,
`app.js`가 전환·직원 선택·복사를 처리합니다. 움직임 줄이기 설정을 지원합니다.
벤치마크 수치는 따로 관리하지 않고 원본 판단 기록과 `featured.json`으로 연결합니다.

## Local verification / 로컬 검증 — 2026-09-26

Rendered and visually reviewed Korean and English desktop/mobile screenshots in
an isolated headless Chrome session. Checked 14 layouts: both languages at
320, 390, 760, 768, 1024, 1440 and 1920 px. No horizontal overflow, clipped
headings or page script errors were observed. Interaction checks passed for:

- All eight employee selections and selection preservation across languages.
- Translation key parity, English copy completeness, metadata and shared URLs.
- Language preference persistence, explicit URL priority and blocked storage.
- Actual clipboard write/read, denied-write feedback and translated feedback.
- Keyboard language selection with focus retained, reduced motion and live changes.

한국어·영어 데스크톱 및 모바일 렌더링을 직접 확인했습니다. 7개 너비 × 2개
언어에서 가로 넘침·제목 잘림·스크립트 오류가 없었으며, 직원 선택과 언어 유지,
클립보드 성공·실패, 키보드 전환과 모션 설정 변경을 검증했습니다.

These are local UI checks, not model-performance evidence or hosted release checks.
This remains a local design preview. / 로컬 UI 검증이며 모델 성능 측정이나 호스팅
릴리스 검증이 아닙니다. 현재는 로컬 디자인 프리뷰입니다.
