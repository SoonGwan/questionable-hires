# Owned Linux service01 — frozen separate-prefix native HTTPbin

2026-09-27,parent`f68c1f4d`,unchanged8skills,zero models/selected-case tests.
Reverify exact11 wheel bytes/digests from service-wheels01 and expose them readonly
in existing ARM Linux guest; official image root also readonly. Native image Python
pip installs offline/no-deps/no-cache/no-version-check into **guest tmpfs service
prefix only**, never the official client site-packages. No host/global installer.
Keep existing client Python3.9.20/pytest7.4.4/source unchanged; do not add pytest2.8.

Launch a separate native service process with prefix-only PYTHONPATH. Reuse the
HTTPbin app/pytest_httpbin Handler/WSGIServer lifecycle from earlier owned service
controls. Require actual HTTPbin/Flask/Werkzeug/MarkupSafe module paths under the
service prefix and actual MarkupSafe x86 extension load/file digest. HTTP service
binds guest127.0.0.1/dynamic port, VM no NIC/block devices, guest loopback up.
Unmodified project Requests in a separate client process must GET real `/get`
and receive200/exact authored args/echoed URL. A health stub is not substituted.
After stdin shutdown require server thread join/socket close and serviceexit0.
Require client still cannot import service packages after prefix installation.

Bound native pip30s, ready observation10s, request3s, service shutdown10s with
owned guest process-group TERM/KILL cleanup; guest180s/independent parent200s
watchdog. Retain first original failures/source/log, no automatic version upgrades
or same-input retries. Record install/service/client exits, actual imports/native
extension identities, configured PYTHONPATH separation and cleanup. Public outputs
exclude source/test/gold/script/label bodies and keys. Detach after collection.
This gate does not establish TLS/default trust/mixed-scheme, official script/tests/
parser grades or all8 quality/token/time improvements. Separate compatibility
service is prospective, not retroactive success for older declined grades.
