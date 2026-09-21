"""Pinned upstream slugify controls; author preparation, not model measurement."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'f85f9488520148d5f6899b5639199882b605e30a'
BLOBS = {
    'LICENSE': '82af695f594e8c1e83ee98db0bcae758620f1b63',
    'slugify/__init__.py': '6d3279fb1ac2e9c3febeca395a5f7350d8fa5969',
    'slugify/__main__.py': '4cc461622837bf5c765c06d9a5f20f265945d968',
    'slugify/__version__.py': '854038e500d54f104aa0390ad191e81c3ea9dfce',
    'slugify/py.typed': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    'slugify/slugify.py': '09c7e076cf27406c7f0ab324b5ac1da787da3624',
    'slugify/special.py': '918cb2add83f5135b4e9528956abaddeff9c6893',
    'test.py': 'd13ef94f7b36e126871af4a8f4e4e4fedc53cdd1',
}
TARGET = 'slugify/slugify.py'
PREFIX = 'test.TestSlugify.'
SELECTORS = [PREFIX + 'test_non_word_characters', PREFIX + 'test_max_length']
WITNESSES = [PREFIX + 'test_custom_separator', PREFIX + 'test_save_order']
FAULTS = [
    ('omit-separator', 'text = text.replace(DEFAULT_SEPARATOR, separator)', 'text = text', [0, 0, 1, 0]),
    ('ignore-order', 'smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, save_order)',
     'smart_truncate(text, max_length, word_boundary, DEFAULT_SEPARATOR, False)', [0, 0, 0, 1]),
    ('omit-limit', 'if max_length > 0:', 'if False:', [0, 1, 0, 1]),
]


def load_source(checkout):
    revision = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != REVISION:
        raise ValueError('Wrong upstream revision')
    files = {}
    for name, expected in BLOBS.items():
        path = checkout / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Not a regular upstream file: ' + name)
        body = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if digest != expected:
            raise ValueError('Changed upstream file: ' + name)
        files[name] = body
    return files


def preflight(checkout):
    files = load_source(checkout)
    source = files[TARGET].decode()
    rows = []
    with tempfile.TemporaryDirectory(prefix='slugify-preflight-', dir=ROOT / 'benchmarks/local-runs') as folder:
        project = Path(folder)
        for name, body in files.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        modes = {name: (project / name).stat().st_mode & 0o777 for name in files}
        env = dict(os.environ, PYTHONPATH=str(project), PYTHONDONTWRITEBYTECODE='1')
        variants = [('correct', None, None, [0, 0, 0, 0]), *FAULTS,
                    ('equivalent', 'if max_length > 0:', 'if 0 < max_length:', [0, 0, 0, 0])]
        for name, old, new, expected in variants:
            if old is not None and source.count(old) != 1:
                raise ValueError('Ambiguous patch: ' + name)
            (project / TARGET).write_text(source if old is None else source.replace(old, new, 1))
            observations = []
            for selector, code in zip(SELECTORS + WITNESSES, expected):
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', selector, '-v'],
                    cwd=project, env=env, text=True, capture_output=True, timeout=20)
                output = result.stdout + result.stderr
                if (result.returncode != code or 'Ran 1 test' not in output or 'ERROR' in output
                        or (code == 1 and 'AssertionError:' not in output)):
                    raise AssertionError(name + '/' + selector + '\n' + output)
                observations.append(dict(selector=selector, exit_code=result.returncode, output=output))
            rows.append(dict(variant=name, observations=observations))
        (project / TARGET).write_bytes(files[TARGET])
        entries = [dict(target=TARGET, old=old, new=new) for _, old, new, _ in FAULTS]
        entries += [dict(entries[i], tests=[witness, '-v']) for i, witness in enumerate(WITNESSES)]
        recipe = dict(files=list(files), imports=['slugify.slugify', 'test'], runner='unittest',
            invocation='module', tests=SELECTORS + ['-v'], mutations=entries,
            precheck="import importlib\nm = importlib.import_module('slugify.slugify')\n"
                     "t = importlib.import_module('test')\nassert t.slugify is m.slugify\n"
                     "print('copied slugify binding verified', flush=True)\n")
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
            '--source', str(project), '--spec', '-'], input=json.dumps(recipe),
            text=True, capture_output=True, timeout=60)
        if result.returncode:
            raise AssertionError(result.stderr + result.stdout)
        report = json.loads(result.stdout)
        assert report['status'] == 'observed' and len(report['audits']) == 5
        for index, audit in enumerate(report['audits']):
            normal = audit['checks']['correct_tests']
            if index in (1, 2):
                assert normal['observation_ref'] == '#/audits/0/checks/correct_tests'
            else:
                assert normal['exit_code'] == 0
            mutant = audit['checks']['mutant_tests']
            assert mutant['exit_code'] == mutant['native_exit_code'] == int(index >= 2)
            assert mutant['suite_observation'] == dict(tests=2 if index < 3 else 1,
                                                       skipped=0, successful=index < 2)
            assert 'copied slugify binding verified' in mutant['output']
            assert 'ERROR' not in mutant['output']
            if index >= 2:
                assert 'AssertionError:' in mutant['output']
            assert audit['integrity']['owned_scratch_removed']
        assert {str(p.relative_to(project)) for p in project.rglob('*') if p.is_file()} == set(files)
        for name, body in files.items():
            assert (project / name).read_bytes() == body
            assert (project / name).stat().st_mode & 0o777 == modes[name]
        assert sorted(p.name for p in project.iterdir()) == ['LICENSE', 'slugify', 'test.py']
    assert not project.exists()
    return dict(upstream_revision=REVISION, upstream_blob_ids=BLOBS, python=sys.version,
        dependency={'text-unidecode': importlib.metadata.version('text-unidecode')},
        direct_controls=rows, helper_report=report, scratch_removed=True,
        limitation='20 direct native processes plus 8 helper native processes / 12 method executions. '
                   'Author-selected unchanged upstream tests and deliberate faults; not model evidence or a blind holdout.')


if __name__ == '__main__':
    from export import redact_paths
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = preflight(args.checkout.resolve())
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2)) + '\n')
    print('Upstream native controls and helper parity passed; no model calls.')
