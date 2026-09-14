# Duplicate publication

A Publisher instance handles multiple documents. While one publish for a document_id is awaiting its write, another publish for that SAME document_id on that SAME instance must return None promptly without calling its supplied write callback or disturbing the first call. Different document IDs and different Publisher instances must not block or suppress one another. document_id is a nonempty string; exact string equality defines identity, with no normalization.

The callback receives document_id positionally and the original payload object as the payload keyword. Payload is opaque; do not clone, serialize or inspect it. Preserve the exact successful result object and exact exception object. Clear the document's in-flight state after success, asynchronous failure, a synchronous exception raised by calling write, or cancellation, so a subsequent publish can proceed. Retry is caller-initiated, not automatic. Do not change public signatures, add a queue, shared/global lock, automatic retries or transport calls.

Existing tests: python3 -B -m unittest discover -s tests -v. Keep their original checks unchanged. Add bounded, rerunnable regression checks; test-only support is allowed but not required. There is no production I/O or deployment step in this ticket.
