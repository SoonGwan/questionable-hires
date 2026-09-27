# Owned guest binfmt01 — frozen x86 child routing control

2026-09-27,parent`dbfd6a1b`,unchanged8skills,zero models/selected-case tests.
The retained [project01](OWNED-OFFICIAL-PROJECT-01.md) parent runs explicitly via
Rosetta, but automatic Python child execution fails native OSError errno8.
Inspecting the frozen initramfs found loop/squashfs modules for6.12.110-0-virt,
but no binfmt_misc module. Do not repeat that same route without an intervention.

Retrieve the official Alpinev3.22 aarch64 netboot `modloop-virt` into a new private
owned directory; URL matches the frozen kernel release index. Bound download120s,
20MiB maximum, timeout15s; record exact bytes/SHA256 before VM execution. A mutable
URL is not a prior immutable digest. Retain failures without automatic retry.
Inside the owned ARM guest, mount this readonly SquashFS through its existing
loop/squashfs drivers and require exact6.12.110-0-virt module path. Load only the
guest binfmt_misc module; kernel ABI mismatch/error stops readiness claims.
Register x86 ELF magic/mask with the mounted Rosetta interpreter in guest proc
binfmt_misc, using Apple's documented credentials/preserve/fix-binary options
translated to kernel flags. No host module, registration, profile or installation.

Reuse the same readonly reconstructed root and project01 probe, same explicit
parent, source/CWD and child command; add only guest module/routing setup. Record
module/mount/registration exits and handler state. Require actual native child
exit0/stdout42 and unchanged testbed module identity for readiness, not controller0.
Guest proc/tmpfs remain RAM-only; root image remains readonly. No official test,
project/dependency repair, gold/issue/body exposure or alternate shell child route.
Same180s guest/200s independent parent process-group watchdog, retain originals,
explicit guest stop and detach after collection. Full OCI/amd64-kernel/native
benchmark/all8 quality/token-time improvement remains unproven even if it passes.
