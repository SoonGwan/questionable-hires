# Small standalone installation archives

Build an offline installation bundle from a trusted checkout with Python 3.9+:

```sh
python3 -B scripts/package_skills.py --output /existing/output/directory/questionable-hires.tar.gz
```

Choose a new output path; its parent must already exist. Existing files are never
overwritten. The command emits size, file count and archive SHA-256 as JSON. A
failed build may leave its newly created partial archive; inspect it before
manually removing it or selecting a new output path. Do not distribute that partial
file. Sources must not change during packaging; this is not snapshot isolation.

The archive contains all installable skill resources, `scripts/install.py`,
`LICENSE`, and `CONTENTS.json` (resource hashes/modes). It excludes benchmark runs,
images outside skill folders, repository documentation, Git metadata and Python
caches. It is a standalone installation bundle, not the full source/test archive
or a Codex plugin marketplace. Keep the complete repository available for evidence
and development. The content manifest is for consistency, **not authenticity**.

Extract a trusted archive into a new empty directory with your archive tool. From
the extracted `questionable-hires` directory:

```sh
python3 -B scripts/install.py --dest /path/to/project/.agents/skills --dry-run
python3 -B scripts/install.py --dest /path/to/project/.agents/skills
python3 -B scripts/install.py --dest /path/to/project/.agents/skills --check
```

Optional `--skill <name>` selects one hire. The same existing installer refuses
conflicts; `--check` compares without writing. No npm account, dependencies, Git
history or network is needed for this Python installation path. Downloading a
private artifact still requires authorized access. This command does not upload,
publish or create a GitHub release, and does not change `npx skills add` behavior.

## Local check — 2026-09-15 KST

Skill/installer source `e8dd5a5`. The new builder produces **43 files, 203,700
uncompressed content bytes, 66,697 archive bytes**, SHA-256
`a90226b2e4cf6ef90e27f412977d48424fec4738be5b1001db77bd1396522765`.
For comparison, `git archive --format=tar.gz e8dd5a5 | wc -c` reports **6,432,300
bytes** for the complete repository. These are different-purpose payloads, not
equivalent source distributions. No install-time or model-performance claim is
derived from their size difference.

`tests/test_standalone_archive.py`: **4 tests pass in 1.208s**. Two builds with
different output filenames are byte-identical; all extracted resource bytes/modes
match the checkout. The extracted installer runs with isolated Python from outside
the checkout, installs exactly eight skills, and reports a complete matching
installation. Copied Python script entrypoints execute `--help`. Existing output
is preserved; linked resources and output inside skill sources are rejected.
This is not exhaustive helper behavior or remote download testing.

Archive member ordering, timestamps, owner metadata and gzip filename/time are
normalized. Reproducibility was checked in this runtime; compressed bytes may
differ across compression-library versions. This local artifact is not yet a
published release asset. User-installed skills and configuration were untouched.

## 한국어

위 명령은 스킬 전체·기존 설치기·라이선스·파일 목록만 담는 작은 설치용 묶음을
만든다. 벤치마크·개발 문서는 원본 저장소에 그대로 남는다. 새 출력 경로를 사용하고,
신뢰하는 아카이브를 빈 디렉터리에 푼 뒤 포함된 Python 설치기를 실행하면 된다.
`--dry-run`은 미리보기, `--check`는 변경 없는 비교이며 기존 설치를 덮어쓰지 않는다.

위 `e8dd5a5` 스냅샷의 로컬 아카이브는 66,697바이트이며 당시 8개 스킬 설치와 파일 일치를 확인했다.
전체 소스 tar.gz는 6,432,300바이트지만 포함 목적이 달라, 이 크기 차이를 모델
성능이나 설치 시간 개선으로 주장하지 않는다. 기존 `npx skills add`의 다운로드
동작도 변경하지 않았다. 공개 업로드·릴리스 생성은 수행하지 않았다.
