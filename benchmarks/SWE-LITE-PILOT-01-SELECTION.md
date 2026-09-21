# External-issue pilot: selection before solution inspection

2026-09-21, parent `7f9786f`. This is preparation, not a launched model experiment
or a new skill-performance result. The current eight-role cost target is unmet.

Prior history/helper experiments repeatedly found non-adoption and mixed or
adverse costs. Another authored task tailored to a helper is not independent
evidence. This pilot instead asks whether the unchanged installed bundle helps
with externally authored bug reports, without telling the model which helper to
use or rewarding invocation. It will not establish all-eight skill superiority.

## Freeze selection before reading issue bodies or solutions

- Source: official `SWE-bench/SWE-bench_Lite`, test split, dataset revision
  `b0dde1093fe417d83b7184254edf8199c1f0dff5`,300 records.
- Two repositories: `psf/requests` and `pytest-dev/pytest`. Both are Python
  developer tooling/libraries, avoiding an initial compiled scientific-stack
  setup. This is a feasibility restriction, not a representative random sample.
- Select one instance per repository by smallest SHA-256 of UTF-8
  `questionable-hires:swe-lite-pilot-01:` followed by instance_id. Break ties by
  instance_id. No filtering by issue text, difficulty, expected skill match,
  gold patch size, tests or eventual result. Retain selected failures; do not
  replace an inconvenient selected instance with another task.
- Read rows only from a response whose `x-revision` matches the frozen revision.
  Record page-body hashes and row counts. Publish only selected identity,
  repository, base/environment commits, version, issue body and selection hash.
  Do not display/export solution patches, hints, test patches or test labels to
  the solving context. Public data may already be in model training; this is
  external authorship, **not proven uncontaminated holdout**.

## Gates before any model calls

First establish a reproducible native environment for both chosen instances and
record the runtime/image/harness identity, available architecture and applicable
licenses. This host is Linux aarch64 through Colima; image compatibility is not
assumed. No cloud submission, publication, billing change or unbounded image build.
Keep answer-bearing scoring artifacts outside model projects/contexts. Tests must
be genuinely runnable, not replaced by author approximations to get a green score.

Then freeze a separate execution protocol: two tasks, baseline versus unchanged
auto-discoverable eight-skill bundle, identical model/settings/project permissions,
reversed condition order across tasks, fresh projects and original session capture.
No forced skill use. Specify time/resource ceilings before execution; stop on
account limits and preserve every attempt. No model run is authorized by a missing
environment gate. The task set remains below the owner's ten-task ceiling.

Review issue resolution, native regressions, scope, skill exposure/adoption, total
tokens and time. Two pairs cannot show a reliable20–30% general gain. Improvements
may follow concrete failure mechanisms, but used cases become development cases;
do not repeatedly tune and report the same cases as fresh validation.

## Sources and limitations

[Official dataset structure](https://www.swebench.com/SWE-bench/guides/datasets/)
distinguishes problem statements from solution patches.
[Official evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/)
describes containerized native evaluation. We have not run that evaluation or
claimed leaderboard comparability. Frozen featured charts remain unchanged.

한국어: 도구에 맞춘 합성 과제 대신 외부 이슈2개를 정해 살펴보는 준비 단계다.
선택은 본문·정답·성공률이 아니라 고정된 저장소와 해시 순서로 결정한다. 공개
데이터의 학습 오염 가능성은 남으며, 실행 환경 검증 전 모델 호출은 하지 않는다.
