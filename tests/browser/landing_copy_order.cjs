// Browser regression: status belongs to the latest copy attempt, in the current locale.
// Usage: node tests/browser/landing_copy_order.cjs <landing-root-url> [playwright-module]
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const copy = JSON.parse(fs.readFileSync(path.join(__dirname, '../../landing/content.json'))).copy;
const base = new URL(process.argv[2]);
const cases = ['normal', 'retry', 'older-failure', 'older-success', 'both-success', 'language-pending'];

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QH_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  let failures = 0;
  try {
    for (const lang of ['ko', 'en']) for (const name of cases) {
      const context = await browser.newContext({ viewport: { width: 390, height: 900 }, reducedMotion: 'reduce' });
      const errors = [];
      try {
        await context.addInitScript(() => {
          window.qhCopyRequests = [];
          Object.defineProperty(navigator, 'clipboard', { configurable: true, value: {
            writeText(text) {
              return new Promise((resolve, reject) => window.qhCopyRequests.push({ text, resolve, reject }));
            }
          }});
        });
        const page = await context.newPage();
        page.setDefaultTimeout(5000);
        page.on('pageerror', error => errors.push(error.message));
        await page.goto(new URL(`${lang}/`, base).href, { waitUntil: 'load', timeout: 10000 });
        await page.waitForFunction(expected => document.documentElement.lang === expected, lang);
        const button = page.locator('#copy');
        const status = page.locator('#copy-status');
        const click = async count => {
          await button.click();
          await page.waitForFunction(expected => window.qhCopyRequests.length === expected, count);
        };
        const settle = async (index, success) => {
          await page.evaluate(async ({ index, success }) => {
            const request = window.qhCopyRequests[index];
            if (success) request.resolve();
            else request.reject(new Error('Controlled clipboard denial'));
            await Promise.resolve();
          }, { index, success });
        };
        let expectedLanguage = lang;
        let expectedState = 'copied';
        await click(1);
        if (name === 'normal') {
          await settle(0, true);
        } else if (name === 'retry') {
          await settle(0, false);
          assert.equal(await status.textContent(), copy[lang].copyFailed);
          await click(2);
          await settle(1, true);
        } else if (name === 'language-pending') {
          expectedLanguage = lang === 'ko' ? 'en' : 'ko';
          await page.getByRole('link', { name: expectedLanguage.toUpperCase(), exact: true }).click();
          await page.waitForFunction(expected => document.documentElement.lang === expected, expectedLanguage);
          await settle(0, true);
        } else {
          await click(2);
          const latestSuccess = name !== 'older-success';
          expectedState = latestSuccess ? 'copied' : 'copyFailed';
          await settle(1, latestSuccess);
          assert.equal(await status.textContent(), copy[lang][expectedState]);
          await settle(0, name !== 'older-failure');
        }
        assert.equal(await status.textContent(), copy[expectedLanguage][expectedState]);
        assert.equal(await status.isVisible(), true);
        assert.equal(await status.getAttribute('role'), 'status');
        assert.equal(await button.isEnabled(), true);
        assert.deepEqual(await page.evaluate(() => window.qhCopyRequests.map(request => request.text)),
          Array(name === 'normal' || name === 'language-pending' ? 1 : 2).fill('npx skills add SoonGwan/questionable-hires'));
        assert.deepEqual(errors, []);
        console.log(JSON.stringify({ lang, case: name, result: 'PASS', expectedLanguage, expectedState }));
      } catch (error) {
        failures++;
        console.log(JSON.stringify({ lang, case: name, result: 'FAIL', error: error.message, pageErrors: errors }));
      } finally {
        await context.close();
      }
    }
  } finally {
    await browser.close();
  }
  console.log(JSON.stringify({ cases: cases.length * 2, failures, browserClosed: true,
    scope: 'Real browser clicks and rendered status; controlled clipboard promises, no OS clipboard writes' }));
  process.exitCode = failures ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
