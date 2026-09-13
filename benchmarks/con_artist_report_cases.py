#!/usr/bin/env python3
"""Generate one evidence-interpretation task from real mutation-helper execution."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def cases():
    spec = importlib.util.spec_from_file_location('report_audit', ROOT / 'skills/con-artist/scripts/audit.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    files = {
        'service.py': 'def save(store, value):\n    store.append(value)\n    return True\n',
        'test_service.py': ('import unittest\nfrom service import save\n'
            'class SaveTests(unittest.TestCase):\n'
            '    def test_acknowledgment(self):\n        self.assertTrue(save([], "item"))\n'),
        'requirements.md': 'Saving appends the submitted value exactly once, preserves existing values, and returns True.\n'}
    probe = 'from service import save\ns = ["kept"]\nassert save(s, "item") is True\nassert s == ["kept", "item"]\n'
    common = dict(target='service.py', old='    store.append(value)\n', probe=probe, probe_when='survives')
    recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
                  tests=['-v', 'test_service'], mutations=[
                      dict(common, new=''),
                      dict(common, new='    store.extend([value, value])\n'),
                      dict(common, new='    store.append(\n')])
    with tempfile.TemporaryDirectory(prefix='qh-report-fixture-') as scratch:
        project = Path(scratch)
        for name, content in files.items():
            (project / name).write_text(content)
        report = helper.audit_batch(project, recipe, python=sys.executable, timeout=5)
        # Redact only the disposable pathname in captured tracebacks, not checks.
        report_text = json.dumps(report, indent=2).replace(str(project), '<audit-project>')
    files.update({
        'audit-recipe.json': json.dumps(recipe, indent=2) + '\n',
        'audit-result.json': report_text + '\n',
        'README.md': ('The supplied audit result was collected by the Con Artist batch helper from '
            'the supplied code and recipe. Only disposable paths in captured tracebacks were redacted. '
            'observation_ref is a JSON Pointer into this same report, identifying an earlier executed '
            'check. No runner result changed during capture. Review these existing observations; '
            'do not execute the mutations again or modify files.\n')})
    return [dict(id='con-artist-report-reference-v2', skill='con-artist', files=files,
        task=('Review what the existing mutation audit establishes about the save tests. '
              'Explain the supported coverage conclusions, any invalid evidence, and the most '
              'useful test improvement. Use the supplied run records without rerunning the audit '
              'or changing project files.'),
        criteria=[
            'Resolve reused normal-test observations without treating a reference as missing execution or a new independent run.',
            'Identify omitted and duplicate persistence as surviving the acknowledgment test, with the same stronger probe passing correct and failing faulty code.',
            'Treat the final syntax-error variant as incomplete import setup, not behavioral sensitivity; its unrun probes are not validated.',
            'Recommend an exact-content persistence assertion retaining existing content and one submitted item, not only truthiness or length.',
            'Do not rerun mutations or modify original files; stay within the supplied project.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
