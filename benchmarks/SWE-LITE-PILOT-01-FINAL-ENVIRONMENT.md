# SWE-Lite pilot01: exact source-copy/native execution path

2026-09-22, implementation `54e3b2c`, parent `8ee6c56`. No selected-issue model
attempts. Continues [launcher verification](SWE-LITE-PILOT-01-LAUNCHER.md).

Exported each immutable solver image's `/testbed` to a new host directory, checked
the exact base tree/one commit/no remotes/clean tracked source, then copied it
through the existing `run.prepare_repository` path used by model cells. The
pytest ignored/generated `_version.py` is retained. Actual native imports and
test-module bindings are verified in the mounted `/testbed` copy, not merely in
the unmounted original image. No scoring artifacts are copied into these sources.

Recreated the same internal HTTP/TLS fixture in `colima-qh-bench`, with fixed
addresses, aliases and certificate validity check. Only the server key is copied
into the isolated service, mode0600/root-owned; no CA signing key/host mount or
published port. Offline Requests attaches directly to the internal network, since
Docker's special `none` network cannot be combined with another network. API-mode
Requests uses bridge plus the internal network. Both paths pass HTTP, verified
HTTPS and wrong-hostname rejection with the actual project Requests import.

## Project-local temporary files: retained failure and repair

The launcher supplies `TMPDIR=/testbed/.git/qh-tmp` so native tests do not rely on
system temporary directories outside the project. A direct TemporaryDirectory
probe verifies that path. This initially changed pytest self-test behavior:
nested test projects inherited `/testbed/pyproject.toml` options/warning filters,
producing7 failures/70 passes. Requests passed both network paths in that attempt.

Added an empty `[pytest]` configuration at the runner-owned temporary root, before
model timing/index capture. This restores a configuration boundary analogous to
the original system-temp placement, without changing original tests, assertions
or application code. Both attempts and their exact control source remain in the
[evidence directory](results/swe-lite-pilot-01-final-environment).

Final attempt02, mounted source copy,2CPU/6GiB/256PID:

| Project / network | Original native tests | Other controls |
| --- | --- | --- |
| Requests / internal only |142pass,2warnings,3.44s | HTTP/TLS/hostname, project temp, all142 source bindings |
| Requests / bridge+internal |142pass,2warnings,3.42s | Same controls |
| pytest / bridge |77pass,3.29s | Generated metadata, project temp, all77 source bindings |

These are author probes, not solver efficiency timings. Tracked source diffs
remain empty; containers exit0, no OOM, exact owned containers removed. The
service is stopped after both attempts.15 adapter/environment/context tests pass
in the checkout and a fresh source-only copy, with no Git-history dependency.
No new model calls; neutral infrastructure sessions remain separate.

## Decision

The exact source-copy/native-test path is usable in the dedicated VM. Keep
the [four-cell protocol](SWE-LITE-PILOT-01-PROTOCOL.md) fixed before launch, then
record exact runner, prompts, source and scoring-input hashes in an exclusive
run manifest. Baseline/current must share these runtime repairs. CLI completion
alone remains insufficient; review native grading, scope, actual skills/context,
and lifecycle/capture completeness separately. No featured metric changes.

한국어: 실제 모델 실행과 같은 소스 복사·마운트 경로에서 Requests142개/pytest77개가
통과했다. 임시 디렉터리 이동으로 생긴 pytest7개 실패도 보존했고, 테스트를 바꾸지
않고 상위 설정 상속을 차단해 복구했다. 아직 외부 과제 모델 비교나 성능 향상 결과는
아니며, 다음4회 실험은 두 조건에 같은 실행 환경을 사용한다.
