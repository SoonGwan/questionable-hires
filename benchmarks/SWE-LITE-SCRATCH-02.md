# Isolated scratch02: remove the native pytest root-discovery confound

2026-09-22; parent `551dce3`. Author environment replay, **not a model run or
skill-performance improvement**. The four completed pilot01 sessions, their
frozen fixture and all chart values remain unchanged.

## Reproduction and alternative

Use immutable pytest solver image
`sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923`
in `colima-qh-bench`: linux/amd64 compatibility, network none, 2CPU/6GiB,
256PID, all capabilities dropped, no-new-privileges. No credentials, skill
bundle, model patches, hidden tests or gold solution were supplied. Source is
the image's original base checkout, not either model's completed project.

Both author commands first import pytest in a fresh process and print its path
(`/testbed/src/pytest/__init__.py`) plus an actual `tempfile.mkdtemp()` path.
Both then execute the same unchanged native command:

```sh
python -m pytest testing/test_skipping.py testing/test_unittest.py testing/test_runner.py --basetemp=SCRATCH/native -q --tb=short
```

Shared environment: `PYTHONPATH=/testbed/src`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. `TMPDIR` is SCRATCH.

| Scratch setup | Exit | Native outcomes |
| --- | ---: | --- |
| `/qh-scratch`, separate tmpfs, no ancestor project config | 0 | 184 passed, 9 skipped, 1 xfailed |
| `/testbed/.git/qh-tmp`, existing empty `[pytest]` config | 1 | 181 passed, 3 failed, 9 skipped, 1 xfailed |

The isolated run occurred first. The first legacy launch failed before Python
with Docker exit125: its requested bind source in the old model workspace no
longer existed. No tests ran in that launch. The retained final-environment02
`pytest.ini` supplied the same nine-byte `[pytest]\n` configuration in a second,
separately named legacy container. The bind is read-only. Both completed native
outputs are retained in [results](results/swe-lite-scratch-02/); progress output
chunks are concatenated. These are native author timings, not efficiency claims.

Legacy failures show rootdir `/testbed/.git/qh-tmp` and unwanted `native/...`
prefixes in node IDs/locations: `test_logstart_logfinish_hooks`,
`test_collect_result`, `test_current_test_env_var`. Actual and expected values
are visible, confirming assertion failures rather than setup exceptions.
Removing the ancestor config by using separate scratch restores these three
unchanged tests without suppressing them or modifying application code.

## Explicit new option, not silent migration

The container adapter accepts `scratch_mode='isolated-v2'` (CLI
`--scratch-mode isolated-v2`). It mounts container-private tmpfs `/qh-scratch`,
sets TMPDIR there and records the mode/path in lifecycle evidence. It creates
no project `pytest.ini`. The default remains `project-config-v1`, preserving
pilot01's configuration and disclosed limitations. The pilot01 scheduler has
**not** been switched to the new mode.

Future task instructions must explicitly authorize `/qh-scratch` as disposable
scratch in addition to `/testbed`; this is not a project-only execution claim.
Temporary data vanishes with the container. The adapter does not enforce the
model's entire filesystem scope or automatically rewrite task instructions.
Future tests must also check the exact mounted-source/model execution path,
native source bindings, failure controls and cleanup before freezing a protocol.
This replay verifies the image-native tests, not a complete future launch.

Validation: 23 SWE-Lite adapter/environment/runtime/scheduler checks pass in the
checkout and a fresh source archive with the changed files overlaid. New checks
cover explicit mode routing, no project configuration, Docker tmpfs/TMPDIR and
lifecycle recording/cleanup with mocked Docker. The native replay above uses
real Docker with equivalent scratch arguments; it does not invoke the adapter
or a model. All three named replay containers are absent after execution.

한국어: 기존 임시 설정 때문에 생긴 경로 오류 3개를 원본 테스트로 재현했다.
별도 임시 공간에서는 테스트를 바꾸지 않고 184개가 통과했다. 새 옵션을 추가했지만
기존 벤치마크는 변경하지 않았다. 다음 과제에는 임시 공간 허용 범위를 명시해야
하며, 실제 모델 실행 경로의 검증도 남아 있다. 스킬 성능 향상 수치는 아니다.
