# Necromancer compact transport — 2026-09-15

Measured source: `b9799dd`, clean checkout before the change. This is serialized
output-size arithmetic, **not** an Astra token/time or whole-task benchmark.

## Same observations, fewer formatting bytes

The collector's default CLI JSON used two-space indentation on every current line,
blame row and commit field. Change the default to compact JSON. `--pretty` retains
the old human-readable representation. The `trace()` API, Git commands, selected
evidence, source whitespace, caps and limitation fields are unchanged.

The following three explicit current-source ranges were each collected once at
the measured revision. Both serializations were derived from that same result;
`json.loads(pretty) == json.loads(compact) == result` passed for every range.
Counts exclude the one final CLI newline, common to both modes.

| Source range | Indented UTF-8 bytes | Compact UTF-8 bytes | Fewer bytes |
| --- | ---: | ---: | ---: |
| `scripts/install.py`, 25–29 | 5,579 | 5,031 | 9.82% |
| `scripts/install.py`, 15–70 | 26,849 | 21,935 | 18.30% |
| `skills/necromancer/scripts/trace.py`, 168–250 | 44,408 | 37,144 | 16.36% |

The ranges have 5/56/83 blame rows and 1/2/3 returned commits. The last range
reports four omitted commits in **both** representations; it is not complete
history. Paths and ranges were selected to inspect short and repeated collection,
not sampled from a representative developer population. Do not aggregate these
bytes as a measured skill score or equate bytes with model tokens.

## Reproduction and controls

In a clean checkout at `b9799dd`, the measurement was:

```python
import json, runpy
trace = runpy.run_path('skills/necromancer/scripts/trace.py')['trace']
for path, start, end in [('scripts/install.py', 25, 29),
                         ('scripts/install.py', 15, 70),
                         ('skills/necromancer/scripts/trace.py', 168, 250)]:
    result = trace('.', path, start, end)
    pretty = json.dumps(result, indent=2, ensure_ascii=False)
    compact = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    assert json.loads(pretty) == json.loads(compact) == result
    a, b = len(pretty.encode()), len(compact.encode())
    print(path, start, end, a, b, round((1 - b / a) * 100, 2))
```

New CLI regression coverage compares both real subprocess outputs with the API
result on clean, dirty and untracked files, including Korean source, CRLF and a
literal escaped tab. Dirty attribution remains null and unavailable history stays
unavailable. It also checks the exact legacy representation under `--pretty`.
Before implementation, the compact-default assertion failed on actual output;
the three `--pretty` invocations exited 2 because that flag did not exist. Those
option errors are **not** evidence of a prior history-analysis defect.

Run the collector checks with:

```sh
python3 -B -m unittest discover -s tests -p test_history_helper.py
python3 -B -m unittest discover -s tests -p test_history_collector_benchmark.py
```

Validation after the change: 29 history-helper tests, one collector-benchmark
test, 12 build tests and 20 installer tests pass (**62 targeted tests**). Skill
validation, repository metadata/local links, featured synchronization and
whitespace checks pass. The full suite was not rerun for this serialization-only
change; the preceding 601-test checkpoint remains tied to its previous source.

No new model sessions or featured-graph changes. This removes formatting overhead
without collecting less evidence; whether the default reduces overall model cost
or affects interpretation requires separate behavioral measurement. It does not
solve the existing full-Git-output memory limitation.

## 한국어

기본 JSON에서 들여쓰기만 제거하고, 사람이 읽을 때 기존 형식을 선택할 수 있도록
`--pretty`를 추가했다. 같은 결과 객체를 두 형식으로 직렬화했을 때 세 구간의
UTF-8 출력 크기가 9.82~18.30% 감소했다. 내용·소스 공백·누락 경고는 동일하다.
이는 출력 바이트 비교이지 모델 토큰·시간·전체 작업 성능 개선율이 아니다.
정상·수정 중·미추적 파일의 실제 CLI 결과를 API와 대조하며, 기존 그래프는
변경하지 않는다. Git 출력 전체를 메모리에 보관하는 기존 한계도 유지된다.
