#!/usr/bin/env python3
"""Paired local helper timing, not a model benchmark. Executes trusted Git code."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
import time
import types
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = 'skills/receipt/scripts/compare.py'


def load(relative):
    spec = importlib.util.spec_from_file_location(relative.replace('/', '_'), ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def historical(ref):
    sha = subprocess.check_output(['git', 'rev-parse', '--verify', '--end-of-options',
                                   ref + '^{commit}'], cwd=ROOT, text=True).strip()
    source = subprocess.check_output(['git', 'show', sha + ':' + HELPER], cwd=ROOT)
    module = types.ModuleType('receipt_' + sha)
    exec(compile(source, sha + ':' + HELPER, 'exec'), module.__dict__)
    return module, dict(revision=sha, sha256=hashlib.sha256(source).hexdigest())


def screen(before, after, repeats=3):
    if not 1 <= repeats <= 10:
        raise ValueError('repeats must be in [1, 10]')
    runner = load('benchmarks/run.py')
    modules, sources = {}, {}
    for label, ref in [('previous', before), ('candidate', after)]:
        modules[label], sources[label] = historical(ref)
    rows = []
    fixtures = [
        ('benchmarks/receipt_equal_work_cases.py', ['records/decode.py'],
         ['records.decode', 'records.settings'], 'checks.test_records',
         'too many values to unpack', 'Ran 1 test'),
        ('benchmarks/receipt_assembly_cases.py',
         ['assembly/__init__.py', 'assembly/reader.py', 'assembly/writer.py', 'assembly/service.py'],
         ['assembly.service', 'assembly.reader', 'assembly.writer'], 'test_assembly',
         'FAILED (failures=2)', 'Ran 2 tests'),
    ]
    for index, (path, varying, imports, test, failure, count) in enumerate(fixtures):
        case = load(path).cases()[0]
        with tempfile.TemporaryDirectory(prefix='receipt-screen-') as scratch:
            project = Path(scratch) / 'project'
            runner.prepare(case, project)
            originals = {name: ((project/name).read_bytes(), (project/name).stat().st_mode)
                         for name in case['files']}
            recipe = dict(fixed=[name for name in case['files'] if name not in varying],
                          vary=varying, before='HEAD^', after='HEAD', imports=imports,
                          runner='unittest', tests=['-v', test])
            identity = None
            for repeat in range(repeats):
                order = ['previous', 'candidate'] if (index + repeat) % 2 == 0 else ['candidate', 'previous']
                for label in order:
                    module = modules[label]
                    with patch.object(module, 'git', wraps=module.git) as calls:
                        started = time.perf_counter()
                        result = module.compare(project, recipe)
                        elapsed = time.perf_counter() - started
                    assert result['status'] == 'observed', result
                    assert result['checks']['before']['exit_code'] == 1, result
                    assert failure in result['checks']['before']['output'], result
                    assert result['checks']['after']['exit_code'] == 0, result
                    for check in result['checks'].values():
                        assert not check['timed_out'] and not check['output_truncated'], check
                        assert count in check['output'], check
                        for name in imports:
                            assert 'Verified copied import: ' + name in check['output'], check
                    current_identity = (result['revisions'], result['fixed_sha256'])
                    if identity is None:
                        identity = current_identity
                    assert identity == current_identity
                    assert originals == {name: ((project/name).read_bytes(), (project/name).stat().st_mode)
                                         for name in case['files']}
                    assert runner.command(['git', 'status', '--porcelain'], project) == ''
                    assert not list(project.glob('.receipt-*'))
                    rows.append(dict(case=case['id'], repeat=repeat + 1, arm=label,
                                     seconds=elapsed, git_processes=len(calls.call_args_list),
                                     blob_processes=sum(c.args[1] == 'cat-file' for c in calls.call_args_list),
                                     observations=json.loads(json.dumps(result).replace(str(project), '<project>'))))
    summary = []
    for case in sorted({row['case'] for row in rows}):
        means = {arm: statistics.mean(row['seconds'] for row in rows
                                     if row['case'] == case and row['arm'] == arm)
                 for arm in modules}
        summary.append(dict(case=case, mean_seconds=means,
                            candidate_change_percent=100 * (means['candidate']/means['previous'] - 1)))
    return dict(sources=sources, repeats=repeats, rows=rows, summary=summary,
                limitation='Local helper-only timing; shared host/cache; no model calls or token claims. '
                           'Preparation excluded; compare and call instrumentation included; alternating order, no retries.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', default='cb10067')
    parser.add_argument('--after', default='b8d5edc')
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Reserve exclusively before executing; a failed run leaves an empty marker,
    # never an apparently successful report. No overwrite or automatic retries.
    with args.output.open('x') as target:
        report = screen(args.before, args.after, args.repeats)
        json.dump(report, target, indent=2)
        target.write('\n')
    print(json.dumps(report['summary'], indent=2))


if __name__ == '__main__':
    main()
