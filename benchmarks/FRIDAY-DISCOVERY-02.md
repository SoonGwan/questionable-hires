# Friday discovery candidate 02 — 2026-09-15 KST

Parent `a1700a3`. [Active review 01](FRIDAY-ACTIVE-01-REVIEW.md) observed more
shell calls and repeated inventories in both Friday sessions. The compatible
skill cell split discovery, entry, hidden inventory, release inputs and readers
across five commands before native execution. Its hidden inventory also listed
Git objects because an exclusion glob contained a space. Neither cell used the
optional matrix. No performance cause is established by those two observations.

Candidate: one entry paragraph asks for grouping known release inputs with
applicable project instructions, discovering missing paths rather than repeating
full inventories, excluding Git internals from file discovery, and reopening
changed/incomplete inputs or unresolved questions. It does not constrain relevant
history, set a hard tool-call cap, suppress inactive-consumer diagnostics, change
SQL verification or require helper adoption. All other skill resources and release
requirements remain unchanged.

This **adds 363 UTF-8 bytes**: entry 3,106 → 3,469 bytes. These are not model
tokens. The paragraph must justify its extra input through observed behavior;
shorter tool traces and token/time savings are currently unmeasured. If the model
ignores it or it makes discovery worse, reconsider the paragraph rather than
accumulating stricter rules or repeatedly rerunning until a favorable sample.

`test_friday_discovery.py` executes the command extracted from the actual entry
in a disposable project-local tree. It finds root and hidden nested AGENTS.md,
release input and nested reader, excludes root/nested Git internals, and preserves
all file bytes. One test passes in 0.015s. This is command behavior, not a model
compliance test; normal ripgrep ignore behavior still applies. Missing or ignored
task inputs may need explicit reads or focused discovery.

Frontmatter/repository validation passes. A new model behavior screen is still
needed before any performance claim; historical cases, outcomes and charts are
unchanged. Any reuse of active-review cases is development feedback, not held-out
generalization evidence.

## 한국어

실행 기록에서 반복 탐색과 잘못된 Git 제외 패턴을 확인해, 알려진 입력·프로젝트
지침을 묶어 읽고 누락된 경로를 중심으로 탐색하는 문단을 추가했다. 변경·누락·
미해결 질문이 있으면 다시 읽을 수 있고 기존 배포 검토 기준은 유지한다.

지침은 363바이트 늘었다. 실제 명령은 숨김 지침을 보존하고 Git 내부 파일을
제외했지만, 모델의 행동 변화와 비용 절감은 아직 미검증이다. 문단 추가만으로
성과를 주장하지 않으며, 동일 과제 재사용은 개발용 검사로 구분한다.
