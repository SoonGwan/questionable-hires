# Public-path review01: classify the existing inventory

2026-09-22. This classifies all284 matched object-lines from the earlier
[bounded history scan](PUBLIC-HISTORY-REVIEW-01.md), source`4174c18`.
It is **not a new scan of current HEAD** or a complete semantic/secret audit.
[Machine-readable ledger](results/public-path-classification-01.json) retains
object IDs, representative paths, original line numbers, categories and decoded
line hashes without copying matched source text. Original files/history are unchanged.

| Category | Object-lines | Interpretation / remaining disposition |
| --- | ---: | --- |
| Known owner home |28|26 in then-current blobs and2 historical-only. Real author paths; eight-file derivative set covers the identified current artifacts, not historical removal. |
| Account directory |12|Three app-server artifacts. Labeled derivatives replace the path UUID; original blobs remain reachable. |
| macOS temporary shape |4|Three authored report lines and one exporter regression fixture; do not confuse the synthetic fixture with author data. |
| Task temporary shape |225|75 protocol/report lines,144 recorded-result lines,6 test/scanner/runtime-source lines. A task path is not inherently a secret, but this category alone is not a privacy verdict. |
| Retained upstream documentation |1|Example traceback in retained HTTPX quickstart; not evidence of this repository owner's home directory. |
| Retained URL test data |12|Literal file-URL fixtures in a captured diff. Altering these in original evidence would alter observed test data. |
| URL test-data explanation |1|Report explicitly discussing those retained file-URL fixtures. |
| Prose substring |1|`workspace/home/temp redaction` matches the broad home-path pattern; not an absolute home path. |

Classification precedence is owner home, account directory, macOS temporary,
task temporary, then individually inspected remaining lines. A single line can
contain several matches; counts remain object-lines, not path occurrences,
unique files, secrets or affected people. Historical path hints identify one
representative name, not every name under which a blob ever appeared.

The four macOS-shaped lines are in the boundary-formatter report, workspace
identity report (two lines), and exporter-privacy test. Task-temporary counts
are grouped by their recorded path's role, not by an assumption that every
recorded path is acceptable for publication. No scanner exclusions were added.
No benchmark assertion, URL fixture, failure value or frozen result was edited.

## What this resolves and does not resolve

All284 earlier path-shaped findings now have an explicit category; none is
silently discarded. This narrows review work and prevents deleting negative
tests or upstream URL fixtures just to obtain a clean pattern scan. The separate
private-key-header finding remains a deliberate rejection-test marker, not a
discovered key body. The absence of bearer matches remains only a pattern result.

[Eight reading derivatives](results/public-path-derivatives-01/README.md) are
available with original/derived hashes. They do not remove original owner paths
or account identifiers from a public clone. Owner disposition for original and
historical artifacts remains required before changing visibility. No destructive
history operation, public release, credential check against a service or account
configuration change was performed. Later commits and additional privacy/license
categories need their own review; this older inventory cannot certify them.

한국어: 이전 스캔284개를 전부 분류했다. 작성자 경로28개·계정 경로12개는
원본/이력 처리 판단이 여전히 필요하다. 임시 경로229개는 기록·설명·테스트가
섞여 있고, 나머지15개는 외부 문서·URL 테스트·설명이다. 가짜 경로를 지워
검사를 통과시키거나 원본 벤치마크를 바꾸지 않았다. 현재 HEAD 전체 검사나
공개 승인으로 해석하면 안 된다.
