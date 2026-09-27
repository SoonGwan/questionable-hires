# Skill snapshot / 스킬 스냅샷

This archive contains eight skills, their helper resources, an installer and the
MIT license. `CONTENTS.json` records each file's SHA-256 and permissions. The
download's adjacent `skills.sha256` identifies the complete archive. This is a
snapshot of the website release; the GitHub installation command can point to a
different version. Historical benchmark charts measure their explicitly named
resources, not this download. Lower whole-task token use across all eight skills
has not been demonstrated.

스킬 8개와 보조 파일, 설치 프로그램, MIT 라이선스가 들어 있습니다.
`CONTENTS.json`에서 파일별 SHA-256·권한을, 다운로드 옆 `skills.sha256`에서
전체 압축 파일의 해시를 확인할 수 있습니다. 웹사이트 배포에 포함된 스냅샷이며
GitHub 설치 명령이 가리키는 버전과 다를 수 있습니다. 과거 실험 그래프는 각각
표시된 리소스의 측정값입니다. 스킬 8개 모두의 작업 전체 토큰 감소는 아직
입증되지 않았습니다.

## Install / 설치

Requires Python 3. Extract the archive, open a terminal in its
`questionable-hires` directory, and replace `/path/to/project` with your project.
Read the selected `skills/<name>/SKILL.md` before installing. Add repeated
`--skill receipt` options to select individual skills; omitting them installs all
eight. Use the destination your agent supports (for example `.agents/skills`).

Python 3가 필요합니다. 압축을 풀고 `questionable-hires` 폴더에서 터미널을
여세요. `/path/to/project`를 실제 프로젝트 경로로 바꾸고, 먼저 설치할
`skills/<이름>/SKILL.md`를 읽어보세요. `--skill receipt`처럼 스킬을 선택할 수
있으며, 생략하면 8개 모두 설치됩니다. 사용하는 에이전트가 지원하는 스킬
폴더를 지정하세요(예: `.agents/skills`).

```sh
python3 scripts/install.py --dest /path/to/project/.agents/skills --dry-run
python3 scripts/install.py --dest /path/to/project/.agents/skills
python3 scripts/install.py --dest /path/to/project/.agents/skills --check
```

Existing skill folders are never overwritten. For an update, first run `--check`,
back up the affected installed folders outside the skill discovery directory,
and then install. Keep any personal edits in that backup. Reload your agent's
skills after installation if needed. The snapshot needs no Git checkout or npm.

기존 스킬 폴더는 덮어쓰지 않습니다. 업데이트할 때는 먼저 `--check`로 비교하고,
변경할 기존 폴더를 스킬 검색 경로 밖으로 백업한 뒤 설치하세요. 개인 수정 내용도
백업에 보존하세요. 필요한 경우 에이전트의 스킬 목록을 새로 불러오세요.
이 스냅샷 설치에는 Git 저장소나 npm이 필요하지 않습니다.
