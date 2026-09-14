# Header design review: fewer calls, higher token cost

Frozen launch `5c6e1a0`; [protocol](../../HTTPX-HEADERS-DESIGN-01-PROTOCOL.md).
Landlord resource `bd1d8b8`, actual HTTPX checkout
`26d48e0634e6ee9cdc0533996db289ce4b430177`. New authored header ticket on the
same project as prior experiments, not an independent project holdout.
GPT-6 Astra / medium, baseline then skill, one persisted session each, 240s cap.

| Arm | Total input + output tokens | Seconds | Shell / outer calls |
| --- | ---: | ---: | ---: |
| Baseline | 116,759 | 103.291 | 8 / 4 |
| Skill | 160,999 | 88.301 | 7 / 4 |

Skill records **+37.89% tokens / −14.51% time**. Cached input is counted once.
Both satisfy the required review: native **27 tests pass**, all twelve actual
header representations are recorded correctly, and both trace real transport
and cookie consumers. No setup failures, retries, timeouts or account limits.
This is not a net efficiency win. Shared host/cache, n=1, fixed order and different
extra work prevent causal or broad inference. No featured/chart promotion.

Both distinguish joined indexing from separate field boundaries, original bytes
and casing. Both explain the P2 collision between repeated fields and a single
comma-valued field, reject comma splitting as an inverse, and identify where
normalization/encoding/state would move if the wrapper disappeared. Both treat
reconstruction as an information-loss probe, not a replacement transport test.
Baseline additionally suggests consolidating joining logic; that suggestion is
static, not implemented or verified by a new refactor.

## Concrete workflow observation

Skill combines the entry with a large numbered batch: `_models.py` lines 1–420,
the full headers test module and full default transport. That command emits
43,865 CLI characters. Its stored response is shorter under an outer output
budget; skill then reads the first 178 test lines again alongside configuration.
The reread can be necessary to recover omitted evidence—it is not independently
scored as waste. But grouping paths has not kept selected context proportional.
Baseline splits eight shell reads/checks across four outer calls and also has one
budget-truncated source response. Fewer shell commands alone did not lower tokens.

The next candidate should select relevant symbol/consumer regions within large
files and recover missing evidence after truncation. Do not forbid full-file
context when needed or change this already-measured task to force a cheaper path.

## Original evidence and scope

[comparison.json](comparison.json), answers, commands, metadata, selected public
source and `tool-records.json` are retained for both arms. All 125 original file
hashes and installed resource hashes are unchanged; no non-Git/non-skill extras
remain. Reviewed commands perform no source writes, network or installs. Final
identity does not prove absence of every transient write.

Fifteen shell commands have fifteen parsed stored outputs. Thirteen output/exit
pairs match CLI records exactly after path normalization. Exceptions:

- Baseline `item_5`: CLI 17,062 characters, stored response 16,102 with explicit
  inner truncation. Native pytest/probe outputs are separate and complete.
- Skill `item_2`: CLI 43,865 characters, parsed stored output 37,515 under an
  explicit **outer** budget warning. The outer block contains two JSON lines,
  not one JSON object; parsing it as a whole initially missed both outputs.
  Line-by-line inspection recovers the two valid records, not omitted text.
  The actual `.raw` transport handoff remains present in the stored source.

Parallel response order differs from CLI completion order, so match exact
outputs before pairing the two remaining truncated responses. Do not infer that
the larger CLI text was all model-visible. All requested probe observations and
both 27-pass summaries are in original stored records, not author reruns. No
missing/unmatched/duplicate outer call IDs. Full rollouts remain local because
they contain private instructions; exported hashes identify unredacted originals.

한국어: 실제 헤더 설계 검토에서 양쪽 모두 27개 검사와 12개 관찰·소비자 근거를
충족했다. 스킬은 시간 14.51% 감소했지만 토큰은 37.89% 증가했다. 큰 파일 일괄
읽기가 출력 예산에 걸렸고 테스트 일부를 다시 읽었다. 호출 수 감소를 성능 개선으로
포장하지 않으며, 다음 지침 수정은 큰 파일에서 필요한 구간을 고르는 데 한정한다.
현재 결과와 출력 잘림은 그대로 보존하고 그래프는 바꾸지 않는다.
