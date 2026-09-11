---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

## Inspect the lease

Inspect supplied design/code paths and their consumers/contracts within project scope. Search unresolved callers in relevant source, test and configuration roots first. Installed skill examples or copied documentation are not application consumers merely because text matches; follow them when imports, configuration or supported usage makes them relevant. Expand when needed—a narrow search cannot prove consumers absent. Retain citation line numbers on first source inspection.

Compare the nearest viable project/platform alternative on decision-changing differences. Preserve behavior, accessibility, security, portability and support contracts; stop surveying when they settle the choice.

A single consumer can justify a security, testing or external-API boundary. Neither repetition nor fewer lines/files/dependencies establishes the right abstraction.

Test the design against a concrete needed change: where will policy live, and which compatibility promises survive? Removing a layer can merely move necessary complexity into callers. Reuse evidence; execute checks for unresolved equivalence, consequential behavior or explicit requirements.

Prefer a known lightweight relevant test group. Narrow for runtime, setup, side effects or isolation—not test count alone. Retain decision-changing probes.

## Deliver and stop

Lead with keep, simplify or remove, concrete costs and references; separate observations from inference. A clean review is valid. Stop at the supported recommendation and required checks. Review authorizes neither edits nor publication; implement only when requested, preserving user changes, validation and behavior. Keep humor optional.
