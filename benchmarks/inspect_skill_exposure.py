"""Report exact installed skill-body exposure without exporting private messages."""
import hashlib
import json
from pathlib import Path

from extract_rollout_tools import extract


def output_strings(value):
    """Unwrap recorded tool output envelopes; never inspect tool-call inputs."""
    if isinstance(value, str):
        yield value
        remaining = value.lstrip()
        if remaining.startswith(('{', '[')):
            decoder = json.JSONDecoder()
            try:
                while remaining:
                    decoded, end = decoder.raw_decode(remaining)
                    yield from output_strings(decoded)
                    remaining = remaining[end:].lstrip()
            except (ValueError, RecursionError):
                return
    elif isinstance(value, list):
        for item in value:
            yield from output_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from output_strings(item)


def summarize(raw, entries):
    """Conservative exact-content observations, not an invocation/success score."""
    observations = {name: [] for name in entries}
    first_tool = None
    for number, line in enumerate(raw.splitlines(), 1):
        record = json.loads(line)
        if record.get('type') != 'response_item':
            continue
        payload = record.get('payload', {})
        kind = payload.get('type')
        if kind in ('function_call', 'custom_tool_call'):
            if first_tool is None:
                first_tool = number
            continue
        if kind in ('function_call_output', 'custom_tool_call_output'):
            strings = list(output_strings(payload.get('output', [])))
            phase = 'tool_output'
        elif kind == 'message' and payload.get('role') in ('user', 'developer', 'system'):
            # Only structured injected skill messages, not catalog text or prose
            # quotations, establish message-level body exposure here.
            strings = [b.get('text', '') for b in payload.get('content', [])]
            phase = 'initial_message' if first_tool is None else 'later_message'
        else:
            continue
        for name, entry in entries.items():
            if phase == 'tool_output':
                matched = any(entry in text for text in strings)
            else:
                matched = any(text.startswith('<skill>\n<name>' + name + '</name>\n')
                              and '</path>\n' in text and text.endswith('\n</skill>')
                              and text.split('</path>\n', 1)[1][:-len('\n</skill>')] == entry
                              for text in strings)
            if matched:
                observations[name].append(dict(line=number, phase=phase))
    return dict(first_tool_line=first_tool, skills={name: dict(
        entry_sha256=hashlib.sha256(entry.encode()).hexdigest(), observations=observations[name])
        for name, entry in entries.items()},
        limitation='Exact full-body exposure in recorded injected messages or tool outputs only; filenames, catalog mentions and announcements are not body reads. Missing matches remain unobserved, not proof of absence. Exposure does not prove use, necessity or task success.')


def inspect(rollout, events, skills_root):
    raw, tools = extract(Path(rollout), Path(events))
    entries = {p.parent.name: p.read_text() for p in Path(skills_root).glob('*/SKILL.md')}
    if not entries:
        raise ValueError('No installed skill entries')
    result = summarize(raw, entries)
    result.update(session_id=tools['session_id'], source_sha256=tools['source_sha256'])
    return result
