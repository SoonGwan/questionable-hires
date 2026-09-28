# Mobile title and tagline separation — 2026-09-28

Parent `c88fe0b0`. Visual review of English at320px showed the absolute-positioned
tagline intersecting the first title line. Existing page-overflow checks had not
detected text-to-text overlap. Actual rendered text ranges also reproduce it at390px.

At the existing mobile breakpoint, the tagline now follows the title in normal
flow. Line breaks collapse into ordinary spaces, with a14px margin. Desktop
positioning, typography, approved palette and copy remain unchanged. This adds no
asset or runtime dependency. [The rendered320px result](../benchmarks/results/landing-hero-layout01/en-320-after.png)
was visually inspected along with the1440px navigation feedback state.

[Browser geometry checks](../tests/browser/landing_hero_layout.cjs) inspect actual
text-node client rectangles, rather than the wide containing h1 box. Two languages,
eight widths (320,360,390,760,768,1024,1440,1920) and JavaScript enabled/disabled
produce32 cases. They require visible text rectangles, viewport containment, no
horizontal page overflow and no title/tagline text intersection.

[Before](../benchmarks/results/landing-hero-layout01/before.txt):28 pass/4 fail,
all failures English320/390 in both JavaScript modes; native process exit1.
[After](../benchmarks/results/landing-hero-layout01/after.txt):32 passing case records,
zero failures. This local after shell also ran the screenshot script, so its final
exit0 is not a separately captured geometry-process exit; the individual assertion
records provide the local outcome evidence. Hosted geometry will run as its own
command. These are installed Mac Chrome checks, not every browser/font/platform.

The landing maintenance guide now identifies integration07 (`1be35120`) as the
shown dated resource and preserves integration05/06 archive addresses. It had
still described integration06 despite the earlier actual publication. This is a
guide correction, with no frozen chart or model measurement change.

한국어: 영어320·390px에서 소개 문구가 제목과 겹치던 문제를 실제 글자 영역으로
재현했다. 모바일 문구를 제목 아래로 배치해 한영8개 너비×JavaScript 켜짐/꺼짐
32개 검사가 통과했다. 데스크톱 배치·실험 수치는 유지하며 토큰 절감으로 계산하지 않는다.
