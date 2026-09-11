#!/usr/bin/env python3
"""Run one trusted local command with a POSIX process deadline; not a sandbox."""
import argparse
import codecs
import json
import math
import os
import selectors
import signal
import subprocess
import time


def run(command, timeout=10, cwd=None):
    if os.name != 'posix' or not math.isfinite(timeout) or not 0 < timeout <= 300:
        raise ValueError('Requires POSIX and a finite timeout in (0, 300]')
    if not isinstance(command, (list, tuple)) or not command or not all(isinstance(arg, str) for arg in command):
        raise ValueError('Expected a command argument list')
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               start_new_session=True)
    started = time.monotonic()
    deadline = started + timeout
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    output, size, timed_out = '', 0, False
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 4096)
                    decoded = decoder.decode(chunk, final=not chunk)
                    size += len(decoded)
                    output = (output + decoded)[-12000:]
                    if not chunk:
                        selector.unregister(key.fileobj)
            process.wait(timeout=max(0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        timed_out = True
    finally:
        # Kill only this invocation's process group, also on interruption and when
        # a child has closed its output but is still running after its parent exits.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.stdout.close()
        process.wait()
    return dict(exit_code=process.returncode, timed_out=timed_out,
                elapsed_seconds=round(time.monotonic() - started, 3),
                output=output, output_truncated=size > 12000)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Example: run_probe.py --timeout 10 -- python3 -B experiments/probe.py

Use the project's actual command. No shell, dependency installation or copies;
inherits working directory/environment. Foreground commands only: remaining group
members are killed even after normal completion. Escaped process groups are not
contained. Requires Python 3.9+ and POSIX. Reuse existing deadlines when available.

JSON stdout: actual exit_code, timed_out, elapsed_seconds, output (last 12,000
combined-output characters), output_truncated. No result file is required.
CLI status: 0 child success; 1 child failure; 124 wrapper timeout; 2 invalid input.
A child exiting 124 maps to CLI 1. Timeout/truncated evidence is not causal proof.
Keep assertions and task cleanup in the probe; this supplies a process deadline.''')
    parser.add_argument('--timeout', type=float, default=10,
                        help='finite seconds in (0, 300], default 10')
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help='after --, the executable and its arguments')
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        result = run(command, args.timeout)
    except (OSError, ValueError) as error:
        parser.exit(2, 'Probe not started: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))
    # Preserve the actual status in JSON. CLI 124 uniquely means our timeout;
    # other unsuccessful commands map to 1 (including a child exiting 124).
    return 124 if result['timed_out'] else (0 if result['exit_code'] == 0 else 1)


if __name__ == '__main__':
    raise SystemExit(main())
