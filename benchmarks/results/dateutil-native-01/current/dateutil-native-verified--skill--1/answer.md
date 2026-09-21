I’m using the con-artist skill to run the six fault/test combinations in independent disposable copies, verify the gap assertions, and check that all original files remain unchanged.


Both selected tests start on day 17, and the Friday test starts on a Wednesday. Those inputs appear to miss the day-28 cap and the already-matching weekday fault. I found upstream tests for both requested gap assertions and will run them unchanged against correct and faulty copies.


Only `testNextMonth` detected a requested regression: ignoring relative months. The other five fault/test combinations passed.

| Independent fault in `relativedelta.__add__` | `testNextMonth` | `testNextFriday` |
|---|---|---|
| Replace destination month length with 28 | PASS — survives | PASS — survives |
| Add seven days for an already-matching positive weekday | PASS — survives | PASS — survives |
| Replace `month += self.months` with `month += 0` | **FAIL — detected** | PASS — survives |

Both selected tests passed on correct code; that single matching baseline was reused across the three faults.

The detecting assertion compares the complete datetime. Ignoring months produced this native failure at test line 63:

```text
AssertionError: datetime.datetime(2003, 9, 17, 20, 54, 47, 282310)
!= datetime.datetime(2003, 10, 17, 20, 54, 47, 282310)
```

The surviving gaps follow from the inputs: both tests start on day 17, below the cap. `testNextMonth` requests no weekday. `testNextFriday` moves from Wednesday to Friday, so it never exercises an already-matching weekday; it also requests no relative months.

Both requested gap assertions were verified using unchanged upstream witness tests:

| Witness and assertion | Correct code | Matching fault |
|---|---|---|
| `testLastDayOfFebruaryLeapYear`: `date(2020, 2, 1) + relativedelta(day=31) == date(2020, 2, 29)` | PASS, exit 0 | FAIL, exit 1: `2020-02-28 != 2020-02-29` |
| `testNextWednesdayIsToday`: `date(2003, 9, 17) + relativedelta(weekday=WE) == date(2003, 9, 17)` | PASS, exit 0 | FAIL, exit 1: `2003-09-24 != 2003-09-17` |

Every execution used the supplied interpreter with `-B -m unittest <selectors> -v` from its disposable copy root. Same-process checks verified copied imports and that all four test methods bound `relativedelta` to the copied implementation, including its `__add__`. All failures were assertion failures; no setup errors or skips occurred.

The entire test file stayed unchanged in every copy. Whole-project integrity checks confirmed original bytes, modes, and paths unchanged, and all owned scratch was removed. No harness or report was retained.
