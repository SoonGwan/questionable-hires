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

## Manual candidate workflow

In GitHub Actions, select **Prepare release candidate**, choose the intended
branch and select **Run workflow**. This is candidate preparation, not publication.
It first calls the complete Python3.9/3.11/3.12 and source-archive validation
workflow. Only after all jobs pass does it build the bundle twice, compare bytes,
scan extracted contents, install into a temporary consumer and verify that install.

The retained `candidate-<full commit SHA>` artifact contains only:

- `questionable-hires.tar.gz`: the standalone installation bundle;
- `SHA256SUMS`: the bundle's SHA-256, not the enclosing Actions artifact digest;
- `SOURCE_COMMIT`: the checkout revision used to build it.

Download within14 days and verify the bundle using `shasum -a 256 -c SHA256SUMS`
from the downloaded directory. The checksum detects mismatches, not an untrusted
publisher. No raw runs, consumer files or repository history are uploaded. Actions
has read-only repository permissions; no release, tag or visibility change occurs.
This does **not** clear privacy findings in a full repository clone.

Local tests execute the actual build shell and check that a failed build emits no
upload-directory output. In disposable source copies, a synthetic key-header
finding stops before installation, and an injected installer verification failure
stops after installation without signaling a completed candidate. No real
credentials or shipped resources are changed by those controls.
Hosted scheduling, artifact upload and permissions still
need a successful Actions run; the recorded account billing/limit blocker is not
fixed by this workflow. See [release readiness](RELEASE-READINESS.md).

한국어: Actions의 **Prepare release candidate → Run workflow**는 검증된 설치
후보를 만드는 버튼이다. 전체 검증 성공 후에만 압축·재현성·설치 일치를 확인하고
설치 묶음·체크섬·원본 커밋 번호만14일 보관한다. 공개 전환이나 GitHub Release
게시 버튼은 아니다. 원격 CI 결제/한도 문제와 Git 이력의 공개 검토는 별도로 남는다.

## Installed recent-capability checkpoint — 2026-09-22, resources `11d9a36`

The expanded offline package/extract/install test now executes the installed
Necromancer and Receipt helpers outside the checkout with isolated Python.
UTF-8 BOM input yields the complete CRLF-preserving function excerpt, original
byte hash/count and physical line1; a missing name remains incomplete with exit1.

Receipt compares two actual historical Git versions against one uncommitted
current version using identical native assertions. Both historical versions fail
different boundary assertions; current passes. Three native checks retain full
revision identities, same-process copied-module provenance, exits and actual
failure values. Source/Git bytes and modes remain unchanged, scratch is removed,
and the installer confirms that all installed resources still match afterward.
No personal skill directories or application settings are modified.

All four expanded archive tests pass on Python3.11.16 (1.647s) and3.9.6 (3.157s).
The same tests also pass from a fresh source archive without project history or
local-run artifacts. These are installed-capability checks, not a new remote
installation, model-cost measurement, complete hosted matrix or public release.

한국어: 압축·설치된 스킬로 BOM 입력과 다중 과거 버전 검증까지 확인했다.
실제 실패값·현재 통과·원본 보존·임시 파일 정리·설치본 일치를 검사했다.
모델 성능 향상 수치나 공개 배포 완료를 의미하지 않는다.

### Local distributable candidate — source `1fbcc40`, 2026-09-22

An actual retained local installation bundle contains54 files (including
`CONTENTS.json`),308,730 uncompressed content bytes and98,261 compressed bytes.
SHA-256: `0ddeabba07e9c92b28e3a1008eb1388cfca64b45f05a834d26f15780bc61dded`.
Two differently named builds in the same runtime are byte-identical. All53
manifest-listed originals match checkout bytes/modes. The archive excludes Git
history and benchmark artifacts; it is not a substitute for the complete source.

This specific bundle was extracted into a new local directory and installed into
a temporary consumer project, not the user's personal skill directory. All8
skills match; all9 installed Python entrypoints pass `--help`. The installed
BOM/multiple-before checks described above pass from this exact artifact, and
the installer still reports matching resources afterward. An existing-pattern
scan of extracted content has zero findings, not a complete privacy certificate.
The archive is retained locally only: no upload, tag, GitHub release, npm
publication, public repository or performance claim is implied.

한국어: 실제 로컬 설치 후보 파일은54개·98,261바이트이며 두 빌드가 완전히
일치한다. 이 압축 파일에서8개 스킬 설치와9개 Python 진입점, BOM/다중 버전
동작을 확인했다. Git 이력과 벤치마크 자료는 포함하지 않았으며 외부에 게시하지 않았다.

## Installed guard checkpoint — 2026-09-21, resources `40f381c`

The offline extraction/install test now executes the installed audit helper with
isolated Python outside the repository. Native original tests pass correct/faulty
code; the same probe passes correct and rejects faulty code with `AssertionError:
2`. Whole-root preservation is reported only after checking originals and scratch
cleanup. A separate deliberate edit to unselected owner notes makes the installed
CLI exit2 without a success JSON, names the changed file, removes scratch and
leaves the edit visible rather than silently restoring it. Installed resources
still match afterward. All changes occur in test-owned temporary projects.

Four expanded archive tests pass under Python3.9.6 (2.424s) and3.11.16 (1.091s).
Before this test expansion, the full checkout at `40f381c` passed928 tests in
160.286s under Python3.11.16, with no skips. This is local deployment-readiness
evidence, not hosted CI, public installation or model-performance evidence.

한국어: 압축 해제·설치한 도우미로 정상/결함 실행과 미선택 원본 변경 감지를
확인했다. 변경을 숨기거나 자동 복원하지 않으며 임시 파일도 제거된다.
확장한 설치 검사4개가 Python3.9/3.11에서 통과했다. 확장 전 전체928개도
통과했지만, 원격 배포나 모델 성능 향상을 뜻하지는 않는다.

## Historical local archive checkpoint — 2026-09-21, resources `61f30db`

The builder at that revision produced **52 files, 265,227 uncompressed content bytes,
85,769 archive bytes**, SHA-256
`7531327db4b22a66b58cdc83567a26e403713519a3e52405312f1ff7e5269724`.
The complete source archive at the same revision is14,337,274 bytes. This
comparison describes different-purpose payloads, not an install-time or model
performance improvement. The standalone archive remains a local artifact, not a
published release asset or a change to the `npx` download path.

The archive test now extracts and installs outside the repository, runs each
copied Python script's `--help`, then invokes installed Con Artist context
collection with isolated Python (`-I -B`). Compact mode returns the smaller index;
pretty mode returns complete numbered source with the original SHA-256. Consumer
bytes/mode stay unchanged; no extra consumer files appear; installer `--check`
still reports every installed resource matching after execution. This verifies
the recent representation correction survives the actual package/install path,
not just that checkout code passes an import-based test.

All four archive tests pass on Python3.9.6 (1.873s) and3.11.16 (0.671s).
They also verify reproducibility, conflict preservation and link/source-output
refusal. No network, user skill directory, host registration or visibility change.
This does not replace the separate model evidence or hosted release gates.

한국어: `61f30db`의 설치 묶음은52개 파일·85,769바이트다. 저장소 밖에서
압축 해제→8개 스킬 설치→설치본 실행→파일 일치 재확인까지 통과했다.
최근 소스 수집기 수정도 설치본에서 검증했다. 원격 공개 설치나 모델 성능
개선을 증명한 것은 아니며, 실제 공개 릴리스는 만들지 않았다.

## Historical local check — 2026-09-15 KST

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
