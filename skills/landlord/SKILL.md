---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

## Inspect the lease

Start with supplied paths and contracts. For unknown locations, discover filenames first; for known files, read relevant definitions and consumer context rather than dumping every keyword match before reading them again. Batch independent reads with line numbers and reuse inspected context. Search unresolved consumers in relevant source, tests and configuration, expanding when needed; narrow results cannot prove absence. Installed skills and copied examples are not consumers without a supported usage/binding. Stay within project scope.

Compare the nearest viable alternative against behavior, accessibility, security, portability and support contracts. Stop surveying once decision-changing differences settle the choice.

A single consumer may justify security, testing or API separation; repetition or fewer lines alone does not justify an abstraction.

Trace a concrete needed change: where does policy move, and which compatibility promises survive? Removing a layer must not merely spread its complexity into callers. Execute for decision-changing unknowns or explicit requirements, not to reconfirm settled source facts. Static analysis cannot establish unresolved runtime behavior.

When executing, reuse a known lightweight relevant test group. Narrow for runtime, setup, side effects or isolation, not test count alone; retain decision-changing probes.

## Deliver and stop

Lead with keep, simplify or remove, costs and source references; distinguish observation from inference. A clean review is valid. Stop at the supported recommendation and required checks. Review authorizes neither edits nor publication. Implement only when requested, preserving user changes and required verification. Humor is optional.
