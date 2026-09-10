class Worker:
    def process(self, job, provider, acknowledge):
        provider.send(job, idempotency_key=job)
        acknowledge(job)
