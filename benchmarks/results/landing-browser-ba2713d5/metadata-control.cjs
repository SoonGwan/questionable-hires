const assert = require('node:assert/strict');
const {chromium} = require('/tmp/qh-landing-qa/node_modules/playwright');
(async () => {
 const browser = await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const page = await browser.newPage();
  const results=[];
  for (const lang of ['ko','en']) {
   const url=`https://hires.no-money-do-you-have-money.com/${lang}/`;
   assert.equal((await page.goto(url,{timeout:20000})).status(),200);
   assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),url);
   const og = await page.locator('meta[property="og:image"]').getAttribute('content');
   assert.equal(og,`https://hires.no-money-do-you-have-money.com/assets/og-${lang}.png`);
   assert.equal(await page.locator('meta[name="twitter:image"]').getAttribute('content'),og);
   assert.equal(await page.locator('meta[property="og:locale"]').getAttribute('content'),lang==='ko'?'ko_KR':'en_US');
   const response=await page.request.get(og,{timeout:20000}); assert.equal(response.status(),200);
   const png=await response.body(); assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
   assert.equal(png.readUInt32BE(16),1200); assert.equal(png.readUInt32BE(20),630);
   results.push({language:lang,canonical:url,ogImage:og,width:1200,height:630});
  }
  console.log(JSON.stringify({result:'PASS',checks:results}));
 } finally {await browser.close();}
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
