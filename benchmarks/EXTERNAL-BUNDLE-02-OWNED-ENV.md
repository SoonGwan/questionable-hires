# External bundle02 — isolated dependency preparation, 2026-09-27

Parent `8e9ae08a`; candidate skills remain `7172b50c`. Author bootstrap only,
zero model calls, no claim of lower tokens/time or issue-test readiness.

The original selection policy prohibited all dependency changes. Before model
execution, its explicitly dated amendment permits author-owned disposable venvs
under the owner’s broad improvement authorization. Existing environments/global
packages/accounts stay unchanged. No selected issue, source, grading requirement
or measured skill resource changes. Earlier failed imports remain historical.

An owned Python3.11 venv at `/tmp/qh-external-bundle-02-owned-envs/modern` was
created from the existing validation interpreter. Its seven requested package
versions are pinned in [requirements](results/external-bundle-02-owned-envs/requirements.txt);
installation uses explicit public PyPI, isolated pip, disabled cache, binary wheels,
zero retries and bounded network/process timeouts. No pytest distribution or
project code was installed. [Evidence](results/external-bundle-02-owned-envs/summary.json)
retains all four subprocess statuses and original output hashes, plus downloaded
wheel SHA256s; [freeze](results/external-bundle-02-owned-envs/freeze.txt) records
actual installed packages including pip. Raw output/report remain local.

Venv creation, dependency installation, pip check and freeze all exit0.
A fresh public-entry import against unchanged selected pytest11143 source exits1:
`ModuleNotFoundError: No module named '_pytest._version'`. The earlier missing
pluggy dependency is resolved for this environment; metadata generation is still
required. No fabricated version module, pretend version or application patch was
used. Other selected sources have not been tested in this new environment.

Next obtain genuine metadata for the exact upstream base revision, exercise the
project’s own build, then verify cold import and real native assertion controls.
Complete required project-test and runtime gates for every selected issue before
freezing model execution. Dependency consistency is not project compatibility,
issue correctness, a solver result or evidence of all-eight-role improvement.

한국어: 별도 임시 환경에 고정 의존성을 설치했고 pip 일관성 검사가 통과했다.
pytest11143의 실제 소스 import는 생성 버전 파일 누락으로 여전히 실패한다.
기존 환경·선택 이슈·스킬은 바꾸지 않았으며 모델 측정과 성능 개선 증거가 아니다.
