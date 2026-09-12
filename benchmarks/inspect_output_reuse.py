#!/usr/bin/env python3
"""Count exact long-line recurrence across command outputs; not wasted-work scoring."""
import argparse
import json
from pathlib import Path


def inspect(events, minimum_length=80):
    if minimum_length < 1:
        raise ValueError('minimum_length must be positive')
    seen_ids, seen_lines, commands = set(), set(), []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError('Expected JSON objects')
        item = event.get('item', {})
        if (event.get('type') != 'item.completed' or not isinstance(item, dict)
                or item.get('type') != 'command_execution'):
            continue
        identity = item.get('id')
        if not isinstance(identity, str) or identity in seen_ids:
            raise ValueError('Missing or repeated completed command identity')
        seen_ids.add(identity)
        output = item.get('aggregated_output', '')
        if not isinstance(output, str):
            raise ValueError('Expected textual command output')
        lines = output.splitlines(keepends=True)
        eligible = [line for line in lines if len(line.rstrip('\r\n')) >= minimum_length]
        recurring = [line for line in eligible if line in seen_lines]
        commands.append(dict(id=identity, exit_code=item.get('exit_code'),
                             output_characters=len(output),
                             eligible_characters=sum(map(len, eligible)),
                             recurring_characters=sum(map(len, recurring)),
                             recurring_lines=len(recurring)))
        # Repetition inside a single output is not a second command read.
        seen_lines.update(eligible)
    return dict(commands=commands, command_count=len(commands),
                output_characters=sum(c['output_characters'] for c in commands),
                recurring_characters=sum(c['recurring_characters'] for c in commands),
                minimum_line_length=minimum_length,
                limitation='Exact recurrence can be necessary verification or shared boilerplate. '
                           'Changed formatting is missed. Characters are not model tokens, '
                           'and recurrence does not establish avoidable work or causal cost.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logs', type=Path, nargs='+')
    parser.add_argument('--minimum-length', type=int, default=80)
    args = parser.parse_args()
    for path in args.logs:
        events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        result = inspect(events, args.minimum_length)
        # Deliberately omit raw command/output text from aggregate reports.
        print(json.dumps(dict(log=str(path), **result)))


if __name__ == '__main__':
    main()
