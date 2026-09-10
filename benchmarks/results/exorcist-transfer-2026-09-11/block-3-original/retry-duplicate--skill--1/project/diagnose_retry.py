"""Deterministic local diagnosis; no network, threads, or real email delivery."""

from worker import Worker


def experiment(fail_first_ack):
    worker = Worker()
    job = "confirmation-123"
    deliveries = []
    events = []
    ack_calls = 0

    def assert_lock_held():
        acquired = worker.lock.acquire(blocking=False)
        if acquired:
            worker.lock.release()
        assert not acquired, "Callback ran without the worker's lock held"

    def send(current_job):
        assert_lock_held()
        deliveries.append(current_job)
        events.append("send accepted (lock held)")

    def acknowledge(current_job):
        nonlocal ack_calls
        assert current_job == job
        assert_lock_held()
        ack_calls += 1
        if fail_first_ack and ack_calls == 1:
            events.append("acknowledge raised (lock held)")
            raise RuntimeError("injected acknowledgement failure")
        events.append("acknowledge succeeded (lock held)")

    # The second invocation begins only after the first has returned or raised.
    # For the control this is a replay; for the failure case it is a queue retry.
    for attempt in (1, 2):
        events.append(f"attempt {attempt} begin")
        try:
            worker.process(job, send, acknowledge)
        except RuntimeError as error:
            assert fail_first_ack and attempt == 1
            assert str(error) == "injected acknowledgement failure"
            events.append("attempt 1 raised")
        else:
            events.append(f"attempt {attempt} returned")
        assert not worker.lock.locked()
        completed = job in worker.completed
        assert completed == (not fail_first_ack or attempt == 2)
        events.append(f"completed={completed}; lock released")

    expected = 2 if fail_first_ack else 1
    assert deliveries == [job] * expected
    assert ack_calls == expected
    print("ACK FAILURE + RETRY" if fail_first_ack else "SUCCESS + REPLAY")
    for event in events:
        print(f"  {event}")
    print(f"  accepted deliveries: {len(deliveries)}\n")


if __name__ == "__main__":
    experiment(fail_first_ack=False)
    experiment(fail_first_ack=True)
