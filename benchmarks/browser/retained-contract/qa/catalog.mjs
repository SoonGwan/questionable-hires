import { chromium } from 'playwright-core';
import { writeFile } from 'node:fs/promises';

// Run from repository root: timeout 45s node qa/catalog.mjs
const evidencePath = new URL('./catalog-evidence.json', import.meta.url);
const evidence = { layer: 'headless Chromium, trusted keyboard input, rendered DOM', cases: [], blockedRequests: [], cleanup: {} };
let browser;
let activeContext;
let infrastructureFailure = false;
const deadline = setTimeout(() => {
  console.error('ERROR: 35s overall deadline exceeded; outer timeout bounds process cleanup');
  process.exit(2);
}, 35000);

async function snapshot(page) {
  return {
    requests: await page.evaluate(() => window.transport.requests()),
    input: await page.locator('#query').inputValue(),
    results: await page.locator('#results').innerText(),
    error: await page.locator('#error').innerText(),
    focus: await page.locator(':focus').getAttribute('id'),
  };
}

async function runCase(name, body) {
  activeContext = await browser.newContext();
  const context = activeContext;
  const record = { name, observations: [], cleanup: false };
  evidence.cases.push(record);
  try {
    await context.route(/^https?:\/\//, async route => {
      evidence.blockedRequests.push(route.request().url());
      await route.abort();
    });
    const page = await context.newPage();
    page.setDefaultTimeout(3000);
    page.setDefaultNavigationTimeout(3000);
    await page.goto(new URL('../index.html', import.meta.url).href);
    const input = page.locator('#query');
    await input.click();
    const type = text => input.pressSequentially(text);
    const complete = (index, records) => page.evaluate(({ index, records }) => window.transport.complete(index, records), { index, records });
    const fail = index => page.evaluate(index => window.transport.fail(index), index);
    const check = async (step, expected) => {
      const observed = await snapshot(page);
      const matches = Object.entries(expected).every(([key, value]) => JSON.stringify(observed[key]) === JSON.stringify(value));
      record.observations.push({ step, expected, observed, matches });
    };
    await body({ input, type, complete, fail, check });
    record.outcome = record.observations.every(item => item.matches) ? 'PASS' : 'FAIL';
  } catch (error) {
    record.outcome = 'ERROR';
    record.error = String(error.stack || error);
    infrastructureFailure = true;
  } finally {
    await context.close();
    activeContext = undefined;
    record.cleanup = true;
  }
}

const requests = (...queries) => queries.map(query => ({ query, trusted: true }));
const state = (input, results, error = '') => ({ input, results, error, focus: 'query' });
try {
  if (!process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH) throw new Error('PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH is required');
  browser = await chromium.launch({ executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH, headless: true, timeout: 5000 });
  await runCase('normal success, current failure, retry', async ({ type, complete, fail, check }) => {
    await type('a');
    await complete(0, ['A']);
    await check('current success', { ...state('a', 'A'), requests: requests('a') });
    await type('b');
    await fail(1);
    // Requirements do not specify whether a current failure retains previous results.
    await check('current failure preserves input and focus', { input: 'ab', error: 'Search unavailable. Try again.', focus: 'query', requests: requests('a', 'ab') });
    await type('c');
    await check('new input retries and clears error', { input: 'abc', error: '', focus: 'query', requests: requests('a', 'ab', 'abc') });
    await complete(2, ['ABC']);
    await check('retry success', state('abc', 'ABC'));
  });
  await runCase('older success after newer success', async ({ type, complete, check }) => {
    await type('ab');
    await complete(1, ['AB']);
    await check('newer success', { ...state('ab', 'AB'), requests: requests('a', 'ab') });
    await complete(0, ['A']);
    await check('older success must not replace latest results', state('ab', 'AB'));
  });
  await runCase('older failure after newer success', async ({ type, complete, fail, check }) => {
    await type('ab');
    await complete(1, ['AB']);
    await check('newer success', { ...state('ab', 'AB'), requests: requests('a', 'ab') });
    await fail(0);
    await check('older failure must not mark latest success as failed', state('ab', 'AB'));
  });
  await runCase('older success after clear', async ({ input, type, complete, check }) => {
    await type('a');
    await input.press('ControlOrMeta+A');
    await input.press('Backspace');
    await complete(1, []);
    await check('empty query success', { ...state('', ''), requests: requests('a', '') });
    await complete(0, ['A']);
    await check('older response must not repopulate cleared results', state('', ''));
  });
} catch (error) {
  infrastructureFailure = true;
  evidence.diagnostic = String(error.stack || error);
  evidence.dependentCases = 'Any cases not recorded above are unrun';
} finally {
  try {
    if (activeContext) await activeContext.close();
    evidence.cleanup.contexts = 'closed';
    if (browser) await browser.close();
    evidence.cleanup.browser = browser ? 'closed' : 'not launched';
  } catch (error) {
    infrastructureFailure = true;
    evidence.cleanup.error = String(error);
  }
  await writeFile(evidencePath, JSON.stringify(evidence, null, 2) + '\n');
  clearTimeout(deadline);
}
for (const record of evidence.cases) {
  const differences = record.observations.filter(item => !item.matches).map(item => ({ step: item.step, expected: item.expected, observed: item.observed }));
  console.log(`${record.outcome}: ${record.name}; cleanup=${record.cleanup}; ${JSON.stringify(differences)}; evidence=${evidencePath.pathname}`);
}
if (evidence.diagnostic) console.log(`ERROR: ${evidence.diagnostic}; dependent cases unrun; evidence=${evidencePath.pathname}`);
console.log(`Cleanup: ${JSON.stringify(evidence.cleanup)}; HTTP(S) requests blocked=${evidence.blockedRequests.length}`);
process.exitCode = infrastructureFailure ? 2 : evidence.cases.some(record => record.outcome === 'FAIL') ? 1 : 0;
