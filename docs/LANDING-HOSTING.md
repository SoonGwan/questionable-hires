# Landing hosting on this Mac / 이 Mac에서 랜딩 호스팅

The deployment follows the existing `money-money-hal-money` setup: a dedicated
loopback origin and a dedicated Cloudflare Tunnel run as macOS LaunchAgents.
The landing services are `com.questionable-hires.web` and
`com.questionable-hires.tunnel`; origin port defaults to **4180**.

기존 가계부와 같은 LaunchAgent + Cloudflare Tunnel 방식입니다. 랜딩은 별도
서버·터널을 사용하며, 가계부의 서비스·포트·설정을 수정하지 않습니다.

## Deploy / 배포

Required: Python 3, `cloudflared`, an authenticated origin certificate from
`cloudflared tunnel login`, and a signed-in macOS user session. The site must be
built with its actual HTTPS origin so static OG, canonical and sitemap URLs agree.

Commit the source first, then run from this repository:

```sh
python3 -B scripts/deploy_landing_mac.py \
  --domain hires.no-money-do-you-have-money.com
```

The command:

1. Builds only the static web bundle with the actual public origin.
2. Copies the origin server into a dated release under
   `~/Library/Application Support/questionable-hires/releases/`.
3. Switches `current` atomically and starts the web LaunchAgent on loopback.
4. Verifies the app identity and source revision at `/_health`.
5. Creates or reuses the dedicated `questionable-hires` tunnel and validates ingress.
6. Adds the subdomain DNS route without overwriting an existing record.
7. Starts the tunnel LaunchAgent and verifies the same revision over public HTTPS
   using Cloudflare DNS-over-HTTPS, avoiding stale local negative DNS responses.

Cloudflare credentials stay outside the repository in `~/.cloudflared/`.
Only the generated `site/` directory is served; directory listings, hidden files
and paths/symlinks outside that directory return 404. Runtime configuration and
logs stay in the user's Library directories. Deployment phase is retained in
`deployment.json`, so an interrupted public verification can be resumed.

생성한 웹 디렉터리만 공개합니다. 배포 전후 앱 식별자와 소스 커밋을 확인하며,
도메인 레코드가 이미 있으면 강제로 덮어쓰지 않습니다. 인증 파일은 Git에 넣지
않습니다. 중간 상태를 보존하여 배포가 중단되어도 재시도할 수 있습니다.

[Dated hosting verification / 날짜별 호스팅 확인](LANDING-HOSTING-2026-09-26.md)

## URLs and checks / 주소와 확인

- 한국어: `https://hires.no-money-do-you-have-money.com/ko/`
- English: `https://hires.no-money-do-you-have-money.com/en/`
- Health: `https://hires.no-money-do-you-have-money.com/_health`
- OG images: `/assets/og-ko.png`, `/assets/og-en.png` (1200 × 630)
- Discovery: `/sitemap.xml`, `/robots.txt`

```sh
curl -fsS https://hires.no-money-do-you-have-money.com/_health
launchctl print "gui/$(id -u)/com.questionable-hires.web"
launchctl print "gui/$(id -u)/com.questionable-hires.tunnel"
```

Actual third-party card previews may be cached by social platforms; fetching
localized HTML and PNGs verifies the hosted inputs, not each platform's rendered
preview. Local UI checks and a live landing check are distinct from model
benchmark evidence and the skill project's hosted test matrix.

공개 HTML·PNG 응답 검증은 소셜 플랫폼별 공유 미리보기의 렌더링 검증과 다릅니다.
랜딩 호스팅 확인은 스킬의 모델 성능 측정이나 원격 테스트 매트릭스 통과가 아닙니다.

## Update and rollback / 갱신과 복구

Make a focused commit, then run the same deploy command. Prior release files remain
on disk. To restore the preceding local release:

```sh
python3 -B scripts/deploy_landing_mac.py --rollback
```

The release selector is `~/Library/Application Support/questionable-hires/current`.
Logs are under `~/Library/Logs/questionable-hires/`. If local startup fails, the
command restores the previous origin. A failed DNS/public check is reported as
incomplete and retains its deployment phase; inspect the dedicated tunnel log and
retry the same command. It does not claim public success from a local 200 alone.

The LaunchAgents start when this user logs in and restart crashed processes.
The Mac must remain awake and connected for the hosted site to be available.
This matches the existing machine's service model, rather than an always-on cloud
origin. See [Cloudflare's macOS service guidance](https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/as-a-service/macos/).

로그인 시 자동 시작하고 프로세스가 종료되면 다시 실행합니다. 호스팅을 유지하려면
Mac이 깨어 있고 인터넷에 연결되어 있어야 합니다.
