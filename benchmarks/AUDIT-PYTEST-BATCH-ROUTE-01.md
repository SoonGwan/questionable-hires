# Distinguish pytest from native unittest batch routing

2026-09-21, parent `644c12f`. Entrypoint correction; runtime unchanged and model
impact unmeasured. Uses skill-creator's decision-specific routing principle,
without adding another guide, mandatory helper step or general audit rule.

The [specifier comparison](PACKAGING-SPECIFIER-01-REVIEW.md) observed no helper
or helper-reference use in either skill session. Both multiple arms already
reused their correct baseline. Those facts do not establish the reason for
non-adoption or prove that adopting a helper would improve cost.

Inspection found a narrower documentation issue: the independent-Python-fault
entrypoint led directly to the native **unittest** batch recipe, whose module
invocation explicitly excludes pytest. The common guide supports pytest and
links batch fields, but the first route did not distinguish these choices.

The entry now directs pytest to the existing common CLI/batch contracts with
`runner:pytest` and default bootstrap invocation; required `python -B -m unittest`
retains its dedicated recipe. Single-fault phases remain single audits. Existing
project support/direct checks remain valid, helpers are optional, and completed
checks must not be rerun just to adopt support. No production behavior, model
effort, test criteria, scopes, descriptions or invocation-policy setting changes.

## Executable integration control

The new `test_audit_pytest_batch_route.py` extracts the common JSON example from
an actual built skill under a path with spaces, composes the documented batch
fields and selects native pytest without module invocation. It uses the existing
public batch example, not the exposed packaging benchmark.

Two variants preserve the same requested faults (omit persistence / duplicate
persistence). The weak native test passes both mutants; a stronger native test
passes correct code and rejects both with actual assertion failures. Each variant
executes one correct baseline and two independent mutant checks; the second audit
references the first correct observation. Native binding proof, actual pytest
counts/exits, complete output, original0600 modes/bytes and scratch cleanup are
checked. This is six author pytest processes, not model work or time savings.

- Python3.11.16 integration test: both variants pass,0.925s, pytest8.3.4.
- Python3.11.16 entire `test_audit*.py` suite:113 passed,17.844s.
- Fresh `git archive 22c0300`, no Git history/local-run artifacts: the same
  Python3.11.16 integration control passes both variants in0.931s, no skips.
- Repository/skill validation, featured synchronization and whitespace checks pass.
- The integration test explicitly skips if pytest is unavailable; such a skip
  must not be represented as passing native validation.

These checks prove the documented composition works; they do not prove models
will choose it or outperform direct native code. The previous single/multiple
costs and original source/initial-index limitations remain unchanged. Do not
replay packaging specifiers to tune adoption, force the helper, or promote the
new text as an efficiency release. Any model assessment needs a separately frozen
request and preservation of both adverse results and a simple-work control.

한국어: 여러 Python 결함 감사 안내에서 pytest와 unittest 전용 경로를 명확히
구분했다. 새 도구나 필수 읽기 단계를 늘리지 않고 기존 계약으로 연결했다.
배포된 도구의 실제 pytest 실행에서 결함 생존·검출·재사용·원본 보존을 확인했고
감사 테스트113개가 통과했다. 모델 선택·토큰·시간 개선은 아직 미측정이다.
