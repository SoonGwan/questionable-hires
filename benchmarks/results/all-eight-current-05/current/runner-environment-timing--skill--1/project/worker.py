import os

RETRIES = int(os.environ.get('REQUEST_RETRIES', '2'))

def deliver(send):
    for attempt in range(RETRIES + 1):
        try:
            return send()
        except RuntimeError:
            if attempt == RETRIES:
                raise
