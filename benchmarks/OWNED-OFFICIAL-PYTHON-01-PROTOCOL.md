# Owned official Python guest01 — frozen runtime probe, 2026-09-27

Parent `51134006`, unchanged eight skills. Zero model or external case runs.
Use the actual Rosetta/ARM VM path from [x86 control01](OWNED-LINUX-X86-01.md)
to test the Requests2674 image's interpreter and core imports. This is not full
image/official grading parity and does not replace any frozen selected case.

Pin the already verified Linux/amd64 manifest
`sha256:c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2`.
Reuse the private environment layer at index6, SHA256
`0e43bc2a78057e6e6737b70d65be5424e7d737f26029c7a5bc282292ce5dffa7`,
350,262,563 compressed bytes. Native path inspection identifies
`opt/miniconda3/envs/testbed/bin/python3.9` and its shared libpython.
Download only OS base layer0 if required, SHA256
`39a945af8df2ad9343f141c82355d3f2c4b576d432eda34c460d630607462b60`,
29,736,517 compressed bytes, process download ceiling120 seconds. Registry public
pull authorization is in memory only; no auth/account/profile file accesses.

New extraction scope supersedes no old checkpoint: copy only the testbed Conda
environment subtree and selected OS x86 library directory files into a fresh owned
private runtime. Do not extract testbed/project/evaluation/source/Git trees or
image history commands. Reject noncanonical paths and links escaping the selected
runtime; hardlinks may read public package-cache data only, never project/gold
paths. Retain skipped/rejected entry counts rather than asserting full parity.
No archive extractall or native host installation. Raw runtime/library data is
private and not provided to model solving sessions or redistributed publicly.

Guest kernel/initramfs remain frozen from VM01. Use no network devices or disks,
readonly runtime shares and only separately owned writable probe data if needed.
No host Rosetta install or global binfmt registration. Use explicit translation
invocation; dynamic-loader aliases/search paths are owned guest/runtime changes
and must be reported. Probe actual interpreter exit/version and core module
imports (sys, ssl, pytest, pluggy, platform), actual import paths and selected
runtime identities. No source repair or dependency upgrade to manufacture success.

Bound guest start/commands and parent process, retain first failed attempts,
actual native statuses, imports/loader errors and exact input/output hashes. Do
not infer executable readiness from installed metadata or process0 alone. No
external gold/test/issue text enters this runtime probe. Passing these imports
is not native case execution, whole-image parity, all8 quality or token savings.
A successful probe permits a separately frozen official native preflight; failures
require decision-changing diagnostics, not repeated same-input retries.
