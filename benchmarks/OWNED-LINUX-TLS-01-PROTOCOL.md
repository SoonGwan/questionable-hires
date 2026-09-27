# Owned Linux TLS01 — frozen trusted and adverse transport controls

2026-09-27,parent`0a7c5b5c`,unchanged8skills,zero models/selected-case tests.
Reuse exact Linux separate-prefix service wheels/native image/client source and
existing owned dual-protocol WSGIServer implementation, without client/package/
test repair. Before execution, recheck existing owned CA and leaf checkend3600;
leaf CN127.0.0.1 expires2026-09-29 00:54:46UTC. Match old certificate/key digests;
keep key0600/private0700, never publish key body or install global trust.

Mount certs readonly in disposable guest; separate service process loads own leaf
and accepts HTTP and HTTPS on the same dynamic loopback port via existing socket
peek/TLS wrapping. Require actual plainHTTP200, trusted HTTPS200 using explicit
owned CA (never verify=False), default/untrusted CA rejected with native SSLError
and certificate-verification message, and wrong hostname rejected with native
SSLError/hostname-mismatch message. Use numeric loopback alias127.1 for mismatch
against CN127.0.0.1; retain unexpected resolver/transport errors rather than treat
any exception as successful hostname validation. Record actual URLs/echo behavior
separately; do not infer full HTTPbin endpoint parity from status alone.

Service prefix stays separate, official client/source readonly and package absence
preserved. Native extension/import identities and service thread/socket/process
cleanup required. Pip30s/ready10s/request3s/shutdown10s then owned guest group
TERM/KILL; guest180s/independent parent200s watchdog. Retain first failures and
changed hypotheses, detach after collection. Original Mac controls are historical,
not rescored; successful Linux controls are not official script/FAIL-PASS grading,
default trust readiness for selected tests, all8 quality or token/time savings.
