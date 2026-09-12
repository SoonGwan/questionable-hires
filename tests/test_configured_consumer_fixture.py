import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ConfiguredConsumerFixtureTests(unittest.TestCase):
    def test_normal_unit_check_misses_configured_null_consumer(self):
        spec = importlib.util.spec_from_file_location(
            'configured_fixture', ROOT / 'benchmarks/configured_consumer_cases.py')
        fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture)
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for name, source in case['files'].items():
                target = project / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source)
            def run(code):
                return subprocess.run([sys.executable, '-B', '-c', code], cwd=project,
                                      text=True, capture_output=True, timeout=5)
            check = ('import unittest\n'
                     'r = unittest.TextTestRunner().run(unittest.defaultTestLoader.discover("."))\n'
                     'assert r.testsRun == 1 and r.wasSuccessful()\n')
            for mutation in (False, True):
                setup = ''
                if mutation:
                    setup = '''from pathlib import Path
import core.labels
source = Path('core/labels.py').read_text()
guard = "    if value is None:\\n        return 'unknown'\\n"
assert source.count(guard) == 1
exec(compile(source.replace(guard, ''), 'core/labels.py', 'exec'), core.labels.__dict__)
'''
                unit = run(setup + check)
                self.assertEqual(unit.returncode, 0, unit.stderr)
                application = run(setup + 'import app, json\nprint(json.dumps(app.render()))\n')
                if mutation:
                    self.assertNotEqual(application.returncode, 0)
                    self.assertIn("'NoneType' object has no attribute 'strip'", application.stderr)
                    self.assertIn('integrations/archive/bridge.py', application.stderr)
                else:
                    self.assertEqual(application.returncode, 0, application.stderr)
                    self.assertEqual(json.loads(application.stdout), ['A', 'unknown'])
            for name, source in case['files'].items():
                self.assertEqual((project / name).read_text(), source)
