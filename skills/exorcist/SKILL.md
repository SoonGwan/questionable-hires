---
name: exorcist
description: Diagnose an uncertain bug by designing experiments that distinguish competing causes, especially speculative cache, timing, environment, or concurrency explanations.
---

# Exorcist

> You keep saying cache. Let's test that belief.

## Find the decision-changing observation

Start at the reported failure and trace only enough of its path to distinguish plausible causes. Reuse existing reproduction evidence. Do not manufacture a hypothesis list when the mechanism is already established.

Before another experiment, identify which possible result would change the diagnosis or corrective action. Prefer the cheapest check that separates those outcomes. Reuse one small harness; vary a relevant factor with comparable inputs and controlled timing. Repetition is useful for unresolved intermittency, not for collecting more passing output.

Exercise the affected implementation, not a rewritten model of it. If a suspected dependency is absent and the symptom persists, it is unnecessary for that reproduction—not disproved in every production incident. Explain why the existing safeguard does or does not address this mechanism, rather than merely showing its setting.

When evidence is missing, identify the specific observation that would discriminate remaining causes. Don't replace unavailable runtime evidence with increasingly elaborate simulations. A restart that removes symptoms is not by itself causal proof; preserve logs and user state before any authorized reset.

## Finish at the evidence boundary

Report the supported mechanism, decisive command/result, relevant alternative or safeguard, and remaining uncertainty. Link a retained reproduction instead of repeating its full code and output. Keep humor optional.

For diagnosis, leave production code unchanged. For a requested fix, implement within scope and rerun the original reproduction plus relevant checks. Preserve user changes and explicit requirements.

Stop when the evidence supports the next action or identifies the unavailable check. Continue only for an unresolved distinction or verification the task requires—not a general audit.
