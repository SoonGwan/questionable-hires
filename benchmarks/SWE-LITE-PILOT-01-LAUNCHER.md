# SWE-Lite pilot01: model execution boundary

2026-09-22; adapter/tests `6a9fd17`, following [runtime preparation](SWE-LITE-PILOT-01-SOLVER-RUNTIME.md).
**Two neutral infrastructure model sessions, zero selected external-issue model
attempts. No skill gain or benchmark promotion.**

## Implemented and checked

[Adapter](swe_lite_container.py) plugs into the existing `run.run_cell` callback.
It uses immutable image IDs, explicit Docker context, bounded resources, a
per-cell project mount and a separate fresh session directory. Authentication is
mounted read-only then copied to container tmpfs; it is not in the image or
persisted session directory. Model processes in this container can technically
read their runtime credential: this is not credential isolation from the model.
No Docker socket or whole host home/repository mount is supplied to the solver.

Sessions are retained for initial-context/tool/usage review. The adapter adapts
the host workspace path to `/testbed` and uses container-level isolation in place
of the nested CLI sandbox. This follows the controlled-container use described
by [official Codex non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode),
checked against CLI0.153.4. The wrapper stops/removes only its uniquely named,
ownership-labelled container. A Docker daemon error is not treated as proof of
removal; unknown cleanup state is retained as unknown/error. SIGKILL of the outer
wrapper is not covered by the SIGTERM control and still requires external review.

Six adapter tests and four context-builder tests pass in the checkout and a fresh
source-only copy,10/10 in each. Native lifecycle controls use dummy `{}` auth,
not an API account. They verify project import/generated pytest metadata, source
write, synthetic session persistence and exits0/1/124/143 for normal execution,
deliberate assertion failure, timeout and SIGTERM. Every final control removes
its container. The assertion contains actual/expected `(6, 7)`, not setup failure.

All author attempts remain in [retained artifacts](results/swe-lite-pilot-01-launcher):
control01 passed; control02 exposed a cleanup-parser defect (Docker emits
lowercase `error: no such object`), although authoritative listing found no
remaining owned container. Control03 passed after the parser fix. These early
controls were run while the adapter was uncommitted and evolving; do not claim
the initial two used the final adapter bytes. Neutral model02 records exact
runner/adapter SHA256 values in its protocol. Initial model01 predates that
fingerprint capture; retain this provenance limitation.

## Real model connectivity: failure retained, then environment repair

Both fresh sessions use GPT-6 Astra/medium, CLI0.153.4, the same neutral prompt,
one synthetic README and no installed project skills. They only request Python
version/cwd, writing `observed.txt` and reading its exact content back. No selected
SWE issue body, gold patch, hidden test or source is supplied through that project
mount. They are not scored development tasks or a before/after skill comparison.

| Neutral attempt | Actual task result | Resource / lifecycle evidence |
| --- | --- | --- |
|01 | File absent; three recorded code-mode calls return SIGKILL. CLI itself reports completed/exit0. | Default Colima≈2GiB; container2GiB; Docker `OOMKilled=true`; removed. |
|02 | Python3.9.20/cwd confirmed; exact file written and read back by recorded tools. | Separate Colima8GiB; container6GiB; `OOMKilled=false`; removed; one matching session retained. |

This is why CLI exit0/turn completion alone is not a task-success verdict.
Attempt01 input47520/output271,26.217s; attempt02 input35634/output169,29.565s.
These are whole runner wall times including container lifecycle; cache and task
execution differ, so **no efficiency improvement is inferred**. Usage profiles
reconcile retained session counters with CLI totals. Exact-body exposure checks
find no full body of our eight skills; that is not proof of all context absence.
Full private rollouts remain local; exports contain reviewed tool records,
sanitized CLI events, source hashes and aggregate exposure/usage evidence only.

## Separate VM, unchanged unrelated service

The host has64GiB memory. Created `qh-bench` with2CPU/8GiB,40GiB data disk,
VZ/Rosetta and only this workspace host mount. `--activate=false` preserved the
existing default Docker context. Existing `moneyradar-mysql` remained healthy
without restart; the original2GiB Colima was not reconfigured.

Transferred the two exact local solver images and HTTP service image to
`colima-qh-bench`; no image rebuild or registry publication. Solver02 confirms
the pytest image ID from the runtime report. A private temporary auth copy under
local-runs made the existing credential available through the narrow VM mount;
that copy was removed after the probe, and the original credential was untouched.
At handoff the dedicated VM is running with no containers; default MySQL remains
running. These are local environment changes, not public deployment.

## Remaining before external comparison

Verify Requests' combined service/network path in the dedicated VM and validate
the exact per-cell source exports, including ignored generated pytest metadata.
Then freeze the two-task/four-cell schedule, skill resource, limits, task prompts,
scoring inputs and network policy before running any selected issue. A bridge
network is needed for this API path and permits more than API traffic; disabled
web search/project-only instructions are **not enforced outbound filtering**.
Retain and review tool traces for lookup/scope violations. Do not silently call
these public issues uncontaminated or reuse author-investigated outcomes as blind
evidence. Broad20–30% skill gains and release readiness remain unproven.

한국어: 실제 모델의 도구 실행이2GB 환경에서 OOM으로 실패한 기록을 보존했다.
다른 프로젝트를 중단하지 않고 전용8GB VM을 만든 뒤 같은 중립 작업에서 파일
작성·읽기가 성공했다. 실행기 점검이며 외부 문제 해결이나 스킬 성능 비교 결과가
아니다. 실패 기록, 비용, 접근 제한의 한계는 모두 유지한다.
