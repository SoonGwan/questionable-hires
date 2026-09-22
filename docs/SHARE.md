# Share Questionable Hires

Copy-ready introductions, not automatically published posts. Link to the
[repository](https://github.com/SoonGwan/questionable-hires), and show the
[actual example](../examples/con-artist.md), not an invented benchmark win.

## English

I made eight questionable coworkers for your AI coding agent.

One asks why the legacy code exists. One demands a before/after reproduction.
One checks whether your tests still pass when the code is broken.

Questionable Hires is an open-source set of developer skills, built with Codex
and GPT-6 Astra in mind. Install the team or pick one:

```sh
npx skills add SoonGwan/questionable-hires
```

It's a development preview. The repo includes real examples, comparisons and
unfavorable results—not a promise that eight personalities make every task faster.

Try Con Artist on a weak test and tell us what it missed:
https://github.com/SoonGwan/questionable-hires

## 한국어

AI 코딩 에이전트에 붙일 수상한 동료 8명을 만들었습니다.

레거시 코드가 남은 이유를 캐는 고고학자, 수정 전후 증거를 요구하는 검증관,
코드를 망가뜨려도 통과하는 테스트를 잡는 사기 감별사까지.
캐릭터는 이상하지만 맡기는 일은 실제 개발 작업입니다.

```sh
npx skills add SoonGwan/questionable-hires
```

Codex와 GPT-6 Astra를 염두에 둔 오픈소스 개발 스킬 모음입니다.
아직 개발 프리뷰이며, 실제 예시·비교 결과·불리했던 결과도 함께 공개했습니다.
모든 작업이 더 빨라진다는 주장은 하지 않습니다.

테스트 사기 감별사부터 써보고 놓친 사례를 알려주세요:
https://github.com/SoonGwan/questionable-hires

## A real demo, without model usage

From a trusted checkout, on POSIX with Python3.9+:

```sh
python3 -B skills/con-artist/scripts/audit.py \
  --source examples/con-artist-batch \
  --spec examples/con-artist-batch/recipe.json
```

Show the lost-write and duplicate-write cases. Existing tests pass on faulty
code; the stronger assertion fails. The helper runs trusted code in disposable
copies, not a security sandbox. Read the [full interpretation](../examples/con-artist.md#try-the-helper-without-model-usage),
including reused observations. This is a helper demo, not a fresh model run,
speed comparison or proof the baseline cannot solve the task.

## Share responsibly

- Use [the social card](../assets/social-preview.png); editable [SVG source](../assets/social-preview.svg).
- Invite specific feedback in [Discussions](https://github.com/SoonGwan/questionable-hires/discussions).
- Respect each community's promotion rules; do not mass-post, buy stars or trade engagement.
- Do not claim a GitHub endorsement, guaranteed Trending placement or broad20–30% gains.
- No external post, release announcement or account-profile change is made by this document.
