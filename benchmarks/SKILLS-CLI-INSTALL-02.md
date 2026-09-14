# Current CLI copies execute recent helpers — 2026-09-15

Source archive `0f2706a`; installed skill resources are unchanged from `0526c9e`.
The existing local `skills@1.5.26` runtime (declared Node >=22.20.0) is used in a
disposable Linux arm64 container, Node v24.20.0/Python 3.12.3. Existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Networking disabled, telemetry opt-outs set, source/CLI mounts read-only. No
downloads, global installation, private credentials or host agent registration.

[Checker output](results/skills-cli-install-02/install-check.json) retains all
20 commands, their exits, inputs and outputs, plus installed file hashes/modes:

- Listing discovers eight skills without installing them.
- `add <source> --agent codex --skill '*' --copy -y` installs exactly eight.
- All **43 selected resource files** match source bytes/modes, without symlinks.
  Source and installed resources remain unchanged after behavioral checks.
- All **eight Python script entrypoints** run `--help` with isolated Python.
- Installed Python/JavaScript controlled callbacks retain argument and result
  identity and complete owned cleanup, as in the previous checker.
- Installed named-function selection returns the exact requested method without
  executing a module that raises. A missing name returns incomplete output/exit 1.
- Installed Receipt's native mode runs the same actual age-boundary assertion on
  two locally created Git revisions: **before fails with AssertionError; after
  passes**, one discovered/executed test each. Copied-import readiness, native
  exits, full output, unchanged original tree/Git contents and copy cleanup are
  verified. The surrounding Ubuntu startup environment is not disabled.

## Initial launcher mistake retained

The [first invocation](results/skills-cli-install-02/initial-cli-path-error.txt)
pointed to the extracted npm package, not its dependency-installed runtime. It
failed on missing `yaml` before listing/installing anything. The corrected call
uses the already-present `runtime/node_modules/skills/bin/cli.mjs`; no dependency
download, source correction or third-party CLI modification. This was an author
launcher error, not a skill execution defect or successful first attempt.

## Ongoing regression and limits

`tests/test_installed_recent_helpers.py` adds the two recent behaviors to ordinary
offline CI using the bundled installer and isolated installed CLIs. That test
passes on macOS (0.694s); four standalone-archive checks also pass (1.299s).
The actual third-party CLI run above is separate evidence, not simulated by that
unit test. No new full-suite run was required for the checker-only change; the
prior 623-test/platform evidence retains its original source IDs.

This verifies local installation and selected real helper behavior, **not** remote
`npx` download/authentication, public availability, automatic model selection,
host registration or model efficiency. No graph values change. Repository data
is not removed to make installation appear smaller; the existing standalone
archive remains a separate optional handoff, not a changed `npx` download path.

한국어: 최신 8개 스킬·43개 파일을 실제 `skills` CLI로 로컬 설치하고 원본 일치와
설치본 실행을 확인했다. 함수 추출의 정상/미발견 처리와 Receipt의 실제 결함 탐지·
수정 후 통과가 포함된다. 최초 CLI 경로 선택 오류도 보존했다. 네트워크를 끈
임시 환경이므로 원격 인증·공개 설치·자동 스킬 선택·모델 성능 검증은 아니다.
