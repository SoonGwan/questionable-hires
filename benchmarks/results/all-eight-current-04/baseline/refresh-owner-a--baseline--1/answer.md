I’ll compare `Preview.refresh` with the requirements, add controlled async tests, and run the requested unittest command.


`refresh` clears `pending` unconditionally, so an earlier call can clear it while the latest call is still running. I’ll guard that cleanup with the existing generation check and test both completion orders, failures, cancellation, retries, and instance isolation using controlled futures.


Fixed `preview.py` so only the latest-started refresh clears `pending`.

Added 8 standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual `python3 -B -m unittest discover -v` result: **8 tests ran, all OK**, in 0.041s. **Process exit: 0.**
