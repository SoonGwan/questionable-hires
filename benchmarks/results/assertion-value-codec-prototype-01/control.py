"""Local reversible native codec controls; no model calls or installed changes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run
from receipt_versions_cases import cases
from export import redact_paths
spec = importlib.util.spec_from_file_location('codec_helper', ROOT / 'skills/receipt/scripts/compare.py')
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
source = Path(__file__).with_name('observer.py').read_text()

def decode(value, compact):
    if isinstance(value, list):
        return [decode(v, compact) for v in value]
    if isinstance(value, dict):
        if 'bytes_hex' in value:
            return bytes.fromhex(value['bytes_hex'])
        if compact:
            assert set(value) == {'tuple'}
            return tuple(decode(v, compact) for v in value['tuple'])
        assert set(value) == {'kind', 'items'}
        items = [decode(v, compact) for v in value['items']]
        return items if value['kind'] == 'list' else tuple(items)
    return value

def normalize(report, compact):
    return [dict(row, actual=decode(row['actual'], compact), expected=decode(row['expected'], compact))
            for row in report['observations']]

def size(report):
    return len(json.dumps(report, separators=(',', ':'), ensure_ascii=True).encode('ascii'))

rows, native_evidence = [], []
with tempfile.TemporaryDirectory(prefix='qh-value-codec-') as temp:
    for case in cases(sys.executable):
        project = Path(temp) / case['id']; run.prepare(case, project)
        recipe = dict(fixed=['test_windows.py'], vary=['windows.py'],
                      before='HEAD~2' if case['id'].endswith('multiple') else 'HEAD^',
                      after='HEAD', imports=['windows', 'test_windows'], runner='unittest',
                      tests=['-v', 'test_windows'], observe_assertions=True, guard_tree=True)
        if case['id'].endswith('multiple'):
            recipe['additional_before'] = ['HEAD^']
        initial = helper.tree_inventory(project)
        for mode in ('bootstrap', 'module'):
            baseline = helper.compare(project, dict(recipe, invocation=mode))
            with patch.object(helper, 'assertion_startup', return_value=source+'\n'+helper.ASSERTION_WRAPPER):
                candidate = helper.compare(project, dict(recipe, invocation=mode))
            native_evidence.append(dict(case=case['id'], mode=mode, baseline=baseline, candidate=candidate))
            assert baseline['status'] == candidate['status'] == 'observed'
            assert baseline['revisions'] == candidate['revisions']
            for result in (baseline, candidate):
                assert result['originals']['unchanged'] and result['tree_guard']['unchanged'] and result['comparison_copies_removed']
            for label, before in baseline['checks'].items():
                after = candidate['checks'][label]
                assert before['native_exit_code'] == after['native_exit_code'] == (0 if label == 'after' else 1)
                assert before['suite_observation'] == after['suite_observation']
                assert before['suite_observation']['tests'] == 6 and before['suite_observation']['skipped'] == 0
                if mode == 'module':
                    assert before['provenance_ready'] and after['provenance_ready']
                for check in (before, after):
                    assert all('Verified copied import: '+name+' ' in check['output'] for name in recipe['imports'])
                a, b = before['assertion_observation'], after['assertion_observation']
                assert a['complete'] and b['complete'] and a['reason'] is b['reason'] is None
                assert len(a['observations']) == len(b['observations']) == 7
                assert normalize(a, False) == normalize(b, True)
                assert size(b) <= 4096
                rows.append(dict(case=case['id'], mode=mode, label=label, native_exit=after['native_exit_code'],
                                 tests=6, report_before_bytes=size(a), report_candidate_bytes=size(b),
                                 baseline=a, candidate=b, decoded_equal=True))
            assert helper.tree_inventory(project) == initial
namespace = {}; exec(compile(source, 'observer.py', 'exec'), namespace)
encode = namespace['encode']
values = [None, True, 42, 'a', b'\x00\xff', [], (), [1, (True, b'a')], ([1], ('x',))]
for value in values:
    restored = decode(encode(value, [32]), True)
    assert type(restored) is type(value) and restored == value
class Unsafe:
    def __repr__(self):
        raise AssertionError('Do not call repr')
for value in (Unsafe(), [Unsafe()], 'x'*257, list(range(17)), 1 << 257):
    try:
        encode(value, [32])
    except namespace['UnavailableValue']:
        pass
    else:
        raise AssertionError('Unavailable value encoded')
summary = dict(checkpoint='assertion-value-codec-prototype-01', date='2026-09-27',
               resource_parent='c2ad2c35', source_sha256=hashlib.sha256(source.encode()).hexdigest(),
               native_comparisons=8, native_processes=20, records_compared=len(rows)*7,
               primitive_roundtrips=len(values), unavailable_controls=5,
               report_before_bytes=sum(r['report_before_bytes'] for r in rows),
               report_candidate_bytes=sum(r['report_candidate_bytes'] for r in rows),
               model_runs=0, installed_changes=False,
               limitation='Reused authored local fixtures; output bytes are not whole-task model tokens or latency. In-memory codec injection only.')
summary['report_byte_change_percent'] = (summary['report_candidate_bytes']/summary['report_before_bytes']-1)*100
Path(__file__).with_name('results.json').write_text(redact_paths(json.dumps(dict(summary=summary, rows=rows, native_evidence=native_evidence), indent=2))+'\n')
print(json.dumps(summary, indent=2))
