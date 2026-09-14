"""New authored review ticket on an existing pinned real HTTPX checkout."""
HEAD = '26d48e0634e6ee9cdc0533996db289ce4b430177'
HEADERS = [None, '</next>', '</next>; rel=next',
           '</next>; rel=next; type=text/plain',
           '</next>; token=a=b; rel=next', '</next>; preload; rel=next']


def case(python):
    return dict(id='link-history', skill='necromancer', task='''Review two independent proposed cleanups in httpx._models._parse_header_links:
A: change only url, params = val.split(";", 1) to url, params = val.split(";").
B: change only key, value = param.split("=") to key, value = param.split("=", 1).
Keep the surrounding try/except, breaks, stripping and caller unchanged.
Do not combine the proposals. Are they behavior-preserving at Response.links?
This is a compatibility review, not an instruction to improve standards support.

Observe actual httpx.Response(200, headers=...).links for current, A-only and
B-only, independently, with these six Link header inputs in this order:
1. No Link header.
2. </next>
3. </next>; rel=next
4. </next>; rel=next; type=text/plain
5. </next>; token=a=b; rel=next
6. </next>; preload; rel=next
Retain the complete returned mapping (keys and values) or actual error for each
of all 18 observations. Explain changes and unchanged controls through the actual
public property and parser. Compatibility means preserving these current
observations; a potentially useful behavior change is not equivalent cleanup.

Establish locally evidenced history: inspect the relevant attributed change and
an earlier operational implementation plus its Response.links caller. Distinguish
code movement/renaming from introduction. Cite actual ancestor code; first-ever
origin or author intent is not required and must not be invented. Use only
ancestors of pinned HEAD, not external issues or other branch tips.
Give separate retain/simplify/remove recommendations and the behavior to preserve.

Preserve all original files and installed resources. No network, installations,
fetching, commits or publishing. Use <PREINSTALLED_PYTHON> with -B; pytest also
with -p no:cacheprovider. In-memory substitutions or owned disposable copies are
allowed; no particular implementation technique is required. Scratch must stay
inside this project and be removed before finishing. Captured output is enough;
no separate report file or persistent harness is required.'''.replace(
        '<PREINSTALLED_PYTHON>', str(python)))
