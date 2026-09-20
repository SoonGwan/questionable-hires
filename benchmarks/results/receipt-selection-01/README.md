# Receipt selection 01: mixed results, no broad efficiency win

Reviewed 2026-09-20. Frozen launch `627c830`; original Receipt `6cf9fb1`,
candidate `ca3da48`. [Protocol](../../RECEIPT-SELECTION-01-PROTOCOL.md),
[native preflight](../../RECEIPT-SELECTION-01-PREFLIGHT.md),
[all six reviewed observations](comparison.json), [manifest](run.json).

One authored allocation scenario, with or without an existing adequate native
comparison command. Astra medium, one fresh session per cell, fixed serial order,
shared host/cache. These are not two independent real projects or an eight-role
evaluation. Every scheduled attempt completed; no replacement, timeout or replay.

| Existing native support | Condition | Total tokens | Wall seconds | Shell commands | Full task |
|---|---|---:|---:|---:|---|
| Present | Baseline | 69,337 | 36.394 | 3 | Pass |
| Present | Original | 99,481 | 57.116 | 4 | Pass |
| Present | Candidate | 73,759 | 37.009 | 3 | Pass |
| Absent | Baseline | 71,441 | 74.212 | 3 | Pass |
| Absent | Original | 121,890 | 54.490 | 5 | Pass |
| Absent | Candidate | 145,743 | 60.115 | 6 | Pass |

Tokens include input (cached input counted once) plus output. Candidate versus
original: present **25.9% fewer** tokens; absent **19.6% more**. Summed across the
two conditions, candidate uses **0.84% fewer tokens and 12.98% less wall time**
than original, but **55.9% more tokens than baseline**. These descriptive sums are
not statistical estimates. The favorable present cell does not establish a
general 20–30% improvement. No featured-chart promotion.

## Original evidence and task review

All six satisfy the four frozen criteria. Each runs the same five current native
tests against historical parent/latest implementations: two intended failures and
three passing controls before; five passes after; native exits 1/0. Duplicate
orders return `{'a': 5, 'b': 4}` instead of `{'a': 3, 'b': 4}` before the fix;
aggregate shortage fails to raise `ValueError`. The input-preservation assertions
after those failing assertions are not reached in the before version.

Full revisions and copy-local imports are recorded in the native test process.
Original file bytes and 0644 modes, HEAD and installed resources are unchanged;
owned project-local scratch is removed. Reviewed commands do not install, contact
the network, commit, edit production files or discover outside the project.
Persisted context confirms matching skill entry exposure in all four skill cells
before the first tool; neither baseline has a matching entry. Catalog metadata is
hashed; private full initial instructions are not published.

Each condition directory retains both attempts' original CLI events, answers,
commands, metadata, source snapshots, selected stored tool records and review.
Four CLI outputs omit leading text: each present cell's final comparison command,
and absent baseline's comparison command. Matching original stored responses
retain the missing material, including the absent baseline's before failures.
The other 20 of 24 command output/exit pairs match after path normalization.
Use `native_evidence_stored_line` in each `review.json` to locate decisive evidence;
no missing observation was repaired by rerunning a model or native comparison.

## What changes next

All three present cells chose the existing native command, including the original
skill. This does **not** prove the new wording changed tool choice. Both absent
skill cells used Receipt; baseline built a native isolated comparison. Candidate
present avoided the detailed helper reference. Absent skill cells inspected helper
implementation after execution, and candidate repeated final Git checks to expose
individual exit codes. These are observed extra operations, not established causes
of the cost difference.

A concrete interface question is whether the helper can expose loaded-code
provenance directly enough to avoid implementation inspection for that evidence.
Improve that reusable capability with native tests, then measure transfer on new
work. Do not ban justified inspection or repeatedly tune this same fixture until
its numbers look favorable. The remaining seven roles and broader real-source
efficiency are still part of the unresolved objective.

한국어: 여섯 원본 세션 모두 정해 둔 검증·보존 요구사항을 충족했다. 수정본은
기존 도구가 있는 조건에서 토큰이 25.9% 줄었지만, 없는 조건에서는 19.6% 늘었다.
두 조건 합계는 수정 전보다 토큰 0.84% 감소, 시간 12.98% 감소이며 무스킬보다
토큰을 55.9% 더 썼다. 유리한 조건만으로 전체 성능 향상을 주장하지 않는다.
실행 후 도우미 내부를 읽어 출처를 확인한 작업을 바탕으로 결과 인터페이스 개선을
검토한다. 원본·불리한 결과도 보존하고 기존 대표 그래프는 변경하지 않는다.
