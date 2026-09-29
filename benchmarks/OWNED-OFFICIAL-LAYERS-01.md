# Owned official layers01 — complete pinned blob acquisition

Dated checkpoint **2026-09-27**, protocol/resource `cb39b28f`, parent `29b6d978`.
[Protocol](OWNED-OFFICIAL-LAYERS-01-PROTOCOL.md),
[freeze](results/owned-official-layers-01/freeze.json),
[actual outcomes](results/owned-official-layers-01/outcomes.json).
Zero models, external-case runs, source/test changes or host installation.

All **10** compressed layers of the unchanged official Linux/amd64 manifest
`c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2`
now have verified exact compressed sizes and SHA256 digests. Existing7 blobs were
rechecked without replacing them; missing3 downloaded **635,410,855 bytes**.
The complete set totals **1,015,436,188 compressed bytes**. Acquisition and tar
header inspection completed in **17.651 seconds**, process exit0, no retry.
Raw blobs remain in private owned directories; no body was extracted or exposed
to solver sessions. No token or redirect was saved in public artifacts.

The header-only inventory totals **68,884 entries**, **2,676,891,628 regular
payload bytes**, 37,840 regular entries, 6,756 directories, 8,966 symbolic links
and 15,322 hard links. No special entry types, whiteout markers or absolute/parent
traversal **entry paths** were observed. Absolute and parent-relative symlink
*targets* exist and remain separate counts in the outcome. They must be resolved
inside an owned root; lack of unsafe entry paths does not make host extraction
through these links safe. Hard-link sizes are not extra regular payload bytes;
overlaid and linked entries mean these totals are not final filesystem size.

[Acquisition source](results/owned-official-layers-01/acquire.py) and
[original console copy](results/owned-official-layers-01/acquisition-console.txt)
retain each layer result. The first attempt completed successfully. **Execution
boundary deviation:** the600-second total deadline was checked inside download
and header loops; the launch did not add an independent parent watchdog promised
by the protocol. Reads had15-second timeouts and per-download checks180 seconds,
and observed execution finished17.651 seconds, but no independent parent deadline
is claimed. This attempt is retained; do not repeat acquisition to erase that gap.
Future reconstruction must have an actual parent process watchdog.

This is completed blob acquisition, **not** completed OCI layer application,
filesystem/ownership/mode parity, prepared project import, official native suite,
FAIL/PASS grading, solver quality or whole-task token/time saving. The earlier
[selected Python imports](OWNED-OFFICIAL-PYTHON-01.md) remain separately scoped.
Full reconstruction requires a new frozen protocol, Linux-root confinement,
link/overlay handling and bounded processes before any official-case test.
Unchanged8skills and frozen featured charts are not promoted on this outcome.

한국어: 같은 공식 이미지의10개 계층을 전부 확보하고 크기·해시를 검증했다.
약17.651초에 끝났으며 추출·공식 과제·모델 실행은0회다. 심볼릭·하드 링크가
다수 있어 경로 검사만으로 호스트 추출 안전성을 단정하지 않는다. 독립 부모
감시 프로세스가 빠진 실행 한계도 보존한다. 전체 파일시스템 재현·테스트
통과·스킬 품질·토큰 절감은 아직 입증하지 않았다.
