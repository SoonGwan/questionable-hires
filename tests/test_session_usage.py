import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'benchmarks'))
from profile_session_usage import summarize


class SessionUsageTests(unittest.TestCase):
    def raw(self, *values):
        return '\n'.join(json.dumps(dict(type='event_msg',payload=dict(type='token_count',info=dict(total_token_usage=v)))) for v in values)

    def usage(self, inputs, cached, output):
        return dict(input_tokens=inputs,cached_input_tokens=cached,output_tokens=output,reasoning_output_tokens=7)

    def test_advances_duplicates_and_cache_accounting(self):
        a,b = self.usage(100,80,10),self.usage(220,180,30)
        result=summarize(self.raw(a,a,b),b)
        self.assertEqual(result['total_tokens'],250)
        self.assertEqual(result['uncached_input_tokens'],40)
        self.assertEqual(result['duplicate_counter_records'],1)
        self.assertEqual(result['recorded_advances'][1],dict(line=3,input_tokens=120,cached_input_tokens=100,output_tokens=20))

    def test_resets_missing_fields_and_invalid_cache_are_rejected(self):
        for raw in (self.raw(self.usage(100,80,10),self.usage(50,40,5)),
                    self.raw({}),self.raw(self.usage(100,101,10)),
                    self.raw(self.usage(True,0,0))):
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                summarize(raw,self.usage(100,80,10))

    def test_cli_mismatch_and_absence_are_not_estimated(self):
        with self.assertRaises(ValueError):
            summarize(self.raw(self.usage(100,80,10)),self.usage(101,80,10))
        with self.assertRaises(ValueError):
            summarize('',self.usage(0,0,0))

    def test_response_records_reconcile_and_deduplicate_by_identity(self):
        a,b = self.usage(100,80,10),self.usage(120,100,20)
        def response(name, value):
            return json.dumps(dict(type='token_usage_record',payload=dict(response_id=name,usage=value)))+'\n'
        raw=response('a',a)+response('a',a)+response('b',b)+self.raw(self.usage(220,180,30))
        self.assertEqual(len(summarize(raw,self.usage(220,180,30))['recorded_responses']),2)
        with self.assertRaisesRegex(ValueError,'reconcile'):
            summarize(response('a',a)+self.raw(self.usage(220,180,30)),self.usage(220,180,30))
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            summarize(response('a',a)+response('a',b),a)
