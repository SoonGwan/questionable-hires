# Solver issue imports01 — 2026-09-27

Parent `2510829d`; all8 fixed external sources, guest bootstrap only. Models0,
native issue tests0. This does not replace any original base/gold grading outcome.

Reuse the [RAM Python guest](SOLVER-PYTHON-RAM-01.md) with one Rosetta translation
share, no arbitrary host data shares/storage/network, and1.5GiB RAM. Append only
the retained import/check scripts and declared pure Python dependencies to the
frozen initramfs. Every issue imports its public entrypoint in a **fresh Python3.9.20
process**, with `-I -B`, explicit source path and an assertion that the actual module
path lies within its selected `/solver/<issue>` project. No cached import from a
failed process, selected test, gold or private grading resource enters the checks.

All four guest attempts terminate normally; each schedules every8 import cells
without stopping at the first dependency error. Complete PASS/FAIL lines identify
observed cell outcomes; process0 means the collection finished, not that all8 passed.

| Retained attempt | Imports | Observed next blocker / change |
| --- | --- | --- |
| [Original runtime](results/solver-issue-imports-01/result.json) |5 PASS,3 FAIL |Legacy pytest missing six/atomicwrites. |
| [Compatibility1](results/solver-issue-imports-01/compat-result.json) |5 PASS,3 FAIL |Existing modern `py` shim depends on `_pytest._py`, absent in legacy source; attr missing. |
| [Compatibility2](results/solver-issue-imports-01/compat2-result.json) |5 PASS,3 FAIL |Legacy imports still require more_itertools. |
| [Compatibility3](results/solver-issue-imports-01/compat3-result.json) |8 PASS |All fresh public entrypoints inside selected projects; executable0,guest stop,no timeout. |

The separate compatibility directory uses existing owned pure Python packages:
six1.15.0, atomicwrites1.4.0, py1.11.0, attrs19.1.0, more-itertools7.2.0. Metadata
versions were inspected in the existing legacy environment before copying its
source files; no network acquisition, host environment install or issue-source edit.
Compatibility2/3 select this directory **only** for the three selected legacy pytest
projects; Requests and modern pytest retain the original dependency path. This
avoids changing the working modern path to fit a legacy shim. Original failures
remain adverse bootstrap observations, not relabeled as passes. These repeated
imports with changed runtime inputs are related development controls, not independent
validation or model-task retries.

Per-attempt input records hash each added package file and exact base/augmented
initramfs, chaining to the frozen source/runtime provenance. Probe Swift and exact
import/check sources, original complete guest stdout and per-cell summaries remain
in `results/solver-issue-imports-01/`. Compatibility3 uses the same probe/import/check
sources as compatibility2, adding only the recorded more_itertools files. Its elapsed
10.276s is bootstrap time, not developer completion speed. No microbenchmark or
whole-task cost benefit is claimed. Each VM has25-second deadline/35-second parent
wait and bounded kill on timeout; compilation/signing/archive compression have no
independent coordinator deadline and completed. All four VMs are terminal.

The host8/8 import observation is not substituted for this new guest evidence.
Nevertheless, public import8/8 does not prove native test collection, required test
statuses, old pytest hook/runtime compatibility, child-process execution, HTTP/TLS
services, solver tool bridge, output transfer or grading/solver separation. Those
remain explicit next gates. Existing selected cohort gold/runtime failures remain
unresolved. Ordinary skill capabilities, README, featured and hosted efficiency
claims are unchanged; all8 developer quality and lower whole-task tokens plus faster
completion remain unmet.

한국어: 실제 Linux RAM 게스트에서 선정된8개 원본 이슈를 각각 새 Python
프로세스로 import했다. 세 번의5/8 실패를 보존하고 선언된 순수 Python 의존성을
추가한 네 번째 입력에서8/8 통과를 확인했다. 이슈 소스·평가 패치는 바꾸지 않았다.
기존 호스트 통과를 게스트 결과로 대신하지 않으며, 이슈 검사·모델 도구 연결·
전체 품질·토큰·속도 비교는 아직 미실행이다.
