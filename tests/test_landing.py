"""Static landing checks: original evidence, locale metadata and raster integrity."""
import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('build_landing', ROOT / 'scripts/build_landing.py')
landing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(landing)


class Head(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.meta = {}
        self.links = []
        self.language = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta[attrs.get('property', attrs.get('name'))] = attrs.get('content')
        elif tag == 'link':
            self.links.append(attrs)
        elif tag == 'html':
            self.language = attrs['lang']


class LandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.preview = landing.build()
        cls.evidence = landing.featured()
        cls.content = landing.read_json(ROOT / 'landing/content.json')

    def test_featured_pointer_and_published_values_are_the_sources(self):
        pointer = landing.read_json(ROOT / 'benchmarks/featured.json')
        for language in ('ko', 'en'):
            source = self.files[language + '/index.html'].decode()
            self.assertIn(Path(pointer['result_directory']).name, source)
            for metric in ('total_tokens', 'elapsed_seconds'):
                value = self.evidence['data']['resource_ratios'][metric]['skill']
                self.assertIn(f'{value-100:+.1f}<small>%</small>', source)
                self.assertIn(f'{value:.1f}%', source)
            self.assertIn(self.evidence['revision'], source)
            self.assertIn(self.evidence['date'], source)

    def test_all_cells_including_adverse_values_are_rendered(self):
        evidence = self.evidence
        source = self.files['en/index.html'].decode()
        for cell in evidence['cells']:
            self.assertIn(cell['case'], source)
            self.assertIn(f'{cell["input_tokens"] + cell["output_tokens"]:,}', source)
            self.assertIn(f'{cell["elapsed_seconds"]:.3f}', source)
        for case in {cell['case'] for cell in evidence['cells']}:
            records = {cell['arm']: cell for cell in evidence['cells'] if cell['case'] == case}
            for metric in ('total_tokens', 'elapsed_seconds'):
                def value(arm):
                    cell = records[arm]
                    return cell['input_tokens'] + cell['output_tokens'] if metric == 'total_tokens' else cell[metric]
                self.assertIn(f'{100 * value("skill") / value("baseline"):.1f}%', source)
        self.assertIn('129.8%', source)  # This higher-cost case must stay visible.
        self.assertIn('126.4%', source)
        self.assertIn('Ratios of raw sums differ', source)
        self.assertIn('general whole-team superiority', source)

    def test_cost_interpretation_preserves_increases_and_actual_usage(self):
        en = self.files['en/index.html'].decode()
        ko = self.files['ko/index.html'].decode()
        for phrase in ('29.8% more', '6.4% more', '31.6% less',
                       'Without 64,055 → with 83,165',
                       'Tokens decreased on 3, increased on 2 / 5 tasks',
                       '18.54% more summed tokens', '9.06% more time',
                       'integration05', '2026-09-27', '75183f2f',
                       'Detailed quality review remains incomplete',
                       'ALL-EIGHT-CURRENT-05-COSTS.md', 'Cached input is included once'):
            self.assertIn(phrase, en)
        for phrase in ('29.8% 증가', '6.4% 증가', '31.6% 감소',
                       '토큰 감소 3개 · 증가 2개 / 5개 과제', '토큰 18.54%',
                       '시간 9.06% 증가', '품질 상세 검토는 미완료'):
            self.assertIn(phrase, ko)

    def test_changed_source_evidence_cannot_silently_change_published_chart(self):
        original = landing.read_json
        def changed(path):
            value = original(path)
            if path.name == 'cells.json':
                value = copy.deepcopy(value)
                value[0]['quality_target_met'] = False
            return value
        with patch.object(landing, 'read_json', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'quality differs'):
                landing.featured()

    def test_each_locale_has_static_metadata_and_copy_without_javascript(self):
        for language in ('ko', 'en'):
            source = self.files[language + '/index.html'].decode()
            head = Head(source)
            text = self.content['copy'][language]
            self.assertEqual(head.language, language)
            self.assertEqual(head.meta['og:title'], text['title'])
            self.assertEqual(head.meta['og:description'], text['description'])
            self.assertEqual(head.meta['og:locale'], 'ko_KR' if language == 'ko' else 'en_US')
            self.assertEqual(head.meta['twitter:card'], 'summary_large_image')
            self.assertTrue(head.meta['og:image'].endswith(f'/assets/og-{language}.png'))
            self.assertEqual(head.meta['og:image:width'], '1200')
            self.assertEqual(head.meta['og:image:height'], '630')
            self.assertEqual(head.meta['og:image:alt'], text['ogAlt'])
            self.assertIn(text['heroHeading'], source)
            self.assertNotIn('{{', source)
            self.assertIn('Without skill' if language == 'en' else '스킬 미적용', source)
            self.assertIn('<button type="button" class="hire"', source)
            self.assertIn('class="task-chart"', source)
            self.assertEqual({link['hreflang'] for link in head.links if 'hreflang' in link}, {'ko', 'en', 'x-default'})

    def test_production_origin_and_subdirectory_are_applied_everywhere(self):
        files, preview = landing.build('https://hires.example.org/project/')
        self.assertFalse(preview)
        for language in ('ko', 'en'):
            source = files[language + '/index.html'].decode()
            head = Head(source)
            self.assertEqual(head.meta['og:url'], f'https://hires.example.org/project/{language}/')
            self.assertEqual(head.meta['og:image:secure_url'], f'https://hires.example.org/project/assets/og-{language}.png')
            self.assertEqual(head.meta['robots'], 'index, follow, max-image-preview:large')
            self.assertIn('href="../ko/"', source)
            self.assertIn('src="../assets/team-characters.png"', source)
            self.assertNotIn('localhost', source)
        self.assertIn('https://hires.example.org/project/sitemap.xml', files['robots.txt'].decode())
        self.assertIn('https://hires.example.org/project/en/', files['sitemap.xml'].decode())

    def test_preview_is_not_indexable(self):
        self.assertTrue(self.preview)
        self.assertEqual(Head(self.files['index.html'].decode()).meta['robots'], 'noindex, nofollow')
        self.assertIn('Disallow: /', self.files['robots.txt'].decode())

    def test_production_url_rejects_invalid_or_local_metadata(self):
        for url in ('example.org', 'http://hires.example.org', 'https://localhost/',
                    'https://hires.example.org/?secret=x', 'https://user:password@hires.example.org/'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                landing.build(url)

    def test_localized_fragments_match_static_page_experiments(self):
        for language in ('ko', 'en'):
            source = self.files[language + '/index.html'].decode()
            fragment = self.files['experiments/' + language + '.html'].decode()
            self.assertIn(fragment, source)

    def test_generated_preview_is_current_and_rasters_match_sources(self):
        for name, expected in self.files.items():
            self.assertEqual((ROOT / 'landing' / name).read_bytes(), expected, name)
        landing.verify_rasters(self.files)


if __name__ == '__main__':
    unittest.main()
