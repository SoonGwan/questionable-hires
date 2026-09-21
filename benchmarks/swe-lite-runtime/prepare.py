"""Prepare dependencies only in a disposable, base-only solver image."""
from pathlib import Path
import subprocess
import sys

TREES = {
    'requests': '980e006268fb816b7d2686baef7242418d895d9a',
    'pytest': '877d433795f3d7288b9edd5696724bb2d8e47f88',
}


def main(project):
    assert Path('/.dockerenv').is_file() and Path.cwd() == Path('/testbed')
    tree = TREES[project]
    def git(*args):
        return subprocess.check_output(['git', *args], text=True).strip()
    assert git('rev-parse', 'HEAD^{tree}') == tree
    assert git('rev-list', '--all', '--count') == '1'
    assert not git('remote') and not git('status', '--porcelain')
    if project == 'requests':
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-index',
            '--find-links=/opt/qh-wheels', 'pytest==4.6.11', 'pluggy==0.13.1',
            'atomicwrites==1.4.1', 'py==1.11.0', 'six==1.17.0',
            'attrs==23.2.0', 'more-itertools==9.1.0', 'packaging==24.2',
            'wcwidth==0.2.13', 'certifi==2024.8.30'], check=True)
        import certifi
        bundle = Path(certifi.where())
        assert not str(bundle).startswith('/testbed/')
        with bundle.open('ab') as stream:
            stream.write(b'\n' + Path('/opt/qh-ca.pem').read_bytes())
    assert git('rev-parse', 'HEAD^{tree}') == tree
    assert not git('status', '--porcelain')


if __name__ == '__main__':
    main(sys.argv[1])
