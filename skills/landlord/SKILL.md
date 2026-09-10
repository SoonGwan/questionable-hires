---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

## Inspect the lease

Scope the review to the requested design or diff. Read its consumers and existing project conventions. For each material new abstraction, dependency, or configuration surface, identify the behavior it enables, who uses it today, and the ongoing compatibility or maintenance obligation.

Look for an existing implementation, standard library, platform feature, or installed dependency that satisfies the actual requirements. Compare behavior, accessibility, security, portability, and support requirements before recommending a smaller option.

A single consumer can justify a boundary for security, testing, or volatile external APIs. Multiple similar lines do not automatically justify a framework. Don't equate fewer lines, fewer files, or zero dependencies with lower maintenance cost.

Compare the proposed design with the smallest viable alternative on a concrete change the project actually needs: how many places change, what policy is duplicated, and which compatibility promises must remain? Count distinct obligations, not files. Reuse existing checks or a few discriminating examples; don't exhaustively enumerate inputs merely to justify a review recommendation. Keep a layer when removing it only moves its necessary complexity into callers.

## Deliver and stop

Report only actionable costs with file or design references and a suggested alternative. A clean review is valid. Apply changes only when simplification or implementation was requested, preserving validation and behavior.

Stop after the scoped design choices have a defensible keep/simplify/remove recommendation and any requested changes are checked. Don't turn one expensive abstraction into a repository-wide eviction.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Separate observed evidence from inference; keep humor optional. Reuse existing artifacts and report decisive evidence without duplicating full logs.
