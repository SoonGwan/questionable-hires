Python 3.9+ standard library, cooperative asyncio in one loop.
Each fetch call creates its own Request, even with repeated keys. Its application
task returns the exact object chosen through that Request.complete. The test owns
application tasks. Cancelling a pending started waiter must reach that waiter and
must not consume an undelivered request or cancel its application task. Already
delivered handles are consumed; later cancellation does not undo delivery.
No network, threads, browser or blocking code is in scope.
