import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';

const executablePath = process.argv[2];
if (!executablePath) throw new Error('Supply the path to an installed Chrome executable');
const observations = [];
const browser = await chromium.launch({executablePath, headless: true, timeout: 15000});
try {
  for (const [driver, guarded] of [['fill', false], ['fill', true], ['keyboard', false], ['keyboard', true]]) {
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
      const inputs = driver === 'keyboard' ? ['o', 'n', 'r'] : ['old', 'new', 'normal'];
      async function enter(value) {
        if (driver === 'fill') return input.fill(value);
        await input.click();
        await input.press('ControlOrMeta+A');
        await input.press(value);
      }
      await enter(inputs[0]);
      await enter(inputs[1]);
      await page.evaluate(() => window.fixture.complete(1, 'new result'));
      const afterNew = await result.textContent();
      await page.evaluate(() => window.fixture.complete(0, 'old result'));
      const afterOld = await result.textContent();
      await enter(inputs[2]);
      await page.evaluate(() => window.fixture.complete(2, 'normal result'));
      const normal = await result.textContent();
      const submitted = await page.evaluate(() => window.fixture.submitted());
      const focused = await input.evaluate(element => element === document.activeElement);
      assert.deepEqual(submitted, inputs.map(value => ({value, trusted: true})));
      const keys = await page.evaluate(() => window.fixture.keys());
      if (driver === 'keyboard') {
        assert.deepEqual(keys.filter(event => inputs.includes(event.key)).map(event => event.key), inputs);
        assert.ok(keys.every(event => event.trusted));
      }
      assert.equal(afterNew, 'new result');
      assert.equal(afterOld, guarded ? 'new result' : 'old result');
      assert.equal(normal, 'normal result');
      assert.equal(focused, true);
      await enter(inputs[0]);
      await page.evaluate(() => window.fixture.fail(3));
      const recovery = {
        error: await page.locator('#error').textContent(),
        retainedInput: await input.inputValue(),
        focusedAfterFailure: await input.evaluate(element => element === document.activeElement),
      };
      assert.equal(recovery.error, 'Search failed. Try again.');
      assert.equal(recovery.retainedInput, inputs[0]);
      assert.equal(recovery.focusedAfterFailure, true);
      await enter(inputs[2]);
      recovery.errorOnRetry = await page.locator('#error').textContent();
      await page.evaluate(() => window.fixture.complete(4, 'recovered result'));
      recovery.result = await result.textContent();
      recovery.errorAfterSuccess = await page.locator('#error').textContent();
      recovery.focusedAfterSuccess = await input.evaluate(element => element === document.activeElement);
      assert.equal(recovery.errorOnRetry, '');
      assert.equal(recovery.result, 'recovered result');
      assert.equal(recovery.errorAfterSuccess, '');
      assert.equal(recovery.focusedAfterSuccess, true);
      recovery.submitted = await page.evaluate(() => window.fixture.submitted());
      assert.deepEqual(recovery.submitted, [...inputs, inputs[0], inputs[2]].map(value => ({value, trusted: true})));
      assert.deepEqual(errors, []);
      observations.push({driver, guarded, submitted, keys, afterNew, afterOld, normal, focused, recovery});
    } finally {
      await context.close();
    }
  }
  console.log(JSON.stringify({complete: true, browser: browser.version(), observations}, null, 2));
} finally {
  await browser.close();
}
