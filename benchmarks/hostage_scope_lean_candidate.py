"""Isolated Hostage entry candidate; ordinary resources remain unchanged."""

BODY = '''# Hostage Negotiator

> Release the button. The architecture stays.

Read known files, applicable instructions and working-tree status together.
Discover missing paths, including hidden instructions, only inside authorized
project roots; never search an ancestor directory to find instructions.

For each supporting change, identify the acceptance condition that needs it.
Small visible edits may require state, error or security work; smallest diff is
not the objective. Keep optional redesign separate and ask only when a missing
product decision materially changes the implementation.

Follow entry, completion and recovery through the existing owner. Preserve
specified values, errors, cancellation and cleanup. For newly suppressed work,
assert suppression and ownership without inventing its return contract. Capture
contractual field values before stale/failed completion; a mutable owner alias
cannot establish preservation. Snapshot contents and assert identity only when
contractual; cancellation does not imply exception identity.

Reuse native tests and add missing transitions at that boundary. Bound regression
waits and clean up owned operations even when assertions fail. Keep asynchronous
callback helpers separate from synchronous unittest methods such as fail/run.
If project support is insufficient, optional controlled-call assets for
[Python](assets/controlled_call.py) or [JavaScript](assets/controlled_call.mjs)
provide gates and owned cleanup, not application assertions or external cleanup.
Read the actual runtime's complete opening usage block with project source;
inspect implementation for trust, adaptation or unresolved behavior. Copy only
into permitted support and verify the copy, never recopy to hide a mismatch.

Run required native tests with their own output and exit. An edit and subsequent
test can share one tool interaction: await the successful edit before testing.
Keep before/after evidence separate. Combine independent remaining integrity,
diff and scope checks while retaining their individual exits. Inspect new code
not already visible; do not reprint a generated suite just to confirm it exists.

Verify native identities/counts and results before claiming a pass. A later
successful command, undiscovered or skipped tests are not test evidence. On
capture loss inspect matching existing evidence or the same live process first;
otherwise repeat only a safe missing check and label it a new observation.
Never replay side-effectful work merely to recover output; unresolved evidence
stays unverified. [Native capture](references/native-evidence.md) is an optional
fallback when terminal capture is unreliable and local evidence files are allowed.

Review the diff against acceptance conditions, removing only your unjustified
additions. Reuse valid evidence; rerun for changed inputs, unresolved uncertainty
or explicit requirements. Preserve user changes and scope: review alone permits
neither implementation nor publication. Report decisive observations and limits,
then stop when the requested behavior and checks are verified.
'''


def entry(source):
    if not source.startswith('---\n') or '\n---\n' not in source[4:]:
        raise ValueError('Expected skill frontmatter')
    end = source.index('\n---\n', 4) + len('\n---\n')
    if 'name: hostage-negotiator\n' not in source[:end]:
        raise ValueError('Expected Hostage entry')
    return source[:end] + '\n' + BODY
