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
import sys
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
    cleanup_complete = True
    group_stopped = False
    def stop_group():
        nonlocal group_stopped
        if not group_stopped:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            group_stopped = True
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                # A finished foreground command can leave a descendant holding
                # the pipe. Start the promised group cleanup now, then drain
                # buffered output instead of waiting out the whole deadline.
                if process.poll() is not None:
                    stop_group()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                for key, _ in selector.select(min(remaining, 0.05)):
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
        stop_group()
        process.stdout.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Do not replace an in-flight interruption with a cleanup timeout.
            cleanup_complete = False
    return dict(exit_code=process.returncode, timed_out=timed_out,
                cleanup_complete=cleanup_complete,
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
combined-output characters), output_truncated, cleanup_complete. No result file is required.
Default is compact JSON; --pretty indents it. UTF-8 stdout emits Unicode directly;
other stdout encodings use ASCII escapes. Both retain identical parsed evidence.
CLI status: 0 child success; 1 child failure; 124 wrapper timeout; 2 invalid input.
125 means child exit could not be confirmed within 5 seconds after group kill;
it takes precedence over 124. This is not an OS-level containment guarantee.
A child exiting 124 maps to CLI 1. Timeout/truncated evidence is not causal proof.
Keep assertions and task cleanup in the probe; this supplies a process deadline.''')
    parser.add_argument('--timeout', type=float, default=10,
                        help='finite seconds in (0, 300], default 10')
    parser.add_argument('--pretty', action='store_true',
                        help='Indent JSON; default is compact. Parsed evidence is unchanged.')
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help='after --, the executable and its arguments')
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    try:
        result = run(command, args.timeout)
    except (OSError, ValueError) as error:
        parser.exit(2, 'Probe not started: ' + str(error) + '\n')
    # Keep UTF-8 logs readable without expanding every non-ASCII character.
    # Retain ASCII escapes on other output encodings to avoid losing the result.
    utf8_output = codecs.lookup(sys.stdout.encoding or 'utf-8').name == 'utf-8'
    print(json.dumps(result, ensure_ascii=not utf8_output,
                     indent=2 if args.pretty else None,
                     separators=None if args.pretty else (',', ':')))
    # Preserve the actual status in JSON. CLI 124 uniquely means our timeout;
    # other unsuccessful commands map to 1 (including a child exiting 124).
    if not result['cleanup_complete']:
        return 125
    return 124 if result['timed_out'] else (0 if result['exit_code'] == 0 else 1)


if __name__ == '__main__':
    raise SystemExit(main())
