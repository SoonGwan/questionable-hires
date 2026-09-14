# Con Artist core-guide candidate 01 — 2026-09-14

Previous source `58d31fb`; this is a documentation candidate, not a model result.
In [checkpoint 08](BUNDLE-CONTRACT-08-REVIEW.md), Con Artist read the core guide
and the full 27,725-character audit implementation before one supported audit.
It used 102,509 tokens versus baseline 82,484, despite lower elapsed time.
The trace supplies a cost mechanism to investigate, not proof that documentation
length caused that difference or that legitimate trust review should be forbidden.

The routine guide now keeps the executable CLI recipe, selection/binding rules,
actual output interpretation, integrity boundaries and operational limits together.
Conditional single-fault probes are explained in place; fixture-native probes,
batch reuse and source-root setup still route to the existing advanced guide.
Process-group cleanup mechanics move to its existing cleanup section. Required
foreground work and unsupported background/escaped groups stay in the core.
Source inspection remains appropriate for concrete trust/adaptation/troubleshooting.

| Documentation | Previous bytes | Candidate bytes | Change |
| --- | ---: | ---: | ---: |
| Routine core | 7,189 | 5,190 | −27.81% |
| Core plus advanced | 16,683 | 15,136 | −9.27% |

Core word count is 925 → 629. These are document measurements, **not** model tokens
or an accepted performance gain. SKILL.md and executable runtime are unchanged.

Local validation after the edit:

- 76 mutation-helper tests pass in 14.333s, covering intended fault detection,
  surviving faults, import/precheck/setup failures, conditional/native probes,
  output/deadline/integrity limits and process cleanup.
- 12 packaging tests pass in 3.122s. The existing shipped-recipe test extracts the
  actual JSON from this guide, executes the bundled CLI on the real example files,
  and checks correct-code passes, surviving original assertions, the stronger
  intended AssertionError, same-process binding output and preserved originals.
- Skill structure validation passes. No model timing overlaps these tests.

Next evidence needed: a frozen model adoption/transfer screen that records reads,
all required audit checks, original output gaps and costs. Do not substitute this
byte reduction for model efficiency or overwrite historical/featured graphs.
