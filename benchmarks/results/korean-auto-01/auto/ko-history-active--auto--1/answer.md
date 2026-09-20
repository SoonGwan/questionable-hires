`necromancer` 스킬을 사용해 현재 호출부와 테스트, Git 변경 이력에서 호환 처리의 목적과 남은 의존성을 확인하겠습니다. 코드는 수정하지 않겠습니다.


**지금은 삭제하면 안 됩니다.** 현재 호출부가 `name` fallback에 의존하며, 제거하면 실제로 실패합니다.

- **현재 사용처:** [consumer.py:5](project/consumer.py#L5)의 `partner_label()`은 `{'name': 'Ada'}`만 전달합니다. [labels.py:2](project/labels.py#L2)의 fallback이 있어야 정상 동작합니다.
- **도입 이력:** `9e7cfdb`에서는 `payload['display_name']`만 읽었습니다. `d5fc972`에서 API v1 파트너의 마이그레이션 기간 호환성을 위해 fallback과 해당 호출부를 함께 추가했습니다.
- **지원 기간:** [consumer.py:3](project/consumer.py#L3)에 API v1을 **2027년 12월까지 지원**한다고 명시되어 있습니다. 현재 날짜인 2026년 9월은 그 기간 안입니다. 주석뿐 아니라 현재 호출부도 의존성을 뒷받침합니다.
- **실행 확인:** 현재 `partner_label()`은 `'Ada'`를 반환합니다. 파일 수정 없이 메모리에서 도입 전 구현으로 교체하면 같은 호출이 `KeyError: 'display_name'`으로 실패합니다.

최소 다음 조치는 v1 지원 종료 또는 호출부의 `display_name` 전환을 확인한 뒤 삭제를 재검토하는 것입니다. 그때까지는 `name`만 있는 입력의 동작을 보존해야 합니다.

파일 수정·설치·외부 접근·커밋은 하지 않았고, 기존 미추적 `.agents/`도 그대로 보존했습니다.
