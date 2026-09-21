I’ll use the hostage-negotiator skill to keep this focused on the filter and its regression tests, then run the project’s native test command.

Implemented keyword-only `project_ids=None` in `selection.py`, preserving archive behavior, order, duplicates, identity, and inputs. Zero, empty iterables, and one-shot iterables are covered.

Added six regression tests; existing test preserved. All 7 tests passed with `python3 -B -m unittest discover -v`. No commits or publication.
