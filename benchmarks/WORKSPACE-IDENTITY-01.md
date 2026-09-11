# Workspace identity: remove an observed alias mismatch, not a proven patch cause

The two skill traces in [Receipt profile 01](RECEIPT-PROFILE-01.md) each contain
an outside-project patch rejection without a captured rejected target. Their
metadata workspace begins `/var/folders/`, while shell `pwd` begins
`/private/var/folders/`. On this host, Path.resolve and samefile confirm these
temporary-root spellings name the same directory. Accepted file-change events
use the `/var` spelling; this does not reveal which path the rejected attempt used.
Neither those captures nor the inspected [official security documentation](https://learn.chatgpt.com/docs/security)
establish that aliases caused the rejection. Do not relabel prior scope unknowns.

Runner `fd8d578` resolves its allocated temporary workspace before preparation,
resource installation, CLI `-C` and evidence capture. Metadata also retains the
allocated spelling. This applies equally to baseline, control, skill and auto;
no extra writable root, sandbox relaxation, skill change or altered task prompt.
Historical reports and adverse samples remain unchanged. Future reports must
identify this runner revision rather than silently pool path environments.

The regression uses a real directory symlink and actual Git fixture preparation
for all four arms, intercepting only the model launch. It checks physical `-C`,
same directory identity, unchanged sandbox arguments, resource integrity and
retained artifacts. Running it against the previous runner produces four expected
alias-versus-physical-path assertion failures; the changed runner passes. All 14
runner tests and 144 repository tests pass (full suite: 16.067 seconds).

This proves consistent launch-path plumbing, not actual Codex patch acceptance,
lower model cost or improved skills. No model session was launched for this audit.
Do not add a skill-wide path rule or claim the repeated patch problem solved
without direct runtime evidence. The performance objective remains unmet.
