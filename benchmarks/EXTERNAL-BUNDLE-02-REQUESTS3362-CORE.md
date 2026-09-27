# External bundle02 — Requests3362 full core module, 2026-09-27

Parent `b02b88bd`; exact application base unchanged, skill resource `7172b50c`.
Author environment preparation only; zero model calls, no issue-solution or
whole-task efficiency claim. No new issue/gold solution fields were inspected.

Execute the **entire existing** tests/test_requests.py module with native source-
bound Requests2.10, pytest2.8/plain and the existing owned HTTP/HTTPS/mock fixtures.
Use owned config/HOME/TMPDIR/basetemp, minimal environment,90-second process-group
limit and native server-thread join/termination checks. Certificate checkend3600
passes before the run; this is not indefinite certificate readiness. No test
selectors were omitted within this module. This is not all Requests test modules.

First result:182 passed,1 failed,1 xfailed,1 xpassed; native exit1,24.583seconds.
The cookie-expiration assertion fails while the server logs an actual500 response:
httpbin0.4.1 supplies headers.lists() to Flask1.1 jsonify, which rejects that generator
as nonserializable. Preserve the complete original failure/stack and all outcomes.
This is observed fixture incompatibility, not a model's failed repair.

Restore the project's declared Flask0.10.1 and Werkzeug0.11.4 pins in the **owned
fixture environment only**. Download exact distributions, hash them, install offline
with no dependency resolution/build isolation, and use the existing setuptools plus
pinned wheel0.41.3 for the pure-Python source build. Other fixture dependencies and
owned certificate refresh remain as previously prepared; this is not a recreation
of the complete historical lockfile. Pip check passes and the new freeze is retained.
No application, project test, installed plugin Python source or native assertion
was manually patched. The two stack-version changes are a joint compatibility
repair; no separate one-variable causal measurement is claimed.

Second **same full module** result:183 passed,2 xpassed,zero failed; native exit0,
24.276seconds. The formerly failing cookie-expiration check now passes. Both XPASS
identifiers remain visible: auth stripped on redirect off host; iter_lines reentrant.
Do not count XPASS as ordinary passes or claim all185 are independently verified
fixes. An expected-failure outcome also changes under this runtime; preserve the
unequal original outcomes rather than implying every environment is equivalent.
The existing mocker-based proxy-close check is included among the183 passes.

Since the server stack changed, rerun the same four HTTP/TLS trust controls: all4
pass (HTTP/HTTPS success, untrusted CA rejection, wrong hostname rejection), and
native fixture threads join/terminate. Original stderr includes a brief socket-
request exception header from a negative TLS control; retain it without rewriting
or interpreting it as a silent successful handshake. Native caught exceptions are
checked by the unchanged control assertions. No verify=False or insecure trust
fallback is introduced. All140 original archive file bytes remain unchanged after
both native runs. No author subprocess/server is live.

[First result](results/external-bundle-02-requests3362-core/first/summary.json),
[historical-stack result](results/external-bundle-02-requests3362-core/historical-stack/summary.json),
[trust controls](results/external-bundle-02-requests3362-core/historical-stack/trust-summary.json)
and [dependency artifacts/freeze](results/external-bundle-02-requests3362-core/dependencies/)
retain exact native outputs as deterministic path-redacted gzip reading copies,
original/reading/compressed hashes and actual source preservation evidence.
Earlier partial tests and earlier native/default-assertion incompatibilities remain
historical. Plain assertion mode remains provisional until selected-issue native
grading proves the full required contract under this runtime.

Next run exact selected-issue test/gold controls in private author grading outside
solver contexts, establish remaining Requests versions/services and required tests,
then freeze fresh solver isolation/runtime/protocol before model comparisons.
This module's passing behavior cannot substitute for all8 role-specific quality,
lower whole-task tokens and faster completion. Featured/site/model claims and
skill READMEs remain unchanged because no skill capability/model result changed.

한국어: 원본 핵심 테스트 전체의 첫 실행은 서버 JSON 호환 문제로1개 실패했다.
당시 Flask·Werkzeug 버전으로 맞춘 동일 모듈 실행은183개 통과·XPASS2개·실패0개였다.
첫 실패와 기대 결과 변화도 보존한다. TLS 신뢰/호스트 검사4개도 다시 통과했지만
과제별 회귀 검증·모델 효율·전체8개 역할 개선은 아직 입증되지 않았다.
