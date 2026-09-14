Python 3.9+ standard library; python3 -B -m unittest -v test_receipts.
Successful handle_upload must preserve the integer ID and exact bytes payload in
the disk SQLite database, visible from a newly opened connection after it returns.
Previously committed events must survive. The acknowledgment is not durability proof.
IDs are distinct positive integers and payloads are bytes, including empty/binary bytes.
No networking or concurrent writers are in scope. Existing production/test files are
immutable for this audit. Use disposable project-local copies, clean owned scratch,
and preserve all original bytes/modes. Do not install packages or change warnings.
