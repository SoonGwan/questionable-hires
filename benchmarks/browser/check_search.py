#!/usr/bin/env python3
"""Check a synthetic DOM interaction with an explicitly supplied local Chrome."""
import argparse
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import sys


class IncompleteCheck(RuntimeError):
    def __init__(self, message, observations):
        super().__init__(message)
        self.observations = list(observations)


class ReceiptParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.collect = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'pre' and dict(attrs).get('id') == 'receipt':
            self.collect = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.collect = False

    def handle_data(self, data):
        if self.collect:
            self.parts.append(data)


def check(browser):
    if os.name != 'posix':
        raise ValueError('This local runner currently requires POSIX process groups')
    fixture = Path(__file__).with_name('search-order.html').resolve()
    observations = []
    for mode in ('off', 'on'):
        with tempfile.TemporaryDirectory(prefix='qh-browser-profile-') as profile:
            process = subprocess.Popen([
                str(browser), '--headless=new', '--disable-gpu', '--no-first-run',
                '--no-default-browser-check', '--disable-background-networking',
                '--disable-extensions', '--disable-component-update', '--disable-sync',
                '--timeout=10000',
                '--user-data-dir=' + profile, '--dump-dom',
                fixture.as_uri() + '?guard=' + mode],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                start_new_session=True)
            try:
                stdout, stderr = process.communicate(timeout=30)
            except BaseException as error:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass  # The dedicated process group already exited.
                try:
                    process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    # An escaped descendant might retain a pipe; do not wait
                    # indefinitely for EOF after killing the owned group.
                    process.stdout.close()
                    process.stderr.close()
                    process.wait(timeout=5)
                if isinstance(error, subprocess.TimeoutExpired):
                    def byte_count(value):
                        return len(value.encode('utf-8') if isinstance(value, str) else value or b'')
                    # Keep raw browser logs private; retain enough information
                    # to identify whether any output arrived before timeout.
                    raise IncompleteCheck(
                        'Browser timed out in guard=' + mode + '; check incomplete; '
                        f'captured stdout bytes={byte_count(error.output)}, '
                        f'stderr bytes={byte_count(error.stderr)}', observations) from error
                raise
            if process.returncode:
                raise IncompleteCheck('Browser exited with status ' + str(process.returncode), observations)
            parser = ReceiptParser()
            parser.feed(stdout)
            try:
                observed = json.loads(''.join(parser.parts))
            except ValueError as error:
                raise IncompleteCheck('Browser did not return a JSON receipt', observations) from error
            if not isinstance(observed, dict):
                raise IncompleteCheck('Browser receipt is not an object', observations)
            if observed.get('submitted') != ['old', 'new', 'normal']:
                raise AssertionError('Browser did not execute the input sequence')
            expected = 'old result' if mode == 'off' else 'new result'
            if (observed.get('afterNew') != 'new result' or observed.get('afterOld') != expected
                    or observed.get('normal') != 'normal result' or not observed.get('focusPreserved')
                    or observed.get('passed') is not (mode == 'on')):
                raise AssertionError('Unexpected rendered behavior: ' + json.dumps(observed))
            observations.append(observed)
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.browser.resolve(strict=True)), indent=2))
    except IncompleteCheck as error:
        print(json.dumps(dict(complete=False, error=str(error),
                              completed_variants=error.observations), indent=2))
        sys.exit(1)
