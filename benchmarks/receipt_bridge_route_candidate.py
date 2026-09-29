"""Optional direct-tool route candidate; ordinary Receipt guidance stays unchanged."""
ANCHOR = "For an already-present fix, compare isolated versions"
ROUTE = "For an already-present Python fix, first check whether the launch-authorized project tool `receipt_compare` is available. If needed, use the available tool discovery to find that exact tool and inspect its input schema. Prefer it for supported native unittest version comparisons: it runs the same isolated comparison and returns native outputs, assertion observations, provenance and cleanup. Supply the requested revisions, current tests and evidence options; inspect the returned observations rather than also running the CLI for the same comparison. If the tool is unavailable or incompatible, use the ordinary project/CLI route below. Tool discovery is not execution or proof of a repair.\n\n"


def entry(source):
    if 'name: receipt\n' not in source.split('\n---\n')[0]:
        raise ValueError('Expected Receipt entry')
    if source.count(ROUTE) == 1:
        return source
    if source.count(ANCHOR) != 1:
        raise ValueError('Expected original comparison guidance')
    return source.replace(ANCHOR, ROUTE + ANCHOR)
