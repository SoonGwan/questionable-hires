# Landing cache boundary audit — 2026-09-28

Native audit of owner-repository source `e8993de3`, using the existing Con Artist
single-audit helper. This is not a model comparison, independent holdout, hosted
check or token/time improvement. The production server was correct and unchanged.

Only full 64-character lowercase hexadecimal artwork names qualify for immutable
caching. A controlled change from `[0-9a-f]{64}` to `[0-9a-f]+` incorrectly accepts
shorter/longer fingerprints. Existing tests did not detect this reachable fault.

| Native phase | Methods | Exit | Observation |
| --- | --- | --- | --- |
| Original tests, correct source | 7 | 0 | Pass |
| Original tests, faulty copy | 7 | 0 | Fault survives |
| Proposed tests, correct source | 8 | 0 | Pass |
| Proposed tests, faulty copy | 8 | 1 | Four cache-header assertion failures |

The added method serves existing 63- and 65-character names in PNG and WebP.
It verifies the actual 200 response/body and `no-cache`, then conditional 304 and
HEAD responses. Each faulty-copy subtest fails at the first GET cache assertion:
actual `public, max-age=31536000, immutable`, expected `no-cache`. Its later
conditional/HEAD assertions therefore do not execute on faulty code; all execute
on correct code. This demonstrates one fault, not complete cache-policy coverage.

The actual native runner is `python -B -m unittest discover -s tests -p
test_landing_server.py -v`. Each of four fresh copies verifies the loaded test
module and the test's dynamically loaded origin path/hash in that same process.
No skips, timeouts, truncated output or setup errors occurred. Selected source
bytes/modes were preserved and helper-owned copies removed. The existing fixture
uses ordinary OS temporary directories and loopback ephemeral ports; this audit
is not a sandbox or whole-repository/external-effects inventory. Production
services were not modified. Exactly the verified test edit was applied afterward.

Retained [recipe](../benchmarks/results/landing-cache-boundary-01/recipe.json),
[native observations](../benchmarks/results/landing-cache-boundary-01/native.json)
and [source/test hashes](../benchmarks/results/landing-cache-boundary-01/metadata.json).
The owner repository's absolute path is replaced by `<repository>` in exported
observations; metadata retains the raw observation hash. To replay original and
proposed tests, use the recipe against source `e8993de3`, not the already-improved
working tree. Do not count a replay as a new model observation.

한국어: 실제 서버는 정상이며 수정하지 않았다. 지문 길이를 잘못 허용하는 결함을
격리된 복사본에 넣으면 기존 7개 테스트는 모두 통과했다. 보강한 8개 테스트는
정상 코드에서 통과하고, 잘못된 코드에서는 PNG·WebP의 캐시 헤더 오류 4건을
검출했다. GET 실패 이후의 조건부 요청·HEAD 검사는 결함 복사본에서 실행되지
않았다. 검증된 테스트 변경만 적용했으며 모델 토큰·시간 개선이나 공개 배포
검증으로 간주하지 않는다.
