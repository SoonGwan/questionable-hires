# Audit copy preparation — 2026-09-15

Local helper optimization, not a model benchmark. Source before correction is
`d1615c4` (same runtime as `648f0bf`). The retained measurement command is:

```sh
python3 -B benchmarks/profile_audit_materialization.py --script skills/con-artist/scripts/audit.py
```

The authored fixture selects 514 files: two small Python modules and 512 data
files of 2,048 bytes in eight directories. Each sample performs four real checks
in separate copies: correct test/probe pass; mutant test/probe fail with actual
`8 != 7` and `(8, 7)` assertion diagnostics. The helper verifies selected original
bytes/modes and removes all owned scratch. Fixture creation/removal is outside
the measured audit interval; copy creation/removal and native executions are inside.

## Observations

Three original runs followed by three corrected runs on the same macOS host:

| Runtime | Seconds per audit | Path.mkdir calls per audit |
| --- | --- | ---: |
| Original | 0.554480, 0.532797, 0.526028 | 2,068 each |
| Corrected | 0.532470, 0.518012, 0.512452 | 44 each |

Median **0.532797 → 0.518012 seconds**, about **0.014786 seconds / 2.78% lower**.
This is a small observed local difference, not evidence of a repeatable wall-time
gain: fixed order, three samples, warm shared host and instrumented `Path.mkdir`
limit inference. Request reduction is real, but **97.87% fewer mkdir calls is not
97.87% faster copying or development**. No token savings, model adoption, end-to-end
performance claim or featured chart change.

## Change and preserved work

Each newly allocated check directory tracks parents already created while
materializing selected/probe files. Repeated siblings no longer request the same
parent again. The set is discarded between checks; it contains paths only, not
cached test results or file contents. Every check still gets a fresh copy,
every file is written, original modes are applied, new probe files retain exclusive
creation, and original snapshot/revalidation and cleanup remain unchanged.
No hard links, shared mutable copies or cross-invocation cache is introduced.

The first regression test fails before the correction with **8 != 1** parent
creation requests. It also runs the real helper, inspects copied bytes/modes,
changes a phase-local asset, confirms later copies receive pristine input, and
checks actual fault detection/original preservation/cleanup. After correction
that test passes, and all then-current **79 mutation-helper tests pass** (13.861s).
A second native probe-file test verifies two distinct phase directories each
created once, correct-pass/mutant-assertion-failure and absent original probe files;
it passes separately. No new skill instructions or user-facing workflow burden.

한국어: 복사본마다 이미 만든 부모 디렉터리를 기억해 같은 디렉터리의 반복 생성
요청을 줄였다. 514개 파일·네 실제 검사에서 생성 요청은 2,068→44회지만, 도구
전체 실행 중앙값 차이는 0.533→0.518초 정도에 불과하다. 호출 감소율을 성능
향상률로 포장하지 않는다. 파일 내용·권한·검사별 독립성·원본 무결성·정리를
검증했고, 모델 토큰·시간 절감이나 대표 그래프의 수치로 사용하지 않는다.
