# Packaging specifier audit01: mixed cost, no helper adoption

2026-09-21, resource `c8fd471`, launch `5aa96b7`.
[Protocol](PACKAGING-SPECIFIER-01-PROTOCOL.md) ·
[all four original sessions](results/packaging-specifier-01/README.md) ·
[original capture reconciliation](results/packaging-specifier-01/capture-review.json).

All four sessions complete the requested native detection work. Both arms use
direct authored pytest harnesses, **not the shipped audit helper or its batch
interface**. Both multiple-fault runs execute the correct suite once and reuse
that observation for all three independently executed mutants. This experiment
does not demonstrate additional baseline reuse caused by the skill.

## Recorded costs

| Request | Baseline tokens / seconds | Current tokens / seconds | Current difference |
| --- | --- | --- | --- |
| Single | 141,921 / 67.817 | 115,629 / 64.385 | tokens −18.53%; time −5.06% |
| Multiple | 148,555 / 75.893 | 156,564 / 86.393 | tokens +5.39%; time +13.84% |

Input plus output, cached input counted once. All four original attempts, source
reads and nonzero shell status remain included. No timeout, replacement, replay
or account-limit stop. Original contexts confirm Astra medium and original usage
counters reconcile. Recorded responses: single6→5, multiple6→6; this is not a
count of native child processes. The linked arithmetic validates every original
profile and records its digest, but does not attribute token differences to causes.

Single baseline performs an additional post-test source read. Its earlier broad
source search is truncated in the original stored output. Current single's final
file-discovery `rg` finds no AGENTS/conftest file and exits1 after successful source
reads; it is not a failed native test or setup error. Neither event was removed
from costs. Both multiple arms add per-test import-binding checks, with different
hooks/summary detail. Different inspection and instrumentation remain part of
the observed work; do not advertise either pair as an equal-work causal gain.

## Native execution and criteria

The four reviewed original commands use the supplied Python3.11.16, `-B`, fresh
copy-local source/test imports and native pytest with the unchanged selector:
`tests/test_specifiers.py -x -q --tb=short -p no:cacheprovider`.

| Actual variant | Collected | Native result | Exit | First witness |
| --- | ---: | --- | ---: | --- |
| Correct | 806 | 806 passed | 0 | — |
| Compatible return→False | 806 | 376 passed,1failed | 1 | `1` with `~=1.0` |
| Equality return→False | 806 | 311 passed,1failed | 1 | `2.0` with `==2` |
| Inequality return→False | 806 | 338 passed,1failed | 1 | `2.1` with `!=2` |

Single arms execute the first two rows (two processes each). Multiple arms
execute all four rows (four processes each). These are the model's actual checks,
not the earlier author controls. All detecting failures occur at the original
`test_specifiers` membership assertion, line482. The expected positive membership
is false in the requested mutant; no import, collection or support failure is
credited as detection. Fail-fast does not establish all later mutant cases.

Code and original evidence support native criteria1–4 in every cell:

- Collection hooks verify actual package, specifiers and test-module paths plus
  `tests.test_specifiers.Specifier is packaging.specifiers.Specifier` in each
  native test process. Multiple arms additionally verify at each executed test
  (baseline call hook; current setup hook). No installed-package substitution.
- Each disposable copy starts from the original code; exact replacement counts
  are checked, mutants are independent, test bytes/modes are checked unchanged.
- Native summaries, assertion values and subprocess exits substantiate every
  detection claim. The enclosing harness exits0 after reporting mutant exit1;
  it does not hide the native statuses.
- No survivor exists in these requested cases, so stronger tests are not required
  and neither arm changes existing assertions to manufacture detection.

For preservation/scope, all final original files/modes and installed resources
match, HEAD is unchanged, and no extra files remain. Actual try/finally or context
cleanup removes project-local copies; model inventories around execution include
Git files and report equality. No out-of-project discovery, dependency install,
repair, publication or detected scope violation occurs. Single baseline runs
`git status --short` before its inventory: optional index refresh is possible.
The harness did not retain initial pre-model index bytes, so whole-session exact
index-byte identity is not independently established. The retained pre-collection
index is after model work, not an initial baseline. Do not turn in-command
inventory equality into proof of every earlier or transient action, or publish
an unqualified strict5/5 score from these observations.

## Original output review, without replay

For all four native commands, original output equals the exported CLI aggregate
plus only its leading run label. Actual same-session polling links are confirmed:

- Single baseline: original output33; omitted CLI prefix `RUN correct` plus newline.
- Single current: original output35; omitted prefix newline + `RUN correct` + newline.
- Multiple baseline: outputs34/39; returned session47662 is polled by call37.
  Concatenation restores the full native output; only the leading run label is
  absent from the CLI aggregate.
- Multiple current: outputs35/40; returned session93657 is polled by call38.
  Same result, with the leading `=== RUN correct ===` label.

No native assertion/count/cleanup observation is missing in these reconciled
commands. Automatic matcher JSON is retained unchanged; its inability to match
a final polling chunk to a combined CLI record is not a missing-test verdict.
Single baseline source-read output21 still contains a truncation warning inside
its stored envelope, despite the matcher's outer `truncated:false`. Later focused
reads cover the concrete comparator/membership path; the entire original broad
source read is not reconstructed or claimed fully visible to the model.

Both current sessions have the exact selected skill body observed in tool output;
baseline has no exact body match. This does not prove absence from unavailable
context or causal use. No helper reference is read or helper executed. Listing
resource filenames in multiple/current is not executable-body exposure.

## Decision

Keep all results, including the slower/more expensive multiple pair. The single
pair's lower costs are a descriptive observation on one author-selected task,
not broad20–30% performance or independent validation. The correlated requests,
n=1, shared host/cache and fixed alternating order remain limitations.

Do not infer that a larger native suite automatically improves skill efficiency:
the baseline already avoided repeated setup here, and both arms wrote their own
harnesses. Do not force helper usage, repeat this unchanged task until favorable,
or add another generic batching hint based on this result. No skill change,
featured-chart promotion or publication approval follows from this review.
Broader cost/usefulness and release requirements remain unfinished.

한국어:4회 모두 실제 원본 테스트와 독립 결함을 검사했다. 단일 과제는 토큰18.53%·
시간5.06% 감소, 다중 과제는 토큰5.39%·시간13.84% 증가였다. 양쪽 모두 자체 검사
코드를 작성하고 정상 결과를 한 번만 실행해 재사용했으므로 배치 도구의 효과로
주장하지 않는다. 분할된 원본 출력은 연결을 확인했고 빠진 부분은 시작 표지뿐이다.
잘린 소스 출력과 초기 Git 인덱스 검증 한계는 남겨 두며 전체 성능 개선으로 채택하지 않는다.
