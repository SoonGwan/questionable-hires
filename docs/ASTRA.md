# The Astra employment contract

This project targets GPT-6 Astra without hardcoding a model into skill files. Select the model in your host. The skills also use the portable Agent Skills format; other-model quality has not been established.

The [official Astra guide](https://developers.openai.com/api/docs/guides/latest-model) describes strong instruction following, clarification behavior, detailed writing, and thorough verification. Our design response is deliberately narrow:

| Tendency | Skill design choice |
| --- | --- |
| Sensitive to instructions in skill files | Make user intent take precedence over character preferences; avoid blanket rules. |
| Clarification can interrupt progress | Resolve routine decisions from context; ask only for consequential missing choices. |
| Verification can expand beyond the task | Define the specific evidence needed and a stopping condition for each hire. |
| Detailed formatted answers | Lead with the result, retain technical evidence, and keep jokes optional and brief. |

Those are design choices informed by the guide, not experimentally demonstrated improvements. A skill's wording does not enable async tools, select a reasoning effort, grant permissions, or create access to a browser.

## What a comparison must hold constant

Use the same model, reasoning setting, tools, starting code, task, and permitted actions. Run baseline and skill variants in clean independent sessions. Avoid unrelated installed skills contaminating the baseline. Give the evaluator the raw task, not the expected diagnosis. Judge findings against executable behavior and sources, not matching phrases.

Record unsuccessful runs and environmental failures. Separate findings, correctness, scope drift, and cost. Don't use fewer words as a proxy for a better fix, or claim an improvement from one favorable example.

See the [evaluation plan](EVALUATION.md) for case-specific expectations.
