# Invoice history/necessity screen — 2026-09-15

Launch `14a8556`; Necromancer resources `401eab9`. See the frozen
[protocol](../../HISTORY-INVOICE-01-PROTOCOL.md) and
[payload](../../history-invoice-01-cases.json). One new authored task, one fresh
GPT-6 Astra medium session per arm; skill first, then baseline, serial, 240-second
limits. Both complete. This is not a production workload or isolated old/new
serialization experiment.

## Result: correct decisions, no efficiency improvement

| Measure | No skill | Necromancer |
| --- | ---: | ---: |
| Total input + output tokens, cache included | 91,090 | 94,406 |
| Process wall time | 51.499s | 57.133s |
| Shell commands | 6 | 7 |
| Outer tool calls | 4 | 4 |
| Shell command failures | 1 | 1 |

Skill costs **3.64% more tokens and 10.94% more time**. Both correctly recommend
removing the unreachable integer branch (A), retaining rounding (reject B), and
identify the distinct introducing diffs and current normalization boundary.
Both observe all nine required current/A-only/B-only entrypoint results, then run
the existing three tests under each variant (another nine calls). The observed
results agree: `[101, -101, 234]` for current/A, `[100, -100, 234]` for B. B fails
the actual positive and negative half-cent assertions; it is not a setup error.

No history collector or guide is read/executed. Native Git is appropriate for
this tiny four-commit repository. The preceding compact-output change therefore
has **no demonstrated adoption or cost effect here**. Do not force helper use to
manufacture an improvement, call this whole-task performance acceptance, or
attribute the difference to one instruction or to serialization.

## Actual work and limitations

- Both initially try unavailable `python`, receive exit 127, and use `python3 -B`
  successfully afterward. Preserve these original failures; no author retry or
  launch repair is subtracted from cost. A new runtime rule is not supported by
  this shared baseline/skill failure alone.
- Skill reads its entry, inventories files, uses blame, reads introducing diffs
  and then the normalization commit. Baseline reads the short complete relevant
  log/patch history and stat information. Both inspect current files and callers.
  Skill has an extra shell command, but both group work into four outer calls.
- Both print the required value comparisons and execute the native tests. Skill
  uses verbose unittest transcripts, baseline a compact TestResult summary with
  the actual failure messages. They cover the same requested cases, not every
  possible Decimal input or precision context. Additional presentation/history
  work and shared host/cache limit causal interpretation.
- All five original project files per arm are byte-identical to the frozen
  fixture, with no extra non-Git/non-skill files or bytecode retained. Installed
  skill manifests are unchanged. Commands show no project writes, external
  services, delegation or dependency installation. Final file identity alone is
  not proof that no transient writes ever occurred.

## Original evidence and author checks

| Evidence | No skill | Necromancer |
| --- | --- | --- |
| Answer | [answer](history-invoice-boundary--baseline--1/answer.md) | [answer](history-invoice-boundary--skill--1/answer.md) |
| CLI commands/output | [commands](history-invoice-boundary--baseline--1/commands.json) | [commands](history-invoice-boundary--skill--1/commands.json) |
| Stored original tool responses | [records](history-invoice-boundary--baseline--1/tool-records.json) | [records](history-invoice-boundary--skill--1/tool-records.json) |
| Author source/capture check | [integrity](history-invoice-boundary--baseline--1/author-integrity.json) | [integrity](history-invoice-boundary--skill--1/author-integrity.json) |

All six baseline and seven skill shell outputs and exit codes match their stored
original responses exactly after workspace-path normalization. Two skill outputs
are wrapped in `Promise.allSettled` fulfilled records; comparison unwraps those
records, without rerunning commands. No missing, unmatched or duplicate selected
tool call/output IDs. Full original rollouts remain local because they include
private context; only reviewed selected tool records are exported. These checks
do not prove universally complete model context or fix older capture gaps.

[Comparison arithmetic](comparison.json), [run manifest](run.json) and
[metadata summary](summary.json) retain the scheduled pair. The project exports
contain all five fixture source files but not executable Git history; regenerate
that from the frozen fixture for author reproduction. Export hashes identify
unredacted originals, so intentionally path-redacted exported bytes can differ.

Keep compact serialization as a lossless transport option, not a measured model
win. This screen adds adverse evidence rather than another instruction tweak.
The next efficiency investigation should involve materially repeated historical
collection in a less trivial repository, without requiring the optional helper
or recycling this exposed task for a favorable score. Featured charts unchanged.

## 한국어

새 과제에서 두 조건 모두 과거 도입 이유와 현재 필요성을 구분했고, 실제 호출
경로의 필수 9개 결과와 기존 테스트를 확인했다. 그러나 스킬은 토큰 3.64%·시간
10.94%가 더 들었다. 양쪽 모두 첫 `python` 명령이 실패한 뒤 `python3 -B`로
진행했으며 그 비용을 제외하지 않았다. 출력 크기를 줄인 이력 도우미는 사용되지
않았으므로 해당 변경의 모델 효과는 이번에도 미측정이다. 원본 파일·설치 자원은
보존됐고 원본 도구 응답과 CLI 출력 13개도 일치한다. 일반 성능 향상으로 채택하거나
그래프를 바꾸지 않으며, 불리한 결과도 그대로 남긴다.
