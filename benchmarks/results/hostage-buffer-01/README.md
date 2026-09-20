# Buffer transfer 01 — 2026-09-20

Optional Python task ownership is adopted and works in both current sessions,
but this is **not an accepted overall efficiency win**. Current summed tokens
are **−5.93%** and wall time **−5.43%** versus the previous skill; versus no skill,
tokens are **+80.97%** and time **−3.47%**. All six sessions meet the five explicit
task/scope criteria. No original attempt was excluded, replaced or repeated.

한국어: 새 작업 관리 도구는 두 실행 모두 사용됐고 정상 작동했다. 이전 스킬보다
합산 토큰 5.93%, 시간 5.43%가 줄었지만, 무스킬보다 토큰은 80.97% 더 들고
시간은 3.47%만 줄었다. 전체 효율 개선으로 인정할 결과는 아니다. 6회 실행
모두 요구사항과 작업 범위를 충족했으며 불리한 결과도 보존했다.

## Frozen comparison

[Protocol](../../HOSTAGE-BUFFER-01-PROTOCOL.md), launch `ae3ee43`.
Original resources `83c138b`; current `3083086` adds optional `OwnedTasks` to
the same standalone Python callback asset. One newly authored buffer-flush task
in faulty and conforming variants, **not two independent tasks or real projects**.
GPT-6 Astra medium, n=1, serial, 360 seconds per cell. Fault order is
baseline/original/current; clean reverses it. Original always runs in the middle;
fixed order and shared host/cache remain limitations. Only the named skill is
installed/invoked in skill arms; this is not all-eight automatic discovery.

| Variant | Baseline tokens / seconds | Original tokens / seconds | Current tokens / seconds |
| --- | ---: | ---: | ---: |
| Faulty | 75,686 / 112.267 | 171,814 / 113.115 | 175,387 / 116.703 |
| Conforming | 89,561 / 123.402 | 146,093 / 127.437 | 123,653 / 110.786 |
| Sum | 165,247 / 235.669 | 317,907 / 240.552 | 299,040 / 227.489 |

Current versus original: faulty **+2.08% tokens / +3.17% time**, conforming
**−15.36% / −13.07%**. Current versus baseline: faulty **+131.73% / +3.95%**,
conforming **+38.07% / −10.22%**. None of the current/baseline pairs reduces both.
These are descriptive observed ratios, not confidence intervals or causal gains.
Tokens count full input (including cached input) plus output once; reasoning is
not added again. Wall time is whole process time, not test runtime. No dollar
estimate. [Arithmetic and reviewed rows](comparison.json).

## Original native evidence and review

All fault arms make the same one-line fix: prepend the detached batch instead of
overwriting concurrent additions. Each original seven-method suite first has
four intended restoration assertion failures, then seven passes after the fix.
There are no test repairs. All clean arms preserve production byte-for-byte;
baseline/current pass seven methods and original passes nine. Original clean
uses separate falsy-receipt methods where others use subtests; this is not an
extra correctness win by method count.

| Cell | CLI native items | Matching stored tool-record lines | Final native result |
| --- | --- | --- | --- |
| [Fault baseline](baseline/buffer-flush-fault--baseline--1/) | 5, 8 | 27, 38 | 7 pass |
| [Fault original](original/buffer-flush-fault--skill--1/) | 6, 8 | 39, 49 | 7 pass |
| [Fault current](current/buffer-flush-fault--skill--1/) | 6, 8 | 37, 47 | 7 pass |
| [Clean current](current/buffer-flush-clean--skill--1/) | 7 | 41 | 7 pass |
| [Clean original](original/buffer-flush-clean--skill--1/) | 5 | 40 | 9 pass |
| [Clean baseline](baseline/buffer-flush-clean--baseline--1/) | 6 | 34 | 7 pass |

All native success exits are 0; original faulty pre-fix exits are 1. Delivered
suites cover actual callback entry, empty/busy suppression without calling send,
exact item/receipt/ordinary-error identity, success with concurrent additions,
ordered recovery and retry after async failure/cancellation/synchronous failure,
independent buffers, bounded waits and owned cleanup. None requires private
backing-container identity or cancellation-exception identity. Baseline clean
also checks immediate suppression by driving the coroutine to StopIteration,
opaque items whose equality raises, and an exception object used as a receipt.
These nonidentical additional checks prevent claims of identical work.

Requirements, instructions, owner notes, HEAD and installed resources are
unchanged. Only production (fault arms) and local tests/support are changed.
No external discovery, installs, publishing or retained scratch was observed.
Final answers match actual native outputs.

Original command/output records were inspected, including empty copy/integrity
outputs. Mechanical any-output matches are only screening hints, not command
correlation. No missing native output was found in this comparison. Original
clean initially chains final checks, then records individual exits in an extra
command; its new-file no-index diff exits 1 without whitespace diagnostics.
That cost is retained, not hidden as setup. Baseline clean's final chained scope
command does not independently capture every exit; original-file hashes/diffs
also support preservation. Native tests have their own captured process exit.

Both current sessions read the complete asset and use `OwnedTasks`; original
fault reads/copies `ControlledCall` and writes task plumbing, while original
clean reads the asset but writes its own callback and task plumbing. Baselines
write their own support. Recorded responses (fault/clean): baseline **4/5**,
original **8/7**, current **8/6**. Final current checks are several shell commands
inside one outer parallel call, not several model round trips. Adoption alone
does not prove savings, and a larger asset/full reads can increase context cost.

Each cell includes original CLI events, selected stored tool records, delivered
files, diff, metadata, original-source hashes, reviewed outcomes, skill exposure
and reconciled numerical usage. Exact selected skill bodies are present in the
initial context of all four skill sessions; no exact skill body was observed in
the two baseline sessions. Private initial instructions/raw rollouts are not
exported. This does not prove absence of all broader model knowledge.

## Separate author controls

After all original sessions ended, [24 untimed author checks](author-controls.json)
ran in disposable project-local copies, leaving original artifacts unchanged:

- Every delivered suite passes correct code and valid container replacement.
- Every suite produces four real assertion failures on the original faulty code;
  no support-code errors or timeouts.
- The independently authored six-test contract oracle passes every delivered
  production implementation.

These are not extra model tasks or repaired original transcripts. The frozen
preflight, recorded in [run.json](run.json), separately shows the author oracle
passing both valid variants and producing three intended faulty assertions before
model launch. None of these finite controls certifies universal correctness.

## Decision

Retain optional task ownership as tested reusable support, **not as a proven
token-efficiency improvement over no skill**. Broad all-eight 20–30% claims,
featured-chart promotion and release approval are unsupported. The next useful
optimization target is repeated full-source/context and extra interaction cost,
while preserving application assertions; it requires a separately frozen future
comparison rather than relabelling these results.

한국어: 정상 구현·다른 정상 구현 통과와 결함 검출을 별도 24개 대조 검사로
확인했다. 이 검사는 모델 성능 측정에 합산하지 않았다. 도구는 유지하되 전체
성능 개선이나 배포 승인 근거로 포장하지 않는다. 기존 차트·측정값은 변경하지
않고, 다음 개선에서는 필요한 정보만 읽는 방식과 추가 대화 비용을 다룬다.
