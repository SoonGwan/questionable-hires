# Receipt: several historical versions, one current test run

2026-09-22, parent `efc1439`. Optional capability for requested multi-version
verification, not evidence of model adoption or broad20–30% efficiency gains.

Previously, using the pairwise helper against two historical implementations
required repeating its current-version native check. `additional_before` now
accepts up to seven extra commit expressions with unittest. Each distinct
historical commit receives its own isolated native run and full result under
`before`, `before_2`, etc.; `after` runs once. All use the same once-frozen
current tests/configuration and one existing runtime. A single comparison stays
two runs. There is no cross-invocation result cache or automatic extra history
search. An adequate project-native multi-version comparison can already reuse
its current result; this feature is not an advantage over every native workflow.

All requested snapshots are prepared before any native execution. Resolved
duplicate historical commits, malformed/missing revisions, unsupported runners
and shared20MB snapshot overflow reject before tests. Every historical reference
still counts toward that existing budget, even if its Git blob is reused.
Timeout/incomplete provenance stops subsequent checks; absent after evidence
must not be treated as a pass. Existing selected-original checks, optional whole
tree guard, source provenance and cleanup remain. Limits are per invocation /
per native check as documented, not a new total wall-time deadline.

## Local native controls

An author fixture has two different boundary defects: one historical version
rejects18, another accepts17, while current accepts18/rejects17. Both current
assertions run in every copy. Separate pairwise calls perform4 actual native
checks; one multiple-before call performs3. The two failures and one pass retain
test identities, native output, selected-file hashes and copied-import evidence.
The original whole-tree inventory remains identical and comparison copies are
removed. The single-pair control still performs2 checks.

This is **one fewer native check**, not25% fewer model tokens or elapsed seconds.
No timing claim, benchmark task rerun, fresh holdout, model API call or featured
chart change is involved. The mechanism is useful only when equivalent current
work would otherwise be repeated; it is inappropriate when tests, dependencies
or requested execution semantics differ across versions.

Seven new checks cover native behavior/process count, CLI native-module mode,
ordinary single-pair behavior, unsupported runners, distinct revision validation,
incomplete stopping and snapshot limits. On the predecessor, three capability
checks error on the unsupported field; after implementation all7 pass on Python3.9
and in a fresh source archive with no Git history. Schema validation also passes.
The full Receipt-prefixed group passes183 checks on Python3.11.16 in69.129s;
synthetic scheduler prints in that group are controls, not new model sessions.
These authored developer controls do not establish independent generalization.

The entrypoint and automatic-selection description are unchanged. Following
skill-creator's progressive-disclosure guidance, the optional field is documented
in the existing Python comparison guide and CLI help, not made mandatory for
ordinary fixes. EN/KO capability descriptions are synchronized. Behavioral
transfer and useful model-level savings remain unproven.

한국어: 동일한 현재 테스트로 여러 과거 버전을 비교할 때 현재 버전 검사를
중복 실행하지 않는 선택 기능을 추가했다. 두 과거 버전의 서로 다른 실패를
유지하면서 실제 네이티브 검사4회를3회로 줄였고, 단일 비교는2회를 유지한다.
토큰·시간25% 개선을 뜻하지 않으며 모델 사용·성능 검증은 아직 필요하다.
