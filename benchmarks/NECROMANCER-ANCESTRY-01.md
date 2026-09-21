# Explicit-base history recipe — 2026-09-21

Parent: `31a68d5`. Narrow instruction correction, not a new performance result.

## Observed mechanism

[Slugify history](SLUGIFY-HISTORY-01.md) records both arms trying the invalid
`git log --all=false` before recovering. [urllib3 history](URLLIB3-HISTORY-01.md)
records the candidate combining `--all --ancestry-path HEAD..HEAD` and reading
non-ancestor history despite an explicit ancestor-only task. Neither result
proves the prior wording caused the mistake. Both remain unmodified and adverse
cost/scope outcomes remain part of the evidence.

The entrypoint now supplies `git log HEAD -- <path>` for current ancestry, with
an explicit requested-base substitution and optional pickaxe placement. The
existing conditional reference explains other-ref expansion, empty ranges and
why first-parent traversal is not equivalent. No executable, new helper,
mandatory additional call, reduced assertion coverage or blanket reading limit
is introduced. This follows skill-creator's preference for concrete, scoped
guidance over general instructions or accumulating another workflow.

## Local semantic control

`tests/test_history_ancestry_recipe.py` builds a real disposable Git DAG with a
merged behavior change, independent main-branch work and a later non-ancestor
commit reachable from another ref. It checks:

- explicit `HEAD` includes the merged change and excludes the later ref;
- pickaxe identifies the actual relevant merged change;
- `--all` admits the non-ancestor, while `HEAD..HEAD` alone yields no commits;
- `--all=false` fails and first-parent traversal omits the merged branch commit;
- an explicit older base still selects the same history after HEAD advances.

The fixture lives inside the repository, deletes only its owned temporary
directory, and requires no network or project-source execution. Git writes are
fixture construction/checkout, not edits to the surrounding repository.

```sh
python3 -B -m unittest discover -s tests -p test_history_ancestry_recipe.py -v
```

This regression fixture is author-created from known failure classes, not a
blind task. Path/pickaxe queries still filter changes; renamed paths and shallow
history still require appropriate interpretation. Passing commands does not
prove a model selects them or spends fewer tokens.

Validation: Python3.9 history suite50/50 (17.338s), Python3.11 new ancestry
control1/1 (0.486s), skill metadata, repository links, bilingual featured-sync
and whitespace checks pass. No full-suite or hosted-validation claim.

## Performance decision

Keep this as a scoped correctness correction pending model evidence, not an
efficiency promotion. Do not rerun the exposed slugify/urllib3 tasks for a better
number. A future comparison must freeze a different task with both merged
ancestors and unrelated refs, make the permitted base explicit, retain all arms
and judge actual queried history as well as the final answer. A non-history
control should catch unnecessary history work. No fresh model sessions were
launched here; existing cost profiles and featured/localized charts are unchanged.

한국어: 서로 다른 실험에서 나온 잘못된 옵션과 이력 범위 확장에 대해 정확한
명령 예시를 추가했다. 실제 병합 이력 대조로 명령 의미를 검증했으며, 모델의
채택·토큰 절감·속도 개선을 입증한 결과는 아니다.
