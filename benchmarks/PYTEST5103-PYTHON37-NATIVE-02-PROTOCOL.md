# pytest5103 Python37 native preparation02 — 2026-09-28

Retain the first [preparation protocol](PYTEST5103-PYTHON37-NATIVE-01-PROTOCOL.md)
`65a4c0e8` and all outcomes. Source export verifies418 files and existing Git HEAD.
The first control container fails before dependency installation: directory creation
requested0755 under private umask077, resulting in0700. With capabilities dropped,
the Docker-copied directory's owner differs from the process; regular0644 wheel
files remain unreadable through that parent. Record the actual PermissionError;
no install/import/control ran, and terminal/OOM inspection was skipped by the
original driver's early assertion. Cleanup still confirms zero containers and a
stopped VM. This is author setup failure, not a pytest or skill regression.

Fresh private native02 root: reuse the exact exported source tar and unchanged
15 wheels, preflight and observer. Explicitly chmod the wheel directory0755
after creation; files0644, containing private root0700. Freeze hashes and modes.
Run one fresh native control container with all original bounds/criteria. No source
export repeat, no image/layer change, no new dependency or issue test. Record
terminal state in finally even if attach exits nonzero. Retain both attempts;
do not count the failed first setup as a passed test or silently overwrite it.
Require the unchanged8GiB guest threshold; recovery from native01 is already done.
Cleanup remains mandatory. Zero models, no performance or original issue claim.

한국어: 최초 시도는 개인 디렉터리 umask 때문에 wheels 폴더가0700이 되어 읽기에
실패했다. 원본 기록을 보존하고 소스·패키지·검사 내용은 그대로 두며 해당 폴더만
명시적으로0755로 만든 새 컨테이너를 검증한다. 실패 때도 종료 상태를 수집한다.
