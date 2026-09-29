# Solver native controls01 — 2026-09-27

Parent `dc3f3b02`; native runner bootstrap for all8 fixed sources, models0,
selected issue tests0. It does not amend the original external grading contracts.

Reuse the [guest import runtime](SOLVER-ISSUE-IMPORTS-01.md),1.5GiB RAM, Rosetta-only
share, no host data directories/network/storage. Add only a two-test author fixture,
empty pytest configuration and the exact check scripts. Each project/mode uses a
fresh Python3.9.20 process with `-I -B`. Public project-module path is asserted;
Requests uses pytest7.4.4 from `/runtime/env`, while pytest issues use their actual
project-local pytest sources. Compatibility libraries remain scoped to legacy pytest.

[Fixture](results/solver-native-controls-01/test_control.py) has a normal7==7
assertion and a deliberate `observed != expected` failure. Each native process
selects one method. The author collector requires native exit0/one passed call for
the normal case, or native exit1/one failed call containing the expected mismatch
evidence for the adversarial case. The collector exits0 for a valid controlled
failure without calling that failing test a passing test. It never imports an
answer-bearing grading tree or selected regression.

Use an explicit empty configuration and controlled `--confcutdir`, plain assertions,
disabled plugin autoload and cache provider. This verifies native runner/fixture
execution; it deliberately does **not** verify each project's configuration,
conftest dependencies, selected test collection or HTTP/TLS service behavior.

The [initial complete16-cell attempt](results/solver-native-controls-01/result.json)
is **16 INVALID**: every pytest start fails before the assertion because the
minimal guest lacks `/dev/null`. Original complete guest output and Swift source
remain unchanged. VM/controller0 means the collection ended, not any valid check.

The separate second Swift configuration mounts guest-only `devtmpfs` on `/dev`
and checks `/dev/null` is a character device before launching the same checks.
It changes no fixture, package, source, native command or initramfs. This exposes
only devices configured for this VM, not a host disk or arbitrary host path.
[Second complete16-cell result](results/solver-native-controls-01/devtmpfs-result.json)
is **16 VALID**, all8 normal checks and all8 deliberate failures correctly detected,
guest stopped, executable0, no timeout. The [native output](results/solver-native-controls-01/devtmpfs-guest.txt)
retains actual pytest paths/versions, exit values, call records and mismatch text.
Both related attempts are retained; no independent validation or model savings
are inferred from bootstrap correction. Elapsed16.412s is only author runtime time.

Exact runner/check sources, Swift configurations, input hashes and complete outputs
remain in `results/solver-native-controls-01/`. Both VMs have45-second internal
deadline and55-second parent wait followed by a bounded kill if needed. Cpio is
bounded30 seconds; compilation/signing/compression are not independently bounded
and completed. Both VM processes are terminal. No persistent guest root disk or
host source mount exists. No post-test guest file/mode inventory is claimed.

Next verify child-process/tool execution inside the guest and isolated output
delivery, then actual frozen native issue grading and role-appropriate model
comparisons. Existing full-cohort gold/reporting/runtime limits remain unresolved.
These controls neither establish native issue readiness nor improve ordinary
skills. README/featured/site efficiency claims stay unchanged; all8 quality and
joint whole-task token/time goals remain unmet.

한국어: 실제 게스트의 8개 실행 경로에서 정상 assertion과 의도한 실패를 각각
검사했다. 최초16개는 `/dev/null` 누락으로 assertion 전에 실패했고 이를 보존했다.
게스트 내부 devtmpfs 추가 후16개 모두 정상 통과/실패를 올바르게 판정했다.
테스트 실패 종료1을 통과로 세지 않는다. 이슈 회귀 검사·모델 연결·전체 효율
비교는 미실행이며 전체8개 품질·토큰·속도 목표는 아직 미달이다.
