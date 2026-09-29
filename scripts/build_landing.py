#!/usr/bin/env python3
"""Build bilingual static landing pages from the canonical copy and featured data."""
import argparse
import html
import hashlib
import io
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
import zipfile
from urllib.parse import urlsplit
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / 'landing'
sys.path.insert(0, str(ROOT / 'benchmarks'))
from audit_mother_in_law_checkpoint import summarize  # Reuse the existing evidence audit.
sys.path.insert(0, str(ROOT / 'scripts'))
from package_skills import package

GITHUB = 'https://github.com/SoonGwan/questionable-hires'
VOID = {'meta', 'link', 'img', 'br', 'input', 'hr', 'source', 'wbr'}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def integration07():
    directory = ROOT / 'benchmarks/results/all-eight-current-07'
    rows = read_json(directory / 'comparison.json')['rows']
    records = {(row['case'], row['condition']): row for row in rows}
    cases = sorted({row['case'] for row in rows})
    if len(rows) != 16 or len(records) != 16 or len(cases) != 8:
        raise ValueError('integration07 must retain all16 unique attempts')
    for case in cases:
        for condition in ('baseline', 'current'):
            row = records.get((case, condition))
            if (row is None or not row['completed'] or row['total_tokens'] <= 0
                    or row['elapsed_seconds'] <= 0
                    or not 0 <= row['cached_input_tokens'] <= row['input_tokens']
                    or row['output_tokens'] < 0 or row['recorded_responses'] < 1
                    or row['total_tokens'] != row['input_tokens'] + row['output_tokens']):
                raise ValueError('integration07 comparison is incomplete or inconsistent')
    sums = {condition: {metric: sum(records[(case, condition)][metric] for case in cases)
                       for metric in ('total_tokens', 'input_tokens', 'cached_input_tokens',
                                      'output_tokens', 'recorded_responses', 'elapsed_seconds')}
            for condition in ('baseline', 'current')}
    return dict(records=records, cases=cases, sums=sums)


def integration_evidence_files(checkpoint='integration07'):
    # Keep historical URLs while preserving each report's original relative links.
    roots = {'integration05': ROOT / 'benchmarks', 'integration06': ROOT, 'integration07': ROOT}
    evidence_root = roots[checkpoint]
    number = checkpoint.removeprefix('integration')
    report_prefix = 'benchmarks/' if checkpoint != 'integration05' else ''
    names = read_json(LANDING / 'evidence-manifest.json')[checkpoint]
    if len(names) != len(set(names)):
        raise ValueError('duplicate reviewed evidence path')
    approved = {}
    for name in names:
        source = evidence_root / name
        if (Path(name).is_absolute() or '..' in Path(name).parts
                or not source.resolve().is_relative_to(evidence_root.resolve())
                or source.is_symlink() or source.suffix not in {'.md', '.json', '.txt', '.py'}):
            raise ValueError('invalid reviewed evidence path: ' + name)
        approved[source.resolve()] = source.read_bytes()
    for name in (f'ALL-EIGHT-CURRENT-{number}-COSTS.md', f'ALL-EIGHT-CURRENT-{number}-REVIEW.md'):
        if (evidence_root / report_prefix / name).resolve() not in approved:
            raise ValueError('missing reviewed report: ' + name)
    for source, content in approved.items():
        if source.suffix != '.md':
            continue
        for href in re.findall(r'\]\(([^)]+)\)', content.decode()):
            link = urlsplit(href)
            if not link.scheme and not link.netloc and link.path:
                if (source.parent / link.path).resolve() not in approved:
                    raise ValueError('unreviewed evidence link: ' + href)
    return {'evidence/' + checkpoint + '/' + source.relative_to(evidence_root.resolve()).as_posix(): content
            for source, content in approved.items()}


