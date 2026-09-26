const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('/tmp/qh-landing-qa/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const origin=process.env.QH_QA_ORIGIN||'http://127.0.0.1:4181';
 try {
  const context=await browser.newContext({reducedMotion:'reduce'}); const page=await context.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'/?lang=ko'); await page.waitForURL('**/ko/');
  const english=page.getByRole('link',{name:'EN',exact:true});assert.equal(await english.evaluate(el=>el.href),origin+'/en/');
  const opened=context.waitForEvent('page'); await english.click({modifiers:['ControlOrMeta']});
  const popup=await opened;await popup.waitForLoadState();assert.equal(popup.url(),origin+'/en/');assert.equal(await popup.locator('html').getAttribute('lang'),'en');await popup.close();
  for(const lang of ['ko','en']){
   await page.goto(origin+'/'+lang+'/');
   const details=page.locator('.checkpoint-details'); await details.locator('summary').click();
   assert.equal(await details.locator('tbody tr').count(),8);
   assert.equal(await details.locator('tfoot').innerText().then(x=>x.includes('606,355')&&x.includes('718,747')),true);
   for(const width of [320,390,760,768,1024,1440,1920]){
    await page.setViewportSize({width,height:1000});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,lang+' '+width);
   }
   const next=lang==='ko'?'en':'ko';await page.getByRole('link',{name:next.toUpperCase(),exact:true}).click();
   await page.waitForFunction(wanted=>document.documentElement.lang===wanted,next);
   assert.equal(await page.locator('.checkpoint-details').evaluate(el=>el.open),true);
   const links=await page.locator('[data-evidence-file]').evaluateAll(xs=>xs.map(x=>({path:x.dataset.evidenceFile,href:x.href})));
   assert.equal(links.length,3);
   for(const link of links){
    assert.equal(link.href,origin+'/'+link.path);
    const response=await page.request.get(link.href);assert.equal(response.status(),200);
    const expected=link.path.endsWith('comparison.json')?'benchmarks/results/all-eight-current-05/comparison.json':'benchmarks/'+link.path.split('/').pop();
    assert.deepEqual(await response.body(),fs.readFileSync(expected));
   }
  }
  assert.deepEqual(errors,[]);await page.screenshot({path:'/tmp/qh-landing-qa/evidence-open-mobile.png'});
  console.log(JSON.stringify({result:'PASS',origin,rootModifierNavigation:true,openTableLayouts:14,comparisonTasks:8,downloadFiles:3,downloadBytesMatch:true,tableStateAcrossLanguage:true,pageErrors:errors}));
 } finally {await browser.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
