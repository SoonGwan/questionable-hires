import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';

const executablePath = process.argv[2];
if (!executablePath) throw new Error('Supply the path to an installed Chrome executable');
const observations = [];
const browser = await chromium.launch({executablePath, headless: true, timeout: 15000});
try {
  for (const guarded of [false, true]) {
    const context = await browser.newContext();
    try {
      const page = await context.newPage();
      page.setDefaultTimeout(5000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      // Only local file content is needed; block page-originated web requests.
      await context.route(/^https?:\/\//, route => route.abort());
      const url = new URL('./search-order.html', import.meta.url);
      url.search = `manual=1&guard=${guarded ? 'on' : 'off'}`;
      await page.goto(url.href);
      const input = page.locator('#query');
      const result = page.locator('#results');
      await input.fill('old');
      await input.fill('new');
      await page.evaluate(() => window.fixture.complete(1, 'new result'));
      const afterNew = await result.textContent();
      await page.evaluate(() => window.fixture.complete(0, 'old result'));
      const afterOld = await result.textContent();
      await input.fill('normal');
      await page.evaluate(() => window.fixture.complete(2, 'normal result'));
      const normal = await result.textContent();
      const submitted = await page.evaluate(() => window.fixture.submitted());
      const focused = await input.evaluate(element => element === document.activeElement);
      assert.deepEqual(submitted, ['old', 'new', 'normal'].map(value => ({value, trusted: true})));
      assert.equal(afterNew, 'new result');
      assert.equal(afterOld, guarded ? 'new result' : 'old result');
      assert.equal(normal, 'normal result');
      assert.equal(focused, true);
      assert.deepEqual(errors, []);
      observations.push({guarded, submitted, afterNew, afterOld, normal, focused});
    } finally {
      await context.close();
    }
  }
  console.log(JSON.stringify({complete: true, browser: browser.version(), observations}, null, 2));
} finally {
  await browser.close();
}
