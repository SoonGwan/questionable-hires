#!/usr/bin/env python3
"""Run the frozen full-checkout HTTPX audit comparison, excluding oracle context."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import subprocess

from run import ROOT, command, disabled_skills, run_cell

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'
TASKS = {
    'wsgi-cleanup': 'Audit whether tests/test_wsgi.py protects response-iterable cleanup when a client closes a response. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.',
    'asgi-head': 'Audit whether tests/test_asgi.py protects HEAD response-body handling. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.',
    'asgi-exceptions': 'Audit whether tests/test_asgi.py protects default application-exception propagation. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is adequate for the targeted fault, report that without demanding a stronger test. Do not change the original source or tests.',
}
DESIGN_TASKS = {
    'transport-design': 'Review httpx/_transports/base.py and httpx/_transports/mock.py for maintenance cost. Recommend whether any simplification is justified by actual consumers and supported contracts in this checkout. Do not edit existing files or perform a general repository audit.',
}
AUTH_DESIGN_TASKS = {
    'auth-flow-design': 'Review Auth.auth_flow, Auth.sync_auth_flow and Auth.async_auth_flow in httpx/_auth.py for maintenance cost. A proposal suggests replacing these similar-looking entrypoints with one universal authentication callback. Recommend whether that simplification is justified by actual consumers and supported contracts in this checkout. Do not edit existing files or perform a general repository audit.',
}
DIAGNOSIS_TASKS = {
    'redirect-auth': 'Diagnose this report against the HTTPX checkout: a GET with an explicit Authorization header follows a 302 from http://example.org/start to https://example.org:8443/end, but the redirected request has no Authorization. The reporter suspects a transport or cache issue because redirecting instead to https://example.org/end keeps it. Reproduce both outcomes locally without network access, identify the responsible mechanism, and recommend a safe next action. Include a same-origin normal control. Do not edit original source/tests, install dependencies, or globally disable credential protections.',
}
STREAM_DIAGNOSIS_TASKS = {
    'response-preview': 'Diagnose this HTTPX report: a logging preview consumes response.iter_bytes() inside client.stream(), then application response.read() raises StreamConsumed. A preview using response.read() instead appears to work; an ordinary client.get response also remains readable after an iter_bytes preview. The reporter suspects premature pooled-connection closure. Reproduce all three paths offline with actual Client/MockTransport and the same nonempty body, recording preview bytes, later body or exception, consumption/closed state and underlying stream close calls. Explain which boundary distinguishes the outcomes and recommend a safe next action, including the memory tradeoff of buffering. Use actual HTTPX objects, not a simulation of their internals. Preserve original files; do not fix production, use network, install dependencies, commit or publish. Keep any disposable probes project-local and remove them; captured output and a scoped diagnosis suffice.',
}
QUERY_BUILD_TASKS = {
    'query-build': '''Diagnose an HTTPX report: Client.build_request seems to lose query
values already embedded in a URL after an adapter starts passing params or the
client is given default params. The reporter suspects encoding or request caching.
Reproduce offline with actual Client.build_request, without sending any requests.
Use URL https://example.invalid/items?from=url&tag=url1&tag=url2 for four cases:
1. No client params; omit request params.
2. No client params; explicitly pass request params={}.
3. Client params={'tenant': 'client'}; omit request params.
4. Client params={'tenant': 'client', 'tag': ['client1', 'client2']}; request
   params={'tag': ['request1', 'request2'], 'page': '2'}.
For each, record the built URL and ordered repeated query items. Locate the
responsible mechanism in this checkout, distinguish URL-query behavior from
client/request params merging, and explain why omission and an empty mapping may
differ. Recommend a scoped caller-side approach for preserving intended URL
values without dropping repeated values or silently overriding caller precedence.
The requested deliverable is a diagnosis, not a library fix or general API audit.
Preserve original files, use no network or installs, and do not commit/publish.
Keep any disposable probes project-local and remove them; captured output suffices.
''',
}
DECODER_TASKS = {
    'text-finalization': 'Audit whether tests/test_decoders.py protects UTF-8 text-stream finalization when the stream ends with an incomplete multibyte sequence. Demonstrate sensitivity with one narrow isolated behavioral mutation. If coverage is missing, verify a focused assertion against correct and faulty behavior, including a valid multibyte sequence split across chunks as a normal control. If existing coverage detects the fault, identify the detecting check. Do not change original source or tests.',
    'line-crlf-split': 'Audit whether tests/test_decoders.py protects a CRLF line ending split across response chunks. Demonstrate sensitivity with one narrow isolated behavioral mutation of the CR carry-over behavior. If existing coverage detects the fault, identify the detecting assertion without demanding another test; otherwise verify a focused assertion against correct and faulty behavior. Include nearby unsplit CRLF behavior. Do not change original source or tests.',
}
QUERYPARAM_TASKS = {
    'queryparams-repeated-values': 'Audit whether tests/models/test_queryparams.py protects QueryParams.get_list returning all values for a repeated query key in order. Demonstrate sensitivity with one narrow isolated behavioral mutation. Include a single-value key as a normal control. If existing coverage detects the fault, identify the detecting assertion without demanding another test; otherwise verify a focused assertion against correct and faulty behavior. Do not change original source or tests.',
}
HEADER_TASKS = {
    'headers-two-boundaries': 'Audit whether tests/models/test_headers.py protects two separate Headers contracts: case-insensitive __getitem__ lookup and get_list preserving repeated values in order with its default split_commas=False behavior. Demonstrate each with one separate narrow isolated behavioral mutation. For each fault, identify the detecting existing assertion if killed, or verify a stronger assertion on correct and faulty code if missed. Verify a lowercase single-value header as a normal control against correct code and each fault. Do not change original source/tests or demand new tests where the selected fault is already detected.',
}
COOKIE_TASKS = {
    'cookies-scoped-clear': 'Audit whether tests/models/test_cookies.py protects Cookies.clear(domain=..., path=...) deleting only the requested path while preserving cookies at another path in the same domain and in a different domain. Demonstrate sensitivity with one narrow isolated behavioral mutation of scoped clearing. If existing coverage detects the fault, identify the detecting assertion; otherwise verify a focused assertion on correct and faulty code. Verify domain-only clearing as a normal control on correct and faulty code. Do not change original source/tests, and do not demand new tests for a fault already detected.',
}
URL_REPR_TASKS = {
    'url-repr-password': 'Audit whether the existing URL/auth tests protect URL.__repr__ masking a nonempty password while preserving the username and ordinary URL components. Use the existing tests/models/test_url.py suite plus tests/client/test_auth.py::test_auth_hidden_url for the correct baseline and the same unchanged tests against one narrow isolated masking fault. Use the supplied interpreter with pytest -q -p no:cacheprovider. Identify the detecting assertion if covered; otherwise verify a focused assertion on correct and faulty behavior. Check username-only and no-userinfo URLs as normal controls on correct and faulty code. Use only synthetic example credentials, no network. Inspect copied implementation provenance in each check process. Remove owned disposable copies, preserve all original source/tests/configuration, and report the actual evidence and scoped conclusion. Captured output is sufficient; no retained harness/report or new test is required for an already detected fault. Do not fix production, change warning policy, commit or publish.',
}


HEADER_EQUALITY_TASKS = {
    'headers-duplicate-equality': 'Audit whether tests/models/test_headers.py protects Headers equality preserving the number of identical repeated header pairs, while ignoring header-name case and pair ordering. Run that unchanged suite on correct code and one narrow isolated fault that discards duplicate multiplicity during equality. Use the supplied interpreter with pytest -q -p no:cacheprovider. Identify the detecting assertion if covered; otherwise verify the same focused assertion on correct and faulty behavior, showing actual and expected equality. Check reordered/case-varied distinct header pairs and unequal values as normal controls on both versions. Inspect copied implementation provenance in each check process. Remove owned disposable copies and preserve all original source/tests/configuration. Captured evidence and a scoped conclusion suffice; no retained harness/report is required. Do not fix production, change warning policy, use network, install dependencies, commit or publish.',
}

COOKIE_DESIGN_TASKS = {
    'cookie-storage-design': 'Review the proposal to replace the Cookies/CookieJar storage boundary with a plain dict[str, str] keyed only by cookie name. Assess maintenance cost against actual request/response/client consumers and supported domain/path behavior in this checkout. Recommend keep, simplify, or remove with source locations and the nearest viable alternative. Verify any decision-changing runtime compatibility using the existing relevant tests or a bounded local probe, including same-name cookies at different scopes and a single-cookie normal control. Do not assume fewer layers preserve semantics. Preserve original files; do not implement the proposal, install dependencies, use network, commit or publish.',
}


def select_profile(profile, requested=None):
    profiles = {'audit': ('con-artist', TASKS), 'design': ('landlord', DESIGN_TASKS),
                'diagnosis': ('exorcist', DIAGNOSIS_TASKS),
                'auth-design': ('landlord', AUTH_DESIGN_TASKS),
                'decoder-audit': ('con-artist', DECODER_TASKS),
                'queryparams-audit': ('con-artist', QUERYPARAM_TASKS),
                'headers-audit': ('con-artist', HEADER_TASKS),
                'cookies-audit': ('con-artist', COOKIE_TASKS),
                'url-repr-audit': ('con-artist', URL_REPR_TASKS),
                'header-equality-audit': ('con-artist', HEADER_EQUALITY_TASKS),
                'cookie-design': ('landlord', COOKIE_DESIGN_TASKS),
                'stream-diagnosis': ('exorcist', STREAM_DIAGNOSIS_TASKS),
                'query-build-diagnosis': ('exorcist', QUERY_BUILD_TASKS)}
    if profile not in profiles:
        raise ValueError('Unknown profile')
    skill, available = profiles[profile]
    names = list(dict.fromkeys(requested or available))
    if any(name not in available for name in names):
        raise ValueError('Case does not belong to selected profile')
    return skill, {name: available[name] for name in names}


def freeze_skill(repository, revision, destination, skill_name='con-artist'):
    """Export the whole committed skill, including optional scripts/references."""
    if skill_name not in ('con-artist', 'landlord', 'exorcist', 'receipt'):
        raise ValueError('Unsupported HTTPX profile skill')
    prefix = f'skills/{skill_name}/'
    entries = subprocess.check_output(['git', 'ls-tree', '-rz', revision, '--', prefix], cwd=repository)
    selected = []
    for entry in entries.split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.decode().split('\t', 1)
        mode, kind, object_id = metadata.split()
        path = Path(name.removeprefix(prefix))
        if not name.startswith(prefix) or path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe skill tree entry')
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Skill snapshot must contain regular files, not links/submodules')
        selected.append((path, object_id, mode))
    if Path('SKILL.md') not in [path for path, _, _ in selected]:
        raise ValueError('Revision has no selected skill')
    destination.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for path, object_id, mode in selected:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        content = subprocess.check_output(['git', 'cat-file', 'blob', object_id], cwd=repository)
        target.write_bytes(content)
        target.chmod(0o755 if mode == '100755' else 0o644)
        hashes[path.as_posix()] = hashlib.sha256(content).hexdigest()
    return hashes


def make_schedule(tasks, arms, repeats):
    if repeats < 1:
        raise ValueError('repeats must be positive')
    schedule = [(case, arm, repeat) for repeat in range(1, repeats + 1)
                for case in tasks for arm in dict.fromkeys(arms)]
    random.Random(20260912).shuffle(schedule)
    return schedule


def interpreter_path(path):
    """Normalize directory aliases without following the venv's Python symlink."""
    path = Path(path).absolute()
    return path.parent.resolve(strict=True) / path.name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profile', choices=('audit', 'design', 'diagnosis', 'auth-design', 'decoder-audit', 'queryparams-audit', 'headers-audit', 'cookies-audit', 'url-repr-audit', 'header-equality-audit', 'cookie-design', 'stream-diagnosis', 'query-build-diagnosis'), default='audit')
    parser.add_argument('--case', action='append')
    parser.add_argument('--arms', nargs='+', choices=('baseline', 'control', 'skill'), default=['baseline', 'control', 'skill'])
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--skill-revision', default='bf420fe')
    parser.add_argument('--persist-session', action='store_true',
                        help='Retain matching session records for reviewed tool-response extraction')
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('repeats must be positive')
    try:
        skill_name, tasks = select_profile(args.profile, args.case)
    except ValueError as error:
        parser.error(str(error))
    skill_revision = command(['git', 'rev-parse', '--verify', args.skill_revision + '^{commit}'], ROOT)
    source, python = args.source.resolve(), interpreter_path(args.python)
    if args.output.exists():
        raise FileExistsError(args.output)
    if command(['git', 'rev-parse', 'HEAD'], source) != REVISION:
        raise ValueError('Wrong upstream revision')
    if command(['git', 'status', '--porcelain'], source):
        raise ValueError('Upstream checkout must be clean')
    # Fail before scheduling if environment no longer passes upstream tests.
    checks = (['tests/test_wsgi.py', 'tests/test_asgi.py'] if args.profile == 'audit' else
              ['tests/client/test_client.py::test_context_managed_transport',
               'tests/client/test_client.py::test_context_managed_transport_and_mount'])
    if args.profile == 'diagnosis':
        checks = ['tests/client/test_redirects.py::test_cross_domain_redirect_with_auth_header',
                  'tests/client/test_redirects.py::test_same_domain_https_redirect_with_auth_header']
    if args.profile == 'stream-diagnosis':
        checks = ['tests/models/test_responses.py::test_read',
                  'tests/models/test_responses.py::test_iter_bytes']
    if args.profile == 'query-build-diagnosis':
        checks = ['tests/client/test_queryparams.py::test_client_queryparams',
                  'tests/client/test_queryparams.py::test_client_queryparams_echo']
    if args.profile == 'auth-design':
        checks = ['tests/client/test_auth.py::test_sync_auth_reads_response_body',
                  'tests/client/test_auth.py::test_async_auth_reads_response_body',
                  'tests/client/test_auth.py::test_sync_auth',
                  'tests/client/test_auth.py::test_async_auth']
    if args.profile == 'decoder-audit':
        checks = ['tests/test_decoders.py']
    if args.profile == 'queryparams-audit':
        checks = ['tests/models/test_queryparams.py']
    if args.profile in ('headers-audit', 'header-equality-audit'):
        checks = ['tests/models/test_headers.py']
    if args.profile in ('cookies-audit', 'cookie-design'):
        checks = ['tests/models/test_cookies.py']
    if args.profile == 'url-repr-audit':
        checks = ['tests/models/test_url.py', 'tests/client/test_auth.py::test_auth_hidden_url']
    subprocess.run([str(python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                    *checks], cwd=source, check=True, timeout=60)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    snapshot = output / 'skills' / skill_name
    skill_files = freeze_skill(ROOT, skill_revision, snapshot, skill_name)
    schedule = make_schedule(tasks, args.arms, args.repeats)
    manifest = dict(upstream_revision=REVISION, revision=command(['git', 'rev-parse', 'HEAD'], ROOT),
                    codex_version=command(['codex', '--version'], ROOT), model='gpt-6-astra', effort='medium',
                    seed=20260912, timeout_seconds=360, jobs=1,
                    session_persistence_requested=args.persist_session,
                    profile=args.profile, skill_name=skill_name, preflight_checks=checks,
                    interpreter_supplied=str(args.python), interpreter_effective=str(python),
                    skill_sha256=hashlib.sha256((snapshot / 'SKILL.md').read_bytes()).hexdigest(),
                    skill_files_sha256=skill_files,
                    tasks=tasks, schedule=schedule, skill_revision=skill_revision, completed_cells=[], stopped_after_limit=False,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    dependencies=command([str(python), '-m', 'pip', 'freeze'], source))
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    disabled = disabled_skills()
    for name, arm, repeat in schedule:
        instructions = f'\n\nUse the preinstalled interpreter {python} for all Python/pytest commands. Do not install dependencies. Keep disposable mutation copies and diagnostic artifacts inside this project, without modifying its existing files.'
        case = dict(id=name, skill=skill_name, task=tasks[name] + instructions)
        try:
            result = run_cell(case, arm, repeat, output, 'gpt-6-astra', 'medium', 360, disabled, output / 'skills', source,
                              persist_session=args.persist_session)
        except Exception as error:
            manifest['runner_error'] = f'{type(error).__name__}: {error}'
            (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
            raise
        manifest['completed_cells'].append(dict(case=name, arm=arm, repeat=repeat, completed=result['completed']))
        manifest['stopped_after_limit'] = result.get('limit_detected', False)
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(name, arm, repeat, 'completed' if result['completed'] else 'incomplete', flush=True)
        if manifest['stopped_after_limit']:
            raise SystemExit('Account limit: remaining scheduled cells unattempted; no retries')
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    if not all(row['completed'] for row in manifest['completed_cells']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
