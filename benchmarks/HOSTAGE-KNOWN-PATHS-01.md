# Hostage known-path routing candidate — qualified transfer evidence

The [combined gate](BUNDLE-CURRENT-02-REVIEW.md) records six shell calls for
`necessary-state` skill versus three for baseline. Inspection of the retained
skill commands shows four preparation calls:

1. `pwd` and a filename-pattern inventory.
2. Skill entrypoint read and `ls -a`.
3. Direct reads of `requirements.md` and `form.py`.
4. Git status and another hidden-file inventory.

The remaining calls execute tests and inspect final changes. This observation
does not attribute tokens to individual calls or establish that all discovery
was redundant: applicable instructions and missing tests still need finding.
The arms also differ in cancellation coverage and retained tests, so the old
timing difference is not an equal-work optimization target.

[Compact regression](HOSTAGE-COMPACT-01.md) likewise records fragmented
discovery despite the existing instruction to batch independent reads. The
[packaging pair](PACKAGING-REPAIR-01.md) records an empty AGENTS search whose
success-only chain leaves status unrun. More commands do not necessarily mean
more tokens: that skill pair has lower raw tokens with unequal coverage.

The candidate replaces the first discovery paragraph: reuse supplied guidance
and known paths, read a located file directly rather than issuing further
filename-pattern inventories, batch known independent reads, and derive the
runner/unresolved searches from inspected content. It adds no helper or reference
lookup to the skill. It does not forbid legitimate new discovery, prescribe one
inventory for every repository, or remove state/cancellation/verification rules.

This is a workflow hypothesis supported by recorded preparation behavior, not
proof of improved adoption, fewer calls, tokens or time. Do not rerun the exposed
form task solely for better numbers. Validate on a distinct scoped change with
known and unknown paths, actual acceptance tests, preserved user files and a
contemporary baseline before making any performance claim. Existing experiments
and featured charts remain tied to their frozen revisions.

The next [atomic-export transfer](HOSTAGE-ATOMIC-EXPORT-01-PROTOCOL.md) now has
an authored input contract and actual before-fail/after-pass fixture preflight.
[Both model sessions](results/hostage-atomic-export-01/README.md) now complete:
desired direct-read behavior occurs, but baseline uses the same two preparation
calls. Raw tokens −12.85% / time −8.43% have extra-work and temporary-root
limitations, not a causal discovery improvement.
