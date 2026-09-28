// Async locale replacement must preserve the user's current keyboard position.
// Usage: node tests/browser/landing_language_focus.cjs <landing-root-url> [playwright-module]
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = new URL(process.argv[2]);
const cases = [
  ['metric', '[data-metric="elapsed_seconds"]'],
  ['raw-summary', '.raw-details > summary'],
  ['raw-table', '.raw-details .table-scroll'],
  ['checkpoint-summary', '.checkpoint-details > summary'],
  ['checkpoint-table', '.checkpoint-details .table-scroll'],
  ['evidence-link', '[data-evidence-file$="reports.zip"]'],
  ['outside-profile', '[data-hire="3"]']
];
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QH_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  let failures = 0;
  try {
    for (const lang of ['ko', 'en']) for (const [name, selector] of cases) {
      const target = lang === 'ko' ? 'en' : 'ko';
      const context = await browser.newContext({ viewport: { width: 390, height: 900 }, reducedMotion: 'reduce' });
      try {
        const page = await context.newPage();
        page.setDefaultTimeout(5000);
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        let release;
        const gate = new Promise(resolve => { release = resolve; });
        await page.route(`**/experiments/${target}.html`, async route => {
          await gate;
          await route.fulfill({ status: 200, contentType: 'text/html',
            body: fs.readFileSync(path.join(__dirname, `../../landing/experiments/${target}.html`), 'utf8') });
        });
        await page.goto(new URL(`${lang}/`, base).href, { waitUntil: 'load', timeout: 10000 });
        await page.waitForFunction(() => document.querySelector('#main').getAttribute('aria-busy') === 'false');
        await page.locator('.raw-details > summary').click();
        await page.locator('.checkpoint-details > summary').click();
        await page.locator('[data-metric="elapsed_seconds"]').click();
        await page.locator(`[data-language="${target}"]`).click();
        assert.equal(await page.locator('#main').getAttribute('aria-busy'), 'true');
        if (name === 'outside-profile') await page.locator(selector).click();
        else {
          await page.locator('[data-metric="elapsed_seconds"]').click();
          // Reach each disclosure/table/download through native Tab navigation.
          for (let steps = 0; steps < 20 && !(await page.locator(selector).evaluate(e => e === document.activeElement)); steps++) {
            await page.keyboard.press('Tab');
          }
        }
        assert.equal(await page.locator(selector).evaluate(e => e === document.activeElement), true, 'keyboard reached intended control');
        release();
        await page.waitForFunction(expected => document.documentElement.lang === expected && document.querySelector('#main').getAttribute('aria-busy') === 'false', target);
        assert.equal(await page.locator(selector).evaluate(e => e === document.activeElement), true,
          `translation lost focus: ${await page.evaluate(() => document.activeElement.outerHTML.slice(0,100))}`);
        assert.equal(await page.locator('[data-metric="elapsed_seconds"]').getAttribute('aria-pressed'), 'true');
        if (name.endsWith('summary')) {
          await page.keyboard.press('Space');
          assert.equal(await page.locator(selector).evaluate(e => e.parentElement.open), false, 'keyboard still activates disclosure');
        } else if (name === 'metric') {
          await page.keyboard.press('Shift+Tab');
          await page.keyboard.press('Space');
          assert.equal(await page.locator('[data-metric="total_tokens"]').getAttribute('aria-pressed'), 'true');
        }
        assert.deepEqual(errors, []);
        console.log(JSON.stringify({ lang, case: name, result: 'PASS' }));
      } catch (error) {
        failures++;
        console.log(JSON.stringify({ lang, case: name, result: 'FAIL', error: error.message }));
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
  process.exitCode = failures ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
