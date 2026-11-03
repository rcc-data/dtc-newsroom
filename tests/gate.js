// Passcode wall: wrong code shakes, 1738 runs the ticker rain and reveals the site; unlock is remembered.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 await p.route('http://local.test/',r=>r.fulfill({body:fs.readFileSync(__dirname+'/../index.html','utf8'),contentType:'text/html'}));
 await p.goto('http://local.test/');await p.waitForTimeout(500);
 const has=()=>p.evaluate(()=>!!document.getElementById('gate'));const out=['gate shown '+await has()];
 await p.screenshot({path:'/tmp/gate_0.png'});
 await p.keyboard.type('1234');await p.waitForTimeout(200);out.push('wrong hint '+await p.textContent('#gHint'));await p.waitForTimeout(500);
 await p.keyboard.type('1738');await p.waitForTimeout(1200);await p.screenshot({path:'/tmp/gate_1.png'});
 await p.waitForTimeout(3000);out.push('after unlock gate gone '+!(await has()));
 await p.reload();await p.waitForTimeout(600);out.push('remembered '+!(await has()));
 console.log(out.join(' | '),'errors',errs.length?errs:'none');await b.close();process.exit(errs.length?1:0)})();
