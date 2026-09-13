# Atomic export: correct core behavior, qualified lower cost

Hostage's known-path candidate records **12.85% fewer tokens / 8.43% less time**
in one authored atomic-export task. Both arms implement streaming replacement,
demonstrate the original defect, and pass their unchanged regression afterward.
Preparation takes two shell calls in **both** arms; this is not evidence that
the new wording reduced discovery relative to baseline.

한국어 요약: 이번 한 작업에서는 스킬의 토큰이 12.85%, 시간이 8.43% 적었다.
양쪽 모두 실제 수정 전 실패와 수정 후 통과를 확인했다. 그러나 준비 호출은
둘 다 2회였고, baseline의 macOS 임시 파일 정리와 스킬의 추가 예외 검증 등
작업 차이가 있다. 탐색 문구의 효과나 전체 스킬의 성능 향상으로 확정하지 않는다.

## Frozen execution

[Protocol](../../HOSTAGE-ATOMIC-EXPORT-01-PROTOCOL.md), [manifest](run.json).
Runner/fixture `ee77e2f`, Hostage entrypoint `5867752`. Task SHA-256
`c1057149df91fff55beeb9d8a108834f3c9a2f56c3d3b809e35efe76a385c3e2`.
GPT-6 Astra medium; baseline then skill, one fresh session per arm, serial,
240-second deadline. Both complete, no retries, exclusions or changed inputs.
No author test suite runs during model timing.

| Arm | Input + output | Cached input | Seconds | Shell calls |
| --- | ---: | ---: | ---: | ---: |
| [baseline](atomic-report-export--baseline--1/answer.md) | 101,354 | 92,800 | 55.809 | 7 |
| [skill](atomic-report-export--skill--1/answer.md) | 88,329 | 78,464 | 51.103 | 4 |

Ratios minus one: −12.8510% tokens / −8.4323% time. Cached input is already
included in input; reasoning output is not added again. Shared host/cache,
order, n=1, authored scope and workload differences prevent causal attribution
or broad/equal-work performance acceptance. No featured graph changes.

## Actual behavior

Both first inventory paths, then read root/nested instructions, requirements,
exporter and existing tests together. Skill reads its entrypoint within the first
call. Neither issues a second filename inventory after the direct content read.
This shows the desired skill behavior, but baseline already does it too.

Both add one regression method before changing production. Baseline tests existing
and absent destinations with RuntimeError: the captured before run has two actual
assertion failures. Skill tests both destinations with RuntimeError and
KeyboardInterrupt: four failing subtests. Outputs contain wrong bytes or wrong
existence, not dependency/support errors. Both tests check exact exception identity
and directory entries. Existing Unicode/count and empty-output methods remain
AST-identical to the fixture. Only production changes follow the before run;
no later test edit is observed in file-change events or commands.

Both stream rows to a temporary file in the destination directory, close it,
replace the destination only on success, and remove temporary output in finally.
No complete iterator buffering, signature change or unrelated production change
is introduced. Captured after runs pass all three test methods, including subtests.
Both keep production edits within `apps/reports/exporter.py` and add coverage in
`tests/test_export.py`; all five other fixture files remain byte-identical.

Baseline switches its after run to `TMPDIR="$PWD"`, receives Xcode launcher
warnings, discovers a generated `xcrun_db`, removes it, and checks status again.
Those extra commands and their costs stay included. Skill batches after tests,
whitespace check and focused diff with semicolons; shell exit alone cannot certify
earlier checks, but the original output includes the passing unittest summary and
no whitespace diagnostic. Baseline also uses semicolon-separated final checks.

**Fixture scope limitation:** supplied tests use `TemporaryDirectory()` without
an explicit project-local directory. Both before runs, and skill's after run,
therefore use system temporary locations; baseline's after run instead redirects
TMPDIR. The fixture/runner did not enforce a single temporary-root policy despite
the project-only work wording. Do not call this strict project-only scope success
or silently attribute the difference to either agent. No external-service call,
dependency install or out-of-project source discovery is observed. Future task
versions need an explicit test-temporary-root contract; these frozen inputs and
costs are not repaired or rescored.

Installed resource inventories remain unchanged. Capture diagnostics flag only
baseline's successful empty-output `rm xcrun_db` command; this is legitimate
silence, not missing assertion output. No invalid JSON, rejected-patch or error
event flags appear. Diagnostics do not guarantee every original byte was captured.

## Separate author confirmation and next decision

After timing, each final project is copied to a disposable directory. The same
two preregistered hidden contract tests are added without altering model tests,
and the existing interpreter runs unittest with project-local TMPDIR. Both have
five passing methods (model suite plus author checks). This is author replay,
not original model execution or a correction to frozen timing/scope evidence.
Implementation inspection separately confirms streaming rather than buffering.

Exports retain both projects, original commands/events, outputs, answers, changes,
metadata and original artifact hashes. Private temporary paths are redacted;
hashes identify original artifacts, not redacted bytes. Original logs remain in
ignored `benchmarks/local-runs/hostage-atomic-export-01`.

The candidate did useful scoped work, but the experiment cannot establish a
discovery improvement over baseline. Do not keep tuning the same paragraph or
repeat this task for a better score. Resolve temporary-root control in future
fixtures and use independent work for the still-missing all-eight confirmation.
