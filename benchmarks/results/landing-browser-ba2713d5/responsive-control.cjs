const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const { chromium } = require('playwright');
const source = fs.readFileSync(process.cwd() + '/landing/content.js', 'utf8');
const { COPY, HIRES } = vm.runInNewContext(source + '\n({ COPY, HIRES })');
assert.deepEqual(Object.keys(COPY.ko).sort(), Object.keys(COPY.en).sort());
for (const lang of ['ko', 'en']) {
  for (const [key, value] of Object.entries(COPY[lang])) assert.equal(typeof value, 'string', `${lang}.${key}`);
  for (const hire of HIRES) assert.deepEqual(Object.keys(hire.ko).sort(), Object.keys(hire.en).sort());
}
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  const context = await browser.newContext({ locale: 'ko-KR', permissions: ['clipboard-read', 'clipboard-write'], reducedMotion: 'reduce' });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  let layouts = 0;
  for (const lang of ['ko', 'en']) {
    for (const width of [320, 390, 760, 768, 1024, 1440, 1920]) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(`http://127.0.0.1:4180/${lang}/`);
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
      assert.equal(await page.title(), COPY[lang].title);
      assert.equal(await page.locator('.hire').count(), 8);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `horizontal overflow ${lang} ${width}`);
      const missing = await page.evaluate(() => [...document.querySelectorAll('[data-i18n]')].filter(el => !el.textContent || el.textContent === 'undefined').map(el => el.dataset.i18n));
      assert.deepEqual(missing, []);
      const clipped = await page.evaluate(() => [...document.querySelectorAll('h1,h2,h3,.hire strong,.command code')].filter(el => el.scrollWidth > el.clientWidth + 1).map(el => el.textContent));
      assert.deepEqual(clipped, [], `clipped content ${lang} ${width}`);
      if (lang === 'en') assert.equal(/[가-힣]/.test(await page.locator('body').innerText()), false, `untranslated Korean ${width}`);
      assert.equal(await page.evaluate(() => document.getAnimations().length), 0);
      layouts++;
    }
  }
  // Select every employee; keep selection, prompt and evidence link across language changes.
  await page.setViewportSize({ width: 1440, height: 1000 });
  for (let i = 0; i < 8; i++) {
    await page.locator('.hire').nth(i).click();
    assert.equal(await page.locator('.hire[aria-pressed="true"]').count(), 1);
    assert.equal(await page.locator('#profile-name').textContent(), HIRES[i].en.name);
    assert.equal(await page.locator('#skill-prompt').textContent(), `$${HIRES[i].id}\n${HIRES[i].en.prompt}`);
    assert.equal(await page.locator('#example-link').getAttribute('href'), `https://github.com/SoonGwan/questionable-hires/blob/main/examples/${HIRES[i].id}.md`);
    await page.getByRole('link', { name: 'KO', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'ko');
    assert.equal(await page.locator('#profile-name').textContent(), HIRES[i].ko.name);
    assert.equal(await page.locator('#skill-prompt').textContent(), `$${HIRES[i].id}\n${HIRES[i].ko.prompt}`);
    await page.getByRole('link', { name: 'EN', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'en');
  }
  await page.getByRole('link', { name: 'KO', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'ko');
  assert.equal(new URL(page.url()).pathname, '/ko/');
  await page.goto('http://127.0.0.1:4180/');
  assert.equal(await page.locator('html').getAttribute('lang'), 'ko');
  await page.goto('http://127.0.0.1:4180/?lang=en');
  assert.equal(await page.locator('html').getAttribute('lang'), 'en');
  // Exercise the actual clipboard, then a denied-write recovery.
  await page.getByRole('button', { name: COPY.en.copyLabel }).click();
  await page.waitForFunction(() => document.querySelector('#copy-status').textContent.startsWith('Copied.'));
  assert.equal(await page.evaluate(() => navigator.clipboard.readText()), 'npx skills add SoonGwan/questionable-hires');
  await page.getByRole('link', { name: 'KO', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'ko');
  assert.equal(await page.locator('#copy-status').textContent(), COPY.ko.copied);
  await page.evaluate(() => Object.defineProperty(navigator.clipboard, 'writeText', { value: async () => { throw new Error('Denied'); }, configurable: true }));
  await page.getByRole('button', { name: COPY.ko.copyLabel }).click();
  await page.waitForFunction(() => document.querySelector('#copy-status').textContent.startsWith('복사하지'));
  await page.getByRole('link', { name: 'EN', exact: true }).click();
    await page.waitForFunction(() => document.documentElement.lang === 'en');
  assert.equal(await page.locator('#copy-status').textContent(), COPY.en.copyFailed);
  // Block preference storage; explicit language still works.
  const blocked = await browser.newContext({ locale: 'en-US', reducedMotion: 'reduce' });
  await blocked.addInitScript(() => Object.defineProperty(window, 'localStorage', { get() { throw new Error('Blocked'); } }));
  const blockedPage = await blocked.newPage();
  await blockedPage.goto('http://127.0.0.1:4180/?lang=invalid');
  assert.equal(await blockedPage.locator('html').getAttribute('lang'), 'en');
  await blockedPage.getByRole('link', { name: 'KO', exact: true }).click();
  await blockedPage.waitForFunction(() => document.documentElement.lang === 'ko');
  assert.equal(await blockedPage.locator('html').getAttribute('lang'), 'ko');
  // Keyboard language controls retain focus; reduced motion also works when changed live.
  await page.goto('http://127.0.0.1:4180/?lang=ko');
  await page.getByRole('link', { name: 'EN', exact: true }).focus();
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => document.documentElement.lang === 'en');
  assert.equal(await page.locator('html').getAttribute('lang'), 'en');
  assert.equal(await page.getByRole('link', { name: 'EN', exact: true }).evaluate(el => el === document.activeElement), true);
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.reload();
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.waitForTimeout(100);
  assert.equal(await page.evaluate(() => document.getAnimations().length), 0);
  assert.equal(await page.locator('.reveal:not(.visible)').count(), 0);
  assert.deepEqual(errors, []);
  console.log(JSON.stringify({ result: 'PASS', layouts, languages: 2, skills: 8, checks: ['translation-key parity', 'no overflow or clipped headings', 'full English text', 'selection across language switches', 'shared URLs', 'preference persistence', 'explicit URL priority', 'actual clipboard write/read', 'clipboard failure recovery', 'blocked storage', 'keyboard focus', 'reduced motion and live preference changes'], pageErrors: errors }));
  await browser.close();
})();
