<div align="center">

# questionable-hires

**Weird, but employed. Unfortunately, essential.**

A suspiciously effective engineering team for your AI agent.

One demands receipts. One charges your abstractions rent.<br>
One talks to developers who left in 2019.<br>
Hiring was a mistake. Firing them would be worse.

</div>

---

## Meet your coworkers

Eight instruction-based skills are implemented. Install the whole team or choose a hire. Behavioral evaluation is in progress; there are no performance claims yet.

| Hire | What they say | What they actually do |
| --- | --- | --- |
| **Necromancer** | “The previous developer left. Their reasons didn't.” | Reconstruct why strange code exists from history, callers, and tests before you change it. |
| **Receipt** | “You fixed it? Show me the receipt.” | Connect a bug reproduction to a failing-before, passing-after check. |
| **Landlord** | “Who's paying rent on this abstraction?” | Check whether new abstractions and dependencies earn their maintenance cost. |
| **Mother-in-law** | “And what happens if I click it twice?” | Exercise realistic user behavior: retries, navigation, stale responses, and empty states. |
| **Exorcist** | “You keep saying cache. Let's test that belief.” | Turn debugging guesses into experiments that distinguish competing causes. |
| **Hostage Negotiator** | “Release the button. The architecture stays.” | Keep a small requested change from becoming an unrelated refactor. |
| **Con Artist** | “Your mock is very impressed with itself.” | Find tests that still pass when the behavior they claim to protect is broken. |
| **Friday** | “Can Monday-you undo this?” | Examine deployment changes for rollback, compatibility, and configuration traps. |

## First hire: Necromancer

**Illustrative interaction — not an executed result:**

```text
You: Can we delete this setTimeout?

Necromancer:
This delay was added after navigation started racing the save request.
The current caller still doesn't await the save.

Replace the timing assumption with explicit completion before removing it.
Evidence: introducing commit, current caller, reproduction.

The haunting is asynchronous.
```

The joke should explain the engineering instinct. The output should earn your trust with evidence.

## Built with Astra in mind

Our target is GPT-6 Astra. That's a development target, not a benchmark claim.

Each skill defines a narrow job, the evidence it needs, and a clear stopping condition. Ordinary implementation decisions follow project context. User intent takes precedence over the character. Humor stays brief; findings stay concrete. See the [Astra design notes](docs/ASTRA.md).

We'll compare skills against the same model without the skill, on the same task and starting code. We'll track correctness, useful findings, unnecessary changes, and task cost where measurable. No performance numbers until there are reproducible results.

## Hiring status

**Private development preview. Eight skills, a local installer, and a validated plugin manifest.**

Start with [onboarding](docs/INSTALL.md), then invoke a hire:

```text
$necromancer Can this workaround be removed?
$receipt Show that this fix actually changes the behavior.
$mother-in-law Try the awkward sequences in this checkout flow.
```

No lifecycle hooks. No background workers. No model configuration changes.

- [Hiring plan](docs/ROADMAP.md)
- [How we hire](CONTRIBUTING.md)
- [Skills directory](skills/README.md)
- [Performance review plan](docs/EVALUATION.md)

## Inspiration

[Ponytail](https://github.com/dietrichgebert/ponytail) showed how a memorable character can carry a concrete engineering habit. This project explores a whole team of those habits with original skill instructions.
