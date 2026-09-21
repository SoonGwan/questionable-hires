# Native preflight: identical checks, shorter optional request

2026-09-21. Selection`76a5cc1`, skill resource`aed8a27`, pinned upstream and
workload specified in [selection](PROBE-EDIT-TRANSFER-01-SELECTION.md).
[Retained native results](results/probe-edit-transfer-01-preflight.json) include
all16 actual pytest processes, imports, test-binding assertions, exact assertion
diagnostics and cleanup guards. These are author executions, not model sessions.

| Selected test file | Bytes | Complete-replacement JSON bytes | Exact-edit JSON bytes |
| --- | ---: | ---: | ---: |
| Full upstream file |30,731|35,185|2,100|
| Exact prefix through first method |816|2,820|2,100|

JSON is UTF-8 with compact separators, includes common recipe fields and the
same fault/precheck/selector. These are serialized byte counts, **not model token
counts, elapsed-time savings or an estimate of whole-task improvement**. A model
may create JSON programmatically without emitting a full file, use another valid
workflow or never adopt the helper; none of those outcomes is precluded.

For both sizes and both request forms:

- Fresh process imports the supplied public `packaging` package from local `src`.
- Correct original suite:9pass. Faulty original suite:9pass (survives).
- Correct stronger suite:9pass. Faulty stronger suite:9fail with actual empty
  string versus expected specifier assertion values, not setup/import failures.
- Every actual pytest process verifies copy-local package, implementation, native
  test module and identical Specifier binding. No process reuses another's result.
- Four fresh copies per form, unchanged source bytes/modes and optional whole-tree
  guard, confirmed owned-scratch removal. All outputs complete, no timeouts.

The original selected test checks construction, not serialization. Later unselected
upstream tests already exercise string representation. This is an explicitly
requested strengthening of that selected test, not an upstream full-suite gap.

`tests/test_probe_edit_transfer_cases.py` has four controls: original snapshot
identity/exact prefix; only the intended `__str__` return changes; both request
forms materialize identical test bytes; every retained native phase's test hash
matches its expected original/stronger file. Four pass on Python3.9.6,.090s.
They check retained evidence and construction, not new model behavior.

The initial native run used the existing packaging environment: Python3.11.16,
pytest8.3.4 and its preinstalled dependencies, with no downloads. Original raw
preflight output remains ignored locally; committed output redacts host paths.
The public preflight script uses the same checks, with a caller-selected exclusive
output and project-local temporary inputs rather than relying on ignored folders:

```sh
/path/to/preinstalled/python3.11 -B benchmarks/preflight_probe_edit_transfer_01.py --output /path/to/new-preflight.json
```

Do not overwrite the retained result to reflect later code. A rerun is a separate
author check, not another independent sample. Model task text, six-cell scheduler
freeze and original-session review still remain; no model run or graph promotion
is claimed here.

Archive follow-up at`078f201`: fresh `git archive` without Git/local-run artifacts
passes all four construction/evidence controls on Python3.9.6,.090s. The public
preflight script also executes successfully from that archive on the supplied
Python3.11 environment, reproducing all16 native outcomes and four request byte
counts into a separate temporary output. This is an author reproducibility check,
not16 additional independent model samples or a rewrite of the retained first run.

한국어: 두 입력 방식 모두 동일한 네 단계 검사 결과를 냈고, 실행된 테스트 파일의
해시도 같았다. 큰 파일에서 JSON 입력은35,185→2,100바이트지만 토큰·시간 절감률은
아니다. 아직 모델 사용 여부와 실제 비용을 비교하지 않았으며 다음 실행 조건을
동결한 뒤 확인해야 한다.
