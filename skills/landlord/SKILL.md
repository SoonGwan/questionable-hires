---
name: landlord
description: Review proposed abstractions, dependencies, and configuration for concrete consumers and maintenance cost when simplifying a design or checking overengineering.
---

# Landlord

> Who's paying rent on this abstraction?

## Inspect the lease

Read the design, actual consumers and contracts together, within the requested project boundary. Resolve paths from the real tree or references. For source excerpts likely to support the recommendation, retain line numbers on first inspection rather than rereading unchanged code solely for citations.

Compare the nearest viable project/platform alternative on differences that could change the recommendation. Preserve behavior, accessibility, security, portability and support contracts; stop surveying alternatives when those contracts settle the choice.

A single consumer can justify a security, testing or external-API boundary. Repeated lines alone do not justify a framework. Fewer lines, files or dependencies are not evidence of lower maintenance cost.

Use a concrete needed change: which policy changes, where does it live, and which compatibility promises survive? Keep a layer when removal merely moves necessary complexity into callers. Reuse existing evidence; execute a discriminating check only for unresolved equivalence or consequential behavior, plus explicitly required checks.

Prefer a known lightweight relevant test group over constructing a smaller selection. Narrow when runtime, setup, side effects or isolation justify the selection work; fewer tests alone aren't savings. Retain distinct probes that resolve the recommendation.

## Deliver and stop

Lead with keep, simplify or remove, actionable costs and file/design references. A clean review is valid; distinguish observations from inference. Implement only when requested, preserving user changes, validation and behavior. Review authorizes neither edits nor publication. Stop at the supported scoped recommendation and required checks, not repository-wide cleanup. Keep humor optional.
