"""Deterministic local experiment; callbacks never contact external services."""

from worker import Worker


def main():
    job = "confirmation-123"
    worker = Worker()
    deliveries = []
    events = []
    ack_attempts = 0

    def send(job):
        # Model an email delivery that succeeds independently of queue ack.
        deliveries.append(job)
        events.append("send succeeded")

    def acknowledge(job):
        nonlocal ack_attempts
        ack_attempts += 1
        if ack_attempts == 1:
            events.append("acknowledge raised")
            raise RuntimeError("injected acknowledgement failure")
        events.append("acknowledge succeeded")

    # All calls run sequentially in one thread on one Worker instance.
    try:
        worker.process(job, send, acknowledge)
    except RuntimeError as error:
        assert str(error) == "injected acknowledgement failure"
    else:
        raise AssertionError("expected acknowledgement failure")

    assert deliveries == [job]
    assert job not in worker.completed
    assert worker.lock.acquire(blocking=False), "exception must release lock"
    worker.lock.release()
    print("After failure: deliveries=1, completed=False, lock released")

    worker.process(job, send, acknowledge)
    assert deliveries == [job, job]
    assert job in worker.completed
    assert ack_attempts == 2
    print("After sequential retry: deliveries=2, completed=True")

    worker.process(job, send, acknowledge)
    assert deliveries == [job, job]
    assert ack_attempts == 2
    print("After third call: deliveries=2, acknowledgement attempts=2")
    print("Trace:", " -> ".join(events))

    other = Worker()
    assert other.lock is not worker.lock
    assert other.completed is not worker.completed
    assert job not in other.completed
    # Even holding the first worker's lock cannot block the second instance.
    with worker.lock:
        other.process(job, send, acknowledge)
    assert deliveries == [job, job, job]
    assert job in other.completed
    print("Separate instance, while first lock held: deliveries=3")
    print("PASS: duplicate sends reproduced without simultaneous workers")


if __name__ == "__main__":
    main()
