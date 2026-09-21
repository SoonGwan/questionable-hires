I’ll inspect `selection.py` and its tests, add the project filter and regression tests, then run the required unittest command.

Implemented keyword-only `project_ids=None` in `selection.py`, preserving archived filtering, order, duplicates, identity, and inputs. Added regression tests for zero, empty iterables, and one-shot iterables; existing tests remain unchanged.

All 6 tests pass with `python3 -B -m unittest discover -v`. No commits or publication.