def integration_table(checkpoint, copy, prefix):
    e = html.escape
    parts = [f'<details class="checkpoint-details"><summary data-focus-key="checkpoint-summary">{e(copy["checkpointTable"])}</summary>',
             f'<p class="checkpoint-scroll-hint raw-note">{e(copy["checkpointScrollHint"])}</p>',
             f'<div class="table-scroll" data-focus-key="checkpoint-table" tabindex="0" role="region" aria-label="{e(copy["checkpointTable"])}">',
             '<table><caption>integration07 · 2026-09-28 · 1be35120</caption><thead><tr>',
             f'<th scope="col">{e(copy["rawCase"])}</th>']
    breakdown = []
    for condition, label in (('baseline', 'conditionBaseline'), ('current', 'conditionSkill')):
        totals = checkpoint['sums'][condition]
        breakdown.append('<p class="raw-note">' + e(copy['checkpointTokenBreakdown'].format(
            condition=copy[label], **{key: f'{value:,}' for key, value in totals.items()})) + '</p>')
    parts[1:1] = breakdown + [f'<p class="raw-note">{e(copy["checkpointCacheMeaning"])}</p>']
    for condition in ('conditionBaseline', 'conditionSkill'):
        for metric in ('rawTokens', 'rawElapsed'):
            parts.append(f'<th scope="col">{e(copy[condition])} · {e(copy[metric])}</th>')
    parts.append('</tr></thead><tbody>')
    for case in checkpoint['cases']:
        parts.append(f'<tr><th scope="row">{e(copy["checkpoint-" + case])}<code>{e(case)}</code></th>')
        for condition in ('baseline', 'current'):
            row = checkpoint['records'][(case, condition)]
            parts.append(f'<td>{row["total_tokens"]:,}</td><td>{row["elapsed_seconds"]:.3f}</td>')
        parts.append('</tr>')
    parts.append(f'</tbody><tfoot><tr><th scope="row">{e(copy["rawTotal"])}</th>')
    for condition in ('baseline', 'current'):
        row = checkpoint['sums'][condition]
        parts.append(f'<td>{row["total_tokens"]:,}</td><td>{row["elapsed_seconds"]:.3f}</td>')
    parts.append('</tr></tfoot></table></div></details>')
    for name, label in (('benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md', 'costAnalysis'),
                        ('benchmarks/ALL-EIGHT-CURRENT-07-REVIEW.md', 'checkpointReview'),
                        ('comparison.json', 'checkpointJson'),
                        ('reports.zip', 'checkpointBundle')):
        path = 'evidence/integration07/' + name
        parts.append(f'<a data-focus-key="{label}" data-evidence-file="{path}" href="{e(prefix + path)}" download>{e(copy[label])} ↓</a>')
    return '\n'.join(parts)


def featured():
    pointer = read_json(ROOT / 'benchmarks/featured.json')
    directory = (ROOT / pointer['result_directory']).resolve()
    directory.relative_to(ROOT / 'benchmarks/results')
    data = read_json(directory / 'data.json')
    cells = read_json(directory / 'cells.json')
    summary = summarize(cells)
    for key in ('cases', 'resource_ratios', 'quality', 'clean_false_positives'):
        if data[key] != summary[key]:
            raise ValueError(f'Featured {key} differs from recorded cells')
    date = re.search(r'\d{4}-\d{2}-\d{2}', directory.name)
    revision = re.search(r'\b[0-9a-f]{7,40}\b', data['note'])
    if not date or not revision:
        raise ValueError('Featured evidence needs an explicit date and measured resource')
    return dict(pointer=pointer, data=data, cells=cells, summary=summary,
                date=date.group(), revision=revision.group(), checkpoint=directory.name)


class Localize(HTMLParser):
    """Render translated text server-side without needing a client-side crawler."""
    def __init__(self, copy, language):
        super().__init__(convert_charrefs=False)
        self.copy, self.language, self.parts, self.depth = copy, language, [], 0

    def handle_starttag(self, tag, attrs):
        if self.depth:
            if tag not in VOID:
                self.depth += 1
            return
        attrs = dict(attrs)
        if tag == 'html':
            attrs['lang'] = self.language
        for marker, attribute in (('data-i18n-alt', 'alt'), ('data-i18n-aria', 'aria-label')):
            if marker in attrs:
                attrs[attribute] = self.copy[attrs[marker]]
        if 'data-language' in attrs:
            if attrs['data-language'] == self.language:
                attrs['aria-current'] = 'page'
            else:
                attrs.pop('aria-current', None)
        rendered = ''.join(f' {key}' if value is None else f' {key}="{html.escape(value, quote=True)}"'
                           for key, value in attrs.items())
        self.parts.append(f'<{tag}{rendered}>')
        if 'data-i18n' in attrs:
            self.parts.append(html.escape(self.copy[attrs['data-i18n']]))
            self.depth = 1

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1
            if self.depth:
                return
        self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        if not self.depth:
            self.parts.append(data)

    def handle_comment(self, data):
        if not self.depth:
            self.parts.append(f'<!--{data}-->')

    def handle_decl(self, data):
        self.parts.append(f'<!{data}>')

    def handle_entityref(self, name):
        if not self.depth:
            self.parts.append(f'&{name};')

    def handle_charref(self, name):
        if not self.depth:
            self.parts.append(f'&#{name};')


