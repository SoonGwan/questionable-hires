#!/usr/bin/env node
// Development-only SVG rasterization. The deployed landing has no JS dependencies.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const assets = path.resolve(__dirname, '../landing/assets');
const jobs = [
  ['og-ko.svg', 'og-ko.png', 1200, 630],
  ['og-en.svg', 'og-en.png', 1200, 630],
  ['favicon.svg', 'favicon-32.png', 32, 32],
  ['favicon.svg', 'apple-touch-icon.png', 180, 180]
];
(async () => {
  const browser = await chromium.launch(process.env.CHROME_EXECUTABLE ? {
    executablePath: process.env.CHROME_EXECUTABLE, headless: true
  } : { headless: true });
  const sources = {};
  try {
    for (const [source, target, width, height] of jobs) {
      const svg = fs.readFileSync(path.join(assets, source));
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
      await page.setContent(`<style>html,body{margin:0;width:100%;height:100%;overflow:hidden}img{width:100%;height:100%;display:block}</style><img alt="" src="data:image/svg+xml;base64,${svg.toString('base64')}">`);
      await page.locator('img').evaluate(image => image.decode());
      const png = await page.screenshot({ path: path.join(assets, target) });
      sources[target] = { source, svg_sha256: crypto.createHash('sha256').update(svg).digest('hex'),
        png_sha256: crypto.createHash('sha256').update(png).digest('hex'), width, height };
      await page.close();
    }
    fs.writeFileSync(path.join(assets, 'raster-sources.json'), JSON.stringify(sources, null, 2) + '\n');
    console.log('Rendered 2 social cards, favicon and Apple touch icon.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
