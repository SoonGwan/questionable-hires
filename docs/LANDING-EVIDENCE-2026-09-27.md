# Portable evidence downloads — 2026-09-27

Source `e42e149c`, preceded by `41a50723`. The original two downloadable reports
used repository-relative links, but the landing served only those reports and a
flat comparison JSON. Their protocol/native evidence links had no served target.
The external GitHub protocol URL also returned404 during this audit; no repository
visibility or publication cause is inferred from that response.

The builder now serves23 explicitly reviewed original sources at matching relative
paths, retaining each byte and the existing flat JSON alias. The source
[manifest](../landing/evidence-manifest.json) is reviewed configuration: new report
links fail the build unless their targets are included. No recursive automatic
publication or private grading input is added. The closure is four existing
Markdown reports plus their existing JSON/native text evidence, limited to
integration05. Graphs and measurements are unchanged.

A localized ZIP download packages the same layout for offline reading:24 members,
including the flat JSON alias,47,030 bytes. Stable member metadata keeps builds
reproducible. Extract before opening a report so relative evidence links resolve.
External web links are not archived or newly verified.

[Final failing-before check](../benchmarks/results/landing-evidence-e42e149c/before-final.txt)
identifies the missing protocol target. [Passing-after check](../benchmarks/results/landing-evidence-e42e149c/after.txt)
checks every local reference in every exported report. The subsequent ZIP check
verifies archived relative links and exact member bytes. Current checks are14
landing +4 server tests;37 generated files and featured synchronization pass.
Earlier author diagnostic/fixture-placement mistakes are described in the audit;
the final before observation retains all previous assertions. An intermediate
generated-preview failure preceded regeneration and is separately retained.

[Browser observations](../benchmarks/results/landing-evidence-e42e149c/browser.json)
cover KO/EN at320/390/1440px: no overflow/errors, unchanged8-row cohort table and
606,355/507.824/718,747/553.853 footer, and time graph switching. Both actual390px
[downloads](../benchmarks/results/landing-evidence-e42e149c/downloads.json) match the
generated ZIP and pass archive integrity checks. These are local observations,
not hosted verification, new model measurements or a fourteen-layout sweep.
[Audit](../benchmarks/results/landing-evidence-e42e149c/audit.json) retains hashes,
counts and limitations. Original model/native evidence is not relabeled.

한국어: 원본 보고서의 상대 경로를 유지하며 검토된23개 근거 파일만 함께 제공한다.
원본 바이트·수치·그래프는 그대로다. 한·영 ZIP은24개 구성원과47,030바이트이며
압축을 풀면 로컬에서도 연결 근거를 읽을 수 있다. 상대 링크의 수정 전 실패·
수정 후 통과, 두 언어 실제 다운로드,320·390·1440px 표·그래프를 확인했다.
현재 검사18개·생성 파일37개이며 모델 성능이나 공개 배포 검증은 별도다.
