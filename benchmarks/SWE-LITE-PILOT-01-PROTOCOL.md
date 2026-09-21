# SWE-Lite pilot01: execution protocol

Frozen before any selected-issue model attempt,2026-09-22. Selection follows
[the predeclared external-issue rule](SWE-LITE-PILOT-01-SELECTION.md).
Neutral infrastructure calls are separately retained in the
[launcher report](SWE-LITE-PILOT-01-LAUNCHER.md); they are not task results.

## Fixed schedule and resources

1. `psf__requests-2317`, baseline.
2. `psf__requests-2317`, current auto-discoverable bundle.
3. `pytest-dev__pytest-7432`, current auto-discoverable bundle.
4. `pytest-dev__pytest-7432`, baseline.

One repeat, serial execution. Baseline has no project skills. Current copies all
eight skills and supporting files from Git revision **`8ee6c56`** into
`.agents/skills`; no forced role/helper invocation. This is unchanged skill code
from before inspecting the selected issue solutions, not a pilot-specific rewrite.
Record full commit/resource hashes before execution; later documentation commits
do not implicitly change the measured skill revision.

Model **`gpt-6-astra`**, reasoning **medium**, CLI **0.153.4**. No model fallback,
session continuation, adaptive time increase or favorable replacement. Each cell
has a fresh project, Git database copy and fresh persistent session directory.
Maximum **360seconds inside the container**, **380seconds outer runner**;
2CPU/6GiB/256PID per solver, dedicated Colima8GiB/2CPU, Linux/amd64 compatibility
mode. Timed wall cost includes Docker startup/cleanup and inference/tool use;
source/resource staging and author grading are outside it. Never run competing
validation workloads during timed model execution.

Use exact solver image IDs in [runtime preparation](SWE-LITE-PILOT-01-SOLVER-RUNTIME.md).
Keep original source trees, one fresh base commit/no upstream remote/history,
installed dependencies and required generated pytest metadata. The model runs
native Python in `/testbed`, not through a host path-rewriting wrapper.

## Identical task contract

Read only `problem_statement` from the retained issue-only projected selection
record, SHA256`d906940879ab70be1d5b472b1a8610a1aaf199bd1298f0a3b8d705610d246b5a`.
Use the same issue text and instruction wrapper for both arms:

> Implement a fix for the reported issue in this checkout. Preserve existing
> behavior, add a focused regression test when needed, and run relevant native
> tests using the installed Python environment. Do not weaken or suppress
> existing tests. Do not install or change dependencies, retrieve upstream
> history/solutions, use internet resources, modify installed skills, or make
> commits or stage changes. Keep edits within the project; runtime-created temporary files under
> `.git/qh-tmp` are allowed. Do not deliberately change Git history or configuration. Report the
> changes, verification commands/results, and any remaining uncertainty.

Then give environment facts only: `python` is the prepared interpreter; Requests
tests use local HTTP/HTTPS endpoints via `HTTPBIN_URL` and normal certificate
verification. An empty pytest configuration at the project-local temp root keeps
nested pytest self-tests from inheriting parent project options. Do not supply
failure labels, gold/test patches, evaluation scripts, grader output, author
diagnosis or hints beyond the original issue itself. The shared runner appends
its existing project-only/no-delegation restrictions; baseline also disallows
other installed skills. Store exact resulting prompts before launch.

## Execution boundary and limitations

Use `colima-qh-bench`, never restart/reconfigure default Colima or unrelated
MySQL. Solver bridge networking supports the API; Requests additionally joins
the internal fixture subnet with explicit10.255.255.5, TLS service10.255.255.4,
gateway10.255.255.254 and timeout-test address10.255.255.1 unoccupied. Check
certificate validity and service readiness before starting timing. No grader
mount, Docker socket, whole host home or parent output directory is available.
Credentials are provided only for CLI authentication, are readable by container
processes, and must not be inspected by the solver or exported as evidence.

Disable CLI web search. This plus task instructions is **not network egress
enforcement**; inspect tool traces for lookup/access violations. Source history
stripping is not an exhaustive forensic audit of inherited image files/layers.
These public issues may be in training data. The author has investigated runtime
failures and applied reference patches in separate private graders; new solver
sessions receive none of that author context. Claim external authorship, not
proven uncontaminated/blind evaluation.

Retain original CLI streams, matching private sessions, pre-model/pre-collector
Git index captures, installed-resource manifests, patch/project snapshots and
container lifecycle state. Full initial instructions/credentials stay private;
publish only reviewed/redacted evidence and hashes. Freeze exact runner/source,
prompt, image and private grading-input hashes in the run manifest before cell1.

## Scoring and stop policy

Use the already reviewed pinned dataset test patch/eval script and official
parser extraction in a separate fresh grader after model timing. Preserve all
setup output privately; a shell exit0 is not a passing grade. Setup must succeed,
labels must be present, and native source bindings must be checked. Requests
requires141 labelled checks; pytest78. Requests' nominal8 fail-to-pass labels
include7 already passing in the corrected base runtime: only1 demonstrated
distinguishing failure, not8 bugs fixed. Do not change labels to improve results.

Review issue resolution, required regressions and scope separately from CLI
completion. Report resource modification, test weakening, external lookup or
unsupported success claims rather than hiding them behind native passes. Extra
focused regression tests are allowed; fewer changed lines is not inherently
better. Any author replay is labelled separately, never a substitute for the
original model evidence.

Stop on account limits or an infrastructure defect (OOM, unresolved cleanup,
missing required capture or changed frozen inputs). Preserve all scheduled and
attempted cells; mark unrun ones explicitly. A functional task failure without
infrastructure failure does not permit replacement. Timeouts retain cost and
partial artifacts; do not rerun a timed-out cell with a longer limit. An amended
future protocol cannot overwrite this run.

## Interpretation and iteration

Report exact token input/cache/output, total input+output, wall time, success,
scope, and observed skill exposure/adoption for every cell. No dollar estimate,
significance claim, confidence interval or general20–30% gain from two pairs.
Keep unsuccessful/incomplete work visible; do not advertise cost savings obtained
by doing less requested work. Summed costs and per-task ratios are descriptive.
Featured charts/README claims remain tied to their existing frozen result.

If this pilot reveals actionable waste or failures, improve the relevant skill
mechanism, not the expected answer. These issues then become development cases;
future validation needs separately selected unseen cases. Do not repeatedly tune
and rerun this pair until a favorable percentage appears.

한국어: 외부 과제2개를 순서를 뒤집어 총4회 실행한다. 스킬 리소스·모델·시간·환경은
실행 전에 고정하고, 실패/비용 증가/미실행 항목을 숨기지 않는다. 공개 이슈의 학습
오염 가능성과 비강제 네트워크 제한을 명시한다. 두 쌍만으로 전체20–30% 개선을
주장하지 않으며, 결과를 본 뒤 같은 문제를 독립 검증처럼 반복하지 않는다.
