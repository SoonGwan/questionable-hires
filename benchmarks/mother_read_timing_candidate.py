"""Move existing read guidance into the initially visible description, unchanged."""

GUIDANCE = '''Read supplied requirements, interaction code, native tests, existing test support
and applicable project instructions together when practical. Discover missing
paths, not another inventory before known-file reads.
'''
INLINE = ' '.join(GUIDANCE.splitlines())


def entry(source):
    lines = source.splitlines(keepends=True)
    if not lines or lines[0] != '---\n':
        raise ValueError('Expected YAML frontmatter')
    end = lines.index('---\n', 1)
    descriptions = [i for i in range(1, end) if lines[i].startswith('description: ')]
    if len(descriptions) != 1:
        raise ValueError('Expected one single-line description')
    i = descriptions[0]
    if lines[i].rstrip('\n').endswith(INLINE) and GUIDANCE not in source:
        return source
    if source.count(GUIDANCE) != 1 or INLINE in lines[i]:
        raise ValueError('Expected the unchanged Mother initial-read paragraph')
    lines[i] = lines[i].rstrip('\n') + ' ' + INLINE + '\n'
    return ''.join(lines).replace(GUIDANCE, '', 1)
