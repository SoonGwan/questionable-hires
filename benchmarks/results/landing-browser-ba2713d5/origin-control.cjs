const { chromium } = require('playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  const context = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const lang of ['ko','en']) {
    const response = await page.goto(`http://127.0.0.1:4180/${lang}/`, { timeout: 20000 });
    assert.equal(response.status(),200);
    assert.equal(await page.locator('html').getAttribute('lang'),lang);
    assert.equal(await page.locator('meta[property="og:url"]').getAttribute('content'),`https://hires.no-money-do-you-have-money.com/${lang}/`);
    assert.equal(await page.locator('meta[name="robots"]').getAttribute('content'),'index, follow, max-image-preview:large');
    await page.screenshot({path:`/tmp/qh-landing-qa/origin-ba2713d5-${lang}.png`});
    await page.locator('[data-metric="elapsed_seconds"]').click();
    assert.equal(await page.locator('[data-chart="elapsed_seconds"]').isVisible(),true);
  }
  await page.setViewportSize({width:390,height:844});
  await page.locator('.raw-details summary').click();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  assert.equal(await page.locator('tbody tr').count(),10);
  await page.getByRole('link',{name:'KO',exact:true}).click();
  await page.waitForFunction(()=>document.documentElement.lang==='ko');
  assert.equal(await page.locator('[data-chart="elapsed_seconds"]').isVisible(),true);
  await page.screenshot({path:'/tmp/qh-landing-qa/origin-ba2713d5-mobile-ko.png',fullPage:true});
  assert.deepEqual(errors,[]);
  console.log('PASS: production local-origin browser navigation, both locales, live canonical/OG, indexability, chart switching, mobile raw table and language/metric preservation; no script errors.');
  await browser.close();
})().catch(error=>{console.error(error.message);process.exit(1)});
