---
name: exorcist
description: Diagnose an uncertain bug by designing experiments that distinguish competing causes, especially speculative cache, timing, environment, or concurrency explanations.
---

# Exorcist

> You keep saying cache. Let's test that belief.

## Separate belief from observation

Capture the symptom, conditions, frequency, and known-good comparison. Trace the affected path enough to form plausible competing explanations. Don't require a fixed number of hypotheses when one is already strongly supported.

Choose the cheapest informative experiment: what observation would support or contradict each explanation? Vary one relevant factor when practical. Keep the failing input and environment comparable. Prefer controlled clocks, requests, or seeds for intermittent failures.

Run the experiment and update the explanation from its actual output. A restart or cache clear that removes symptoms is evidence, but doesn't by itself establish a root cause. Preserve useful logs before resets and don't destroy user state as a diagnostic shortcut.

If an experiment is inconclusive, change the observation or hypothesis rather than repeating it indefinitely. Missing runtime access may leave a ranked diagnosis with a specific next experiment; it cannot justify a confirmed root-cause claim.

## Deliver and stop

Explain the supported causal chain, evidence that rules out relevant alternatives, and smallest corrective action. For a fix request, implement and verify it against the original symptom. For diagnosis, keep the output investigative.

Stop when the cause is supported enough to act on, or the decisive unavailable evidence is identified. Don't expand into a general audit or insist every imaginable alternative be disproved.

## Working agreement

Follow the user's requested outcome and repository conventions. User instructions take precedence over this skill's preferences. Resolve routine choices from available context and keep working within authorized scope. Investigation is not permission to implement or publish. Preserve existing user changes.

Use the user's language. Keep the character to an optional short line; never insult people or substitute a joke for evidence. Report observed facts separately from inferences and unavailable checks. If a skill instruction actually prevents progress, cite that instruction and explain the concrete conflict.

