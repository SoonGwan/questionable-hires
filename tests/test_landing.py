"""Static landing checks: original evidence, locale metadata and raster integrity."""
import copy
import hashlib
import io
from html.parser import HTMLParser
import importlib.util
import json
import posixpath
import re
import subprocess
import sys
import tarfile
from pathlib import Path
import tempfile
import unittest
import zipfile
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

    def test_download_installs_exact_resources_and_preserves_existing_install(self):
        payload = self.files['downloads/skills.tar.gz']
        self.assertEqual(self.files['downloads/skills.sha256'].decode(),
                         hashlib.sha256(payload).hexdigest() + '  skills.tar.gz\n')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
                names = archive.getnames()
                self.assertEqual(len(names), len(set(names)))
                for member in archive.getmembers():
                    parts = Path(member.name).parts
                    self.assertTrue(member.isfile())
                    self.assertEqual(parts[0], 'questionable-hires')
                    self.assertNotIn('..', parts)
                    target = root / member.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(member).read())
                    target.chmod(member.mode)
            unpacked = root / 'questionable-hires'
            manifest = json.loads((unpacked / 'CONTENTS.json').read_bytes())
            for name, identity in manifest.items():
                self.assertTrue(name.startswith('skills/') or name in
                                ('scripts/install.py', 'LICENSE', 'docs/INSTALL-SNAPSHOT.md'))
                self.assertEqual((unpacked / name).read_bytes(), (ROOT / name).read_bytes())
                self.assertEqual(hashlib.sha256((unpacked / name).read_bytes()).hexdigest(), identity['sha256'])
                self.assertEqual((unpacked / name).stat().st_mode & 0o777, identity['mode'])
            self.assertEqual(self.files['downloads/INSTALL.md'], (unpacked / 'docs/INSTALL-SNAPSHOT.md').read_bytes())
            command = [sys.executable, '-I', '-B', str(unpacked / 'scripts/install.py'),
                       '--dest', str(root / 'installed')]
            def run(*args):
                return subprocess.run(command + list(args), cwd=root, capture_output=True,
                                      text=True, timeout=15)
            installed = run()
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertEqual(len(list((root / 'installed').glob('*/SKILL.md'))), 8)
            checked = run('--check')
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertTrue(json.loads(checked.stdout)['matches'])
            personal = root / 'installed/receipt/SKILL.md'
            personal.write_text('personal edit')
            refused = run()
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn('Existing skills left untouched', refused.stderr)
            self.assertEqual(personal.read_text(), 'personal edit')

    def test_snapshot_links_and_translations_work_from_every_route(self):
        for route, language in (('', 'en'), ('ko/', 'ko'), ('en/', 'en')):
            source = self.files[route + 'index.html'].decode()
            prefix = '../' if route else ''
            for name in ('skills.tar.gz', 'skills.sha256', 'INSTALL.md'):
                self.assertIn(f'href="{prefix}downloads/{name}"', source)
            for key in ('snapshotDownload', 'snapshotNote', 'snapshotGuide'):
                self.assertIn(self.content['copy'][language][key], source)

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
                       '1.67% more summed tokens', '9.63% less CLI time',
                       'integration07', '2026-09-28', '1be35120',
                       'unequal checks and recovered original output',
                       'ALL-EIGHT-CURRENT-07-COSTS.md', 'Cached input is already included in each response'):
            self.assertIn(phrase, en)
        for phrase in ('29.8% 증가', '6.4% 증가', '31.6% 감소',
                       '토큰 감소 3개 · 증가 2개 / 5개 과제', '토큰 1.67% 증가',
                       '시간 9.63% 감소', '검사량 차이와 원본 출력 복구의 한계'):
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

    def test_integration_comparison_and_downloads_retain_every_attempt(self):
        original = ROOT / 'benchmarks/results/all-eight-current-07/comparison.json'
        self.assertEqual(self.files['evidence/integration07/comparison.json'], original.read_bytes())
        for name in ('ALL-EIGHT-CURRENT-07-COSTS.md', 'ALL-EIGHT-CURRENT-07-REVIEW.md'):
            self.assertEqual(self.files['evidence/integration07/benchmarks/' + name], (ROOT / 'benchmarks' / name).read_bytes())
        rows = json.loads(original.read_text())['rows']
        for language in ('ko', 'en'):
            source = self.files[language + '/index.html'].decode()
            for row in rows:
                self.assertIn(f'{row["total_tokens"]:,}', source)
                self.assertIn(f'{row["elapsed_seconds"]:.3f}', source)
            self.assertIn('592,783', source)
            self.assertIn('602,679', source)
            self.assertIn('data-evidence-file="evidence/integration07/comparison.json"', source)
            self.assertNotIn('github.com/SoonGwan/questionable-hires/blob/main/benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md', source)

    def test_downloaded_report_relative_evidence_links_are_served(self):
        for path, content in self.files.items():
            if not path.startswith('evidence/') or not path.endswith('.md'):
                continue
            for href in re.findall(r'\]\(([^)]+)\)', content.decode()):
                link = landing.urlsplit(href)
                if link.scheme or not link.path:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(path), link.path))
                self.assertTrue(target in self.files, f'{path} links to unserved {href}')

    def test_evidence_bundle_keeps_report_links_and_original_bytes(self):
        for checkpoint in ('integration05', 'integration06', 'integration07'):
            prefix = 'evidence/' + checkpoint + '/'
            with zipfile.ZipFile(io.BytesIO(self.files[prefix + 'reports.zip'])) as archive:
                names = set(archive.namelist())
                for name in names:
                    self.assertFalse(name.startswith('/') or '..' in Path(name).parts)
                    content = archive.read(name)
                    self.assertEqual(content, self.files[prefix + name])
                    if not name.endswith('.md'):
                        continue
                    for href in re.findall(r'\]\(([^)]+)\)', content.decode()):
                        link = landing.urlsplit(href)
                        if not link.scheme and link.path:
                            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), link.path))
                            self.assertTrue(target in names, f'{name} links to absent ZIP member {href}')

    def test_historical_bundle_and_current_resource_boundaries_are_preserved(self):
        self.assertEqual(hashlib.sha256(self.files['evidence/integration05/reports.zip']).hexdigest(),
                         '7582f9eac11e12fffc84a3f7310d475d78b8e878a9abdd2f9b42a407958dcc4a')
        self.assertEqual(hashlib.sha256(self.files['evidence/integration06/reports.zip']).hexdigest(),
                         '0149f9f664fd5b32ac781dcd84b26637381b429d6912cd68a09a76cc4da7cc99')
        manifest = landing.read_json(ROOT / 'landing/evidence-manifest.json')['integration06']
        for name in manifest:
            self.assertEqual(self.files['evidence/integration06/' + name], (ROOT / name).read_bytes())
        self.assertIn('tests/test_receipt_path_observation_candidate.py', manifest)
        for lang in ('ko', 'en'):
            source = self.files[lang + '/index.html'].decode()
            self.assertIn('494.990', source)
            self.assertIn('447.302', source)
            self.assertNotIn('75183f2f', source)

    def test_integration_rejects_missing_duplicate_and_inconsistent_attempts(self):
        original = landing.read_json
        for fault in ('missing', 'duplicate', 'counter', 'cached', 'responses'):
            def changed(path):
                value = original(path)
                if str(path).endswith('all-eight-current-07/comparison.json'):
                    if fault == 'missing':
                        value['rows'].pop()
                    elif fault == 'duplicate':
                        value['rows'][-1] = copy.deepcopy(value['rows'][0])
                    elif fault == 'cached':
                        value['rows'][0]['cached_input_tokens'] = value['rows'][0]['input_tokens'] + 1
                    elif fault == 'responses':
                        value['rows'][0]['recorded_responses'] = 0
                    else:
                        value['rows'][0]['total_tokens'] += 1
                return value
            with self.subTest(fault=fault), patch.object(landing, 'read_json', side_effect=changed):
                with self.assertRaises(ValueError):
                    landing.integration07()

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
            self.assertRegex(source, r'src="../assets/team-characters\.[0-9a-f]{64}\.png"')
            self.assertNotIn('localhost', source)
        self.assertIn('https://hires.example.org/project/sitemap.xml', files['robots.txt'].decode())
        self.assertIn('https://hires.example.org/project/en/', files['sitemap.xml'].decode())

    def test_artwork_identity_changes_url_without_changing_source_bytes(self):
        source = ROOT / 'assets/team-characters.png'
        original = source.read_bytes()
        name = 'assets/team-characters.' + hashlib.sha256(original).hexdigest() + '.png'
        self.assertEqual(self.files[name], original)
        self.assertEqual(self.files['assets/team-characters.png'], original)
        for route in ('', 'ko/', 'en/'):
            prefix = '../' if route else ''
            self.assertEqual(self.files[route + 'index.html'].decode().count('src="' + prefix + name + '"'), 2)
        read_bytes = Path.read_bytes
        changed = original + b'changed release identity'
        def read(path):
            return changed if path == source else read_bytes(path)
        with patch.object(Path, 'read_bytes', read):
            with self.assertRaisesRegex(ValueError, 'Stale artwork derivative'):
                landing.build()

    def test_webp_selection_keeps_original_fallback_and_rejects_stale_bytes(self):
        source = ROOT / 'assets/team-characters.webp'
        original = source.read_bytes()
        name = 'assets/team-characters.' + hashlib.sha256(original).hexdigest() + '.webp'
        self.assertEqual(self.files[name], original)
        for route in ('', 'ko/', 'en/'):
            prefix = '../' if route else ''
            html = self.files[route + 'index.html'].decode()
            self.assertEqual(html.count('<picture>'), 2)
            self.assertEqual(html.count('type="image/webp" srcset="' + prefix + name + '"'), 2)
            self.assertEqual(len(re.findall(r'<img src="[^"]+\.png" width="1536" height="1024"', html)), 2)
        read_bytes = Path.read_bytes
        with patch.object(Path, 'read_bytes', lambda path: b'changed' if path == source else read_bytes(path)):
            with self.assertRaisesRegex(ValueError, 'Stale artwork derivative'):
                landing.build()

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
