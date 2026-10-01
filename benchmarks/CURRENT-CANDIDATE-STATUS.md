# Current candidate: whole-task improvement remains unproven

Decision checkpoint **2026-10-01**. The owner requires better outcomes across all
eight roles, fewer whole-task tokens and faster completion. This remains **unmet**.
The owner separately authorized the published0.2.0 development preview; publication
is not performance proof.

| Dated checkpoint / measured resource | Evidence | Decision |
| --- | --- | --- |
| [Mother module loading01](MOTHER-MODULE-LOADING-01.md),2026-09-30,parent `d2b75455`, candidate file hashes in evidence | Actual CLI dataclass setup failure reproduced for correct and faulty components. Scoped module registration restores normal0/fault1 discrimination and runtime annotation lookup. Related31 tests pass on3.9/3.11 in checkout and explicit Git-free copies. | Native correctness only. Committed as `73abd45d`; [PR #3](https://github.com/SoonGwan/questionable-hires/pull/3). Full checkout1,546 pass, zero skips. No model cost claim or deployed update. |
| [Integration07](ALL-EIGHT-CURRENT-07-REVIEW.md),2026-09-28,measured `1be35120` | Tokens592,783→602,679 (**+1.67%**); CLI494.990→447.302s (**−9.63%**). Only2/8 lower both. | All-eight objective unmet. Exposed n=1, unequal checks and shared-host/context limits; no independent quality superiority. [Full costs](ALL-EIGHT-CURRENT-07-COSTS.md). |
| [0.2.0 delivery](../docs/RELEASE-DELIVERY-2026-09-29.md),2026-09-29,`8f3e4e44` | PR merged, prerelease and site published. Nine site routes and four anonymous release downloads match. | Delivery only. No new browser interaction QA; no connected browser. |

The [previous decision index](CANDIDATE-HISTORY-2026-09-30-BEFORE-MODULE-LOADING01.md)
preserves every preceding native/model checkpoint, unsuccessful optimization and
limitation, including the accepted separate Python3.7 pytest5103 native gate and
adverse official3.9 gate. Chronological experiments remain in that history.

The [independent model execution request](SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md)
remains unresolved. Do not change approval settings or repeat declined candidates
to work around it. [Change reachability](INTEGRATION07-CHANGE-REACHABILITY-01.md)
explains why helper correctness fixes alone do not justify rerunning the old whole
screen. Featured Mother data stays frozen at its own resource.

한국어: 2026-10-01 기준 전체8개 품질·토큰·시간 목표는 여전히 미달입니다.
새 Mother 수정은 실제 dataclass 로딩 오류와 실패 구분을 고친 로컬 정확성 근거이며
모델 비용 절감이 아닙니다. 수정73abd45d를 커밋·push하고 PR #3을 생성했습니다. 전체 검사1,546개도 통과했습니다. 0.2.0 게시와
이후 작업 트리 후보를 구분하고, 과거 유리·불리한 결과는 앞선 날짜별 색인에 보존합니다.
