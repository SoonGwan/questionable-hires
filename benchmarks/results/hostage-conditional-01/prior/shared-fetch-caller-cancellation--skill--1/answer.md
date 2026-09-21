I’ll use the hostage-negotiator skill to keep the fix focused, add controlled cancellation tests, and run the project’s unittest command.

The bug has two parts: cancellation propagates into the shared fetch, and each caller removes the in-flight entry when it exits. I’ll shield the fetch and let its completion callback clear the entry and retrieve any error, including when all callers have cancelled.

All eight tests pass. The new cases cover shared results and errors, cancellation isolation, late callers joining an active fetch, abandoned-fetch cleanup and retry, and independent keys. The first run exposed a reference retained by the test harness; I corrected that so the abandoned-failure test can detect an unobserved exception.

Fixed `Loader.load` to shield shared fetches from caller cancellation and clear them on completion, observing failures even after all callers cancel. Result/error identity is preserved; completed results aren’t cached.

Added seven controlled tests with bounded waits and owned cleanup. Existing test unchanged.

`python3 -B -m unittest discover -v`: **8 tests passed**. No commits or publication.
