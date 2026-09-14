# Reviewable diagnostic observations — 2026-09-15 KST

Outcome: [screen 02 rejected; paragraph reverted](results/reporter-observation-02/README.md).
The proposal below is historical, not the current skill instruction.

Parent `e5c9ef2`. Replace the existing output-choice paragraph, not experiment
coverage, helper mechanics, scope rules or a reporter-specific diagnosis.

Earlier [evidence-path work](EXORCIST-EVIDENCE-PATH.md) avoided needless file
round trips while preserving ordering/provenance when a trace is needed.
[Routing work](EXORCIST-ROUTING-CANDIDATE.md) retained that distinction. The
[reporter diagnosis](results/reporter-diagnosis-01/README.md) now shows its limit:
one diagnostic prints a full native runner definition before many lifecycle
events, but the received CLI output starts mid-experiment. The responsible capture
layer is unknown; this edit cannot repair that layer or any frozen evidence.

The revised paragraph asks for compact decisive ordered observations, normal
controls and native evidence, with source inspection separate from runtime output.
Captured output remains sufficient when it fits. Longer/required traces use one
project-local record and selective reads; claimed events must actually be visible.
Retained records precede considering any safe repeat; requested artifacts survive,
and disposable ones are removed after review. No universal trace schema, recorder
tool, extra probe or mandatory file round trip is added. This refines the existing
general output policy across prior observations, not a new installer rule.

Skill Creator informed the narrow replacement. Official Astra guidance informed
preserving necessary verification without adding repeated tests; neither proves
this candidate works. Structural validation is not behavioral evidence.

## Changed-candidate adoption screen

One fresh skill session on unchanged `reporter-diagnosis-01-cases.json`, Astra
medium, serial, seed 20260915, timeout 240 seconds. Use only committed candidate
resources; no edits/workloads during timing, retries, exclusions or favorable draws.
Prior baseline is historical; no new efficiency claim from that comparison.
This exposed task tests uptake and whether decisive native evidence is retained,
not generalization. All original requirements, preservation and scope apply.
Do not supply the prior diagnosis or this author report to the model. Retain every
received command, error, native count and usage; reconcile before publishing.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/reporter-diagnosis-01-cases.json \
  --arms skill --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/reporter-observation-02
```

If a complete diagnostic is observed, move beyond this installer/reporter pair
instead of repeating it for better costs. If not, preserve the limitation and
investigate the capture mechanism separately. No featured chart change either way.

한국어: 기존 증거 출력 지침을 교체했다. 긴 소스와 실행 관측을 섞지 않고 핵심
순서·정상 대조·실제 실패를 확인 가능한 형태로 남긴다. 짧은 실행은 출력만으로
충분하며 긴 기록만 파일로 남겨 필요한 부분을 확인한다. 원본 누락을 복구하거나
수치 개선을 입증한 것은 아니다. 수정 스킬 1회로 채택·증거 보존을 확인하며
과거 기본 모델 비교는 참고치이고 같은 문제 반복으로 좋은 수치를 고르지 않는다.
