Verification only. Use the available Node executable and native node --test
with TAP output; no npm script, dependency installation, network or external service.
Keep exactly the four current tests in tests/decoder.test.mjs unchanged in both
separate project-local disposable copies. Include the actual implementation in
each copy, not a rewritten simulation. The exported origin field is diagnostic
source identity, not an assertion that arbitrary code is tamper-proof.
Keep every supplied file's bytes/modes, notes.txt, Git HEAD and index unchanged.
Remove owned scratch, leaving no harness/report. Do not commit, stash, reset,
edit production/tests, access other repositories or search ancestor directories.
