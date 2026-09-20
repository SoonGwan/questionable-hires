"""Unadopted conditional-detail candidate; no production resource writes."""
import hashlib

RESOURCE = '104e010'
SOURCE_SHA256 = '8bab259a8b49f9e653ce289dea938d32bdae98137ab8ab80f08cdb8cec484f20'
ORIGINAL = '''For asynchronous probes, bound signals that may never arrive and clean up owned tasks. Asyncio timeouts can wait indefinitely for suppressed cancellation. When an additional process deadline is needed, the installed POSIX helper supplies one (replace paths/interpreter):

```sh
python3 /path/to/exorcist/scripts/run_probe.py --timeout 10 -- python3 -B experiments/probe.py
```

Trusted local foreground commands only: this kills remaining process-group members even after normal completion; it is not a sandbox. JSON retains child status, timeout and bounded output. Timeout or truncated decisive output means incomplete evidence, not causal proof. See [runner details](references/bounded-probe.md) for exit mapping, limits or adaptation; routine invocation doesn't require source inspection.'''
CANDIDATE = '''For asynchronous probes, bound signals that may never arrive and clean up owned tasks. Asyncio timeouts can wait indefinitely for suppressed cancellation. If an additional process deadline is needed, read [the POSIX runner guide](references/bounded-probe.md) for invocation and containment limits. It is for trusted local foreground commands, not a sandbox. Timeout or truncated decisive output is incomplete evidence, not causal proof.'''


def revise(source):
    if hashlib.sha256(source.encode('utf-8')).hexdigest() != SOURCE_SHA256:
        raise ValueError('Expected frozen Exorcist entrypoint from ' + RESOURCE)
    if source.count(ORIGINAL) != 1:
        raise ValueError('Expected exactly one optional runner procedure')
    return source.replace(ORIGINAL, CANDIDATE)
