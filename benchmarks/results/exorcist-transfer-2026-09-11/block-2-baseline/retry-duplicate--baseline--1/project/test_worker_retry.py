"""Deterministic, in-process experiments; no queue or email service is used.

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_worker_retry
"""

import unittest

from worker import Worker


class WorkerRetryExperiment(unittest.TestCase):
    def test_ack_failure_then_sequential_retry_delivers_twice(self):
        worker = Worker()
        job = "confirmation-1"
        deliveries = []
        trace = []

        def send(job):
            deliveries.append(job)  # Simulate a completed external delivery.
            trace.append("delivered")

        def fail_ack(job):
            trace.append("ack raised")
            raise RuntimeError("injected acknowledgement failure")

        def successful_ack(job):
            trace.append("ack succeeded")

        # The first call has fully exited before the retry starts: no overlap.
        with self.assertRaisesRegex(RuntimeError, "injected"):
            worker.process(job, send, fail_ack)
        self.assertEqual(deliveries, [job])
        self.assertNotIn(job, worker.completed)

        # The exception released the lock, as the context manager promises.
        self.assertTrue(worker.lock.acquire(blocking=False))
        worker.lock.release()
        trace.append("first call exited; retry starts")

        worker.process(job, send, successful_ack)
        self.assertEqual(deliveries, [job, job])
        self.assertIn(job, worker.completed)
        self.assertEqual(trace, [
            "delivered", "ack raised", "first call exited; retry starts",
            "delivered", "ack succeeded",
        ])
        print("\nSequential retry trace: " + " -> ".join(trace), flush=True)

    def test_successful_completion_suppresses_same_instance_retry(self):
        worker = Worker()
        deliveries, acknowledgements = [], []
        worker.process("confirmation-1", deliveries.append, acknowledgements.append)
        worker.process("confirmation-1", deliveries.append, acknowledgements.append)
        self.assertEqual(deliveries, ["confirmation-1"])
        self.assertEqual(acknowledgements, ["confirmation-1"])

    def test_separate_instances_do_not_share_lock_or_completion(self):
        first, second = Worker(), Worker()
        self.assertIsNot(first.lock, second.lock)
        self.assertIsNot(first.completed, second.completed)
        deliveries, acknowledgements = [], []
        first.process("confirmation-1", deliveries.append, acknowledgements.append)
        second.process("confirmation-1", deliveries.append, acknowledgements.append)
        self.assertEqual(deliveries, ["confirmation-1", "confirmation-1"])
        self.assertEqual(acknowledgements, ["confirmation-1", "confirmation-1"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
