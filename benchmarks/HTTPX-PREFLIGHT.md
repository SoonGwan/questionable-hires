# Real-repository preflight: HTTPX 0.28.1

Selected before any task model runs: [encode/httpx](https://github.com/encode/httpx), tag `0.28.1`, commit `26d48e0634e6ee9cdc0533996db289ce4b430177`. Selection rationale: maintained real client code with in-process WSGI/ASGI tests, allowing offline behavioral checks without a deployed service. This is one author-selected project, not a representative sample or an endorsement by HTTPX maintainers.

## Verified environment

An isolated checkout and virtual environment were created on September 11, 2026. Python 3.9.6 on macOS. Import inspection confirmed `httpx.__file__` points to the checkout's `httpx/__init__.py`, not the installed wheel. Upstream working tree remained clean after the checks.

```sh
git clone --depth 1 --branch 0.28.1 https://github.com/encode/httpx.git httpx
python3 -m venv venv
venv/bin/python -m pip install -r httpx-preflight-requirements.txt
cd httpx
../venv/bin/python -m pytest -q tests/test_wsgi.py tests/test_asgi.py
```

Copy the adjacent requirements file into the parent directory before using these illustrative commands. Confirm the checked-out full commit; tags alone are not immutable identity.

Initial setup omitted optional Brotli/Zstandard decoders: **34 passed, 2 failed**, both `test_asgi_headers` variants expecting compression support. Adding the required extras yielded **36 passed in 0.06s**. This is environment preflight, not model evaluation; no failed model cells were rerun or discarded. The pinned environment below records the successful dependency set, not a promise of cross-platform wheels.

## Candidate evaluation scope

Next protocol should freeze neutral requests for test-sensitivity audits of WSGI response-stream cleanup and ASGI response behavior. Use unmodified upstream tests as baseline, isolated controlled faults, and independent outcome checks. Whether a fault survives is not known from this preflight; the expected answer must allow existing coverage to be adequate. Do not claim an upstream defect merely because a deliberate mutation survives.

Compare no-skill, generic control, and Con Artist with equal environment and task information. Preserve complete repository context, not a few copied functions presented as real-repository evaluation. Keep mutation oracles and expected findings outside evaluated contexts; report model familiarity with this public version as an unavoidable limitation. Freeze the final requests, scoring, resource limits, and run order before starting those sessions.

No upstream issues, PRs, deployments, or external messages are authorized by this experiment. HTTPX is BSD-3-Clause; retain its license and notices with any redistributed source artifacts. The repository stays outside our source tree for preflight; do not accidentally relicense third-party snapshots under our MIT license.

## Independent behavioral oracle, after task freeze

After committing the [task protocol](PLAN-HTTPX.md), `httpx_oracle.py` tested three faults in separate disposable full-source copies. The original checkout stayed unchanged. Each additional witness passed on correct code and failed with the intended assertion on its faulty copy, with import-path checks confirming the copied source was exercised.

| Targeted fault | Existing suite on correct / faulty code | Independent witness |
| --- | --- | --- |
| Omit WSGI iterable close | 12 pass / 2 fail, 10 pass | Actual client response no longer calls application iterable close |
| Append ASGI HEAD body | 24 pass / 24 pass | GET retains payload in both; HEAD exposes payload only in faulty code |
| Swallow default ASGI app exception | 24 pass / 4 fail, 20 pass | Caller no longer receives application RuntimeError |

WSGI protection comes through `wsgiref.validate` iterator finalization and pytest's unraisable-exception warning policy, not an explicit close assertion. That mechanism is part of the tested environment and may be runtime-sensitive. Preserve it when assessing whether a model accurately explains the result.

These are deliberate local mutations, **not evidence that HTTPX currently ships these defects**. The HEAD observation establishes a targeted coverage gap at this pinned revision; it does not measure the overall quality of HTTPX's test suite. Oracle source and results must not be included in evaluated projects. Original logs remain in ignored local run storage.
