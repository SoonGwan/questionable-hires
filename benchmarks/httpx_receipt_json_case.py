"""Actual HTTPX encoder commit, with identical current native tests/support."""
HEAD = '26d48e0634e6ee9cdc0533996db289ce4b430177'
BEFORE = '8e36f2bc685dfbe43cd7503bc1c422a6ed6e05a5'
AFTER = '9fd6f0ca6616d0310a3ee0b0c6ef509a97995797'
TESTS = (
    'tests/test_content.py::test_empty_content[asyncio]',
    'tests/test_content.py::test_json_content[asyncio]',
    'tests/test_content.py::test_ensure_ascii_false_with_french_characters',
    'tests/test_content.py::test_separators_for_compact_json',
    'tests/test_content.py::test_allow_nan_false',
)


def case(python):
    return dict(id='httpx-json-commit', skill='receipt', task=f'''Verify the encoder change in actual HTTPX commit {AFTER}
against its parent {BEFORE}. This is a retrospective verification, not a repair.
Compare only httpx/_content.py from the two revisions, keeping the checkout's
current package support, test assertions and configuration identical. Do not
claim to reproduce each complete historical dependency environment.

Use the existing interpreter {python} with -B and native pytest -vv. Execute exactly
these five native test cases on each encoder version, with the original project
conftest/configuration and no cache-provider artifacts:
''' + '\n'.join(TESTS) + '''

Inspect the actual commit change, tests and relevant public Request/Response
path. Report each required before/after result, defect-specific assertion values,
the passing control, full revision IDs and the test process's own exit. Establish
that the public HTTPX package and encoder load from the corresponding disposable
copy in the same native test process. Do not substitute a rewritten encoder,
mocked response, import-only process or different assertions for this comparison.

Use project-local copies and remove owned scratch before finishing. Preserve all
original files, modes, user changes and installed skill resources. Captured results
are sufficient; retain no report/harness. No dependency installs, network requests,
external discovery, commits, publishing, global environment changes or production
edits. Existing URLs in content tests are inert constructor values, not authorization
to send requests. All needed dependencies are already installed.
''', criteria=[
        'Identical five native tests/config/support against only the changed encoder.',
        'Defect-specific before failures and after results, with passing empty-body control.',
        'Same-process copy-local package and encoder import evidence with full revisions.',
        'Original files/resources preserved; owned project-local scratch removed; scope respected.',
    ])
