# Owned Linux service wheels01 — frozen separate-service acquisition

2026-09-27,parent`3a2a0069`,unchanged8skills,zero models/selected-case tests.
Actual image lacks HTTPbin stack; do not install it into the official client env.
Reuse the prior Mac service's exact Flask1.1.4/Werkzeug1.0.1/Jinja2 2.11.3/
MarkupSafe2.0.1/itsdangerous1.1.0/click7.1.2/decorator4.4.2/six1.15.0/
httpbin0.4.1/pytest-httpbin0.2.0 and py1.4.31 versions. Exclude pytest-mock, unused
by the standalone service. Official Python3.9.20/pytest7.4.4 remains unchanged;
no pytest2.8 package is added or substituted.

Acquire only exact-version wheels from primary PyPI JSON metadata, compare
files.pythonhosted.org blob byte size/SHA256 to that metadata. Choose universal
pure Python wheels except MarkupSafe, which must be cp39/cp39 Linux manylinux x86_64.
Deterministic filename sorting; reject source builds, other architectures/platforms,
nonpublic hostnames and unexpected ZIP paths. Retain first failures, no automatic
retry/version substitution. Read only wheel headers/METADATA and native ELF headers;
do not install/execute/extract on host or change profiles/auth/client packages.
Token/auth files are not read; use stdlib urllib, not a globally configured installer.

Download loop180s, independent parent210s with owned process-group cleanup,15s reads,
20MiB per wheel/50MiB total bounds. Record exact metadata/blob digests, filenames,
requirements and target interpreter. Raw wheels private, no binary redistribution.
This is acquisition only: transitive dependency/import/runtime compatibility and
separate-prefix installation need a later frozen Linux execution gate. It cannot
establish service/TLS/official grading/all8 quality/token-time improvement.
