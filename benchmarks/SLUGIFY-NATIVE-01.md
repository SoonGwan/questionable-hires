# Slugify native01 — recipe improvement, baseline cost still unmet

Reviewed2026-09-21. Launch `6b85ec1`; prior resources `387c53b`, current
`a7dcbd8`. [Protocol](SLUGIFY-NATIVE-01-PROTOCOL.md),
[preflight](SLUGIFY-NATIVE-01-PREFLIGHT.md),
[retained exports](results/slugify-native-01/),
[comparison data](results/slugify-native-01/comparison.json).

**All arms meet5/5. Current uses fewer tokens than prior, but more than baseline.**
One author-inspected upstream-source task,n=1 per arm, serial current/baseline/prior,
shared host/cache. No timeout, account limit, retry, exclusion or replacement.
Keep the reference correction provisionally; no all-eight20–30% gain or featured
chart promotion is justified.

| Condition | Input | Cached subset | Output | Total | Seconds | Responses | Native processes / method executions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current |114,602|80,256|1,451|116,053|63.895|5|8 /12|
| Baseline |82,901|63,872|2,089|84,990|75.640|4|4 /12|
| Prior |147,562|123,392|1,592|149,154|65.068|6|8 /12|

Current versus prior: **tokens−22.19%, time−1.80%**.
Current versus baseline: **tokens+36.55%, time−15.53%**.
Cached input is a subset, not added twice. Recorded response usage reconciles
with CLI totals. Time covers the whole model process, not isolated native
execution. No dollar estimate, statistical significance or causal allocation.

## Original required outcomes

All three independently introduce only the requested edits inside `slugify()`:
remove final custom-separator conversion, forward False instead of save_order,
and remove requested truncation. All selected test bodies remain unchanged.
The first two faults survive both selected tests; the last survives
`test_non_word_characters` and fails `test_max_length` with expected `jaja-lol`
versus actual `jaja-lol-mememeoo-a`. Its second assertion is not reached under
that fault; answers disclose this rather than claiming both assertions executed.

All arms reuse the existing `test_custom_separator` and `test_save_order`
witnesses, with correct passing and matching faulty assertion failure:
`jaja.lol.mememeoo.a` versus `jaja-lol-mememeoo-a`, and `one-two` versus
`one-two-four`. They correctly explain the earlier long word/later short word
boundary. No setup error is counted as detection. Required correct observations
are identified as shared/reused rather than repeated evidence.

## Actual work and instruction use

Both skill arms read and invoke the same native helper. Each sends five entries:
three faults with the two selected methods, plus two fault/witness pairs.
One correct selected suite is executed and referenced twice. The witness pairs
execute separately. Each arm therefore uses8 native processes for12 methods;
all native results, copied bindings and intended assertions are retained. There
are no skips, timeouts or reported helper-output truncations. Whole-project
preservation is explicitly enabled with `guard_project`.

Prior reads the native recipe and probe guide, searches helper fields, then reads
helper lines400–550 before invocation. Current reads the revised native recipe
without probe/common/advanced guides, but does inspect helper lines1–160.
This is consistent with the targeted routing hypothesis, not proof that every
saved token came from the edit or that inspection should be forbidden. Prior's
six shell commands span six responses; current has four commands/five responses.
The identical entrypoint body is present in initial messages and reread in both.
Baseline has no matching entry-body observation, not proven absence of all context.

Baseline writes temporary orchestration and appends a `setUpModule` binding
check after the unchanged upstream test bodies. It groups all four correct
methods in one process, selected tests plus the matching witness per first two
faults, then the selected pair for omitted truncation: **4 processes,12 methods**.
This is permitted by the frozen task. It reads the whole source/test files and
checks AST identity outside slugify. Its native module hook verifies the imported
function, package/module paths and function code path inside every test process.

Both helpers verify copied imports; their same-process prechecks verify the
global function binding used by all four methods and the copied code path.
Baseline's instrumentation modifies only disposable test-module suffixes; skill
arms leave the whole copied test file intact. Required bodies/results match,
but startup/setup grouping differs. Equal method counts are not a general proof
of equivalent environments or coverage. Baseline's smaller process count also
shows why helper adoption cannot itself establish efficiency.

Original records establish results and cleanup, without author replay. Post-run
inspection confirms every original supplied file byte/mode, HEAD, unchanged
installed resources and no extra root artifacts. Model inventories include Git
metadata. No pre-session binary-index snapshot exists; do not claim independent
binary-index identity across the session.

## Capture and publication

Thirteen CLI shell outputs reconcile with stored originals:12 exact and one
unique equal-exit nonempty suffix match. Baseline item4/original line30 omits
771 redacted characters: the complete first correct-suite command, binding,
four passing method results, native summary and exit0. The stored original
contains that evidence and is exported; no author replay fills the omission.
Both skill arms match exactly. No missing/duplicate call records, unmatched
CLI commands or unmatched stored shell outputs were found.

Private raw sessions are retained with mode0600. Public artifacts include
redacted tool records, usage/exposure/capture summaries, commands, answers,
source snapshots and upstream MIT LICENSE. No private injected instructions
are exported. Pattern scan has no hits; command review shows scoped task work
plus authorized interpreter/skill access. This is not a security certificate.

Runner checks3/3 passed before launch. Local preflight was repeated before
freeze, not during model timing. Repository validation, featured synchronization
and whitespace checks pass. No new full-suite or hosted-CI result is claimed.

## Decision

Keep the narrowly scoped recipe clarification provisionally: both skill arms
perform the same required native checks, and fewer guide transitions plus lower
total tokens are observed in current. However, baseline tokens remain materially
lower and timing differences are single observations. Do not replay this exposed
case until a preferred ratio appears, or label the prior comparison as a no-skill
20% gain. The prior [dateutil](DATEUTIL-NATIVE-01.md) adverse result stays visible.

Before adding more helper features, investigate the remaining cost tradeoff:
the baseline can group existing tests by variant without separate correct/faulty
pair orchestration. Any future grouping must retain native method evidence,
copy binding, failed-correct stopping and cleanup; cached results from different
selections must not be silently declared interchangeable. This observation alone
does not authorize removing those invariants or prove grouping will reduce tokens.

한국어: 현재 안내는 이전 안내 대비 토큰22.19%·시간1.80% 감소했으며 세 조건
모두 필수 검증5개를 충족했다. 그러나 무스킬 대비 토큰36.55% 증가가 남는다.
같은12개 테스트 실행에 스킬은8개, 무스킬은4개 프로세스를 사용했다. 안내 개선은
잠정 유지하되 전체 성능 향상으로 확대하거나 대표 그래프를 바꾸지 않는다.
