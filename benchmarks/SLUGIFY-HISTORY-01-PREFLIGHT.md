# Slugify history preparation — 2026-09-21

**Author checks only; no model sessions or efficiency result.** Necromancer
resource is unchanged at checkout `79fb2e2`. This prepares a different task on
the project used by [Slugify native01](SLUGIFY-NATIVE-01.md), not an independent
project or blind holdout. A model-visible task, criteria and schedule still need
to be frozen before a comparison.

## Source and scope

A separate full clone of [python-slugify v8.0.4](https://github.com/un33k/python-slugify/tree/f85f9488520148d5f6899b5639199882b605e30a)
is pinned at `f85f9488520148d5f6899b5639199882b605e30a`, with 283 reachable
commits. The previous shallow native-audit checkout is untouched. The source
remains MIT-licensed; its license is included in the existing
[native-audit source export](results/slugify-native-01/current/slugify-native-verified--skill--1/project/LICENSE).

The proposed review asks whether the two replacement passes in `slugify()` can
be deduplicated while preserving current behavior, and separately what local
history establishes. Author inspection found:

- The early pass was introduced by `646761e5b4c73b9be7285c60eab4e10c30fe32f4`,
  with replacement examples/tests.
- The late pass was introduced by its immediate child,
  `8aea5c49b960b66e5c81bf20f17ec23e41c8d157`. The message “clean up, up version”
  does not establish a specific design rationale.

Parent/child source and patches establish introduction separately from present
behavior. No historical native execution or first-hand author intent is claimed.
In particular, the late-pass example below is a current compatibility observation,
not proof of a documented case-insensitive replacement contract.

## Native controls

[Script](preflight_slugify_history_01.py) and
[retained observations](results/slugify-history-01-preflight.json) record nine
native unittest processes in disposable project-local copies. Python3.11 uses
the existing text-unidecode1.3 environment. The tests are author-written probes,
not unchanged upstream tests.

| Source variant | `10 \| 20 %`, symbol replacements | `FOO`, `foo`→`bar` replacement | Plain Text |
| --- | --- | --- | --- |
| Current | `10-or-20-percent` | `bar` | `plain-text` |
| Remove early pass only | `10-20` (assertion failure) | `bar` | `plain-text` |
| Remove late pass only | `10-or-20-percent` | `foo` (assertion failure) | `plain-text` |

Both faults fail for actual string differences, not import/setup errors. The
other checks pass. The current history collector also retrieves both introducing
commits from ranges109:111 and186:188 without modifying the clone. Selected
source identities, clean checkout and scratch removal are checked. Output
creation is exclusive; existing evidence is never overwritten.

```sh
/path/to/slugify-venv/bin/python -B benchmarks/preflight_slugify_history_01.py \
  --checkout /path/to/full-slugify-checkout \
  --output /path/to/new-observations.json
```

The recorded execution completed with no fixture repair. These nine native
checks and author collector invocation do not measure model adoption, tokens,
time savings, or all-eight performance. Historical and current evidence must
remain separate in the eventual task. Preserve all scheduled model attempts,
including extra exploration and adverse results; do not require the helper or
give either arm the introducing commit answers.

한국어: 같은 프로젝트의 새로운 이력 검토 과제를 준비했다. 치환 코드 두 곳을
각각 제거하면 서로 다른 실제 출력이 바뀌며, 추가된 커밋도 서로 다르다.
작성자의 의도까지 입증한 것은 아니고, 아직 모델 성능 비교도 하지 않았다.
