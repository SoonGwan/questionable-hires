const {chromium}=require('/tmp/qh-landing-qa/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  for(const language of ['ko','en']){
   await page.goto('https://hires.no-money-do-you-have-money.com/'+language+'/');
   await page.locator('.checkpoint-details summary').click();
   const detail=page.locator('.checkpoint-details');
   const text=await detail.innerText();
   for(const count of ['592,509','13,846','606,355','530,432','705,328','13,419','718,747','613,632'])assert.ok(text.includes(count),count);
   assert.ok(text.includes(language==='ko'?'모델 응답 38회':'38 model responses'));
   assert.ok(text.includes(language==='ko'?'모델 응답 39회':'39 model responses'));
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   await detail.screenshot({path:'/tmp/qh-landing-qa/token-breakdown-'+language+'.png'});
  }
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({result:'PASS',url:'https://hires.no-money-do-you-have-money.com/',locales:2,mobileWidth:390,usageBreakdownMatches:true,pageErrors:errors}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
