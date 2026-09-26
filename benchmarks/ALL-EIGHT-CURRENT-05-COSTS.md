# All-eight integration05 costs — 2026-09-27

Measured bundle **`75183f2f`**, launch **`f2b83b17`**. [Frozen protocol](ALL-EIGHT-CURRENT-05-PROTOCOL.md).
[All16 attempts](results/all-eight-current-05/comparison.json) and [recorded counter analysis](results/all-eight-current-05/input-cost-analysis.json).
All16 fresh serial sessions completed, no timeout/account-limit stop/replacement.
Original turn contexts confirm GPT-6 Astra medium; original per-response counters
reconcile with each final CLI total. Whole-task tokens=input+output; cached input
is included once. No dollar, causal or latency attribution follows.

**Costs are reviewed; quality/artifact review is pending.** A completed session
is not a passing task. This is an exposed integration regression, n=1 per arm,
fixed alternating order/shared cache and host, not independent validation.

| Task | Baseline tokens | Current tokens | Baseline seconds | Current seconds |
| --- | ---: | ---: | ---: | ---: |
| editor-snapshot-present | 78,960 | 68,616 | 45.564 | 52.671 |
| history-invoice-boundary | 81,965 | 108,400 | 50.486 | 78.283 |
| ledger-delivery-b | 66,130 | 87,853 | 68.062 | 38.929 |
| refresh-owner-a | 82,928 | 146,662 | 110.638 | 112.449 |
| runner-environment-timing | 75,329 | 83,713 | 43.271 | 62.005 |
| sqlite-commit-audit | 97,639 | 90,824 | 77.697 | 103.364 |
| store-check-scope | 59,852 | 64,613 | 35.772 | 34.860 |
| view-contract | 63,552 | 68,066 | 76.334 | 71.292 |
| Sum |606,355 |718,747 |507.824 |553.853 |

Current sums: tokens **+18.54%**, time **+9.06%**. No pair improves both metrics.
Two pairs use fewer tokens; three are faster. These counts are descriptive and
are not quality scores. Unequal extra work remains included in every cell.

Baseline SQLite runs `find .. -name AGENTS.md -print`, outside its explicit
project-only boundary. Preserve that scope violation; it does not establish a
general current-quality advantage. Missing `python` recovery and masked shell
status in history work also remain included. Actual native assertions, bindings,
preservation, cleanup and other scope behavior require complete review.

The existing all-condition analyzer initially rejected the native scheduler’s
`case_id` manifest key. A real-data reproduction fails before the fix; afterward
all16 coverage and eight pairs reconcile. Conflicting `case`/`case_id` identities
are rejected; six analyzer tests pass. Original manifests and recorded values
are unchanged. The analyzer fix is after timing, not a skill efficiency result.

Keep this adverse result, no favorable rerun or featured promotion. All-eight
developer-outcome and lower-token/faster-time goals remain unfinished. The next
action is complete original evidence review, then a concrete evidenced mechanism
and distinct workflows, rather than another generic compression instruction.

한국어: 16회 원본 토큰을 검산했지만 적용 합계는 토큰18.54%, 시간9.06% 증가했다.
두 지표가 함께 좋아진 과제는 없었다. 품질·보존·범위 상세 검토는 미완료이며,
미적용 SQLite의 범위 위반과 Python 실행 복구도 그대로 보존한다. 노출된 기존
개발 과제이므로 독립 검증이나 전체 절감 근거로 승격하지 않는다.
