# Pick the job before the coworker

[한국어](CHOOSE-A-HIRE.ko.md) · [Examples](../examples/README.md) · [Install](INSTALL.md)

Start with the outcome you need now. One hire can be enough; installing eight
does not mean loading eight into every task. A routine edit with clear behavior
and existing tests may need no special skill. This is usage guidance, not a
measured token-saving claim.

| What you need | Start with | Evidence to expect |
| --- | --- | --- |
| Find the cause of an uncertain bug | `$exorcist` | An observation that distinguishes causes, or the specific missing observation. |
| Check that a fix prevents the reported bug | `$receipt` | The relevant failure before and success after, with comparable inputs; unavailable evidence stays explicit. |
| Check whether a passing test would catch broken behavior | `$con-artist` | A valid baseline, a meaningful isolated fault, and the assertion that detects it—or fails to. |
| Test a changed interaction across response order, repeats and recovery | `$mother-in-law` | Product-state assertions through relevant transitions, using the actual interaction path. |
| Deliver a small change threatened by unrelated redesign | `$hostage-negotiator` | The requested behavior and necessary prerequisites, verified without optional refactoring. |
| Decide whether legacy behavior can be removed | `$necromancer` | Current consumers/contracts, relevant history, and keep/replace/remove reasoning. |
| Decide whether an abstraction earns its cost | `$landlord` | Concrete consumers and tradeoffs against the nearest viable simpler design. |
| Assess a proposed release and its recovery path | `$friday` | Reachable version/data states, the first incompatible step, and recovery limits. |

## Three distinctions that prevent the wrong assignment

**Cause, fix, or test quality?** Exorcist investigates why it happens. Receipt
checks whether a particular fix prevents it. Con Artist checks whether the tests
would notice a fault. A green suite alone answers none of these automatically.

**Interaction QA or implementation scope?** Mother-in-law is for interaction
coverage. Hostage Negotiator is for delivering a focused change, including state
handling if the behavior requires it. Neither implies browser verification when
only a Python component was exercised.

**Historical reason or design cost?** Necromancer traces current necessity and
origin separately. Landlord compares maintenance/behavior tradeoffs. One consumer
can justify a boundary; an old comment cannot establish a current dependency.

## Give the next hire the evidence, not the whole ceremony

If diagnosis is already settled, provide that result and go directly to the
requested fix or verification. Change hires when the job changes; do not make a
second hire rediscover a supported fact solely for its personality.

For example, adapt this to your actual files and runner:

```text
$receipt Verify the fix in src/submit.py; don't change production code.
The recorded failure is in evidence/before.txt and the retained regression is
tests/test_submit.py. Check whether those inputs still match this fix, use the
project's native runner, and distinguish missing evidence from a passing result.
```

Include the behavior, relevant paths, known evidence and allowed changes. Say
whether you want diagnosis, review, tests or implementation. Do not invent paths
or prior results to fill this template. Review does not authorize implementation;
release review does not authorize deployment, migration or a restore drill.

## When terminal output is unreliable

Hostage's optional [native evidence recipe](../skills/hostage-negotiator/references/native-evidence.md)
retains a new check's command, native output and exit in a fresh allowed local
directory. Prefer existing reports and read retained results before repeating
work. It does not recover a past missing transcript, supply a process deadline,
or permit extra writes in a read-only task. Logs can contain secrets; don't
publish them automatically.

The recipe was used in [two synchronous skill sessions](../benchmarks/HOSTAGE-FLAG-01-REVIEW.md).
Both baseline sessions also retained evidence. Those small comparisons have
unequal work and do not prove broad superiority. Consult the
[current evidence](../benchmarks/CURRENT-CANDIDATE-STATUS.md) for measured limits.
