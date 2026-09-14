"""Frozen reference-only comparison on the existing HTTPX history ticket."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

import run
from run_sqlite_debit_01 import ROOT, git


def task(python):
    protocol = (ROOT / 'benchmarks/HTTPX-AUTH-HISTORY-01-PROTOCOL.md').read_text()
    lines = [line[2:] if line.startswith('> ') else ''
             for line in protocol.splitlines() if line.startswith('>')]
    return '\n'.join(lines).replace('<PREINSTALLED_PYTHON>', str(python))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    args = parser.parse_args()
    source, python = args.source.resolve(), args.python.absolute()
    def source_git(*arguments):
        return subprocess.check_output(['git', *arguments], cwd=source, text=True).strip()
    if (source_git('rev-parse', 'HEAD') != '26d48e0634e6ee9cdc0533996db289ce4b430177'
            or source_git('rev-parse', '--is-shallow-repository') != 'false'
            or source_git('status', '--porcelain') or not python.is_file()):
        parser.error('Requires the clean pinned full-history source and existing interpreter')
    output = ROOT / 'benchmarks/local-runs/history-guide-01'
    output.mkdir(parents=True, exist_ok=False)
    case = dict(id='auth-history', skill='necromancer', task=task(python))
    manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                    started_at=datetime.now(timezone.utc).isoformat(),
                    schedule=['original', 'candidate'], model='gpt-6-astra', effort='medium',
                    repeats=1, jobs=1, timeout_seconds=360, session_persistence_requested=True,
                    source_revision=source_git('rev-parse', 'HEAD'), case=case,
                    protocol_sha256=hashlib.sha256(
                        (ROOT / 'benchmarks/HISTORY-GUIDE-01-PROTOCOL.md').read_bytes()).hexdigest())
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for condition, revision in [('original', '28caeb8'), ('candidate', '3a04643')]:
        directory = output / condition
        directory.mkdir()
        for entry in git('ls-tree', '-r', revision, '--', 'skills/necromancer').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            if kind != 'blob' or mode not in ('100644', '100755'):
                raise ValueError('Unsupported skill resource')
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
        (directory / 'run.json').write_text(json.dumps(dict(
            manifest, condition=condition, skill_revision=revision,
            skill_resources_sha256=run.resource_digest(directory / 'skills/necromancer')),
            indent=2) + '\n')
    disabled = run.disabled_skills()
    for condition in manifest['schedule']:
        print('Starting ' + condition, flush=True)
        directory = output / condition
        result = run.run_cell(case, 'skill', 1, directory, 'gpt-6-astra', 'medium', 360,
                              disabled, skills_root=directory / 'skills',
                              project_source=source, persist_session=True)
        print(json.dumps(dict(condition=condition, **{key: result[key] for key in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')})), flush=True)
        if result.get('limit_detected'):
            break


if __name__ == '__main__':
    main()
