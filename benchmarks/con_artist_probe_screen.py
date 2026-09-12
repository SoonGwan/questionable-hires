#!/usr/bin/env python3
"""Frozen local helper screen; executes trusted Git code, not model sessions."""
import copy
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import types
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def git_file(ref, path):
    return subprocess.check_output(['git', 'show', ref + ':' + path], cwd=ROOT)


def screen():
    modules, identities = {}, {}
    for arm, ref in [('previous', '5f68ac7'), ('candidate', '91fdde3')]:
        source = git_file(ref, 'skills/con-artist/scripts/audit.py')
        module = types.ModuleType(arm)
        exec(compile(source, ref + ':audit.py', 'exec'), module.__dict__)
        modules[arm] = module
        identities[arm] = dict(revision=subprocess.check_output(
            ['git', 'rev-parse', ref], cwd=ROOT, text=True).strip(),
            sha256=hashlib.sha256(source).hexdigest())
    files = {name: git_file('e7fb780', 'examples/con-artist-batch/' + name)
             for name in ('service.py', 'test_service.py', 'recipe.json')}
    rows = []
    for index, case in enumerate(('identical', 'different')):
        recipe = json.loads(files['recipe.json'])
        if case == 'different':
            recipe['mutations'][1]['probe'] += 'assert len(store) == 2\n'
        with tempfile.TemporaryDirectory(prefix='probe-screen-') as directory:
            project = Path(directory)
            for name, source in files.items():
                (project / name).write_bytes(source)
            originals = {p.name: (p.read_bytes(), p.stat().st_mode) for p in project.iterdir()}
            for repeat in range(3):
                order = ['previous', 'candidate'] if (index + repeat) % 2 == 0 else ['candidate', 'previous']
                for arm in order:
                    module = modules[arm]
                    with patch.object(module, 'execute', wraps=module.execute) as execute:
                        started = time.perf_counter()
                        result = module.audit_batch(project, copy.deepcopy(recipe))
                        elapsed = time.perf_counter() - started
                    assert result['status'] == 'observed' and len(result['audits']) == 2
                    expected_count = 6 if arm == 'candidate' and case == 'identical' else 7
                    assert execute.call_count == expected_count
                    for audit, values in zip(result['audits'],
                                             ["['existing']", "['existing', 'new', 'new']"]):
                        for name, check in audit['checks'].items():
                            if 'observation_ref' in check:
                                resolved = result
                                for part in check['observation_ref'][2:].split('/'):
                                    resolved = resolved[int(part)] if isinstance(resolved, list) else resolved[part]
                                assert 'observation_ref' not in resolved
                                assert check['exit_code'] == resolved['exit_code']
                                check = resolved
                            assert check['exit_code'] == (1 if name == 'mutant_probe' else 0)
                            assert not check['timed_out'] and not check['output_truncated']
                            assert 'Verified copied import: service' in check['output']
                        assert 'AssertionError: ' + values in audit['checks']['mutant_probe']['output']
                    assert originals == {p.name: (p.read_bytes(), p.stat().st_mode) for p in project.iterdir()}
                    rows.append(dict(case=case, repeat=repeat + 1, arm=arm, seconds=elapsed,
                                     executions=execute.call_count,
                                     json_bytes=len(json.dumps(result, indent=2).encode())))
    summary = [{ 'case': case, 'arm': arm,
                 'mean_seconds': statistics.mean(r['seconds'] for r in rows
                                                  if r['case'] == case and r['arm'] == arm)}
               for case in ('identical', 'different') for arm in modules]
    return dict(python=sys.version, sources=identities, rows=rows, summary=summary,
                limitation='Shared host/cache; local helper only; JSON bytes are not tokens.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: verification assertions are required.')
    print(json.dumps(screen(), indent=2))
