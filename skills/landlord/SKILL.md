---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

## Inspect the lease

Read the requested design, its actual consumers and project contracts together. Identify the behavior each material layer enables and the obligation it owns. Keep discovery inside any explicitly restricted project boundary.

Resolve related files from the actual repository listing or references before opening guessed paths. Reuse discovered paths. If a file is absent, locate the relevant symbol or contract in the real tree rather than repeating that read or guessing neighboring filenames.

Compare with the nearest viable alternative already available in the project or platform. Focus on differences that could change the recommendation; don't survey replacements once the current contract settles the choice. Preserve applicable behavior, accessibility, security, portability and support requirements.

A single consumer can justify a security, testing or external-API boundary. Repeated lines alone do not justify a framework. Fewer lines, files or dependencies are not evidence of lower maintenance cost.

Use a concrete needed change to compare distinct obligations: what policy must change, where does it live, and which compatibility promises survive? Keep a layer when removing it merely moves necessary complexity into callers. Reuse existing evidence; execute a discriminating check when equivalence or a consequential behavior is unresolved, not a broad suite merely to decorate a review.

When execution is needed, prefer an existing relevant test group known to be lightweight over repeatedly inspecting tests to construct a smaller selection. Narrow further when runtime, setup, side effects or isolation justify that selection work. Test count alone is not the cost; keep any distinct probe needed to resolve the recommendation.

## Deliver and stop

Lead with keep, simplify or remove, supported by actionable costs and file/design references. A clean review is valid. Implement only when requested, preserving user changes, validation and behavior; review does not authorize edits or publication.

Stop when the scoped recommendation and required checks are supported. Don't expand into repository-wide cleanup. Separate observed results from inference; keep humor optional.
