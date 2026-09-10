# Visual direction

Use restrained typography, generous spacing, and one blue accent. The team name and its original tagline carry the personality; avoid decorative badges and extra slogans.

This is the default for all future banners, comparison charts, and other project visuals, not just `team.svg`. Use primary blue for emphasis and neutral tones for comparison series, axes, and grid lines. Use labels, markers, or line styles as well as color to distinguish series. If more colors are needed, choose them from Montage's semantic tokens rather than inventing a separate palette.

Colors follow [Montage's semantic palette](https://montage.wanted.co.kr/docs/foundations/base-material/colors/semantic), checked against the [official token definitions](https://github.com/wanteddev/montage-web/blob/main/packages/wds-theme/src/theme/semantic/index.ts) on 2026-09-11.

| Role | Light | Dark |
| --- | --- | --- |
| `background.normal.alternative` | `#F7F7F8` | `#0F0F10` |
| `label.normal` | `#171719` | `#F7F7F8` |
| `label.neutral` | `#2E2F33` at 88% | `#C2C4C8` at 88% |
| `primary.normal` | `#0066FF` | `#3385FF` |

`team.svg` is original vector artwork with a system-font stack and a dark-theme media query. Its light palette is the fallback for viewers that do not support that query. Plugin metadata uses the light primary blue. No Montage logo, illustration, or font is bundled, and no affiliation is implied.

## Character banner

`team-characters.png` is the approved text-free, two-row doodle cast, displayed immediately below `team.svg` in both READMEs. Keep the sparse black outlines, off-white background, blue accents, deadpan faces, and simple signature props. The deliberately rough character drawing complements the restrained title banner.

Generated with the built-in image-generation tool. The reusable personal skill is `lazy-doodle`; it includes the approved image as its style reference.
