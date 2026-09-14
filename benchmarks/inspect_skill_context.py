"""Inspect recorded initial skill exposure without exporting private instructions.

No model calls or availability inference. A catalog mention is not proof that a
skill can execute; a requested disable count is not proof of absent context.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from extract_rollout_tools import extract


def inspect(rollout, events, entry):
    raw, tools = extract(rollout, events)  # Verify session identity and size first.
    expected = entry.read_bytes()
    name = re.search(r'^name:\s*(\S+)\s*$', expected.decode('utf-8'), re.MULTILINE)
    if name is None:
        raise ValueError('Expected a named skill entry')
    name = name.group(1)
    catalog, injected, first_tool = [], [], None
    for number, line in enumerate(raw.splitlines(), 1):
        record = json.loads(line)
        payload = record.get('payload', {})
        if record.get('type') != 'response_item':
            continue
        if payload.get('type') in {'function_call', 'custom_tool_call'}:
            first_tool = number
            break
        if payload.get('type') != 'message':
            continue
        for block in payload.get('content', []):
            text = block.get('text', '')
            if '<skills_instructions>' in text:
                catalog.extend(re.findall(r'^- (.+?): .+ \(file: .+\)$', text, re.MULTILINE))
            if not text.startswith('<skill>\n<name>' + name + '</name>\n'):
                continue
            if '</path>\n' not in text or not text.endswith('\n</skill>'):
                continue
            body = text.split('</path>\n', 1)[1][:-len('\n</skill>')].encode('utf-8')
            injected.append(dict(line=number, role=payload.get('role'), bytes=len(body),
                                 sha256=hashlib.sha256(body).hexdigest(), exact_entry_match=body == expected))
    return dict(session_id=tools['session_id'], source_sha256=tools['source_sha256'],
                source_lines=tools['source_lines'], skill=name,
                expected_entry_sha256=hashlib.sha256(expected).hexdigest(),
                first_tool_line=first_tool, initial_catalog_names=list(dict.fromkeys(catalog)),
                initial_skill_blocks=injected,
                matching_entry_before_first_tool=first_tool is not None and any(
                    block['exact_entry_match'] for block in injected),
                limitation='Recorded messages before the first tool only. Catalog mentions do not prove executable availability or disable enforcement. Missing matches do not prove absent unrecorded context. No private message text exported.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rollout', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    parser.add_argument('--entry', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.rollout, args.events, args.entry)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))
