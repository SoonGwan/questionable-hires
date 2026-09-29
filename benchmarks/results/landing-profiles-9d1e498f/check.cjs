const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const base='https://hires.no-money-do-you-have-money.com';const observations=[];const links=new Set();
 try {
  for(const lang of ['ko','en']){
   const context=await browser.newContext({reducedMotion:'reduce',viewport:{width:390,height:844}});
   const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(`${base}/${lang}/`);
   assert.equal(await page.locator('.hire').count(),process.env.QH_EXPECT_NINE==='1'?9:8,'roster count');
   for(let i=0;i<8;i++){
    await page.locator('.hire').nth(i).click();
    assert.equal(await page.locator('.hire[aria-pressed="true"]').count(),1);
    assert.equal(await page.locator('.hire').nth(i).getAttribute('aria-pressed'),'true');
    const id=(await page.locator('#profile-code').textContent()).toLowerCase();
    const href=await page.locator('#example-link').getAttribute('href');
    assert.equal(href,`https://github.com/SoonGwan/questionable-hires/blob/main/examples/${id}.md`);
    assert.ok((await page.locator('#skill-description').textContent()).trim());links.add(href);
   }
   const id=await page.locator('#profile-code').textContent();
   const other=lang==='ko'?'en':'ko';
   await page.locator(`[data-language="${other}"]`).click();
   await page.waitForFunction(l=>document.documentElement.lang===l,other);
   assert.equal(await page.locator('#profile-code').textContent(),id);
   assert.equal(await page.locator('.portrait').evaluate(e=>e.getAnimations().length),0);
   assert.deepEqual(errors,[]);
   observations.push({language:lang,profiles:8,selection_preserved:true,reduced_motion_portrait:true,page_errors:errors});
   await context.close();
   const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
   const staticPage=await nojs.newPage();await staticPage.goto(`${base}/${lang}/`);
   assert.equal(await staticPage.locator('html').getAttribute('lang'),lang);
   assert.equal(await staticPage.locator('link[rel="canonical"]').getAttribute('href'),`${base}/${lang}/`);
   assert.equal(await staticPage.locator('meta[property="og:url"]').getAttribute('content'),`${base}/${lang}/`);
   assert.equal(await staticPage.locator('.raw-details tbody tr').count(),10);
   assert.equal(await staticPage.locator('.checkpoint-details tbody tr').count(),8);
   for(const metric of ['total_tokens','elapsed_seconds']) assert.equal(await staticPage.locator(`[data-chart="${metric}"]`).isVisible(),true);
   observations.push({language:lang,javascript:false,canonical_and_og:true,featured_rows:10,cohort_rows:8,both_charts_visible:true});
   await nojs.close();
  }
  fs.writeFileSync('/tmp/qh-landing-complete-01/browser.json',JSON.stringify({result:'PASS',observations,example_links:[...links]},null,2)+'\n');
  console.log('PASS: all eight profiles, reduced motion and preserved selection in both languages; no-JS charts/rows and localized metadata.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
