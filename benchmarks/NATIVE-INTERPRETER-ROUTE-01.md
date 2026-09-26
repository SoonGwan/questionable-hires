# Native interpreter route01 — 2026-09-27, candidate `e918d02d`

Only Necromancer's entry guidance changes. No runtime/helper, mutation semantics,
coverage, compilation settings or public measurement changes. Original module
future flags, actual consumer bindings and required checks stay intact.

Repeated evidence: [integration04](ALL-EIGHT-CURRENT-04-REVIEW.md) and
[integration05](ALL-EIGHT-CURRENT-05-COSTS.md), original resources `0d12dd9` and
`75183f2f`, both history arms try unavailable `python`, then recover with
`python3`. In integration05/current, a later Git status masks the initial exit.
This is an observed preventable failed launch, not a causal token-saving estimate.

The candidate uses a documented project interpreter when supplied. Otherwise it
identifies an available compatible executable alongside initial source reads,
rather than trial-running a guessed executable. Probe exits remain distinct from
later Git status/diff exits. Availability is not dependency or version compatibility;
required unavailable runtimes remain unverified, without silent replacement.

Earlier [Receipt runtime transfer](RECEIPT-TRANSFER-01.md) concerned ignoring a
known documented command; this route additionally addresses an unspecified
executable and masked review-probe exit. No generic compression, discovery sweep,
mandatory helper, new dependency or removed verification is introduced.

Skill Creator metadata and catalog/link checks pass. Subsequent
[route01 measurement](INTERPRETER-ROUTE-01-COSTS.md) records six completed cells:
tokens+0.67%/time−8.39% versus no skill, tokens−4.75%/time+1.73% versus predecessor.
Neither aggregate improves both costs; native quality review remains pending.
The original motivation above precedes this measurement. Integration05 remains
at its original resource; exposed cases are not independent validation.

한국어: 없는 Python 명령 실행·복구와 후속 Git 명령의 종료 코드 가림을 직접
대응했다. 프로젝트가 지정한 실행기를 우선하고 미지정 시 호환 실행 파일을
확인하며 검증 종료 코드를 따로 유지한다. 후속 6회 측정은 두 비용이 함께
줄지 않았으며 상세 품질 검토는 미완료다. 이전 비교를 새 버전으로 소급하지 않는다.
