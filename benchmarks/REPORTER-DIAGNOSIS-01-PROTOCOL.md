# Reporter lifecycle diagnosis 01 — 2026-09-15 KST

Completed: [original evidence review](results/reporter-diagnosis-01/README.md).

New Exorcist workflow: diagnose a reporter exception, not audit mutation sensitivity.
The failure is extracted verbatim from actual baseline item_5 in
[native screen 02](results/installer-native-02/README.md), revision `a5cfdd2`.
`reporter_diagnosis_cases.py` parses the retained shell command and literal runner
assignment without executing the parent command. Exact trace/runner hashes and
native results are in [preflight](reporter-diagnosis-01-preflight.json).

Input uses the same real installer fixture, with its cancellation-handler fault,
unchanged four test bodies and explicitly project-local setup. Reporter source is
unchanged. This reuses a known installer and an observed model-written diagnostic
bug, not a new repository, organic maintainer ticket or independent holdout.
The diagnosis and task are authored; no prior answer or author control is included
in [model inputs](reporter-diagnosis-01-cases.json).

Native Python 3.9.6 preflight checks three isolated variants: observed faulty
installer/reporter raises FileNotFoundError in addFailure and has no completed
counts; standard result handler recovers four native tests, one actual line-303
assertion failure with two unexpected entries; correct installer/original reporter
passes four tests. All copies clean up and original files match. Runtime lifecycle
ordering may vary across Python versions: verify on the supplied interpreter,
do not claim universal ordering. The normal control and reporter adaptation are
author-side preflight only, not model-provided fixes or scored model success.

Schedule one fresh baseline and one unchanged Exorcist session, Astra medium,
serial, seed 20260915, timeout 240 seconds. Freeze before launch; no resources,
tasks or criteria edits during timing. No author workloads during model execution.
Keep both results and all in-session failures. No favorable rerun, stop on limits.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/reporter-diagnosis-01-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/reporter-diagnosis-01
```

Review actual reproduction, deletion/observation ordering, implementation binding,
normal control and recovered native assertion/counts/exits; preserve supplied files
and remove created scratch. All requirements appear in the task. Diagnosis does
not authorize changing original code/tests. Retain all commands/usage, verify export
and original integrity. Compare total input (cache once) + output and wall time only
alongside work equivalence. One related development case is not evidence of broad
20–30% gains; no featured chart update or new Exorcist rule from an isolated failure.

한국어: 앞선 실제 실행에서 발생한 진단 코드 오류를 그대로 추출했다. Python
3.9.6에서 원본 오류·가려진 실제 assertion 실패·정상 대조를 사전 검증했다.
동일 설치 자료를 재사용하는 저자 작성 진단 과제이며 새 실무 이슈나 독립 검증은
아니다. 기본 모델과 Exorcist 각각 1회, 원본 보존과 실제 실행 증거까지 비교한다.
정답·수정안은 모델 입력에 없고 실패를 포함한 모든 비용을 남긴다.
