I’m using the con-artist skill to run the six fault/test combinations in independent disposable copies, verify the two gap assertions, and check that all original files remain unchanged.



Both selected tests use September 17: `testNextMonth` checks a one-month increment, while `testNextFriday` checks Wednesday-to-Friday movement. Neither exercises a day above 28 or an already-matching weekday. Two existing upstream tests cover the requested gap assertions, so I’ll reuse them unchanged.



Only `testNextMonth` detected the ignored-months regression. Both selected tests missed the other two regressions.

| Independent `__add__` fault | `testNextMonth` | `testNextFriday` |
|---|---|---|
| Replace destination month length with 28 | PASS: survives | PASS: survives |
| Add seven days when a positive weekday already matches | PASS: survives | PASS: survives |
| Replace `month += self.months` with `month += 0` | **FAIL: detected** | PASS: survives |

Both selected tests passed on correct code; those controls were reused across the three comparisons. Every PASS exited 0; every FAIL exited 1 with an actual `AssertionError`, not a setup error.

`testNextMonth` asserts October 17, 2003 at `20:54:47.282310`. Ignoring months produced September 17 with the same time, failing its assertion at line 63. Day 17 cannot expose the 28-day cap, and this test requests no weekday.

`testNextFriday` asserts September 19 from Wednesday, September 17. Its dates stay below 28, its starting weekday does not already match Friday, and it requests no relative months—explaining all three survivors.

The requested gap assertions were verified using unchanged upstream witnesses:

| Witness assertion | Correct code | Matching faulty code |
|---|---|---|
| `testLastDayOfFebruaryLeapYear`: `date(2020, 2, 1) + relativedelta(day=31) == date(2020, 2, 29)` | PASS, February 29 | **AssertionError:** February 28 ≠ February 29 |
| `testNextWednesdayIsToday`: `date(2003, 9, 17) + relativedelta(weekday=WE) == date(2003, 9, 17)` | PASS, September 17 | **AssertionError:** September 24 ≠ September 17 |

All 12 observations used the supplied interpreter, from each disposable copy root, with:

```text
<supplied-python> -B -m unittest tests.test_relativedelta.RelativeDeltaTest.<method> -v
```

`PYTHONPATH` selected each copy’s `src/`. Instrumentation verified the test module’s imported class identity and copied `__add__` implementation path **inside every test process**, then logged assertion operands while retaining native assertions.

All upstream test bodies remained unchanged. Original file bytes, modes, and paths were verified unchanged after cleanup; no scratch, harness, or report remains.
