# Isolated scratch02: mounted-source adapter verification

2026-09-22, adapter `0858a26`. Completes the mounted-source follow-up to
[scratch02](SWE-LITE-SCRATCH-02.md); not a model measurement or skill change.
The old pilot01 scheduler, task permissions and results remain unchanged.

The existing source exporter reads the immutable pytest solver image, checks
the base tree `877d433795f3d7288b9edd5696724bb2d8e47f88`, one commit, no remotes,
clean source and generated version metadata. The existing `prepare_repository`
then creates a separate project copy, mounted at `/testbed` by the actual
`container_launcher` and `execute` implementation with `isolated-v2` selected.

Use the dedicated `colima-qh-bench` context, network none, 2CPU/6GiB, 120-second
inner limit, 150-second outer limit. No model API, issue patch, hidden test or
gold solution is used. A literal `{}` dummy auth file exercises the ordinary
mount/copy path; no real account credentials are supplied. The launcher command
is replaced with an author Python probe before execution, not sent to Codex.

## Observed controls

- Fresh-process public pytest import comes from `/testbed/src/pytest/__init__.py`.
- Actual `TemporaryDirectory` is under `/qh-scratch`; no project scratch
  `pytest.ini` exists. Required generated `_version.py` is present.
- All194 outer collected items bind to the three expected test modules and the
  actual imported pytest package in the same process.
- Unchanged native `test_skipping.py`, `test_unittest.py`, `test_runner.py`:
  **184 passed, 9 skipped, 1 xfailed**; native exit0.
- A separate deliberately false assertion under `/qh-scratch` exits1, reports
  `AssertionError`, and preserves `observed-sentinel` / `expected-sentinel`.
  This is a failure-output control, not a new scored obligation or model result.
- Tracked source diff remains empty; separately reviewed `git status --porcelain`
  is empty. Container exit0, no OOM/timeout, lifecycle `removed=true`; subsequent
  Docker listing finds no matching container. The dummy auth file is removed.

[Evidence](results/swe-lite-scratch-adapter-02/) preserves the executed driver,
summary, implementation hashes and full stdout. Original stderr is empty (its
SHA256 is recorded). The driver was executed from `benchmarks/local-runs/`;
the result copy is a record, not a relocatable entrypoint. Native-test seconds
are not model efficiency measurements. No resource-saving percentage or featured
chart update follows from this validation.

The new scratch option is now verified through the mounted-source adapter for
this pytest base. It does not prove every project/environment, model behavior,
interruption path or independent holdout performance. Any future model task
using it must authorize `/qh-scratch` explicitly. Do not rerun the already
exposed pilot pair and describe it as fresh independent evidence.

한국어: 새 옵션을 실제 실행기와 프로젝트 복사·마운트 경로에서 검증했다.
테스트194개의 소스 연결을 확인했고,184개 통과·9개 건너뛰기·예상 실패1개였다.
의도적 실패도 올바르게 보고됐고 원본 변경 없이 컨테이너·가짜 인증 파일을 정리했다.
모델 호출이나 스킬 성능 개선 측정은 아니며, 기존 결과와 그래프는 변경하지 않는다.
