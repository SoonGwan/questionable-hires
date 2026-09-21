# Base-only Git storage and native smoke checks

2026-09-21, parent`d52a57b`. Follows [image inspection](SWE-LITE-PILOT-01-ENVIRONMENT.md).
This is environment preparation, not issue resolution, official grading or a
model experiment. Selected instances and issue inputs are unchanged.

## Preparing disposable source copies

[Executed preparation source](results/swe-lite-pilot-01-isolation/prepare-and-collect.py)
runs only with an explicit disposable-container marker, `/.dockerenv`, cwd
`/testbed`, a real nonsymlink `.git`, and the expected original image HEAD/base
tree. Containers have no network or host mounts. It restores the base archive
over the disposable source, removes only `/testbed/.git`, and creates one fresh
commit containing exactly the original tracked paths. Asserted tree identities:

- Requests: `980e006268fb816b7d2686baef7242418d895d9a`,128 entries.
- pytest: `877d433795f3d7288b9edd5696724bb2d8e47f88`,541 entries.

These tree IDs include original file modes, not just source bytes. Both fresh
repositories have one reachable commit, no remotes and no readable original base
commit object. Original images/read-only containers retain their Git stores for
recovery. This is a bounded Git-store isolation check, not certification that no
other image file can contain task information. Ignored build/install artifacts
remain; pytest's generated `_version.py` is necessary runtime metadata. Further
solver-access and answer-material review is still required before a model run.

Derived **local-only** images after collection, never pushed to a registry:

| Project | Image ID |
| --- | --- |
| Requests | `sha256:f4ede93d2747ddc21d276572cbd2e1df5ea60df8d5d99247f073797bab3e539f` |
| pytest | `sha256:444a87571f10613817b1b0eac7df01a890170a9368a37dc996c3db7093676a07` |

## Native observations

Python3.9.20, network disabled, bytecode/cache writes disabled and third-party
pytest plugin autoload disabled. Public package imports succeed in fresh
processes from `/testbed` after Git replacement. This does not alone prove every
binding in later test processes; same-process provenance remains a scoring gate.

- Requests `test_requests.py`:142 native tests collect successfully. The existing
  `RequestsTestCase::test_basic_building` runs and passes,22 warnings,1.46s,exit0.
  The remaining network-dependent/request tests were not executed or scored.
- pytest `testing/test_skipping.py`: native collection exits0; all77 existing
  tests subsequently pass,14.60s,exit0. These are the unmodified base tests, not
  hidden regression tests for the selected issue.

[Original container logs/commands/states](results/swe-lite-pilot-01-isolation/)
retain full outputs despite terminal display truncation. Import/collection/smoke
success is not the required failing-assertion control or verified grading setup.
No selected issue is marked solved, no model calls or new graph values.

## Preserved setup failures

1. Read-only `--version` checks lacked writable temporary directories, causing
   pytest startup errors. Both originals are retained under `testpaths-01`.
2. Detached interactive launches did not deliver the preparation source over
   stdin. Both waited with unchanged original HEADs, then were explicitly stopped.
   `isolated-01` states/logs remain; foreground stdin launches are `isolated-02`.
3. pytest's first smoke launch raced the local image commit, attempted an implicit
   registry pull and exited125 with pull-access-denied. No container/test existed
   for that attempt. After image commit completion, the actual smoke used its
   immutable local ID with `--pull never` (`native-02`). The terminal error is
   retained here; no synthetic container log is presented for the failed launch.

No model attempt was retried, and no test result was replaced to improve a score.
All owned containers are terminal; the unrelated existing database container was
left untouched. Future local-image launches must wait for creation and use
`--pull never` to avoid accidental registry fallback.

한국어: 실험용 컨테이너의 Git 이력을 기준 소스 한 커밋으로 교체하고 파일 내용과
권한까지 확인했다. 기존 이미지에서 복구 가능하다. Requests 기본 검사1개와 pytest
기존 검사77개가 통과했지만 선정 이슈의 해결·채점 검증은 아니다. 준비 과정의
임시 파일·입력 전달·이미지 생성 순서 오류도 기록했으며 모델 호출은 아직 없다.
