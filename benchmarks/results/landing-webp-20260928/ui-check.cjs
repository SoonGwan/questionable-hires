const {chromium}=require('/tmp/qh-landing-qa/node_modules/playwright');
const assert=require('assert'), fs=require('fs'), crypto=require('crypto');
const hash=extension=>crypto.createHash('sha256').update(fs.readFileSync('assets/team-characters.'+extension)).digest('hex');
const base=process.env.QH_QA_URL||'http://127.0.0.1:4192/';
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const results=[];
 try {
  for(const js of [true,false]) for(const width of [320,390,768,1440]) for(const locale of ['ko','en']) {
   const context=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:js,reducedMotion:'reduce'});
   const page=await context.newPage(),errors=[],requests=[];
   page.on('pageerror',e=>errors.push(e.message)); page.on('request',r=>{if(r.url().includes('team-characters.')) requests.push(r.url())});
   assert.equal((await page.goto(base+locale+'/',{waitUntil:'domcontentloaded'})).status(),200);
   await page.locator('.cast img').evaluate(img=>img.decode());
   const state=await page.evaluate(()=>({src:document.querySelector('.cast img').currentSrc,
    width:document.querySelector('.cast img').naturalWidth,height:document.querySelector('.cast img').naturalHeight,
    overflow:document.documentElement.scrollWidth>innerWidth}));
   assert(state.src.endsWith(hash('webp')+'.webp')); assert.equal(state.width,1536); assert.equal(state.height,1024); assert.equal(state.overflow,false);
   assert.equal(requests.filter(url=>url.endsWith('.png')).length,0);
   if(js) for(let i=0;i<8;i++) {await page.locator('[data-hire="'+i+'"]').click();assert.equal(await page.locator('.portrait img').evaluate(img=>img.currentSrc),state.src)}
   assert.deepEqual(errors,[]); results.push({js,width,locale,...state,artworkRequests:requests.length,pageErrors:errors});
   if(js&&locale==='ko'&&[390,1440].includes(width)) await page.screenshot({path:'/tmp/qh-webp-'+width+'.png',fullPage:true});
   await context.close();
  }
  const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'}), page=await context.newPage(), cache=[];
  for(const locale of ['ko','en','ko']) {
   await page.goto(base+locale+'/',{waitUntil:'domcontentloaded'}); await page.locator('.cast img').evaluate(img=>img.decode());
   cache.push(await page.evaluate(()=>{const r=performance.getEntriesByName(document.querySelector('.cast img').currentSrc)[0];return {transferSize:r.transferSize,encodedBodySize:r.encodedBodySize}}));
  }
  assert(cache[0].transferSize>0); assert.equal(cache[0].encodedBodySize,fs.statSync('assets/team-characters.webp').size); assert.equal(cache[1].transferSize,0); assert.equal(cache[2].transferSize,0);
  await page.goto(base,{waitUntil:'domcontentloaded'});
  await page.locator('[data-language="en"]').click(); await page.waitForURL('**/en/'); await page.locator('.cast img').evaluate(img=>img.decode());
  assert.equal(await page.locator('.cast img').evaluate(img=>new URL(img.currentSrc).pathname),new URL('assets/team-characters.'+hash('webp')+'.webp',base).pathname);
  // Exercise the browser's unsupported-source selection, not a network-error fallback claim.
  await page.locator('picture source').evaluateAll(nodes=>nodes.forEach(node=>node.type='image/x-not-supported'));
  await page.waitForFunction(()=>document.querySelector('.cast img').currentSrc.endsWith('.png'));
  await page.locator('.cast img').evaluate(img=>img.decode());
  const fallback=await page.locator('.cast img').evaluate(img=>({src:img.currentSrc,width:img.naturalWidth,height:img.naturalHeight}));
  assert(fallback.src.endsWith(hash('png')+'.png')); assert.equal(fallback.width,1536);
  const pixels=await page.evaluate(async urls=>{
   const arrays=[];
   for(const url of urls) { const img=new Image(); img.src=url; await img.decode(); const c=document.createElement('canvas'); c.width=img.naturalWidth; c.height=img.naturalHeight; const ctx=c.getContext('2d');ctx.drawImage(img,0,0);arrays.push(ctx.getImageData(0,0,c.width,c.height).data); }
   let differences=0;for(let i=0;i<arrays[0].length;i++) if(arrays[0][i]!==arrays[1][i]) differences++;
   return {channelValues:arrays[0].length,differences};
  },['png','webp'].map(ext=>new URL('assets/team-characters.'+hash(ext)+'.'+ext,base).href));
  assert.equal(pixels.differences,0); await context.close();
  console.log(JSON.stringify({base,results,cache,rootLocaleNavigation:true,fallback,pixels},null,2));
 } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
