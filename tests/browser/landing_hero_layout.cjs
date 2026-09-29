// Check actual text geometry: container bounds alone miss title/tagline collisions.
// Usage: node tests/browser/landing_hero_layout.cjs <landing-root-url> [playwright-module]
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const base = new URL(process.argv[2]);
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.QH_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  let failures = 0;
  try {
    for (const javaScriptEnabled of [true, false]) for (const lang of ['ko', 'en']) {
      const context = await browser.newContext({ javaScriptEnabled, reducedMotion: 'reduce' });
      try {
        const page = await context.newPage();
        page.setDefaultTimeout(5000);
        for (const width of [320, 360, 390, 760, 768, 1024, 1440, 1920]) {
          try {
            await page.setViewportSize({ width, height: 900 });
            await page.goto(new URL(`${lang}/`, base).href, { waitUntil: 'load', timeout: 10000 });
            const geometry = await page.evaluate(() => {
              const rects = selector => {
                const walker = document.createTreeWalker(document.querySelector(selector), NodeFilter.SHOW_TEXT);
                const result = [];
                while (walker.nextNode()) {
                  if (!walker.currentNode.textContent.trim()) continue;
                  const range = document.createRange();
                  range.selectNodeContents(walker.currentNode);
                  result.push(...Array.from(range.getClientRects(), r => ({ left:r.left, top:r.top, right:r.right, bottom:r.bottom })));
                }
                return result;
              };
              return { title:rects('#hero-title'), tagline:rects('.hero-side'),
                overflow:document.documentElement.scrollWidth > innerWidth };
            });
            assert.ok(geometry.title.length && geometry.tagline.length, 'Missing rendered text');
            assert.equal(geometry.overflow, false, 'Horizontal page overflow');
            for (const rect of [...geometry.title, ...geometry.tagline]) {
              assert.ok(rect.left >= 0 && rect.right <= width, JSON.stringify(rect));
            }
            for (const title of geometry.title) for (const tagline of geometry.tagline) {
              const overlap = Math.min(title.right,tagline.right) > Math.max(title.left,tagline.left)
                && Math.min(title.bottom,tagline.bottom) > Math.max(title.top,tagline.top);
              assert.equal(overlap,false,JSON.stringify({title,tagline}));
            }
            console.log(JSON.stringify({lang,width,javaScriptEnabled,result:'PASS'}));
          } catch (error) {
            failures++;
            console.log(JSON.stringify({lang,width,javaScriptEnabled,result:'FAIL',error:error.message}));
          }
        }
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
  process.exitCode = failures ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
