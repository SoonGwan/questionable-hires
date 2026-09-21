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

## Selection result after policy commit0378759

All300 unique identities were examined in three100-row responses, each with the
required revision header. Eligible counts: Requests6, pytest17. The fixed rule
selected these instances before their problem statements were inspected:

| Instance | Base commit | Version |
| --- | --- | --- |
| `psf__requests-2317` | `091991be0da19de9108dbe5e3752917fea3d7fdc` |2.4|
| `pytest-dev__pytest-7432` | `e6e300e729dd33956e5448d8be9a0b1540b4e53a` |5.4|

Requests environment setup commit equals its base; pytest environment setup is
`678c1a0745f1cf175c442c719906a1f13e496910`. Selection hashes respectively:
`241f2e547fb788d0ca42319f24c3bf7a211db0d5bd589aa8fe91beca43912de8` and
`1d432edde3043d7cca25c36a1a855ed159b547454cb721486278c57c0c571eba`.
Page-body SHA-256, offsets0/100/200:

```
570fce982377ed7dc237cb54536942d7489f510cc3228dc550bec7da3db38aff
b3686b4e5f54395616eacb7d4d62af0d13b530f20f2b35bca6b0e9ea4cb7a230
afc2c3547115cfcd926cbc085c43b7a530a54a6ffeb5287e40644c0625232254
```

Answer-bearing fields were received by the loader but neither printed nor saved;
the solving context has not inspected them. Selected issue text was inspected
only after selection. The projected record remains local pending redistribution
license review, SHA-256
`d906940879ab70be1d5b472b1a8610a1aaf199bd1298f0a3b8d705610d246b5a`.
No gold correctness check, native environment preflight, model call or scored
result has occurred. These older versions need environment feasibility checks;
current Python compatibility must not be assumed or repaired into a different task.

## Sources and limitations

[Official dataset structure](https://www.swebench.com/SWE-bench/guides/datasets/)
distinguishes problem statements from solution patches.
[Official evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/)
describes containerized native evaluation. We have not run that evaluation or
claimed leaderboard comparability. Frozen featured charts remain unchanged.

한국어: 도구에 맞춘 합성 과제 대신 외부 이슈2개를 정해 살펴보는 준비 단계다.
선택은 본문·정답·성공률이 아니라 고정된 저장소와 해시 순서로 결정한다. 공개
데이터의 학습 오염 가능성은 남으며, 실행 환경 검증 전 모델 호출은 하지 않는다.
