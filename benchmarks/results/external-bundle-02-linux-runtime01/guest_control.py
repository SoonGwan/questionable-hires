"""Author runtime controls only; no project, issue, grader or credential inputs."""
import hashlib
import json
import os
from pathlib import Path
import platform
import struct
import subprocess
import sys
import tempfile

sentinel = Path(sys.argv[1])
mounts = []
for line in Path('/proc/self/mountinfo').read_text().splitlines():
    left, right = line.split(' - ', 1)
    fields, filesystem = left.split(), right.split()
    if filesystem[0] in ('virtiofs', '9p', 'fuse.sshfs'):
        mounts.append(dict(target=fields[4], kind=filesystem[0], source=filesystem[1]))
report = dict(system=platform.system(), architecture=platform.machine(),
              kernel=platform.release(), python=platform.python_version(),
              cpus=os.cpu_count(), host_sentinel_absent=not sentinel.exists(),
              shared_mounts=mounts, ssh_agent_absent='SSH_AUTH_SOCK' not in os.environ,
              external_solver_staging_absent=not Path('/tmp/qh-external-bundle-02-solver-staging-02').exists())
print(json.dumps(dict(guest=report)), flush=True)
assert report['system'] == 'Linux' and report['architecture'] == 'aarch64'
assert report['cpus'] == 2 and report['host_sentinel_absent'] and report['ssh_agent_absent']
assert report['external_solver_staging_absent']
assert all(m['kind'] == 'virtiofs' and m['source'] == 'vz-rosetta' for m in mounts), mounts

# Minimal static x86-64 ELF with one executable load segment. Its only syscalls
# write a known marker to stdout and exit with the selected scalar status.
# No dynamic linker, network, filesystem reads or external project code.
def executable(status):
    message = b'qh-x86_64-control\n'
    code = (b'\xb8\x01\x00\x00\x00'              # mov eax, SYS_write
            b'\xbf\x01\x00\x00\x00'            # mov edi, stdout
            b'\x48\x8d\x35\x13\x00\x00\x00'  # lea rsi, marker after code
            b'\xba' + struct.pack('<I', len(message)) +
            b'\x0f\x05'                          # syscall
            b'\xb8\x3c\x00\x00\x00'            # mov eax, SYS_exit
            b'\xbf' + struct.pack('<I', status) + b'\x0f\x05')
    size = 64 + 56 + len(code) + len(message)
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    header = struct.pack('<16sHHIQQQIHHHHHH', ident, 2, 62, 1, 0x400078,
                         64, 0, 0, 64, 56, 1, 0, 0, 0)
    segment = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000, size, size, 4096)
    return header + segment + code + message

with tempfile.TemporaryDirectory(prefix='qh-runtime-control-') as owned:
    for expected in (0, 37):
        path = Path(owned)/('exit-'+str(expected))
        data = executable(expected)
        path.write_bytes(data)
        path.chmod(0o700)
        result = subprocess.run([str(path)], capture_output=True, timeout=10)
        print(json.dumps(dict(expected_exit=expected, actual_exit=result.returncode,
                              elf_sha256=hashlib.sha256(data).hexdigest(),
                              stdout=result.stdout.decode(errors='replace'),
                              stderr=result.stderr.decode(errors='replace'))), flush=True)
        assert result.returncode == expected and result.stdout == b'qh-x86_64-control\n' and not result.stderr
print(json.dumps(dict(controls='PASS', native_x86_hardware=False, project_tests_run=0, model_calls=0)), flush=True)
