# External bundle02 solver source staging01 — 2026-09-27

Parent `582a37b4`; all8 fixed selected issues retained. Author source preparation,
not model solving, grading, role quality, cost savings or OS isolation.

[Executed preparation](results/external-bundle-02-solver-staging-01/prepare.py)
copies each original extracted base archive from the retained
[import preparation](EXTERNAL-BUNDLE-02-NATIVE-IMPORTS.md). It never reads private
grading JSON, patches, required labels, base/gold grading trees or issue-solving
logs. [Separate provenance check](results/external-bundle-02-solver-staging-01/provenance-check.json)
matches all8 archive directory commit identities to the frozen selection and records
the executed preparation SHA. Original archives remain unchanged.

Each completed snapshot contains exact original file bytes/modes plus, for pytest,
the explicitly identified genuine version metadata from its existing supported
build. Metadata is separately hashed; upstream source measurements are not renamed.
The file inventory before/after matches this exact permitted set. Each fresh Git
database has one new snapshot commit, no remote and no selected upstream commit
object. Generated ignored version files may remain outside the committed tree;
the full file inventory and metadata hash, not Git alone, identify the runnable
snapshot. No dataset test patch or gold patch is applied.

[All8 actual fresh imports](results/external-bundle-02-solver-staging-01/summary.json)
exit0 using the existing appropriate owned Python3.9/3.11 runtimes with `-I -B`
and an explicit source path. The imported public entrypoint must resolve within
the staged project. All source archives are preserved byte-for-byte and mode-for-mode.
Git setup has30-second process bounds, Git checks10 seconds, native imports30 seconds.
The coordinator has no independent whole-attempt deadline; it is terminal, not an
active solver or grading job. Private staged projects are under a new owned0700
parent at `/tmp/qh-external-bundle-02-solver-staging-02`.

The first staging attempt stopped after the first snapshot: its import guard
compared resolved `/private/tmp/...` to unresolved `/tmp/...` on macOS. A subsequent
diagnostic confirmed the correct project module was imported. Preserve the initial
[path-guard failure](results/external-bundle-02-solver-staging-01/initial-path-check.json)
and its partial owned directory; the corrected preparation resolves both paths.
The completed eight snapshots are a distinct second attempt, not a silently repaired
first result. This artifact depends on the recorded local source/build/runtime inputs;
no Git-free/standalone preparation portability test is claimed.

These are clean source *staging* directories on the same Mac account. Models with
host filesystem access could still reach host grading storage. Separate directories,
no remotes and one Git commit do not establish OS-level isolation or a clean native
grade. Existing full-cohort runtime/reporting/gold failures remain unresolved;
no selected issue is replaced or retried here, no issue tests or models run. Before
a comparison, transfer only declared solver inputs into an actually isolated runtime,
verify inaccessible grader/host paths and freeze the full execution protocol.

Ordinary skills, README capabilities, frozen featured metrics and hosted efficiency
claims are unchanged. All8 developer quality and joint whole-task token/time
reductions remain unmet.

한국어: 고정된 외부 이슈8개 모두에서 평가 패치 없는 원본 소스 작업 공간을
준비했다. 파일·권한 보존, 별도 Git 커밋1개·원격0개·상위 커밋 부재, 실제 소스의
새 프로세스 import를 확인했다. 최초 macOS 경로 별칭 검사 실패도 보존했다.
같은 Mac 계정의 별도 폴더이므로 운영체제 격리는 아니며, 평가 자료 접근 차단과
전체 실행 규약 검증이 남아 있다. 모델·이슈 테스트0회, 전체 품질·토큰·속도
개선 증거가 아니다.
