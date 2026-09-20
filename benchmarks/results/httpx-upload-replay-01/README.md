# HTTPX upload replay diagnosis — reviewed 2026-09-21

**Both conditions satisfy all five criteria; no measured improvement.** Launch
`026f532`, Exorcist resources `9c03f56`, HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`.
[Frozen protocol](../../HTTPX-UPLOAD-REPLAY-01-PROTOCOL.md),
[reviewed comparison](comparison.json), [original run manifest](run.json).

| Condition | Total tokens | Wall seconds | Responses / shell commands | Criteria |
|---|---:|---:|---:|---:|
| Current skill | 104,299 | 81.269 | 5 / 4 | 5/5 |
| No skill | 102,825 | 75.652 | 5 / 4 | 5/5 |

Skill cost is **+1.43% tokens / +7.42% time**. Input includes cached input once;
token totals reconcile with original session usage. One author-selected task,
one run per condition, skill first, shared host/cache and unequal details do not
establish causality or general performance. No retries, timeouts or account limits.

## Original behavior and verification

Both use the supplied interpreter and actual checkout Client, multipart encoder
and 307 redirect implementation. Each constructs four fresh uploads, records both
hops via request hooks and actual local transports, and asserts complete replay
behavior. Every path remains POST → POST, finishes 200 and retains one 307 history
entry. Those statuses alone are not the oracle.

| Path | Skill body lengths | Baseline body lengths | Observed outcome |
|---|---:|---:|---|
| Mock, one-pass file | 171 → 171 | 165 → 165 | Exact replay |
| Direct stream, one-pass file | 171 → 152 | 165 → 152 | Entire payload lost; framing remains |
| Direct stream, seekable file | 171 → 171 | 165 → 165 | Exact replay |
| Direct stream, buffered request | 171 → 171 | 165 → 165 | Exact replay |

Payload lengths differ (19 versus 13 bytes); each session's initial bodies are
byte-identical across its four controls and use the same fixed boundary. They
include binary/control bytes and are captured losslessly. Both assert the failing
body equals the first body with exactly the payload removed. Separately parsing
original records confirms methods, lengths and all eight bodies per condition;
this is evidence inspection, not an author rerun replacing model output.

Both trace MockTransport's `request.read()`, replacement with ByteStream,
method-preserving redirect stream reuse and multipart file exhaustion/rewinding.
Both correctly distinguish unknown wire/server behavior from local observations,
and propose bounded buffering, seekable/spooled storage or deliberate redirection
with fresh input, including memory/I/O tradeoffs. No library change is made.

The skill uses a one-pass file with seek/tell raising UnsupportedOperation; the
baseline file has no seek/tell and records read lengths. Both exercise supported
non-seekable paths. Skill additionally hashes all repository files in its probe;
baseline checks Git status, with independent author inventory/index review covering
both. Neither uses the optional bounded-probe helper, repeats the four-case native
experiment, runs unrelated pytest groups or creates a disposable report. Source
reading differs but no particular read is established as the cause of the cost gap.

## Capture, exposure and preservation

**Baseline CLI `item_5` has empty output.** The corresponding original stored tool
response at line **35** contains the full native output (5,468 characters after
path normalization), exit 0, four controls and final assertion confirmation. It is
retained in [baseline tool records](upload-replay--baseline--1/tool-records.json).
The empty CLI event is preserved, not silently replaced. Baseline's final answer
is supported by that original response, not a post-run recreation. Every other
shell output/exit matches CLI capture. Skill native response is stored line 36.

Skill's exact installed main body appears in initial message line 11 and again
as a tool read at line 17. Baseline exact matching body is unobserved. Neither
catalog mentions nor missing matches establish complete context isolation. Private
initial messages are not published; only exposure locations/hashes are retained.

All **125 original tracked files** retain Git blob identities and modes in both
final projects. Original HEAD and pre-collection index match the upstream tree,
installed resource manifests are unchanged, and no extra project files remain.
Selected public source and LICENSE are exported with explicit `project-export.json`
selection metadata; these excerpts are not a complete runnable checkout. Original
full projects/sessions remain privately retained. Privacy scan passes; this does
not certify universal privacy or correctness.

## Decision

Keep the current Exorcist unchanged. This realistic but prompted diagnostic is
correctly solved without the skill too; adding a mandatory mock/transport audit
would overgeneralize this example without demonstrated benefit. Do not rerun the
same exposed task until a favorable percentage appears, promote this result to
featured graphs or treat native preflight success as model improvement. Broader
usefulness and the requested whole-bundle efficiency goal remain unproven.

한국어: 실제 HTTPX 진단은 양쪽 모두 성공했지만 스킬은 토큰 1.43%, 시간 7.42%
증가했다. 무스킬 CLI에서 빠진 출력은 같은 원본 세션에서 확인했고 재실행으로
대체하지 않았다. 원본 파일·권한·Git·스킬 보존을 확인했으며 이 사례를 근거로
불필요한 범용 규칙을 추가하거나 성능 향상을 주장하지 않는다.
