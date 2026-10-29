const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
const views=process.argv[2]?process.argv[2].split(','):['front','nb-channels','nb-share','nb-bench','nb-creative','nb-q4','nb-meta','nb-library','wire'];
for(const [w,h,scheme,tag] of [[1280,900,'light','d'],[400,860,'dark','m']]){
 const p=await b.newPage({viewport:{width:w,height:h},colorScheme:scheme});
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push(e.message+' @ '+(e.stack||'').split('\n').slice(0,14).join(' | ')));
 const html=fs.readFileSync(__dirname+'/../dtc-newsroom.html','utf8');
 fs.writeFileSync('/tmp/t.html','<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>');

 await p.route('http://local.test/',r=>r.fulfill({body:fs.readFileSync('/tmp/t.html','utf8'),contentType:'text/html'}));
 await p.goto('http://local.test/');await p.waitForTimeout(800);
 for(const v of views){await p.evaluate(v=>location.hash=v,v);await p.waitForTimeout(2500);
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  await p.screenshot({path:`/tmp/s_${tag}_${v}.png`,fullPage:true});console.log(tag,v,'overflow',ov);}
 console.log(tag,'errors',errs);await p.close()}
await b.close()})();
