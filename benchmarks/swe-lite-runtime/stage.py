"""Stage an allowlisted build context; never copy scoring records or credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def stage(destination, root=ROOT):
    sources = []
    groups = [
        ('requests-diagnosis/installed-wheel-hashes.json', 'requests-pytest'),
        ('services/wheel-hashes.json', 'wheelhouse'),
        ('tls/certifi-wheel.json', 'requests-pytest'),
    ]
    for manifest, folder in groups:
        hashes = json.loads((root / 'benchmarks/results' /
                            ('swe-lite-pilot-01-' + manifest)).read_text())
        for name, digest in hashes.items():
            if Path(name).name != name or not name.endswith('.whl'):
                raise ValueError('Invalid wheel filename')
            source = root / 'benchmarks/local-runs' / ('swe-lite-pilot-01-' + folder) / name
            if source.is_symlink() or hashlib.sha256(source.read_bytes()).hexdigest() != digest:
                raise ValueError('Wheel bytes differ from reviewed preflight')
            sources.append((source, 'wheels/' + name))
    for name in ('Dockerfile', 'prepare.py'):
        sources.append((root / 'benchmarks/swe-lite-runtime' / name, name))
    ca = root / 'benchmarks/local-runs/swe-lite-tls-01/ca.pem'
    if ca.is_symlink() or b'PRIVATE KEY' in ca.read_bytes():
        raise ValueError('Expected a public certificate only')
    sources.append((ca, 'ca.pem'))
    destination.mkdir(parents=True, exist_ok=False)
    manifest = {}
    for source, name in sources:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(stage(args.destination), indent=2, sort_keys=True))
