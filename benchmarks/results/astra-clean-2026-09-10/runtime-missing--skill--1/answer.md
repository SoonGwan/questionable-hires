I’ll use the exorcist skill to inspect the snapshot, separate observations from hypotheses, and identify what can be tested locally. I’ll keep this investigative and stay within the project.


The snapshot does not establish a root cause.

Observed in [client.py](project/client.py#L1): `lookup` calls the supplied `request` function with `/lookup` and the key, then awaits its result. It contains no cache, shared state, retry logic, or exception handling. The request implementation and remote service are absent.

A controlled local experiment used the same key for three calls, injecting success, timeout, then success. Each invocation called `request` once with identical arguments; results and the exception passed through unchanged. This confirms propagation behavior, **not a reproduction of the customer failure**.

There is no evidence here to rank service errors, transport failures, input-dependent behavior, or behavior inside `request`. Cache and timing explanations remain unsupported.

The next informative experiment requires the real request boundary: capture a failing call and a successful comparison, including sanitized inputs, elapsed time, exception or response status, and correlation ID. That would distinguish an error response from a transport exception and reveal whether failures track particular inputs.

No corrective code change is justified by this snapshot. Files were left unchanged.
