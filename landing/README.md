# Landing page / 랜딩페이지

Bilingual static landing using the approved artwork and Wanted Montage palette.
Includes selectable employee profiles, the frozen featured experiment, per-task
charts, all ten raw cells and explicitly dated evidence/limitations.

승인된 캐릭터와 Montage 컬러를 사용하는 한국어·영어 랜딩입니다. 직원별 프로필,
대표 실험의 과제별 그래프, 원시 기록 10개와 날짜·측정 리소스·한계를 표시합니다.

## Preview / 미리보기

From the repository root / 저장소 루트에서:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

- 한국어: http://localhost:4173/landing/ko/
- English: http://localhost:4173/landing/en/

The language-specific URLs have complete HTML and metadata without JavaScript.
KO / EN preserves employee selection, chart metric and expanded raw records.
The root follows the saved preference or browser language; legacy `?lang=ko|en`
links still work for human visitors. Explicit locale paths override preferences.

언어별 주소에는 JavaScript 없이도 본문·그래프·OG 정보가 들어 있습니다. 언어를
전환해도 선택한 직원, 그래프 종류와 펼친 원시 기록을 유지합니다.

## Sources and rebuild / 원본과 재생성

Edit `content.json` for translated copy and `templates/page.html` for markup.
`index.html`, `ko/index.html`, `en/index.html`, `content.js`, experiment fragments,
social SVGs, the artwork copy, sitemap and robots are generated. Runtime has no
external dependencies, fonts or analytics; the builder uses Python's standard library.

```sh
python3 -B scripts/sync_featured_benchmark.py
python3 -B scripts/build_landing.py
python3 -B scripts/sync_featured_benchmark.py --check
python3 -B scripts/build_landing.py --check
```

`benchmarks/featured.json` is the only featured-result pointer. The builder reuses
`audit_mother_in_law_checkpoint.summarize` to verify `data.json` against every
record in `cells.json`. Chart means use equal-weight task ratios; raw sums are
shown separately. No new model experiment or favorable-result promotion occurs.
Review both README languages when changing featured data or claims.

대표 데이터는 `featured.json`에서만 선택하며 기존 감사 코드로 원시 기록과 대조합니다.
과제별 비율 평균과 원시 합계는 구분합니다. 생성 파일이나 숫자만 따로 수정하지 마세요.

## Sharing and production build / 공유와 공개 빌드

Includes localized Open Graph and X large-image cards, PNG dimensions/alt text,
canonical, reciprocal `hreflang`/`x-default`, WebSite/WebPage JSON-LD, sitemap,
robots, SVG/PNG favicon and an Apple touch icon. Source SVGs and PNGs are under
`assets/`; no performance claim is included in social cards.

The default `site.json` has no public origin, so checked-in local previews use
localhost metadata and `noindex, nofollow`. Specify the actual HTTPS URL at build
time, including any deployment prefix, to generate publishable absolute URLs:

```sh
python3 -B scripts/build_landing.py \
  --site-url https://hires.no-money-do-you-have-money.com/ \
  --output dist/landing
```

Serve **only** the generated directory. It includes all runtime files and assets;
repository files and benchmark logs are not needed by the public server. On a
subdirectory deployment, place `robots.txt` at the host root if you want crawlers
to use it. Actual social-platform previews require a publicly reachable deployment.

기본 로컬 프리뷰는 검색 수집을 막습니다. 실제 HTTPS 주소를 지정하면 OG 이미지,
canonical과 사이트맵을 함께 생성합니다. 생성한 디렉터리만 공개 서버에서 제공하세요.
실제 플랫폼의 공유 미리보기 검증은 공개 주소에 배포한 뒤 수행할 수 있습니다.

Social SVG changes require raster regeneration. Development-only Playwright is
used for rendering; it is not a deployed dependency:

```sh
npm install --prefix /tmp/qh-landing-tools playwright
# Use an installed Chrome; adjust its executable path for your machine.
NODE_PATH=/tmp/qh-landing-tools/node_modules \
CHROME_EXECUTABLE='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
node scripts/render_landing_assets.cjs
```

`--check` verifies source/raster hashes and PNG dimensions, so stale social images
cannot silently be exported.

## Local verification / 로컬 검증 — 2026-09-26

```sh
python3 -B -m unittest discover -s tests -p test_landing.py -v
```

Nine static checks cover frozen-source validation, every raw cell including adverse
costs, crawler-readable localized HTML/OG, deployment prefixes, preview indexing,
translation fragments and raster integrity. Korean/English screenshots were
rendered and visually inspected. Browser checks passed at 320, 390, 760, 768,
1024, 1440 and 1920 px for both languages, with no horizontal page overflow or
clipped headings. Extra checks cover metric switching, raw-table scroll containment,
selection/details preservation, language request races, failed translation recovery,
actual clipboard success/failure, keyboard focus and reduced motion.

9개 정적 검사와 두 언어 × 7개 너비에서 검증했습니다. JavaScript를 끈 상태에서도
언어별 OG·그래프·원시 기록을 확인했고, 느린 언어 요청과 실패 시 복구도 검사했습니다.
이는 로컬 UI 검증이며 모델 성능 근거나 공개 배포의 검증을 대신하지 않습니다.
