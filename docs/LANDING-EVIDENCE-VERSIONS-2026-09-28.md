# GitHub evidence version wording — 2026-09-28

The landing called its GitHub status link “current candidate evidence,” but the
linked public document describes2026-09-22. Read-only `git ls-remote origin
refs/heads/main` returned `995c67f7c7829f85f650ec31018d25588691d892`; the page was
also inspected publicly. The currently downloadable resource is newer, and no Git
push is part of this change. A reachable page alone is not proof of current evidence.

Both language dictionaries now call this “Evidence published on GitHub” and say
it applies to the versions named there, which may differ from the page's download.
Static English/Korean HTML and JavaScript copy are generated together. The GitHub
link, benchmark numbers, frozen evidence bundles and skill archive stay unchanged.

Local validation:151 generated files;19 existing landing tests pass. Actual Chrome
checks cover KO/EN ×320/1440px ×JavaScript on/off (eight combinations), exact heading
and description, unchanged link destination, visible link and no document overflow.
Both mobile JavaScript cases preserve correct copy after language switching; no
page errors. Both320px link screenshots were visually reviewed. The in-app browser
selector returned unavailable and its discovered list was empty; standalone local
Chrome was used after that check. No full accessibility/browser matrix is claimed.

[Native checkout validation](../benchmarks/RELEASE-VALIDATION-EXECUTION01.md) is a
separate earlier source checkpoint, not a model experiment or this hosted release.

한국어: GitHub의 과거 기록을 ‘현재 후보’로 부르던 문구를 양쪽 언어에서 바로잡았다.
링크된 문서에 적힌 버전의 근거이며 현재 다운로드와 다를 수 있음을 표시한다.
수치·자료·다운로드는 그대로다. 기존 웹 검사19개와 화면8개 조건·언어 전환이
통과했으며, 모델 절감 성과로 계산하지 않는다.

## Public delivery

Source **`70f97fea2a6e309a0d1c7ff61e9d699aa09fbc09`** is hosted.
[Six HTTPS observations](../benchmarks/results/landing-evidence-versions01/public.json)
verify its health revision, exact KO/EN pages and generated JavaScript, canonical
URLs/indexability, and unchanged skill download/checksum. Both pages contain the
new version wording while retaining integration07 and measured source `1be35120`.
The archive stays106,932 bytes, SHA-256
`7c6470b3c69fd75f96fcc3b14654c0234d0f1a9039393e604c1f788220739d96`.
[Local browser observations](../benchmarks/results/landing-evidence-versions01/local-browser.json)
remain separate from these public HTTP checks. The owned local preview server was
stopped after checks. No new model cost observation or GitHub push is claimed.

한국어: 배포70f97fea의 실제 한영 문구와 메타데이터·파일 동일성을 HTTPS6개
경로에서 확인했다. 공개 스킬 파일과 기존 실험 수치는 그대로 유지됐다.
