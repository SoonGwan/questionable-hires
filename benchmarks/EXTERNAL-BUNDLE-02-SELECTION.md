# External bundle02 — selection policy, 2026-09-27

Parent `7172b50c`; candidate skills from that revision. Preparation only, no model
result or whole-team acceptance. Earlier [SWE-Lite pilot01](SWE-LITE-PILOT-01-REVIEW.md)
and repeatedly exposed authored-role costs remain historical; do not rerun them
until favorable or relabel local memory checks as model efficiency.

Freeze this policy before new issue bodies/solutions are inspected:

- Official SWE-bench/SWE-bench_Lite, test split, dataset revision
  b0dde1093fe417d83b7184254edf8199c1f0dff5, expected300 unique records.
- Eligible repositories psf/requests and pytest-dev/pytest. Select4 per repository
  by ascending SHA256 of UTF-8 questionable-hires:external-bundle-02: plus
  instance_id; break ties by instance_id. No issue-text, difficulty, tests,
  patch size, version or eventual-result filtering.
- Exclude psf__requests-2317 and pytest-dev__pytest-7432, already exposed in pilot01.
  Prior benchmark Markdown identity search found only these two IDs.
- Require returned dataset revision to match; retain source-response hashes/counts.
  Do not silently substitute current data, another split or selected cases when
  retrieval/environment fails. Eight tasks remain below the prior ten-task ceiling.
- Loader projects only instance_id/repo/base_commit/environment_setup_commit/version
  and problem_statement, after ID selection. Never print/save solution or test
  patches, hints or grading labels into the solving context. Raw answer-bearing
  responses remain transient; record hashes rather than publishing them.

This feasibility-limited sample is externally authored, not guaranteed independent
of training or representative of all developer work. Auto-discoverable all8 bundle
on bug fixes does not prove each role's quality. Full objective still requires
role-specific quality plus lower whole tokens and faster completion; do not replace
that scope with aggregate bug-fix success.

Before any model execution, establish actual native public-entry imports, generated
metadata, correct/assertion-fail native controls, required tests, ownership/temp
bounds and reproducible runtime identities for every selected issue. Use existing
runtime tooling/caches; no account/global/dependency changes. Missing environments
are unresolved, not passing checks. Do not launch on catalog acceptance alone.

Then separately freeze execution protocol, current/predecessor/baseline comparison
scope, fixed model/effort/resources, balanced order, fresh projects/contexts, n=1,
serial resource ceilings, no retries/replacements, every original attempt/counter
and private versus exported evidence. Keep answer-bearing grading outside model
contexts. Later native author grading is separate from original model work. No
featured/production/configuration changes or model calls are authorized by this
preparation document alone.

[Official dataset guide](https://www.swebench.com/SWE-bench/guides/datasets/)
separates issue statements from gold/test patches; public issues may be in training.
The pinned test split, not the guide's all-split size, defines this selection.

한국어: external-bundle02(2026-09-27,스킬`7172b50c`)는 외부 이슈8개를 본문·정답
검토 전에 고정 해시 순서로 선택하는 준비다. 이전2개 이슈를 제외하고 실패나 환경
문제로 대체하지 않는다. 실제 실행 환경·정상/실패 native 검사·고정 실행 규약을
확인하기 전 모델 호출을 하지 않는다. 외부 이슈의 학습 노출과 표본 제한은 남고,
자동 선택 번들 검사는 각 역할의 개선이나 전체 토큰·시간 절감을 대신하지 않는다.
