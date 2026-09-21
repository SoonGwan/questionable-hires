# Preserve initial index evidence before model execution

2026-09-21, parent `1cb7a25`. Measurement correction, not skill/model performance.

The [specifier review](PACKAGING-SPECIFIER-01-REVIEW.md) could verify native tests
and final source preservation, but not independently compare initial versus final
Git index bytes. The existing collector retained only the index after model work,
before its own `git add -N`. A model's later inventory cannot fill that earlier
gap, particularly when it runs `git status` before taking its own snapshot.

The runner now captures `git-index.before-model.bin` and its JSON identity after
workspace/resources are prepared and before starting the model process/timer.
It retains the existing separate before-collector capture. Metadata exposes both
identities and a comparison of byte digest, length and mode. An unavailable
capture gives `status:unknown` and a null comparison, not a preservation pass.
Both raw records remain available even if later collector Git commands fail.
Raw binary indices remain local; the exporter publishes identities, not binary
index contents. No task prompt or instruction is added to the evaluated model.

Reuse the existing bounded20MB, regular-file, no-follow local-index reader.
Unsupported Git layouts, symbolic links, oversized/growing files and unavailable
reads are reported, not redirected to an external Git directory. Capture is
outside process timing and adds no model call. It is not an atomic filesystem
snapshot, transient-change detector, semantic staged-content comparison or proof
that all Git metadata is unchanged. A routine index refresh can change bytes
without changing staged content; the comparison does not automatically score a
scope violation.

## Author checks

Actual local Python child processes replace the Codex invocation in controls;
no model sessions are launched. Checks cover staged source/index changes, an
unchanged index, unknown capture, a corrupt index surviving later collector
failure, growth/size/link/layout boundaries, raw-byte export exclusion and original
stream preservation. The changed-index control distinguishes the child index
from the collector's subsequent `git add -N` mutation.

The complete focused `test_benchmark*.py` suite passes43/43 on macOS Python3.9.6
in4.016s. A fresh `git archive 6db0788`, without repository history or local-run
artifacts, passes the same43/43 with no skips in3.899s. Expected invalid-input
diagnostics and synthetic cell logs are test controls, not model calls. Repository,
featured-sync and whitespace checks pass; this is not a new full-platform matrix.
These controls
do not turn historical unknown index identity into an observed pass. All prior
model measurements and featured charts remain unchanged.

한국어: 모델 실행 전에 Git 인덱스를 따로 보존해 실행 후 기록과 비교하도록
측정기를 보완했다. 수집할 수 없으면 미확인으로 남기고, 바이트 차이를 곧바로
범위 위반으로 판정하지 않는다. 기존 결과의 미확인 부분을 소급해 통과로 바꾸거나
스킬 성능 개선 수치로 주장하지 않는다.
