#!/usr/bin/env python3
"""Synchronize the English and Korean README benchmark hero from one dataset."""
import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
START = '<!-- featured-benchmark:start -->'
END = '<!-- featured-benchmark:end -->'


def values():
    featured = json.loads((ROOT / 'benchmarks/featured.json').read_text())
    directory = featured['result_directory']
    data = json.loads((ROOT / directory / 'data.json').read_text())
    return dict(directory=directory, skill=featured['skill'], ko_name=featured['ko_name'],
                cases=data['cases'],
                baseline_quality=data['quality']['baseline'],
                skill_quality=data['quality']['skill'],
                false_positives=data['clean_false_positives']['skill'],
                tokens=data['resource_ratios']['total_tokens']['skill'],
                elapsed=data['resource_ratios']['elapsed_seconds']['skill'])


def block(language, value):
    d, skill, cases = value['directory'], value['skill'], value['cases']
    bq, sq = value['baseline_quality'], value['skill_quality']
    tokens, elapsed = value['tokens'], value['elapsed']
    if language == 'en':
        intro = (f'**Latest frozen confirmation:** `{skill}` met **{sq}/{cases}** reviewed '
                 f'interaction-QA targets versus baseline **{bq}/{cases}**, with '
                 f'**{value["false_positives"]}** skill false positives. Across {cases} new cases '
                 f'committed before execution, the skill used **{tokens:.1f}%** normalized total '
                 f'tokens and **{elapsed:.1f}%** normalized elapsed time. This is one fresh '
                 'session per arm and task, not a whole-team or repeated-sample claim.')
        alt = (f'{cases}-task frozen {skill} confirmation: baseline meets {bq} of {cases} '
               f'reviewed targets and skill meets {sq} of {cases}; normalized tokens 100 and '
               f'{tokens:.1f} percent; normalized elapsed time 100 and {elapsed:.1f} percent.')
        link = f'[Inspect the frozen cases, raw values, method, and limitations]({d}/README.md).'
    else:
        intro = (f'**최신 사전 고정 확인 실험:** {value["ko_name"]}(`{skill}`)는 '
                 f'검토 대상 **{sq}/{cases}**, '
                 f'스킬 미적용 조건은 **{bq}/{cases}**를 충족했고 스킬 오탐은 '
                 f'**{value["false_positives"]}건**이었습니다. 실행 전에 커밋한 새 과제 '
                 f'{cases}개에서 스킬의 정규화 총 토큰은 **{tokens:.1f}%**, 실행 시간은 '
                 f'**{elapsed:.1f}%**였습니다. 과제·조건별 새 세션 1회 결과이며 팀 전체나 '
                 '반복 표본의 우월성을 뜻하지 않습니다.')
        alt = (f'새 과제 {cases}개의 사전 고정 확인 실험. 스킬 미적용 조건은 {bq}개, '
               f'스킬은 {sq}개 기준을 충족했고, 스킬은 정규화 토큰 {tokens:.1f}%, '
               f'실행 시간 {elapsed:.1f}%를 사용했습니다.')
        link = f'[과제·원시 수치·방법·한계 확인]({d}/README.md)'
    return (START + '\n\n' + intro + '\n\n<picture>\n'
            f'  <source media="(prefers-color-scheme: dark)" srcset="{d}/comparison-dark.svg">\n'
            f'  <img src="{d}/comparison-light.svg" alt="{alt}" width="100%">\n'
            '</picture>\n\n' + link + '\n\n' + END)


def synchronized(text, replacement):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('README requires exactly one featured benchmark marker pair')
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    return before + replacement + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    value = values()
    changed = []
    for name, language in (('README.md', 'en'), ('README.ko.md', 'ko')):
        path = ROOT / name
        current = path.read_text()
        expected = synchronized(current, block(language, value))
        if current != expected:
            changed.append(name)
            if not args.check:
                path.write_text(expected)
    if args.check and changed:
        print('Featured benchmark is stale: ' + ', '.join(changed), file=sys.stderr)
        return 1
    if not args.check:
        print('Synchronized: ' + ', '.join(changed or ['already current']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
