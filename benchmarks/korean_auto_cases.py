"""Korean automatic-selection smoke cases, not new performance-transfer tasks."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    'history-active': "display_label에서 'name'으로 넘어가는 예전 호환 처리를 이제 지워도 될까? 현재 사용처와 변경 이력을 근거로 판단해 줘. 코드는 수정하지 마.",
    'boundary-fix': '정확히 만 18세인 고객이 거절되고 있어. 가입 가능 나이 판정을 고치고, 수정 전후 동작을 확인해 줘. 이 문제에 필요한 변경만 해 줘.',
    'formatter-review': '이 금액 포맷터 구조가 유지보수 비용에 비해 필요한지 검토해 줘. 타당한 단순화가 있으면 제안하되 파일은 수정하지 마.',
    'search-order': '검색 흐름 QA를 해 줘. 실제 사용 순서에서 생길 수 있는 문제를 실행 순서가 통제되는 로컬 테스트로 재현해 줘. 운영 코드는 수정하지 마.',
    'search-diagnosis': '새 검색어를 입력했는데 가끔 이전 검색 결과가 보여. 동료는 캐시 문제라고 생각해. 로컬 실험으로 원인을 구분해 줘. 운영 코드를 고치지는 마.',
    'label-change': '결제 버튼 문구를 Buy에서 Place order로 바꿔 줘. 동료가 상태 관리 시스템도 교체하자고 했지만 그건 선택 사항이고 이번 요청에는 포함되지 않아.',
    'persistence-test': '이 테스트가 저장 누락을 잡는지 감사해 줘. 분리된 복사본에 실제 저장만 빠지는 결함을 넣어 결과를 확인해 줘. 원래 운영 코드에 결함을 남기면 안 돼.',
    'rolling-schema': '이 릴리스의 순차 배포와 롤백 계획을 검토해 줘. 실제 배포는 하지 말고, 막히는 지점이 있으면 코드와 순서를 근거로 설명해 줘.',
}
SCOPE = '\n\n이 프로젝트 안에서만 작업하고 외부 서비스·설치·커밋은 하지 마. 기존 사용자 변경과 요청 밖 파일은 보존해 줘. 필요한 테스트나 재현 코드는 만들 수 있어.'


def cases():
    original = json.loads((ROOT / 'benchmarks/cases.json').read_text())
    selected = []
    for source in original:
        row = copy.deepcopy(source)
        row.update(id='ko-' + source['id'], task=TASKS[source['id']] + SCOPE,
                   source_case=source['id'], expected_primary=source['skill'],
                   routing_kind='positive')
        selected.append(row)
    label = copy.deepcopy(next(c for c in original if c['id'] == 'label-change'))
    label.update(id='ko-plain-label', task='checkout.html의 결제 버튼 문구만 Buy에서 Place order로 바꿔 줘.' + SCOPE,
                 expected_primary=None, routing_kind='negative', source_case='label-change',
                 criteria=['Only the requested label changes; submit behavior and state.js remain unchanged.',
                           'No unrelated investigation, redesign or test framework.'])
    selected.append(label)
    selected.append(dict(id='ko-readme-typo', skill='hostage-negotiator',
        expected_primary=None, routing_kind='negative', source_case=None,
        task='README.md에서 Instlal 오타만 Install로 고쳐 줘.' + SCOPE,
        files={'README.md': '# Demo\n\nInstlal dependencies with the project setup command.\n',
               'app.py': 'def greeting():\n    return "hello"\n'},
        criteria=['Only Instlal changes to Install; app.py and other text unchanged.',
                  'No unrelated investigation, redesign or test framework.']))
    return selected
