"""Read-only retrospective at a pinned tree; reuse existing token accounting.

Writes a new sibling analysis.json, never edits source evidence or calls models.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = '73c54664'
sys.path.insert(0, str(ROOT / 'benchmarks'))
from analyze_response_costs import summarize
from extract_rollout_tools import extract


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


tree = subprocess.check_output(['git', 'ls-tree', '-r', SOURCE, '--', 'benchmarks/results'], cwd=ROOT).decode()
blobs = {}
for line in tree.splitlines():
    metadata, name = line.split('\t', 1)
    mode, kind, identity = metadata.split()
    if kind == 'blob':
        blobs[name] = identity


def read(name):
    raw = (ROOT / name).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if actual != blobs[name]:
        raise ValueError('Working copy differs from frozen tree: ' + name)
    return raw


def document(name):
    return json.loads(read(name))


def master_for(path):
    for parent in Path(path).parents:
        name = str(parent / 'run.json')
        if name in blobs:
            master = document(name)
            if isinstance(master, dict) and all(k in master for k in ('cases', 'settings', 'condition_models', 'condition_flags', 'cli_version')):
                condition = Path(path).relative_to(parent).parts[0]
                if condition in master['condition_flags']:
                    return name, master, condition
    return None


def known_inputs(path, meta):
    found = master_for(path)
    if found is None:
        return None
    name, master, condition = found
    cases = [c for c in master['cases'] if c['id'] == meta['case']]
    if len(cases) != 1 or condition not in master['condition_flags']:
        return None
    return dict(case=cases[0], prompt=meta['prompt'], skill_sha256=meta['skill_sha256'],
        skill_resources_sha256=meta['skill_resources_sha256'], installed_resources=meta['installed_resources_before'],
        model=meta['model'], effort=meta['reasoning_effort'], execution=meta.get('execution'),
        settings=master['settings'], cli_version=master['cli_version'],
        condition_model=master['condition_models'][condition], flags=master['condition_flags'][condition]), name


anchor_paths = sorted(n for n in blobs if n.startswith('benchmarks/results/all-eight-current-07/current/')
                      and n.endswith('/metadata.json') and n.count('/') == 5)
assert len(anchor_paths) == 8
anchor_paths += ['benchmarks/results/mother-writes01-model/previous/' + case + '--skill--1/metadata.json'
                 for case in ('editor-snapshot-absent', 'repeat-query-qa')]
anchors = []
for path in anchor_paths:
    meta = document(path)
    inputs, master = known_inputs(path, meta)
    assert inputs['model'] == inputs['condition_model'] == 'gpt-6-astra' and inputs['effort'] == 'medium'
    assert inputs['flags'] == [] and inputs['execution'] == 'host-workspace-write-rules-retained'
    anchors.append(dict(path=path, skill=meta['skill'], case=meta['case'], inputs=inputs,
                        known_inputs_sha256=digest(inputs), observations=[]))
assert len({(a['skill'], a['case']) for a in anchors}) == 10
lookup = {(a['skill'], a['case']): a for a in anchors}
exclusions, sessions, inspected = [], {}, 0
metadata_paths = sorted(n for n in blobs if n.endswith('/metadata.json'))
for path in metadata_paths:
    meta = document(path)
    if not isinstance(meta, dict):
        continue
    anchor = lookup.get((meta.get('skill'), meta.get('case')))
    if anchor is None:
        continue
    inspected += 1
    found = known_inputs(path, meta) if all(k in meta for k in (
        'prompt', 'skill_sha256', 'skill_resources_sha256', 'installed_resources_before',
        'reasoning_effort', 'model')) else None
    reason = []
    if found is None:
        reason = ['missing matching-input manifest or metadata']
    else:
        inputs, master = found
        reason = [k for k, value in anchor['inputs'].items() if inputs[k] != value]
        if meta.get('installed_resources_after') != meta.get('installed_resources_before'):
            reason.append('installed resources changed or after inventory missing')
    if reason:
        exclusions.append(dict(path=path, differing_or_missing_fields=reason))
        continue
    events_name = str(Path(path).with_name('events.jsonl'))
    if events_name not in blobs:
        exclusions.append(dict(path=path, differing_or_missing_fields=['missing CLI events/session identity']))
        continue
    events = [json.loads(line) for line in read(events_name).splitlines()]
    ids = [e['thread_id'] for e in events if e.get('type') == 'thread.started']
    if len(ids) != 1:
        raise ValueError('Missing or ambiguous original session: ' + path)
    completions = [e for e in events if e.get('type') == 'turn.completed']
    if meta['completed']:
        assert len(completions) == 1 and completions[0]['usage'] == meta['usage'], path
    profile_name = str(Path(path).with_name('usage-profile.json'))
    profile, profile_hash = None, None
    if profile_name in blobs:
        full_profile = document(profile_name)
        profile = summarize(full_profile)
        assert all(profile[k] == meta['usage'][k] for k in ('input_tokens', 'output_tokens', 'cached_input_tokens')), path
        profile_hash = hashlib.sha256(read(profile_name)).hexdigest()
    usage = meta.get('usage') or {}
    row = dict(session_id=ids[0], paths=[path], metadata_sha256=hashlib.sha256(read(path)).hexdigest(),
        manifest=master, manifest_sha256=hashlib.sha256(read(master)).hexdigest(),
        known_inputs_sha256=anchor['known_inputs_sha256'], completed=meta.get('completed'),
        timed_out=meta.get('timed_out'), limit_detected=meta.get('limit_detected'),
        total_tokens=usage['input_tokens'] + usage['output_tokens'] if usage else None,
        elapsed_seconds=meta.get('elapsed_seconds'),
        recorded_responses=profile['responses'] if profile else None,
        first_input=profile['first_input'] if profile else None,
        usage_profile_sha256=profile_hash, profile=profile)
    if row['session_id'] in sessions:
        earlier = sessions[row['session_id']]
        for field in ('known_inputs_sha256', 'completed', 'timed_out', 'limit_detected',
                      'total_tokens', 'elapsed_seconds', 'recorded_responses', 'first_input'):
            assert row[field] == earlier[field], (field, path)
        earlier['paths'].append(path)
    else:
        sessions[row['session_id']] = row
        anchor['observations'].append(row)

# Inspect only explicitly matched original sessions; never export private text.
names = subprocess.check_output(['rg', '--files', '--hidden', str(Path.home() / '.codex/sessions')]).decode().splitlines()
by_id = {Path(p).stem[-36:]: Path(p) for p in names if p.endswith('.jsonl')}
for row in sessions.values():
    rollout = by_id.get(row['session_id'])
    if rollout is None:
        row['actual_context'] = dict(status='unavailable')
        continue
    events = ROOT / Path(row['paths'][0]).with_name('events.jsonl')
    raw, identity = extract(rollout, events)
    contexts = [r['payload'] for r in map(json.loads, raw.splitlines()) if r.get('type') == 'turn_context']
    values = [{k: p[k] for k in ('model', 'effort') if k in p} for p in contexts]
    assert values and all(p == dict(model='gpt-6-astra', effort='medium') for p in values), row['paths']
    row['actual_context'] = dict(status='verified', contexts=values, source_sha256=identity['source_sha256'])

for anchor in anchors:
    assert any(anchor['path'] in row['paths'] for row in anchor['observations']), anchor['path']
    anchor['recorded_resource_sha256'] = anchor['inputs']['skill_resources_sha256']
    anchor['case_sha256'] = digest(anchor['inputs']['case'])
    anchor['prompt_sha256'] = hashlib.sha256(anchor['inputs']['prompt'].encode()).hexdigest()
    anchor['installed_manifest_sha256'] = digest(anchor['inputs']['installed_resources'])
    del anchor['inputs']
    anchor['ranges'] = {}
    for field in ('total_tokens', 'elapsed_seconds', 'recorded_responses', 'first_input'):
        values = [row[field] for row in anchor['observations'] if row[field] is not None]
        anchor['ranges'][field] = dict(available=len(values), minimum=min(values) if values else None,
                                     maximum=max(values) if values else None)

result = dict(source_revision=SOURCE, metadata_files=len(metadata_paths), scoped_metadata_files=inspected,
    unique_sessions=len(sessions), anchors=anchors, exclusions=exclusions,
    limitation='Retrospective matching of recorded resources, task inputs and selected settings only. '
               'Not identical complete context, work, runtime/cache state, randomization, a variance estimate, '
               'quality rescoring or new model evidence. No candidate promoted and no original metric rewritten.')
destination = Path(__file__).with_name('analysis.json')
with destination.open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({k: result[k] for k in ('metadata_files', 'scoped_metadata_files', 'unique_sessions')}))
for anchor in anchors:
    print(anchor['skill'], anchor['case'], len(anchor['observations']), json.dumps(anchor['ranges']))
