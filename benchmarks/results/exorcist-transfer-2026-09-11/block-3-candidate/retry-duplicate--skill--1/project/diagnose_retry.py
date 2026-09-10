"""Deterministic local diagnosis; all email and queue operations are fakes."""

from pathlib import Path
import runpy


Worker = runpy.run_path(str(Path(__file__).with_name("worker.py")))["Worker"]


def experiment(fail_first_ack):
    worker = Worker()
    job = "confirmation-123"
    deliveries = []
    events = []
    ack_calls = 0

    def send(value):
        assert worker.lock.locked()
        deliveries.append(value)
        events.append("send accepted (lock held)")

    def acknowledge(value):
        nonlocal ack_calls
        assert value == job
        assert worker.lock.locked()
        ack_calls += 1
        if fail_first_ack and ack_calls == 1:
            events.append("ack raises (lock held)")
            raise RuntimeError("injected acknowledgement failure")
        events.append("ack succeeds (lock held)")

    # These calls are strictly sequential in this single thread.
    for attempt in (1, 2):
        events.append(f"attempt {attempt} starts")
        try:
            worker.process(job, send, acknowledge)
        except RuntimeError as error:
            assert str(error) == "injected acknowledgement failure"
            events.append("queue observes failure; retry scheduled")
        assert not worker.lock.locked()
        completed = job in worker.completed
        assert completed == (not fail_first_ack or attempt == 2)
        events.append(f"attempt {attempt} ends: completed={completed}, lock released")

    expected = 2 if fail_first_ack else 1
    assert deliveries == [job] * expected
    assert ack_calls == expected
    assert worker.completed == {job}
    print("FIRST ACK FAILS" if fail_first_ack else "SUCCESSFUL ACK CONTROL")
    print("\n".join(events))
    print(f"deliveries={len(deliveries)}; assertions passed\n")


if __name__ == "__main__":
    experiment(fail_first_ack=False)
    experiment(fail_first_ack=True)
