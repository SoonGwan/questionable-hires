# Reject omitted audit inputs — 2026-09-21

Parent resource `74b674a`. Inspection found that Con Artist's selected-input
snapshot used `is_file()` to decide what to copy and ignored other directory
entries. A selected FIFO or Unix socket was silently absent from the disposable
test copy. Symlinks were already rejected; post-inspection replacement controls
also existed, but neither covered an initially present special file.

New `tests/test_audit_special_inputs.py` reproduces direct and directory-contained
FIFO/socket omissions and checks rejection before calling the execution helper.
Before the fix, three test methods yielded five failed assertions (four filesystem
subcases and the audit-level rejection); the regular-file control passed.
The audit-level control mocks execution to assert that no check starts; it is not
native behavioral or model evidence. Filesystem controls create actual local
FIFOs/sockets and leave source data unchanged.

The snapshot now classifies each encountered item with `lstat`, rejects objects
other than regular files/directories, and uses that same inspected metadata for
the bounded regular-file read. Existing no-follow/nonblocking open and descriptor
identity checks remain. Unsupported objects are never opened/copied. Empty
directories remain allowed, with the existing file-only snapshot semantics.
This is not atomic traversal, filesystem isolation or support for live IPC fixtures;
use appropriate project facilities for those workflows, not an incomplete copy.

Validation on the changed checkout:

- Python3.11.16: all121 `test_audit*.py` checks pass,22.796s.
- Python3.11.16: all80 mutation-helper checks pass,16.058s.
- Python3.9.6: new three checks pass,.006s.

Runtime observations are not speed comparisons. No model calls, efficiency claim
or featured-chart changes. The common guide, existing-test recipe and both README
capability descriptions disclose the rejection boundary without another mandatory
entrypoint step. `skill-creator` guidance favors this reproduced narrow correction
over forcing helper adoption or adding speculative workflow requirements.

한국어: 선택한 FIFO·소켓이 검사 복사본에서 조용히 빠지는 문제를 재현하고,
실행 전에 거부하도록 수정했다. 원본과 다른 입력으로 검사를 진행할 위험을 줄인
도구 정확성 수정이며, 모델 속도·토큰 개선 실증은 아니다.
