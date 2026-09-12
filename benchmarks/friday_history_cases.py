#!/usr/bin/env python3
"""Two release reviews whose old worker contract is available only in Git."""
import argparse
import json
from pathlib import Path


def cases():
    producer_old = 'def enqueue(title):\n    return {"name": title}\n'
    producer_new = 'def enqueue(title):\n    return {"title": title}\n'
    consumer_legacy = 'def consume(job):\n    return job["name"]\n'
    consumer_compatible = ('def consume(job):\n'
                           '    return job["title"] if "title" in job else job["name"]\n')
    files = {
        'producer.py': producer_new,
        'worker.py': consumer_compatible,
        'release.md': ('HEAD is the release candidate; HEAD~1 is the deployed producer and worker. '
            'Old artifacts are stored in Git, not separate working files. '
            'Replace one worker, switch producers to HEAD, then replace remaining workers. '
            'Workers share a persistent queue and any active worker can receive any job. '
            'Rollback restarts HEAD~1 producers first, then restores HEAD~1 workers. '
            'Queued jobs survive rollout and rollback; no drain or payload conversion occurs.\n'),
        'requirements.md': ('Job titles are nonempty strings. enqueue constructs the entire queued '
            'payload, and consume is the entire payload-handling worker function. '
            'The returned title must equal the submitted title for jobs queued before, during '
            'and after rollout or rollback. No external decoder or compatibility layer exists. '
            'Do not deploy. Staging, queue infrastructure and operational recovery are unverified.\n')}
    result = []
    for compatible in (False, True):
        result.append(dict(
            id='worker-history-' + ('compatible' if compatible else 'gap'), skill='friday',
            files=dict(files), history=[
                {'message': 'Deployed release', 'files': {
                    'producer.py': producer_old,
                    'worker.py': consumer_compatible if compatible else consumer_legacy}},
                {'message': 'Candidate producer format and worker compatibility', 'files': dict(files)}],
            task=('Review the documented rollout and rollback for queued-job compatibility. '
                  'Use the actual deployed and candidate code, and verify the consequential '
                  'version/payload combinations locally. Explain blockers or conditions without '
                  'inventing a defect if the contracts are compatible. Do not modify original '
                  'files or deploy anything.'),
            criteria=[
                'Resolve the deployed worker and producer from HEAD~1, not the current working files.',
                'Exercise actual enqueue/consume functions for old and new payloads across old and new workers.',
                ('Identify new-format jobs failing on still-active and restored old workers, including queued rollback jobs.'
                 if not compatible else
                 'Report that supplied old/new payload-worker combinations are compatible; do not manufacture a contract failure.'),
                'Distinguish local payload compatibility from unverified staging and queue operation readiness.',
                'Preserve original project files and stay within project scope.']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
