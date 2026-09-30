# Mother module loading01 — 2026-09-30

Parent `d2b75455`; the measurements below were recorded from an uncommitted
working-tree candidate on2026-09-30, when `.git` was read-only. Git write access
was enabled on2026-10-01 for commit/push/PR delivery. Exact source hashes and compressed,
path-redacted execution logs are in [evidence](results/mother-module-loading01/evidence.json).
The existing published0.2.0 and installed personal skills are unchanged.

The component loader executed an unregistered module. A supported zero-argument
`@dataclass` with postponed annotations failed before any interaction checks:
`complete:false`, exit2, `'NoneType' object has no attribute '__dict__'`.
Both a guarded implementation and a stale-overwrite implementation hit this same
setup error. The new CLI regression observed two failures before the fix.

The loader now scopes `sys.modules` registration around both source execution and
the complete async probe, including task cleanup. This allows dataclass annotation
resolution at import and `get_type_hints` during actual requests. A prior module
entry is restored on success, failed import, missing class or caller failure; an
initially absent entry is removed. The private Python loader is now a context
manager; its CLI arguments are unchanged. This is not package-relative import
support or rollback of arbitrary source side effects.

The same CLI assertions now distinguish guarded0/[true,true] from faulty1/
[true,false], retaining actual `old result` stale state, matching saved evidence,
empty stderr and unchanged component source bytes. Additional tests exercise
restoration with and without a pre-existing module entry and failed imports.

| Local checks | Tests | Result |
| --- | ---: | --- |
| Python3.11 checkout: module loading, sequence probe, entry handling | 31 | Pass |
| Python3.9 checkout, same suites | 31 | Pass |
| Git-free explicit source copy, Python3.11 | 31 | Pass |
| Git-free explicit source copy, Python3.9 | 31 | Pass |
| Standalone install/archive and generated landing, Python3.11 | 24 | Pass |

Reproduce: `PYTHONPATH=tests python3 -B -m unittest test_sequence_module_loading test_mother_in_law_sequence_probe test_sequence_probe_entry -v`.
The three new tests include one CLI test with two independent implementations.
Git-free results are explicit source-copy checks, not a full repository archive run.
Catalog/current-link checks, featured sync/check and151 generated preview files
also pass. The local archive is109,345 bytes; its hash is recorded in evidence.
It is not deployed or a replacement for the published0.2.0 asset.
No new model calls, whole-task token/time savings, hosted deployment or independent
validation claim. Integration07 and featured benchmark numbers remain unchanged.

한국어: 부모d2b75455의 컴포넌트 로더는 모듈을 등록하지 않아 문자열 타입 주석을
쓰는 dataclass 정상·결함 구현 모두 검사 전에 종료값2로 실패했습니다. 같은 CLI
검사를 유지한 수정 후 정상은0, 오래된 결과 덮어쓰기 결함은1로 구분합니다.
가져오기부터 비동기 검사 정리까지 모듈 등록을 유지하고 성공·실패 후 원래 상태를
복구합니다. Python3.9/3.11의 작업 트리와 Git 없는 명시적 사본에서 각각31개가
통과했고 설치 묶음·랜딩24개도 통과했습니다. 생성된151개 파일과 안내 링크·대표
데이터 동기화도 확인했습니다. 2026-09-30 측정 당시.git 읽기 전용으로 미커밋 상태였고,
2026-10-01 쓰기 권한을 받아 커밋·push·PR을 진행합니다. 모델 토큰·시간 개선이나
기존 공개 릴리스 갱신을 뜻하지 않습니다.
