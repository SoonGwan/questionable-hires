# Local CLI installation checkpoint — 2026-09-21

Source `81149576b21907811dc23e7553cb7545876bc2c6`, exported with `git archive`.
The existing dependency-installed `skills@1.5.26` runtime and Linux arm64 image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`
were reused (Node24.20.0/Python3.12.3 from the preceding checkpoint).
Networking was disabled, source and CLI mounts read-only, and
`DO_NOT_TRACK=1`, `DISABLE_TELEMETRY=1`, `PYTHONDONTWRITEBYTECODE=1` set.
No downloads, global installs, credentials or host registration were involved.

The unchanged `check_skills_cli_install.py` completed with exit0.
[Raw checker output](results/skills-cli-install-03/install-check.json) retains
all21 commands, inputs, outputs, statuses and installed resource hashes/modes:

- Listing discovers eight skills without installation; project-local copy installs eight.
- All51 installable resource files match source bytes/modes with no symlinks.
  The catalog README is not an installable resource. Source and copies remain unchanged.
- All nine Python script entrypoints execute isolated `--help`.
- Installed Python/JavaScript controlled callbacks preserve argument/result identity.
- Named-function extraction succeeds without executing source; missing names exit1.
- Receipt runs an actual native boundary assertion: before fails, after passes,
  one test each, copied-import readiness confirmed, original tree unchanged and copies removed.

## Initial mount error

The first source archive was under host `/tmp`; its mounted container path lacked
the checker. Python exited2 before installation or testing. The
[error](results/skills-cli-install-03/initial-mount-error.txt) and empty initial
stdout are retained. A fresh archive of the same revision under workspace
`benchmarks/local-runs/` was readable; the corrected invocation passed, with empty
stderr. No skill, CLI or checker was changed to obtain the pass.

## Interpretation

This refreshes local distribution and selected installed behavior, not remote
GitHub authentication/download, public availability, automatic skill selection,
all helper behaviors, hosted CI or model efficiency. Existing standalone small
archives remain optional; this does not reduce the `npx` clone payload or remove
benchmark history. Featured measurements and charts are unchanged.

한국어: 해당 커밋의8개 스킬·51개 리소스가 실제 로컬 CLI 설치 후 원본과 일치했다.
Python 진입점9개와 선택한 설치본 기능 검사가 통과했다. 최초 마운트 경로 오류도
보존했다. 원격 설치·공개 배포·모델 성능 개선의 증거는 아니다.
