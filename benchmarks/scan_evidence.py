#!/usr/bin/env python3
"""Flag common private paths and credential shapes; never print matched values."""
import argparse
import json
from pathlib import Path
import re

PATTERNS = {
    'private_path': re.compile(r'/(?:Users|home)/[^\s/]+|/(?:private/)?var/folders/|/tmp/qh-|/private/tmp/qh-'),
    'credential': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'auth_header': re.compile(r'Authorization[\s"\x27:=]+Bearer\s+[A-Za-z0-9._-]{15,}', re.I),
}


def scan(directory):
    findings = []
    for path in sorted(directory.rglob('*')):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text()
        except (UnicodeError, OSError):
            continue
        for line, contents in enumerate(text.splitlines(), 1):
            for kind, pattern in PATTERNS.items():
                if pattern.search(contents):
                    findings.append({'file': str(path.relative_to(directory)), 'line': line, 'kind': kind})
    return findings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    result = scan(args.directory)
    print(json.dumps({'findings': result, 'limitation': 'Pattern scan only; author review is also required.'}, indent=2))
    raise SystemExit(bool(result))