def metadata(copy, language, base, preview):
    url = base + language + '/'
    image = base + f'assets/og-{language}.png'
    locale = {'ko': 'ko_KR', 'en': 'en_US'}
    other = 'en' if language == 'ko' else 'ko'
    def meta(key, value, property=False):
        return f'<meta {"property" if property else "name"}="{key}" content="{html.escape(str(value), quote=True)}">'
    tags = [f'<title>{html.escape(copy["title"])}</title>', meta('description', copy['description']),
            meta('robots', 'noindex, nofollow' if preview else 'index, follow, max-image-preview:large'),
            f'<link rel="canonical" href="{url}">']
    for lang in ('ko', 'en'):
        tags.append(f'<link rel="alternate" hreflang="{lang}" href="{base}{lang}/">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{base}">')
    properties = {'og:type': 'website', 'og:site_name': 'Questionable Hires', 'og:title': copy['title'],
                  'og:description': copy['description'], 'og:url': url, 'og:locale': locale[language],
                  'og:locale:alternate': locale[other], 'og:image': image, 'og:image:type': 'image/png',
                  'og:image:width': 1200, 'og:image:height': 630, 'og:image:alt': copy['ogAlt']}
    if base.startswith('https:'):
        properties['og:image:secure_url'] = image
    tags.extend(meta(key, value, True) for key, value in properties.items())
    tags.extend(meta(key, value) for key, value in {
        'twitter:card': 'summary_large_image', 'twitter:title': copy['title'],
        'twitter:description': copy['description'], 'twitter:image': image, 'twitter:image:alt': copy['ogAlt']
    }.items())
    structured = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', '@id': base + '#website', 'url': base, 'name': 'Questionable Hires',
         'inLanguage': ['ko', 'en'], 'sameAs': GITHUB},
        {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': copy['title'],
         'description': copy['description'], 'inLanguage': language,
         'isPartOf': {'@id': base + '#website'}}]}
    tags.append('<script type="application/ld+json">' + json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c') + '</script>')
    return '\n  '.join(tags)


def experiment(evidence, copy, checkpoint=None, prefix='../'):
    checkpoint = checkpoint or integration07()
    data, cells, summary = evidence['data'], evidence['cells'], evidence['summary']
    records = {(cell['case'], cell['arm']): cell for cell in cells}
    cases = sorted({cell['case'] for cell in cells})
    e = html.escape
    report = GITHUB + '/blob/main/' + evidence['pointer']['result_directory']
    totals = checkpoint['sums']
    def change(metric):
        delta = 100 * (totals['current'][metric] / totals['baseline'][metric] - 1)
        return copy['changeLess' if delta < 0 else 'changeMore' if delta > 0 else 'changeEqual'].format(value=f'{abs(delta):.2f}')
    performance_detail = copy['performanceDetail'].format(
        tokenChange=change('total_tokens'), timeChange=change('elapsed_seconds'))
    parts = ['<article class="experiment" aria-labelledby="experiment-heading">',
             f'<div class="experiment-label">{e(copy["experimentLabel"])}</div>',
             f'<h3 id="experiment-heading">{e(copy["experimentTitle"])}</h3>',
             f'<p class="experiment-intro">{e(copy["experimentIntro"])}</p>',
             f'<p class="experiment-source"><code>{e(evidence["checkpoint"])}</code><span>{evidence["date"]} / {evidence["revision"]}</span></p>',
             '<div class="metric-grid">']
    for key, label in (('total_tokens', 'meanTokens'), ('elapsed_seconds', 'meanElapsed')):
        value = data['resource_ratios'][key]['skill']
        parts.append(f'<div class="metric"><span>{e(copy[label])}</span><strong>{value-100:+.1f}<small>%</small></strong>'
                     f'<p>{e(copy["conditionSkill"])} {value:.1f}% / {e(copy["conditionBaseline"])} 100%</p></div>')
    parts.append('<div class="metric metric-quality">' + f'<span>{e(copy["qualityLabel"])}</span>'
                 f'<strong>{data["quality"]["baseline"]}/{data["cases"]}<small> → </small>{data["quality"]["skill"]}/{data["cases"]}</strong>'
                 f'<p>{e(copy["conditionBaseline"])} → {e(copy["conditionSkill"])} · {e(copy["falsePositiveLabel"])} '
                 f'{data["clean_false_positives"]["baseline"]} → {data["clean_false_positives"]["skill"]}{e(copy["falsePositiveUnit"])}</p></div></div>')
    token_ratios = [100 * (records[(case, 'skill')]['input_tokens'] + records[(case, 'skill')]['output_tokens']) /
                    (records[(case, 'baseline')]['input_tokens'] + records[(case, 'baseline')]['output_tokens']) for case in cases]
    cost_summary = copy['costSummary'].format(lower=sum(r < 100 for r in token_ratios),
                                            higher=sum(r > 100 for r in token_ratios), total=len(cases))
    parts.extend([f'<p class="normalized-note">{e(copy["normalized"])}</p>',
                  f'<p class="token-meaning">{e(copy["tokenMeaning"])}</p>',
                  f'<p class="cost-summary">{e(cost_summary)}</p>',
                  '<div class="chart-top">', f'<h4>{e(copy["chartHeading"])}</h4>',
                  '<div class="chart-controls" role="group" hidden>',
                  f'<button type="button" data-focus-key="tokens" data-metric="total_tokens" aria-pressed="true">{e(copy["tokens"])}</button>',
                  f'<button type="button" data-focus-key="elapsed" data-metric="elapsed_seconds" aria-pressed="false">{e(copy["elapsed"])}</button></div></div>',
                  f'<p class="chart-description" id="chart-description">{e(copy["chartDescription"])}</p>',
                  f'<div class="chart-legend" aria-label="{e(copy["chartLegend"])}"><span class="baseline-key">{e(copy["conditionBaseline"])}</span><span class="skill-key">{e(copy["conditionSkill"])}</span></div>'])
    for metric, label in (('total_tokens', 'chartTokensLabel'), ('elapsed_seconds', 'chartElapsedLabel')):
        def value(cell):
            return cell['input_tokens'] + cell['output_tokens'] if metric == 'total_tokens' else cell['elapsed_seconds']
        ratios = [100 * value(records[(case, 'skill')]) / value(records[(case, 'baseline')]) for case in cases]
        ceiling = max(150, (int(max(ratios) // 50) + 1) * 50)
        parts.append(f'<figure class="task-chart" data-chart="{metric}" aria-describedby="chart-description"><figcaption>{e(copy[label])}</figcaption>')
        for case, ratio in zip(cases, ratios):
            name = copy.get('case-' + case, case)
            change = copy['changeLess' if ratio < 100 else 'changeMore' if ratio > 100 else 'changeEqual'].format(value=f'{abs(ratio - 100):.1f}')
            formatter = (lambda x: f'{x:,}') if metric == 'total_tokens' else (lambda x: f'{x:.3f} s')
            usage = copy['actualUsage'].format(baseline=formatter(value(records[(case, 'baseline')])),
                                             skill=formatter(value(records[(case, 'skill')])))
            parts.append(f'<div class="chart-row"><span class="chart-case">{e(name)}<small>{e(change)}</small></span><div class="chart-bars" style="--baseline-width:{100/ceiling*100:.4f}%">'
                         f'<div class="bar baseline" style="--bar-width:{100/ceiling*100:.4f}%"><span class="sr-only">{e(copy["conditionBaseline"])} </span><span class="bar-value">100%</span></div>'
                         f'<div class="bar skill" style="--bar-width:{ratio/ceiling*100:.4f}%"><span class="sr-only">{e(copy["conditionSkill"])} </span><span class="bar-value">{ratio:.1f}%</span></div><p class="chart-usage">{e(usage)}</p></div></div>')
        parts.append('<div class="chart-axis" aria-hidden="true"><span></span><div>' + ''.join(
            f'<span style="left:{tick/ceiling*100:.4f}%">{tick}%</span>' for tick in range(0, ceiling + 1, 50)) + '</div></div></figure>')
    parts.extend([f'<details class="raw-details"><summary data-focus-key="raw-summary">{e(copy["rawSummary"])}</summary>',
                  f'<p class="method">{e(copy["method"].format(cases=data["cases"]))}</p>',
                  f'<div class="table-scroll" data-focus-key="raw-table" role="region" tabindex="0" aria-label="{e(copy["rawCaption"])}"><table><caption>{e(copy["rawCaption"])}</caption><thead><tr>'])
    parts.extend(f'<th scope="col">{e(copy[key])}</th>' for key in ('rawCase', 'rawArm', 'rawTokens', 'rawElapsed', 'rawQuality'))
    parts.append('</tr></thead><tbody>')
    for case in cases:
        for arm, label in (('baseline', 'conditionBaseline'), ('skill', 'conditionSkill')):
            cell = records[(case, arm)]
            parts.append(f'<tr><th scope="row">{e(copy.get("case-" + case, case))}<code>{e(case)}</code></th><td>{e(copy[label])}</td>'
                         f'<td>{cell["input_tokens"] + cell["output_tokens"]:,}</td><td>{cell["elapsed_seconds"]:.3f}</td><td>{e(copy["met"]) if cell["quality_target_met"] else "—"}</td></tr>')
    parts.append('</tbody><tfoot>')
    for arm, label in (('baseline', 'conditionBaseline'), ('skill', 'conditionSkill')):
        sums = summary['raw_sums'][arm]
        parts.append(f'<tr><th scope="row">{e(copy["rawTotal"])}</th><td>{e(copy[label])}</td><td>{sums["total_tokens"]:,}</td><td>{sums["elapsed_seconds"]:.3f}</td><td>{data["quality"][arm]}/{data["cases"]}</td></tr>')
    parts.extend(['</tfoot></table></div>', f'<p class="raw-note">{e(copy["rawNote"])}</p></details>',
                  f'<aside class="experiment-limit"><h4>{e(copy["limitationTitle"])}</h4><p>{e(copy["limitation"])}</p></aside>',
                  f'<aside class="experiment-limit"><h4>{e(copy["performanceStatus"])}</h4><p>{e(performance_detail)}</p>{integration_table(checkpoint, copy, prefix)}</aside>',
                  f'<div class="experiment-links"><a data-focus-key="full-report" href="{report}/README.md">{e(copy["fullReport"])} ↗</a><a data-focus-key="raw-records" href="{report}/cells.json">{e(copy["rawRecords"])} ↗</a></div></article>'])
    return '\n'.join(parts)


def roster(hires, language):
    return '\n'.join(f'<button type="button" class="hire" data-hire="{index}" aria-pressed="{str(index == 0).lower()}">'
                     f'<span class="number">{index+1:02}</span><span><strong>{html.escape(hire[language]["name"])}</strong>'
                     f'<span class="codename">{hire["id"]}</span></span><span class="arrow" aria-hidden="true">↗</span></button>'
                     for index, hire in enumerate(hires))


def svg_card(copy, language):
    tagline = '이걸 뽑네. 근데 일을 하네.' if language == 'ko' else 'Weird, but employed. Unfortunately, essential.'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">{html.escape(copy['title'])}</title>
  <desc id="desc">{html.escape(copy['ogAlt'])}</desc>
  <rect width="1200" height="630" fill="#F7F7F8"/>
  <g font-family="Helvetica Neue, Arial, Apple SD Gothic Neo, sans-serif">
    <text x="68" y="81" fill="#2E2F33" font-size="16" letter-spacing="2">8 DEVELOPER AGENT SKILLS</text>
    <text x="60" y="253" fill="#171719" font-size="126" font-weight="700" letter-spacing="-7">Questionable</text>
    <text x="60" y="389" fill="#0066FF" font-size="126" font-weight="700" letter-spacing="-7">Hires.</text>
    <text x="68" y="458" fill="#171719" font-size="29">{html.escape(tagline)}</text>
    <path d="M68 510H1132" stroke="#171719" stroke-opacity=".15"/>
    <text x="68" y="559" fill="#2E2F33" font-size="17">OPEN SOURCE / MIT</text>
    <text x="1132" y="559" text-anchor="end" fill="#0066FF" font-size="17">{html.escape(copy['preview'])}</text>
  </g>
</svg>
'''


def build(base=None):
    content = read_json(LANDING / 'content.json')
    if set(content['copy']['ko']) != set(content['copy']['en']):
        raise ValueError('Language dictionaries differ')
    configured = base or read_json(LANDING / 'site.json')['site_url']
    preview = configured is None
    base = configured or 'http://localhost:4173/landing/'
    parsed = urlsplit(base)
    if (parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.query or parsed.fragment
            or parsed.username or parsed.password):
        raise ValueError('site_url must be an absolute HTTP(S) directory URL without credentials/query/fragment')
    if not preview and (parsed.scheme != 'https' or parsed.hostname in ('localhost', '127.0.0.1')):
        raise ValueError('A production site_url must use public HTTPS')
    base = base.rstrip('/') + '/'
    evidence = featured()
    checkpoint = integration07()
    template = (LANDING / 'templates/page.html').read_text()
    artwork = (ROOT / 'assets/team-characters.png').read_bytes()
    webp = (ROOT / 'assets/team-characters.webp').read_bytes()
    artwork_record = json.loads((ROOT / 'assets/team-characters-webp.json').read_text())
    if (hashlib.sha256(artwork).hexdigest() != artwork_record['source_sha256']
            or hashlib.sha256(webp).hexdigest() != artwork_record['webp_sha256']):
        raise ValueError('Stale artwork derivative; run scripts/encode_landing_artwork.py')
    artwork_path = 'assets/team-characters.' + hashlib.sha256(artwork).hexdigest() + '.png'
    webp_path = 'assets/team-characters.' + hashlib.sha256(webp).hexdigest() + '.webp'
    # Keep the original URL available for older pages; new pages use immutable content.
    files = {'assets/team-characters.png': artwork, artwork_path: artwork, webp_path: webp}
    for route, language in (('', 'ko'), ('ko/', 'ko'), ('en/', 'en')):
        copy = content['copy'][language]
        prefix = '../' if route else ''
        first = content['hires'][0][language]
        replacements = {
            '{{HEAD}}': metadata(copy, language, base, preview), '{{ASSET_BASE}}': prefix,
            '{{TEAM_IMAGE}}': prefix + artwork_path,
            '{{TEAM_WEBP}}': prefix + webp_path,
            '{{KO_URL}}': prefix + 'ko/', '{{EN_URL}}': prefix + 'en/',
            '{{EXPERIMENT}}': experiment(evidence, copy, checkpoint, prefix), '{{ROSTER}}': roster(content['hires'], language),
            '{{PROFILE_NAME}}': html.escape(first['name']), '{{PROFILE_QUOTE}}': html.escape(first['quote']),
            '{{PROFILE_DESCRIPTION}}': html.escape(first['description']),
            '{{PROFILE_PROMPT}}': html.escape('$necromancer\n' + first['prompt'])
        }
        text = template
        for marker, value in replacements.items():
            text = text.replace(marker, value)
        # Favicons remain relative, so previews and subdirectory deployments both work.
        text = text.replace('</head>', f'  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">\n'
                            f'  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/favicon-32.png">\n'
                            f'  <link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/apple-touch-icon.png">\n</head>')
        if re.search(r'{{[A-Z_]+}}', text):
            raise ValueError('Unresolved template marker')
        renderer = Localize(copy, language)
        renderer.feed(text)
        files[route + 'index.html'] = ''.join(renderer.parts).encode()
    # This is a generated JS view of the single JSON copy source, not a second authored dataset.
    files['content.js'] = ('// Generated by scripts/build_landing.py; edit content.json.\n'
                           'const COPY = ' + json.dumps(content['copy'], ensure_ascii=False) + ';\n'
                           'const HIRES = ' + json.dumps(content['hires'], ensure_ascii=False) + ';\n'
                           'const SITE = ' + json.dumps(dict(baseUrl=base, preview=preview)) + ';\n').encode()
    for language in ('ko', 'en'):
        files[f'assets/og-{language}.svg'] = svg_card(content['copy'][language], language).encode()
    files['assets/favicon.svg'] = b'<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180"><rect width="180" height="180" rx="32" fill="#0066FF"/><text x="28" y="122" font-family="Helvetica Neue,Arial,sans-serif" font-size="100" font-weight="700" letter-spacing="-8" fill="#F7F7F8">qh.</text></svg>\n'
    for language in ('ko', 'en'):
        files[f'experiments/{language}.html'] = experiment(evidence, content['copy'][language], checkpoint).encode()
    for checkpoint_id in ('integration05', 'integration06', 'integration07'):
        files.update(integration_evidence_files(checkpoint_id))
        number = checkpoint_id.removeprefix('integration')
        prefix = 'evidence/' + checkpoint_id + '/'
        files[prefix + 'comparison.json'] = (
            ROOT / f'benchmarks/results/all-eight-current-{number}/comparison.json').read_bytes()
        bundle = io.BytesIO()
        with zipfile.ZipFile(bundle, 'w') as archive:
            for path in sorted(files):
                if path.startswith(prefix):
                    entry = zipfile.ZipInfo(path.removeprefix(prefix))
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    entry.external_attr = 0o100644 << 16
                    archive.writestr(entry, files[path])
        files[prefix + 'reports.zip'] = bundle.getvalue()
    # Reuse the standalone packager: only skill resources and installation files.
    with tempfile.TemporaryDirectory(prefix='qh-landing-package-') as directory:
        archive = Path(directory) / 'skills.tar.gz'
        identity = package(archive)
        files['downloads/skills.tar.gz'] = archive.read_bytes()
    files['downloads/skills.sha256'] = (identity['sha256'] + '  skills.tar.gz\n').encode()
    files['downloads/INSTALL.md'] = (ROOT / 'docs/INSTALL-SNAPSHOT.md').read_bytes()
    if preview:
        robots = 'User-agent: *\nDisallow: /\n'
    else:
        robots = f'User-agent: *\nAllow: {parsed.path or "/"}\nSitemap: {base}sitemap.xml\n'
    files['robots.txt'] = robots.encode()
    urls = ''.join(f'<url><loc>{xml_escape(base + language + "/")}</loc></url>' for language in ('ko', 'en'))
    files['sitemap.xml'] = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>\n').encode()
    return files, preview


def verify_rasters(files):
    sources = read_json(LANDING / 'assets/raster-sources.json')
    expected = {'og-ko.png': (1200, 630), 'og-en.png': (1200, 630),
                'favicon-32.png': (32, 32), 'apple-touch-icon.png': (180, 180)}
    if set(sources) != set(expected):
        raise ValueError('Missing social card/icon raster source records')
    for name, dimensions in expected.items():
        record = sources[name]
        svg = files['assets/' + record['source']]
        png = (LANDING / 'assets' / name).read_bytes()
        if (hashlib.sha256(svg).hexdigest() != record['svg_sha256']
                or hashlib.sha256(png).hexdigest() != record['png_sha256']):
            raise ValueError('Stale image: ' + name + '; run scripts/render_landing_assets.cjs')
        if png[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II', png[16:24]) != dimensions:
            raise ValueError('Invalid PNG dimensions: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', help='Public HTTPS site directory URL, including any deployment prefix')
    parser.add_argument('--output', type=Path, default=LANDING, help='Output directory (default: checked-in preview)')
    parser.add_argument('--check', action='store_true', help='Verify generated files without writing')
    args = parser.parse_args()
    files, preview = build(args.site_url)
    if args.check or args.output.resolve() != LANDING:
        verify_rasters(files)
    stale = []
    for name, data in files.items():
        path = args.output / name
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if stale:
        print('Stale landing files: ' + ', '.join(stale), file=sys.stderr)
        return 1
    if not args.check and args.output.resolve() != LANDING:
        for name in ('style.css', 'app.js'):
            shutil.copyfile(LANDING / name, args.output / name)
        for name in ('og-ko.png', 'og-en.png', 'favicon-32.png', 'apple-touch-icon.png'):
            shutil.copyfile(LANDING / 'assets' / name, args.output / 'assets' / name)
    print(('Checked' if args.check else 'Built') + f' {len(files)} files ({"local preview / noindex" if preview else "public site metadata"})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
