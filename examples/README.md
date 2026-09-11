# Employee incident reports

These examples link to actual independent Astra runs, including the no-skill and short-instruction controls. They are small synthetic tasks, with one run per condition. Ties are shown honestly.

- [The fallback has a paying customer.](necromancer.md) — necromancer
- [The receipt is an actual failing test.](receipt.md) — receipt
- [One formatter. An entire rental property.](landlord.md) — landlord
- [She typed another letter. Your results went backward.](mother-in-law.md) — mother-in-law
- [The cache has an alibi.](exorcist.md) — exorcist
- [The button was released unharmed.](hostage-negotiator.md) — hostage-negotiator
- [The test congratulated a missing write.](con-artist.md) — con-artist
- [The down migration exists. The rollback still breaks.](friday.md) — friday

Every example includes the ticket, observed result, limitations, raw command evidence, and a reproduction command. Start with Necromancer for historical context, Mother-in-law for interaction failures, or Con Artist for tests that miss broken behavior.

For a no-account first try, [replay the retained interaction test](mother-in-law.md#try-the-retained-test-without-model-usage)
or [run the two-fault audit](con-artist.md). An expected failing regression
demonstrates an application defect; a launch/setup failure does not. Both examples
separate local replay from new model evaluation and its usage costs.

## Real repository follow-up

[Clean up the failed build. Leave the company standing.](packaging-repair.md)
uses this project's actual packaging code. It includes the repair request,
baseline/skill coverage differences and a current-source check command. Unlike
the eight archived examples above, its original model logs remain local and are
not published raw evidence. The task now has a real integrated fix.

## A package-level Receipt

The [Receipt follow-up](receipt.md#when-the-fix-spans-a-package) shows a two-module
historical comparison and a local, no-model-usage reproduction. It also keeps the
mixed cost result visible: less elapsed time, more tokens. Its follow-up report
does not provide publicly archived raw model logs like the original example.
