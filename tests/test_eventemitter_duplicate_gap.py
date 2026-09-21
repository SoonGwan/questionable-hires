import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'benchmarks'))
from eventemitter_boundary_cases import corrected, files
from probe_eventemitter_duplicate_gap import observe


class DuplicateGapTests(unittest.TestCase):
    def test_frozen_reference_loses_duplicate_but_identity_removal_preserves_it(self):
        frozen = corrected(files()['index.js'], 'once-reentrant-dispatch')
        fixed = frozen
        for expression in ('listeners', 'listeners[i]'):
            old = 'this.removeListener(event, ' + expression + '.fn, undefined, true);'
            self.assertEqual(fixed.count(old), 1)
            fixed = fixed.replace(old, 'removeRegistration(this, evt, ' + expression + ');')
        fixed += '''\nfunction removeRegistration(owner, evt, target) {
  var current = owner._events[evt];
  if (current === target) clearEvent(owner, evt);
  else if (current && !current.fn) {
    var remaining = current.filter(function (item) { return item !== target; });
    if (!remaining.length) clearEvent(owner, evt);
    else owner._events[evt] = remaining.length === 1 ? remaining[0] : remaining;
  }
}\n'''
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'index.js'
            for code, expected in [(frozen, 1), (fixed, 0)]:
                source.write_text(code)
                result = observe(source)
                self.assertEqual(result['exit_code'], expected, result)
                self.assertEqual(json.loads(result['output'])['remaining'], 0 if expected else 1)
                if expected:
                    self.assertIn('Throwing registration removed an unconsumed duplicate', result['stderr'])
                else:
                    self.assertEqual(result['stderr'], '')
