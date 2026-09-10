# The interview room

`fixtures/behavior.py` contains intentional defects and corrected variants. The oracle tests in `tests/test_evaluation_fixtures.py` execute them with controlled inputs, futures, and an in-memory database. No arbitrary sleeps or external services are needed.

```sh
python3 -m unittest discover -s tests -p test_evaluation_fixtures.py -v
```

These demonstrate five known behaviors: a boundary error, stale response overwrite, navigation before persistence, a surviving persistence mutation, and schema incompatibility with an old reader. They support preparing evaluations for Receipt, Mother-in-law, Exorcist, Necromancer, Con Artist, and Friday.

These fixtures alone are not skill evaluations. The separate [benchmark runner](../benchmarks/README.md) prepares neutral project files without corrected variants or oracle tests, and creates real synthetic Git history for Necromancer. Actual session results are available in the [report](../benchmarks/REPORT.md).

Landlord and Hostage Negotiator have multi-file synthetic cases in the benchmark suite. Repeated trials and larger real-project cases remain in the [evaluation plan](../docs/EVALUATION.md).
