# Relevant-section read correction — 2026-09-21

**Subsequently withdrawn:** [urllib3 history01](URLLIB3-HISTORY-01.md) did not
meet acceptance conditions. The entrypoint/README wording is restored; this
document preserves the candidate rationale and pre-measurement validation.

**Instruction candidate, not a measured efficiency improvement.** Edit parent
`09d43d3`. Parent evidence
is [Slugify history01](SLUGIFY-HISTORY-01.md), resource `92afe96`: both5/5,
current tokens+34.32%/time+13.97%. All six response records per arm reconcile;
current has a large test/README read with stored-output truncation. These facts
support investigating context selection, not assigning causal savings to a phrase.

The entrypoint previously said to read known implementation and consumer/contract
**files** together. It now says relevant **sections**, and distinguishes locating
affected behavior in large tests/docs from reading its enclosing section. The
model can widen for unresolved context or requested scope. Small files can still
be read whole; imports, enclosing control flow, callers and public contracts must
not be discarded. A narrow search still does not establish absence of callers.

Only that paragraph changes. No helper/runtime, mandatory tool, output cap,
search limit, history requirement, AST technique or permission boundary changes.
The valid AST probe in the measured session is not evidence to delete structural
matching/future-import safeguards, which are retained. No new reference read is
introduced. English/Korean capability rows describe the same section scope.

This follows the skill-creator principle of a narrow correction to a demonstrated
workflow issue rather than a universal procedure. There is deliberately no
wording-matching unit test claiming to establish model behavior. Validate metadata,
local links and packaging; subsequent model evidence must distinguish adoption,
required outcomes and actual costs. The frozen source task, protocol, sessions,
measurements and featured charts remain unchanged. No favorable rerun is made.

Local validation: skill quick validation, repository/link validation, featured
bilingual synchronization and whitespace checks pass. Python3.11 build13 tests
(2.979s), standalone archive4 (1.091s), and Python probe context/matching9 (0.001s)
pass. These check packaging and retained mechanics, not interpretation/adoption
of the new sentence. The earlier full-suite1,054 result predates this instruction
and the three new benchmark-runner tests; it is not relabeled as a new full run.

한국어: 큰 파일을 통째로 읽도록 해석될 수 있는 안내를 관련 부분과 주변 로직을
읽는 안내로 수정했다. 필요한 맥락이나 요청 범위에 따라 더 읽을 수 있고, 실행
안전장치와 이력 검증은 그대로다. 문구 수정만으로 비용 절감을 입증한 것은 아니다.
