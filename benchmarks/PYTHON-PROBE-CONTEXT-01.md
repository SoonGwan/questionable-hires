# Extracted Python probe context — 2026-09-15

Parent source: `488515f`. Instruction candidate, **not measured model savings**.

In the [full-history HTTPX pair](results/httpx-redirect-history-01/README.md), both
arms failed compiling an extracted method after losing the original module's
postponed-annotation setting. Skill had already executed six case observations
before that failure and repeated them after repair. The failures and their cost
remain part of the frozen result; no author replay replaces them.

Add one conditional sentence group to Necromancer's entry: when an actual
behavioral probe recompiles extracted Python, preserve original `__future__`
settings and necessary bindings instead of inheriting the probe's settings.
This does not require extraction, introduce a helper, change the interpreter,
strip annotations or always turn deferred annotations on. Ordinary native test
execution and history-only reviews do not need an extra step.

Four executable controls in `tests/test_python_probe_context.py` verify:

- Deferred references compile and execute in their original context; dropping
  that context reproduces an actual NameError during probe setup.
- Eager annotations retain their actual type objects and global function binding;
  blindly enabling deferred annotations changes their meaning.
- A probe module's future setting can leak through default `compile()` behavior;
  explicit original future flags with `dont_inherit=True` retain the original.
- A real behavioral mutation remains observable and fails `6 != 5` after correct
  setup. Avoiding setup failure is not hiding an application regression.

These are local mechanism tests, not model instruction-following tests. Their
small recompilation function is author test support, not a packaged transplant
API: closures, decorators, class construction and other context may make isolated
extraction inappropriate. The added guidance does not promise generic equivalence.

```sh
python3 -B -m unittest discover -s tests -p test_python_probe_context.py
```

All four pass on Python 3.9.6; 12 build and 20 installer tests also pass
(36 targeted tests total), plus skill, metadata/link and featured-sync checks.
The entry grows from 2,310 to 2,534 UTF-8 bytes (+224 bytes); runtime helpers are
unchanged and the full suite was not rerun for this instruction-only candidate.
The candidate adds entry context, so it must be
assessed for net whole-task cost on fresh work before attributing savings. Do not
rerun the exposed HTTPX ticket until a favorable number appears, or apply this
Python-specific rule indiscriminately across every skill. Featured graphs remain
tied to their actual measured revisions.

## 한국어

앞선 두 모델 세션 모두 메서드를 떼어 검증하면서 원래 모듈의 컴파일 설정을
잃어 실행에 실패했다. 해당 상황에만 원래 설정과 바인딩을 보존하도록 안내를
추가했다. 무조건 타입 표기의 평가를 늦추거나 삭제하는 규칙은 아니다. 네 개의
실제 Python 검사에서 준비 오류 재현·설정 보존·실제 동작 오류 탐지를 확인했다.
모델이 이 안내를 따르는지와 전체 비용 절감은 아직 미측정이며, 이전 실패와
수치를 고쳐 쓰지 않는다.
