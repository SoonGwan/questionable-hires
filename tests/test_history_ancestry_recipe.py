"""Exercise the documented native history scope against real Git DAGs."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class AncestryRecipeTests(unittest.TestCase):
    def test_explicit_base_keeps_merged_history_without_other_refs(self):
        with tempfile.TemporaryDirectory(prefix='history-ancestry-', dir=Path(__file__).resolve().parents[1]) as directory:
            root = Path(directory)
            env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)

            def git(*args, check=True):
                return subprocess.run(['git', '-C', str(root), *args], env=env,
                    check=check, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def commit(path, text, message):
                (root / path).write_text(text)
                git('add', path)
                git('commit', '-m', message)
                return git('rev-parse', 'HEAD').stdout.strip()

            git('init', '-b', 'main')
            git('config', 'user.name', 'Test')
            git('config', 'user.email', 'test@example.invalid')
            first = commit('service.py', 'value = 1\n', 'root')
            git('checkout', '-b', 'merged')
            merged = commit('service.py', 'value = 1\n# retained behavior\n', 'merged behavior')
            git('checkout', 'main')
            commit('notes.txt', 'separate main work\n', 'main work')
            git('merge', '--no-ff', 'merged', '-m', 'merge')
            base = git('rev-parse', 'HEAD').stdout.strip()
            git('checkout', '-b', 'future')
            future = commit('service.py', 'value = 1\n# retained behavior\n# future\n', 'future')
            git('checkout', '--detach', base)
            before = git('status', '--porcelain').stdout

            rows = git('log', '--format=%H', 'HEAD', '--', 'service.py').stdout.splitlines()
            self.assertEqual(set(rows), {first, merged})
            self.assertNotIn(future, rows)
            selected = git('log', '--format=%H', '-S', 'retained behavior', 'HEAD', '--', 'service.py').stdout.splitlines()
            self.assertEqual(selected, [merged])
            self.assertNotIn(merged, git('log', '--first-parent', '--format=%H', 'HEAD', '--', 'service.py').stdout.splitlines())
            self.assertEqual(git('log', '--format=%H', 'HEAD..HEAD', '--', 'service.py').stdout, '')
            self.assertNotEqual(git('log', '--all=false', check=False).returncode, 0)
            self.assertIn(future, git('log', '--all', '--format=%H', '--', 'service.py').stdout.splitlines())
            # A requested older base remains meaningful even when HEAD advances.
            git('checkout', 'future')
            self.assertEqual(git('log', '--format=%H', base, '--', 'service.py').stdout.splitlines(), rows)
            self.assertEqual(git('status', '--porcelain').stdout, before)


if __name__ == '__main__':
    unittest.main()
