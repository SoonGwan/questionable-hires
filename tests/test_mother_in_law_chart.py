import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'render_mother_in_law_chart', ROOT / 'benchmarks/render_mother_in_law_chart.py')
chart = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chart)


class MotherInLawChartTests(unittest.TestCase):
    def data(self):
        return dict(
            title='Interaction QA checkpoint', subtitle='GPT-6 Astra · medium',
            note='Five tasks × two arms × one session', cases=5,
            resource_ratios=dict(total_tokens=dict(baseline=100, skill=90),
                                 elapsed_seconds=dict(baseline=100, skill=80)),
            quality=dict(baseline=4, skill=5),
            clean_false_positives=dict(baseline=0, skill=0),
            quality_rows=[dict(label='Stale error', baseline='MISSED', skill='FOUND')],
            description='Focused comparison', footer='Reviewed evidence only.')

    def test_renders_montage_light_and_dark_palettes(self):
        light = chart.render(self.data())
        dark = chart.render(self.data(), dark=True)
        self.assertIn('#F7F7F8', light)
        self.assertIn('#0066FF', light)
        self.assertIn('#0F0F10', dark)
        self.assertIn('#3385FF', dark)
        self.assertIn('5/5', light)
        self.assertIn('One extra bug.', light)
        self.assertIn('MISSED', light)

    def test_rejects_out_of_range_quality(self):
        data = self.data()
        data['quality']['skill'] = 6
        with self.assertRaises(ValueError):
            chart.render(data)


if __name__ == '__main__':
    unittest.main()
