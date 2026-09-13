I’m using the mother-in-law skill to add standalone component regressions for overlapping submissions, then run the requested unittest command. I’ll preserve production code and leave any discovered bug as a failing test.



The identical-query regression fails at the final checkpoint: the older response overwrites the newest payload. Seed retention and newest completion pass, as does the different-query control. The fetch-key mismatch check also passes, confirming that an incorrect key raises the intended assertion.



Extended `test_search.py`, preserving the initial-state test.

Ran `python3 -B -m unittest -v test_search`: **4 tests, 1 failure**.

- Both sequences preserve the complete seeded payload after each submission and display the newest response.
- Different-query reverse completion passes.
- Identical-query reverse completion fails: the older payload replaces the newest. `Search.submit` compares query values rather than request identity.
- Fetch-key assertion verification passes.

Requests are controlled separately; waits and task cleanup are bounded to one second. The bug remains a failing regression. Production files are unchanged; no scratch was created.

This was component QA, not browser QA.
