# Authenticated remote installation01

2026-09-22. Source `5e6beab30412261aa0bee281d774d75b1040ea43`.
Two independent installation routes read the private GitHub repository using
existing authorized Git credentials. No token values were printed, copied into
the repository or supplied on command lines. No user/global skill installation,
model-setting change, visibility change or publication was requested.

## Executed routes

1. The available skill-installer's `install-skill-from-github.py`, with
   `--repo SoonGwan/questionable-hires --method git --ref 5e6beab30412261aa0bee281d774d75b1040ea43`,
   all eight `skills/<name>` paths and an explicit new temporary destination.
   Exit0; eight installed directories. This tests that helper, not the npm route.
2. Actual `npx` from a new temporary project on macOS: Node24.16.0/npm11.13.0,
   cached `skills@1.5.26` tarball, no fresh registry installation:

   ```sh
   npx --offline --yes --package=/path/to/skills-1.5.26.tgz skills add SoonGwan/questionable-hires --agent codex --skill '*' --copy -y
   ```

   Exit0; CLI reports repository cloned, eight found and eight installed. The
   repository argument is remote, **not** a local source path. npm's `--offline`
   applies to package acquisition; the child CLI still clones GitHub. The remote
   main SHA was checked before and after, unchanged at the source above, and all
   installed bytes/modes agree with the independently pinned helper installation.

Set `DO_NOT_TRACK=1`, `DISABLE_TELEMETRY=1`, `GIT_TERMINAL_PROMPT=0`, an isolated
`XDG_STATE_HOME` and the existing task-specific npm cache for route2. Reviewed
CLI1.5.26 code honors those switches for telemetry/audit lookups and state-lock
placement. This is not enforced network isolation or a full filesystem-write
audit. Neither invocation uses a global install flag. Both installation outputs
were observed in the terminal; full spinner transcripts are not retained.

## Installed behavior and identity

[Recorded checks](results/remote-install-01/installed-check.json) reuse the
existing `check_skills_cli_install.py` inventory and recent-helper controls:

- All8 skill directories /51 regular resources match checkout bytes and modes
  through both routes. Source catalog README is not an installed resource.
- All9 Python entrypoints in the npx-installed copy execute isolated `--help`.
- Installed source-region selection returns the requested function without
  executing the input; missing selection exits1.
- Installed Receipt runs the same actual native assertion: before exits1 with
  the boundary assertion, after exits0, one test each, copied imports verified.
  Original tree remains unchanged and owned comparison copies are removed.
- Both installed inventories still match after the behavioral checks. The
  repository's `install.py --check` separately reports both routes matching.

This uses existing native checks, not a new model task or a fresh hosted CI run.
It does not establish host discovery, all helper behaviors, anonymous public
access, a new npm download or the future behavior of an unpinned CLI. Temporary
installations remain under ignored local-run storage for inspection; they are not
registered as the user's personal skills. Nothing is available in the current
host merely because these temporary projects contain installed files.

한국어: 비공개 GitHub 저장소에서 인증된 원격 설치를 실제로 확인했다.
스킬 설치기와 npx 두 경로 모두8개 스킬·51개 파일이 일치했고, npx 설치본의
Python 진입점9개와 선택한 실제 기능 검사도 통과했다. CLI 패키지는 기존 캐시를
사용했으므로 신규 npm 다운로드나 익명 공개 설치까지 검증한 것은 아니다.
사용자 스킬 폴더와 모델 설정은 변경하지 않았으며 성능 개선 수치도 아니다.
