# Named historical Python regions — 2026-09-15

Resource: `skills/necromancer/scripts/python_regions.py` and its conditional
reference, developed from parent `da20939`. This is an **author correctness
replay**, not a new model run or accepted efficiency gain.

## Why

The [redirect comparison](results/httpx-redirect-history-01/README.md) includes
custom AST extraction of historical methods. The subsequent
[auth comparison](results/httpx-auth-history-01/README.md) retains broad historical
reads and mixed whole-task cost despite avoiding a compiler-context failure.
A small optional selector can replace repetitive extraction code when names and
source revision are already known. It cannot decide which history is relevant.

## Real-source replay

Read `httpx/client.py` from HTTPX revision
`387f04732baa99ea472c6f78c905a9359b3d0e0e` (`ee37a762^`) using `git show`.
The 29,674 source bytes have SHA-256
`c8c1e60dda5b1f8ba440bd414c9d7a981e53b5f99c10dd731bf82243433a7770`.
Select these three names together:

| Name | Physical lines |
| --- | --- |
| `AsyncClient.build_redirect_request` | 426–438 |
| `AsyncClient.redirect_headers` | 482–504 |
| `AsyncClient.redirect_stream` | 506–521 |

All three definitions were complete, totaling 2,128 UTF-8 **region-text** bytes
(not total JSON size or model tokens). Author assertions checked exact equality
with the original source line slices, both caller references, both header names
and the stream's `return None`. No source execution or modification. These checks
preserve selected static evidence, not whole-module semantics or runtime behavior.

For reproduction, pipe the verified Git source into the CLI with all three
`--name` options; enable shell `pipefail` and check the producer. Compare each
region's original start/end line slice and the source hash above. No download is
needed when the full history is already available.

## Controls and limits

Six automated tests cover decorators, duplicate/conditional/nested definitions,
async methods, UTF-8/CRLF/Unicode separator preservation, non-execution of a module
containing a raising statement, missing selections, text/input/match bounds and
real CLI exit statuses. Run:

```sh
python3 -B -m unittest discover -s tests -p test_python_regions.py
```

Whole-repository verification at this checkpoint: **619 tests passed in 94.465s**;
skill validation, repository validation and featured-language synchronization
checks also pass. This includes helper correctness/packaging checks, not new
live-model performance observations.

Truncated/missing text is explicitly incomplete. Excerpts omit surrounding
bindings/comments/context and are not executable replacement modules. The hash
attests stdin identity only. Model adoption, total token/time savings and transfer
to unseen tasks remain unmeasured. No new chart values or featured promotion.

한국어: 이미 확인한 과거 함수 이름으로 필요한 코드만 추출하는 선택형 도구다.
실제 HTTPX 과거 소스에서 함수 3개와 호출 관계·조건의 정적 텍스트 보존을 확인했다.
29,674바이트와 2,128바이트는 전체 소스와 선택된 코드의 크기이지 토큰 절감률이
아니다. 자동 검사 6개는 통과했지만 모델의 사용 여부와 전체 작업 비용 개선은
아직 측정하지 않았다. 기존 불리한 결과와 그래프는 그대로 유지한다.
