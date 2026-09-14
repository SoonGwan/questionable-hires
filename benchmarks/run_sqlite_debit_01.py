"""Frozen two-cell development comparison; no automatic retries."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from cases_sqlite_debit import CASE
import run


ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    output = ROOT / 'benchmarks/local-runs/sqlite-debit-01'
    output.mkdir(parents=True, exist_ok=False)
    manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                    started_at=datetime.now(timezone.utc).isoformat(),
                    schedule=['original', 'candidate'], model='gpt-6-astra', effort='medium',
                    repeats=1, jobs=1, timeout_seconds=240, session_persistence_requested=True,
                    case=CASE, protocol_sha256=hashlib.sha256(
                        (ROOT / 'benchmarks/SQLITE-DEBIT-01-PROTOCOL.md').read_bytes()).hexdigest())
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for condition, revision in [('original', '6eef303'), ('candidate', 'ed4a38a')]:
        directory = output / condition
        directory.mkdir()
        snapshot = directory / 'skills'
        for entry in git('ls-tree', '-r', revision, '--', 'skills/con-artist').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            assert kind == 'blob' and mode in ('100644', '100755')
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
        (directory / 'run.json').write_text(json.dumps(dict(
            manifest, condition=condition, skill_revision=git('rev-parse', revision).decode().strip(),
            skill_resources_sha256=run.resource_digest(snapshot / 'con-artist')), indent=2) + '\n')
    disabled = run.disabled_skills()
    for condition in manifest['schedule']:
        print('Starting ' + condition, flush=True)
        directory = output / condition
        result = run.run_cell(CASE, 'skill', 1, directory, 'gpt-6-astra', 'medium', 240,
                              disabled, skills_root=directory / 'skills', persist_session=True)
        print(json.dumps(dict(condition=condition, result=result)), flush=True)
        if result.get('limit_detected'):
            break


if __name__ == '__main__':
    main()
