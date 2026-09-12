# Mother-in-law frozen confirmation — September 12, 2026

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="comparison-dark.svg">
  <img src="comparison-light.svg" alt="Five-task frozen confirmation comparison. Both arms meet five of five reviewed targets. Skill uses 93.2 percent normalized total tokens and 71.3 percent normalized elapsed time." width="100%">
</picture>

Five previously unexecuted cases and their criteria were committed at `e76efcf`
before execution. Each arm used one fresh GPT-6 Astra medium session. Both arms
met all five reviewed targets, including a guarded clean case; neither produced a
false positive.

Equal-weight task ratios are **93.2% total tokens** and **71.3% elapsed time** for
the skill: reductions of 6.8% and 28.7%. Raw sums are 409,317 versus 370,715
tokens and 317.403 versus 212.049 seconds. One run per cell is descriptive, not a
confidence interval or universal superiority claim.

Verify the published aggregates:

```sh
python3 benchmarks/audit_mother_in_law_checkpoint.py \
  benchmarks/results/mother-in-law-confirmation-2026-09-12
```
