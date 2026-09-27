"""Author control: retain native pytest categories instead of guessing from outcome.

No project/gold inputs. The hook call mirrors these installed versions' terminal
reporter. This is not a replacement official parser or accepted issue grade.
"""
import json
import pathlib
import sys

import pytest


class Capture:
    def __init__(self):
        self.reports = []

    def pytest_configure(self, config):
        self.config = config

    def pytest_runtest_logreport(self, report):
        category, letter, label = self.config.hook.pytest_report_teststatus(report=report)
        self.reports.append(dict(nodeid=report.nodeid, when=report.when,
                                 outcome=report.outcome, category=category,
                                 wasxfail=hasattr(report, 'wasxfail')))


if __name__ == '__main__':
    capture = Capture()
    result = pytest.main(['--assert=plain', '-rA', '--tb=short',
                          '--basetemp', sys.argv[2], sys.argv[1]], plugins=[capture])
    calls = {r['nodeid'].split('::')[-1]: r for r in capture.reports if r['when'] == 'call'}
    expected = {'test_pass': 'passed', 'test_fail': 'failed', 'test_skip': 'skipped',
                'test_xfail': 'xfailed', 'test_xpass': 'xpassed'}
    assert {name: calls[name]['category'] for name in expected} == expected
    assert any(r['nodeid'].endswith('test_setup_error') and r['when'] == 'setup'
               and r['category'] == 'error' for r in capture.reports)
    assert any(r['nodeid'].endswith('test_teardown_error') and r['when'] == 'teardown'
               and r['category'] == 'error' for r in capture.reports)
    assert result == 1, result
    summary = dict(result='PASS', pytest_version=pytest.__version__,
                   pytest_path=str(pathlib.Path(pytest.__file__).resolve()),
                   native_exit=result, expected_categories=expected,
                   xpass_native_outcome=calls['test_xpass']['outcome'],
                   setup_error=True, teardown_error=True, model_calls=0)
    pathlib.Path(sys.argv[3]).write_text(json.dumps(summary, indent=2) + '\n')
