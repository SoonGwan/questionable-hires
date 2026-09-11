# Contract-focused design review candidate

Revision `cb43845` compresses general review guidance and prioritizes the actual
contract versus the nearest viable alternative. It retains single-consumer
boundary justification, required behavior/security/accessibility/portability,
concrete maintenance obligations, scope, and review-only authority. The character
is unchanged. This is an efficiency hypothesis, not a previously observed bug fix.

Existing development cases only; serial Astra medium, one sample each, no retry.

| Case / arm | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| adapter-justified / baseline | 62,353 | 28.260 |
| adapter-justified / skill | 49,164 | 22.819 |
| formatter-review / skill | 49,273 | 27.065 |

Both adapter arms correctly preserve the independently changing provider-schema
boundary. Both inspect the same three source/requirements files and execute no
runtime tests. Baseline additionally recommends missing tests; skill limits its
recommendation to the supported design choice and labels its review static.
The single skill sample uses 21.2% fewer tokens and 19.3% less time; this does
not establish repeatability or a causal improvement over the prior skill.

The formatter sample recommends simplifying the unnecessary registry while
retaining the module, exact formatting expression and consumer interface. It
explains why changing display policy does not require registration machinery.
It makes no claim of executed verification. Previous combined-screen formatter
used 83,254 tokens / 32.579 seconds and ran representative values; this latest
static review is not an equal-depth runtime comparison. Its task requested
review, not implementation or executable equivalence proof.

All three traces and empty diffs were inspected; no outside-project commands
or file edits were observed. Existing task criteria are met in both directions:
keep justified compatibility, simplify unsupported extension machinery. These
are exposed synthetic development cases, not production or held-out evidence.
No new broad efficiency claim or chart is justified.

Local evidence: ignored `local-runs/landlord-focused-01` (adapter pair) and
`local-runs/landlord-focused-02` (formatter). Repository and skill validation
pass. A combined current-snapshot screen and representative workload evidence
remain outstanding; don't repeat these unchanged cases for favorable samples.
