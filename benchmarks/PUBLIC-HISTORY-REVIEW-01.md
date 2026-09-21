# Bounded public-history review01 and scratch-path export repair

2026-09-22. Scanned source `4174c180dd00e935c7845679aa4675463e4606b8`.
Read-only review of HEAD-reachable Git objects, not ignored runtime data,
other repositories, unrelated refs/reflogs, secret validation against services,
an entropy scan, license review or complete semantic privacy certification.

The existing `scan_evidence.py` patterns were reused (SHA256
`1bd3ca739610f7b08cbe2a18028197176453b5e705dbd1bb981b327b83baab4a`).
Synthetic positive/negative controls pass. Enumerated unique objects once via
`git rev-list --objects HEAD` and read with `git cat-file --batch`:1,368 commits,
6,350 trees,11,104 blobs,205,893,209 total object bytes. Blob/commit text was
scanned with UTF-8 replacement decoding; tree metadata was enumerated, not
content-scanned. Findings count matching lines per unique object/category, not
unique secrets or every historical filename occurrence.

## Findings and disposition

| Shape | Matching object-lines | Disposition |
| --- | ---: | --- |
| Credential/private-key |1| Test-only marker; no actual credential established |
| Bearer authorization |0| No match for this pattern, not proof of no secrets |
| Home/temporary path |284| Mixed documentation, fixtures and recorded local paths; publication review remains open |

The sole credential-shaped match is blob
`c0929a44ae80491ffa5ba7d18e445dc10be0c6f3`,
`tests/test_swe_lite_runtime_stage.py:73`: a private-key **header marker alone**
written to a temporary fixture to test rejection. Nearby assertions require
`stage.stage` to raise. It is not a key body or live credential; do not remove
this negative security test to obtain a zero-match report.

Of the284 path matches,231 are in blobs also present in the current tree and53
only in historical blobs. Current-line categories:26 containing the known local
owner home prefix,29 other home-shaped paths,176 temporary-path shapes. These
categories are not privacy verdicts: Docker runtime paths and deliberate test
fixtures can be benign, whereas author workspace locations still need review.
The full local object/line inventory is retained in ignored
`benchmarks/local-runs/public-history-01.json`; no matched values were printed.
Historical benchmark observations and Git history have not been rewritten.

## Concrete exporter gap fixed

The current exporter redacts known home/workspace paths and two macOS temporary
path forms, but leaves task-owned `/tmp/qh-*` and `/private/tmp/qh-*` paths.
Extended the existing regex to cover those forms; no new export pipeline or
automatic historical rewrite. These are redacted derivatives, not original
source bytes or executable paths. Existing source hashes still identify originals.

Two tests fail before repair and pass afterward. The first candidate's extra
word-boundary check also broke paths following JSON-escaped newlines; removed
that restriction to preserve the existing serialized-data behavior. The complete
export test checks events, metadata, summary, answers, diffs and project text,
valid JSON, unchanged raw inputs, original SHA256, native error text and exit
code. A separate control preserves unrelated `/tmp/application` and relative
paths, JSON escapes and actual/expected diagnostics. Eight existing native-node
reporter tests also pass, along with4 evidence,7 index-capture and2 transfer-summary
checks (23 checks total). This is not a full-suite rerun or model measurement.

## Remaining publication work

Do not mark public artifact review complete. Future exports can use the repaired
redactor, but already-published-to-private-Git artifacts still contain paths.
Review and create explicitly labeled sanitized derivatives without changing
benchmark metrics. Removing material from reachable Git history is a distinct,
potentially destructive operation requiring owner direction; no force push,
history rewrite, visibility or account setting change was performed.

한국어:1368개 커밋의 고유 파일 내용을 제한된 패턴으로 점검했다. 인증정보 후보
1개는 실제 키가 아닌 거부 테스트용 헤더였고,경로 후보284개는 추가 공개 검토가
필요하다. 앞으로 내보낼 자료의 임시 경로 누락을 수정했지만 과거 파일이나 Git
이력을 고치지는 않았다. 비밀정보가 전혀 없다는 인증이나 공개 승인도 아니다.
