"""Read pinned resources and existing original CLI outputs; never execute models/helpers."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from inspect_output_reuse import inspect
BEFORE, AFTER = '1be35120', 'ba3a9ec4'
RUN = ROOT / 'benchmarks/results/all-eight-current-07'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def source(revision, path):
    return git('show', revision + ':' + path)

rows = []
for cell in sorted((RUN / 'current').glob('*--skill--1')):
    meta = json.loads((cell / 'metadata.json').read_text())
    skill = meta['skill']
    entry = 'skills/' + skill + '/SKILL.md'
    original = source(BEFORE, entry)
    assert hashlib.sha256(original).hexdigest() == meta['skill_sha256']
    assert original == source(AFTER, entry)
    commands = json.loads((cell / 'commands.json').read_text())
    changed = git('diff', '--name-only', BEFORE, AFTER, '--', 'skills/' + skill).decode().splitlines()
    resources = []
    for name in changed:
        prior, current = source(BEFORE, name), source(AFTER, name)
        exact_reads = [c['id'] for c in commands if prior.decode().strip() in c.get('aggregated_output', '')]
        resources.append(dict(path=name, before_sha256=hashlib.sha256(prior).hexdigest(),
            after_sha256=hashlib.sha256(current).hexdigest(), before_bytes=len(prior),
            after_bytes=len(current), exact_full_original_body_matches=exact_reads))
    baseline_matches = list((RUN / 'baseline').glob(meta['case'] + '--baseline--1/events.jsonl'))
    assert len(baseline_matches) == 1
    recurrence = {}
    for condition, events in [('baseline', baseline_matches[0]), ('current', cell / 'events.jsonl')]:
        data = [json.loads(line) for line in events.read_text().splitlines()]
        recurrence[condition] = {str(n): inspect(data, n) for n in (20, 40, 80)}
    rows.append(dict(skill=skill, case=meta['case'], entry_sha256=meta['skill_sha256'],
        entry_unchanged=True, changed_resources=resources, original_output_recurrence=recurrence))
assert len(rows) == 8
result = dict(measured_resource=git('rev-parse', BEFORE).decode().strip(),
    compared_resource=git('rev-parse', AFTER).decode().strip(), roles=rows,
    summary=dict(entries_unchanged=sum(r['entry_unchanged'] for r in rows),
        changed_resources=sum(len(r['changed_resources']) for r in rows),
        changed_resources_with_exact_original_full_read=sum(bool(p['exact_full_original_body_matches']) for r in rows for p in r['changed_resources']),
        cli_output_recurrence={str(n):{condition:{field:sum(r['original_output_recurrence'][condition][str(n)][field] for r in rows)
            for field in ('command_count','output_characters','recurring_characters')} for condition in ('baseline','current')} for n in (20,40,80)}),
    limitations=['Exact old body matches establish only captured full-text observations, not all reads or execution.',
        'CLI recurrence omits the two originally recovered Con Artist output prefixes; original capture gaps are not repaired here.',
        'Characters are not tokens, and recurrence can be necessary. No causal or avoidable-cost estimate.',
        'Current code is not executed by this audit. Native reachability requires separate review, not substring matching.'])
path = Path(__file__).with_name('audit.json')
with path.open('x') as stream:
    json.dump(result, stream, indent=2); stream.write('\n')
print(json.dumps(result['summary'], indent=2))
for row in rows:
    print(row['skill'], 'changed', len(row['changed_resources']), 'full-read', [r['path'] for r in row['changed_resources'] if r['exact_full_original_body_matches']])
