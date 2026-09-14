# Checkpoint 09 export — 2026-09-14

Model launch `3a7d972`, resources `9071a1c`. This post-run publication step does
not change measured resources or establish completion of the evaluation.

[All 18 exported cells](results/bundle-contract-09/) now retain commands, events,
answers, metadata, original-source hashes and 58 project text files. Manifest,
event transformations, usage and source-file provenance reconcile against local
raw artifacts. Exported project text matches the originals after the documented
path redaction. Pre-collector index binaries remain local, not published.

## Privacy and evidence preservation fix

The formatter answer contained a malformed macOS temporary path without the
`folders` component, which the existing export expression missed. The exporter
now recognizes that observed shape alongside normal temporary paths. Shared
redaction also applies to run-manifest text. JSON escapes and Markdown delimiters
are excluded from a matched path so that following evidence is not consumed.

The native exporter test failed on the prior implementation's exposed manifest
path, then passed after the fix. It exercises manifest, events, command JSON,
metadata, stderr, answers, diffs and a copied log. It verifies intact failure text,
test count, exit code, valid JSON, a surviving normal local source link, raw-source
hashes and unchanged raw artifacts. One new test / 0.009s, five index-capture
tests / 0.341s and 25 runner tests / 2.494s pass. These 31 author tests are not
model benchmarks or performance evidence.

The actual 18-cell export was scanned for home and `/var` paths and key-like
strings; no matches. This is an observed-pattern check, not a universal secret
scanner. Incorrect links are masked, not repaired into invented source evidence.
Link validation caught a masked `<TEMP>` target in the first export. The exporter
now keeps its label as plain text. That candidate export was retained locally;
the final export was regenerated and link-checked, not manually patched.
Raw originals remain unchanged. Historical exports are not rewritten.

## Still unresolved

Both original capture gaps remain in the exported logs: form skill's native
test output and persistence baseline's first comparison phase. Author replays
do not fill them. Four pairs still use more tokens, two more time as well, and
different work limits the aggregate reduction of 13.65% tokens / 19.54% time.
Independent remaining controls and a consolidated review are still due. No
featured pointer, historical chart or success score changes here.

## 한국어

18세션과 프로젝트 텍스트 58개를 내보내고 원본 사용량·로그 변환·해시와
대조했다. 잘못 생성된 임시 경로도 가리고, 뒤의 실패 문구·테스트 개수·JSON
구조는 보존하도록 수정했다. 관련 작성자 테스트 31개가 통과했다. 원본과
과거 공개본은 수정하지 않았고 원본 인덱스 바이너리는 공개에서 제외했다.

원본 출력 누락 2건과 불리한 비용 결과도 그대로다. 이 단계는 공개 데이터
정리이지 전체 성능 개선의 입증이나 평가 완료가 아니다. 추가 대조군과 종합
검토가 남아 있어 대표 그래프는 변경하지 않는다.
