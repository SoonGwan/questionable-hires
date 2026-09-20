"""Exact recorded-token arithmetic, not causal attribution or billable cost."""
import argparse
import hashlib
import json
from pathlib import Path

FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens')


def summarize(profile):
    responses = profile.get('recorded_responses')
    if not isinstance(responses, list) or not responses:
        raise ValueError('Actual per-response records required; advances are not substitutes')
    for row in [profile['totals'], *responses]:
        if any(type(row.get(k)) is not int or row[k] < 0 for k in FIELDS):
            raise ValueError('Invalid token counters')
        if row['cached_input_tokens'] > row['input_tokens']:
            raise ValueError('Cached input exceeds input')
    totals = {k: sum(row[k] for row in responses) for k in FIELDS}
    if totals != profile['totals']:
        raise ValueError('Response counters do not reconcile')
    if totals['input_tokens'] + totals['output_tokens'] != profile['total_tokens']:
        raise ValueError('Total tokens do not reconcile')
    first = responses[0]['input_tokens']
    return dict(responses=len(responses), first_input=first, **totals,
        input_relative_to_first=sum(row['input_tokens']-first for row in responses))


def compare(baseline, current):
    b, c = summarize(baseline), summarize(current)
    # I = n*f + g. Symmetric product decomposition avoids choosing an arm
    # as the reference for the n*f interaction. These are identities, not causes.
    terms = dict(
        response_count_term=(c['responses']-b['responses'])*(c['first_input']+b['first_input'])/2,
        first_input_term=(c['first_input']-b['first_input'])*(c['responses']+b['responses'])/2,
        later_input_term=c['input_relative_to_first']-b['input_relative_to_first'],
        output_term=c['output_tokens']-b['output_tokens'])
    delta = current['total_tokens']-baseline['total_tokens']
    if sum(terms.values()) != delta:
        raise ValueError('Decomposition does not reconcile')
    return dict(baseline=b, current=c, delta_total_tokens=delta, arithmetic_terms=terms)


def analyze(directory):
    directory = Path(directory)
    comparison = json.loads((directory/'comparison.json').read_text())
    pairs = {}
    for row in comparison['rows']:
        condition, case = row['condition'], row['case']
        if condition not in ('baseline', 'current') or condition in pairs.setdefault(case, {}):
            raise ValueError('Unexpected or duplicate comparison arm')
        arm = 'baseline' if condition == 'baseline' else 'skill'
        path = directory/condition/(case+'--'+arm+'--1')/'usage-profile.json'
        raw = path.read_bytes()
        profile = json.loads(raw)
        if profile['total_tokens'] != row['total_tokens']:
            raise ValueError('Published comparison mismatch')
        pairs[case][condition] = (profile, hashlib.sha256(raw).hexdigest())
    rows = []
    for case, arms in pairs.items():
        if set(arms) != {'baseline', 'current'}:
            raise ValueError('Incomplete pair')
        rows.append(dict(case=case, **compare(arms['baseline'][0], arms['current'][0]),
                         profile_sha256={k:v[1] for k,v in arms.items()}))
    return dict(rows=rows,
        limitations='Recorded usage arithmetic only. First input includes all initial context, not just the skill. Later input includes prior conversation and tool results; response-count differences are not inherently unnecessary. No causal savings, dollar estimate, or latency attribution. Cached input is counted once within input.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.directory), indent=2))
