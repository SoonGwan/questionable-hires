from threading import Lock

class Worker:
    def __init__(self):
        self.lock = Lock()
        self.completed = set()

    def process(self, job, send, acknowledge):
        with self.lock:
            if job in self.completed:
                return
            send(job)
            acknowledge(job)
            self.completed.add(job)
