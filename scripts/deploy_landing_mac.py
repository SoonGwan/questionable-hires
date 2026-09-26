#!/usr/bin/env python3
"""Deploy a generated static landing as dedicated macOS/Cloudflare services."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import socket
import subprocess
import sys
import time
import uuid

REPO = Path(__file__).resolve().parents[1]
APP = 'questionable-hires'
BASE = Path.home() / 'Library/Application Support' / APP
AGENTS = Path.home() / 'Library/LaunchAgents'
LOGS = Path.home() / 'Library/Logs' / APP
GUI = f'gui/{os.getuid()}'
WEB = 'com.questionable-hires.web'
TUNNEL = 'com.questionable-hires.tunnel'


def run(*args, check=True):
    result = subprocess.run(args, text=True, capture_output=True, timeout=60)
    if check and result.returncode:
        raise RuntimeError(f'{args[0]} {args[1]} failed: {result.stderr.strip() or result.stdout.strip()}')
    return result


def agent(label, args):
    AGENTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    plist = AGENTS / (label + '.plist')
    plist.write_bytes(plistlib.dumps(dict(Label=label, ProgramArguments=args,
        RunAtLoad=True, KeepAlive=True, ThrottleInterval=5,
        StandardOutPath=str(LOGS / (label + '.log')),
        StandardErrorPath=str(LOGS / (label + '.err.log')))))
    if run('launchctl', 'print', f'{GUI}/{label}', check=False).returncode == 0:
        run('launchctl', 'bootout', f'{GUI}/{label}')
    run('launchctl', 'enable', f'{GUI}/{label}')
    for attempt in range(10):
        result = run('launchctl', 'bootstrap', GUI, str(plist), check=False)
        if not result.returncode:
            return
        time.sleep(.5)
    raise RuntimeError('Could not bootstrap ' + label + ': ' + result.stderr.strip())


def health(url, revision, attempts=20):
    for _ in range(attempts):
        arguments = ['curl', '--fail', '--silent', '--show-error', '--max-time', '4']
        if url.startswith('https://'):
            # New hostnames can be negatively cached by the Mac's local DNS resolver.
            # Resolve the public name through Cloudflare DNS while retaining HTTPS verification.
            arguments.extend(['--doh-url', 'https://cloudflare-dns.com/dns-query'])
        result = run(*arguments, url + '_health', check=False)
        try:
            value = json.loads(result.stdout)
            if not result.returncode and value.get('app') == APP and value.get('revision') == revision:
                return
        except ValueError:
            pass
        time.sleep(1)
    raise RuntimeError('Expected landing release did not respond at ' + url)


def switch_release(release):
    temporary = BASE / ('current-' + uuid.uuid4().hex)
    temporary.symlink_to(release, target_is_directory=True)
    os.replace(temporary, BASE / 'current')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domain', default='hires.no-money-do-you-have-money.com')
    parser.add_argument('--port', type=int, default=4180)
    parser.add_argument('--rollback', action='store_true', help='Restore the previous successful local release')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        parser.error('This deployment command requires macOS')
    if not re.fullmatch(r'[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?', args.domain) or '..' in args.domain:
        parser.error('domain must be a lowercase DNS hostname')
    cloudflared = shutil.which('cloudflared')
    if not cloudflared or not (Path.home() / '.cloudflared/cert.pem').is_file():
        parser.error('Install cloudflared and run cloudflared tunnel login first')
    url = f'https://{args.domain}/'
    current = BASE / 'current'
    previous = current.resolve() if current.is_symlink() else None
    state_path = BASE / 'deployment.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else None
    if state and (state['domain'] != args.domain or state['port'] != args.port):
        parser.error('Existing deployment uses a different domain/port; reconcile it before redeploying')
    with socket.socket() as connection:
        occupied = connection.connect_ex(('127.0.0.1', args.port)) == 0
    if occupied:
        if not state:
            parser.error('Origin port is already occupied; choose another port')
        health(f'http://127.0.0.1:{args.port}/', state['revision'], attempts=1)
    if args.rollback:
        if not state or not state.get('previous'):
            parser.error('No previous successful deployment exists')
        release = Path(state['previous'])
        manifest = json.loads((release / 'site/release.json').read_text())
        revision = manifest['revision']
        print('Restoring previous release', flush=True)
    else:
        if run('git', '-C', str(REPO), 'status', '--porcelain').stdout.strip():
            parser.error('Commit the requested changes before deploying a dated release')
        revision = run('git', '-C', str(REPO), 'rev-parse', 'HEAD').stdout.strip()
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        release = BASE / 'releases' / (stamp + '-' + revision[:8] + '-' + uuid.uuid4().hex[:6])
        release.mkdir(parents=True)
        print('Building static release with ' + url, flush=True)
        result = run(sys.executable, '-B', str(REPO / 'scripts/build_landing.py'), '--site-url', url, '--output', str(release / 'site'))
        print(result.stdout.strip(), flush=True)
        shutil.copyfile(REPO / 'scripts/serve_landing.py', release / 'server.py')
        (release / 'site/release.json').write_text(json.dumps(dict(app=APP, revision=revision,
            site_url=url, built_at=stamp), indent=2) + '\n')
    switch_release(release)
    web_args = [sys.executable, '-B', str(current / 'server.py'), '--directory', str(current / 'site'), '--port', str(args.port)]
    try:
        agent(WEB, web_args)
        health(f'http://127.0.0.1:{args.port}/', revision)
    except Exception:
        if previous:
            switch_release(previous)
            agent(WEB, web_args)
        else:
            run('launchctl', 'bootout', f'{GUI}/{WEB}', check=False)
            current.unlink(missing_ok=True)
        raise
    deployment = dict(domain=args.domain, port=args.port, tunnel_id=state.get('tunnel_id') if state else None,
                      revision=revision, release=str(release), previous=str(previous) if previous else None,
                      dns_routed=bool(state and state.get('dns_routed')), phase='origin-ready')
    state_path.write_text(json.dumps(deployment, indent=2) + '\n')
    print('Local origin identity verified', flush=True)
    tunnels = json.loads(run(cloudflared, 'tunnel', 'list', '--output', 'json').stdout)
    matching = [tunnel for tunnel in tunnels if tunnel['name'] == APP]
    if len(matching) > 1:
        raise RuntimeError('Multiple tunnels share the app name')
    if matching:
        tunnel_id = matching[0]['id']
    else:
        print('Creating dedicated Cloudflare Tunnel', flush=True)
        created = json.loads(run(cloudflared, 'tunnel', 'create', '--output', 'json', APP).stdout)
        tunnel_id = created['id']
    credentials = Path.home() / '.cloudflared' / (tunnel_id + '.json')
    if not credentials.is_file():
        raise RuntimeError('Tunnel credentials are missing; do not overwrite an existing tunnel')
    config = BASE / 'cloudflared.yml'
    config.write_text(f'tunnel: {tunnel_id}\ncredentials-file: {json.dumps(str(credentials))}\nmetrics: 127.0.0.1:0\ningress:\n  - hostname: {args.domain}\n    service: http://127.0.0.1:{args.port}\n  - service: http_status:404\n')
    run(cloudflared, 'tunnel', '--config', str(config), 'ingress', 'validate')
    agent(TUNNEL, [cloudflared, '--no-autoupdate', '--config', str(config), 'tunnel', 'run', tunnel_id])
    deployment['tunnel_id'] = tunnel_id
    state_path.write_text(json.dumps(deployment, indent=2) + '\n')
    if not deployment['dns_routed']:
        print('Adding the subdomain DNS route (without overwriting existing records)', flush=True)
        run(cloudflared, 'tunnel', 'route', 'dns', tunnel_id, args.domain)
        deployment['dns_routed'] = True
        state_path.write_text(json.dumps(deployment, indent=2) + '\n')
    print('Checking the public HTTPS release', flush=True)
    health(url, revision, attempts=30)
    deployment['phase'] = 'live'
    state_path.write_text(json.dumps(deployment, indent=2) + '\n')
    print('Live: ' + url + 'ko/ and ' + url + 'en/', flush=True)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        print('Deployment incomplete: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
