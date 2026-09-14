"""Frozen entry-only Friday follow-up; no favorable retries."""
from datetime import datetime, timezone
import hashlib
import json

from cases_view_contract import CASE
from run_sqlite_debit_01 import ROOT, git
import run


def main():
    output = ROOT / 'benchmarks/local-runs/view-contract-02'
    output.mkdir(parents=True, exist_ok=False)
    manifest = dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                    started_at=datetime.now(timezone.utc).isoformat(),
                    schedule=['candidate', 'original'], model='gpt-6-astra', effort='medium',
                    repeats=1, jobs=1, timeout_seconds=240, session_persistence_requested=True,
                    case=CASE, protocol_sha256=hashlib.sha256(
                        (ROOT / 'benchmarks/VIEW-CONTRACT-02-PROTOCOL.md').read_bytes()).hexdigest())
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for condition, revision in [('candidate', 'dbbbba0'), ('original', '45a2741')]:
        directory = output / condition
        directory.mkdir()
        for entry in git('ls-tree', '-r', revision, '--', 'skills/friday').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            assert kind == 'blob' and mode in ('100644', '100755')
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
        (directory / 'run.json').write_text(json.dumps(dict(
            manifest, condition=condition, skill_revision=git('rev-parse', revision).decode().strip(),
            skill_resources_sha256=run.resource_digest(directory / 'skills/friday')),
            indent=2) + '\n')
    disabled = run.disabled_skills()
    for condition in manifest['schedule']:
        print('Starting ' + condition, flush=True)
        directory = output / condition
        result = run.run_cell(CASE, 'skill', 1, directory, 'gpt-6-astra', 'medium', 240,
                              disabled, skills_root=directory / 'skills', persist_session=True)
        print(json.dumps(dict(condition=condition, **{key: result[key] for key in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')})), flush=True)
        if result.get('limit_detected'):
            break


if __name__ == '__main__':
    main()
