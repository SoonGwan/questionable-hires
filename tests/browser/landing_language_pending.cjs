// Real-browser locale request ownership and pending feedback; network is controlled.
// Usage: node tests/browser/landing_language_pending.cjs <landing-root-url> [playwright-module]
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const content = JSON.parse(fs.readFileSync(path.join(__dirname, '../../landing/content.json'))).copy;
const base = new URL(process.argv[2]);

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QH_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  let failures = 0;
  try {
    for (const lang of ['ko', 'en']) for (const name of ['complete', 'cancel-success', 'cancel-failure', 'resume', 'fallback']) {
      const target = lang === 'ko' ? 'en' : 'ko';
      const context = await browser.newContext({ viewport: { width: 320, height: 900 }, reducedMotion: 'reduce' });
      const errors = [];
      try {
        const page = await context.newPage();
        page.setDefaultTimeout(5000);
        page.on('pageerror', error => errors.push(error.message));
        let release;
        const gate = new Promise(resolve => { release = resolve; });
        let observe;
        const requested = new Promise(resolve => { observe = resolve; });
        await page.route(`**/experiments/${target}.html`, async route => {
          observe();
          const success = await gate;
          if (success) await route.fulfill({ status: 200, contentType: 'text/html',
            body: fs.readFileSync(path.join(__dirname, `../../landing/experiments/${target}.html`), 'utf8') });
          else await route.fulfill({ status: 503, contentType: 'text/plain', body: 'Controlled failure' });
        });
        await page.goto(new URL(`${lang}/`, base).href, { waitUntil: 'load', timeout: 10000 });
        await page.waitForFunction(expected => document.documentElement.lang === expected, lang);
        await page.locator('[data-hire="3"]').click();
        await page.locator('[data-metric="elapsed_seconds"]').click();
        await page.locator('.raw-details summary').click();
        await page.getByRole('link', { name: target.toUpperCase(), exact: true }).click();
        await Promise.race([requested, new Promise((_, reject) => setTimeout(() => reject(new Error('No translation request')), 5000))]);
        assert.equal(await page.locator('html').getAttribute('lang'), lang);
        assert.equal(await page.locator('#main').getAttribute('aria-busy'), 'true');
        const status = page.locator('#language-status');
        assert.equal(await status.getAttribute('role'), 'status');
        assert.equal(await status.textContent(), content[lang][`languageLoading${target.toUpperCase()}`]);
        assert.equal(await status.isVisible(), true);
        const bounds = await status.boundingBox();
        assert.ok(bounds.x >= 0 && bounds.x + bounds.width <= 320, JSON.stringify(bounds));
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
        if (name.startsWith('cancel') || name === 'resume') {
          await page.getByRole('link', { name: lang.toUpperCase(), exact: true }).click();
          await page.waitForFunction(() => document.querySelector('#main').getAttribute('aria-busy') === 'false');
          assert.equal(await status.textContent(), '');
          if (name === 'resume') {
            await page.getByRole('link', { name: target.toUpperCase(), exact: true }).click();
            assert.equal(await page.locator('#main').getAttribute('aria-busy'), 'true');
          }
        }
        const response = page.waitForResponse(r => r.url().endsWith(`/experiments/${target}.html`));
        release(name !== 'cancel-failure' && name !== 'fallback');
        await response;
        // Await application promise reactions and two rendering frames, without timer sleeps.
        if (name === 'fallback') {
          await page.waitForURL(new URL(`${target}/`, base).href);
          await page.waitForLoadState('load');
        } else await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        const expected = name.startsWith('cancel') ? lang : target;
        assert.equal(await page.locator('html').getAttribute('lang'), expected);
        assert.equal(await page.locator('#main').getAttribute('aria-busy'), 'false');
        assert.equal(await status.textContent(), '');
        assert.equal(new URL(page.url()).pathname, new URL(`${expected}/`, base).pathname);
        assert.equal(await page.locator(`a[data-language="${expected}"]`).getAttribute('aria-current'), 'page');
        if (name !== 'fallback') {
          assert.equal(await page.locator('[data-hire="3"]').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('[data-metric="elapsed_seconds"]').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('.raw-details').evaluate(e => e.open), true);
        }
        assert.deepEqual(errors, []);
        console.log(JSON.stringify({ lang, case: name, result: 'PASS' }));
      } catch (error) {
        failures++;
        console.log(JSON.stringify({ lang, case: name, result: 'FAIL', error: error.message, pageErrors: errors }));
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
  process.exitCode = failures ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
