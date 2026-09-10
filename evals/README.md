# The interview room

`fixtures/behavior.py` contains intentional defects and corrected variants. The oracle tests in `tests/test_evaluation_fixtures.py` execute them with controlled inputs, futures, and an in-memory database. No arbitrary sleeps or external services are needed.

```sh
python3 -m unittest discover -s tests -p test_evaluation_fixtures.py -v
```

These demonstrate five known behaviors: a boundary error, stale response overwrite, navigation before persistence, a surviving persistence mutation, and schema incompatibility with an old reader. They support preparing evaluations for Receipt, Mother-in-law, Exorcist, Necromancer, Con Artist, and Friday.

They are not completed skill evaluations. Do not expose corrected variants, oracle tests, or diagnosis-bearing names to a blind model evaluation. Prepare a separate neutral fixture from the faulty behavior and give only the user-visible symptom. Necromancer's historical cases also need a real synthetic Git history; the asynchronous example alone does not establish that capability.

Landlord and Hostage Negotiator need realistic multi-file change fixtures. Full case coverage and independent Astra comparisons remain in the [evaluation plan](../docs/EVALUATION.md).
