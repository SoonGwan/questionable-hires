const {chromium}=require('/tmp/qh-landing-qa/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const page=await browser.newPage(); await page.goto('http://127.0.0.1:4180/?lang=ko');
  await page.waitForURL('**/ko/');
  const actual=await page.getByRole('link',{name:'EN',exact:true}).evaluate(el=>el.href);
  const expected='http://127.0.0.1:4180/en/';
  if(actual===expected)throw new Error('Expected original root-link regression absent');
  console.log(JSON.stringify({result:'REPRODUCED',actual,expected,release:await (await page.request.get('http://127.0.0.1:4180/_health')).json()}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
