// Desks dropdown: hover opens, link navigates and closes, click toggles, Escape closes; mobile tap.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const errs=[];const out=[];
for(const [w,h,touch] of [[1280,800,false],[400,800,true]]){
 const p=await b.newPage({viewport:{width:w,height:h},hasTouch:touch,isMobile:touch});p.on('pageerror',e=>errs.push(e.message));
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 await p.route('http://local.test/',r=>r.fulfill({body:fs.readFileSync(__dirname+'/../index.html','utf8'),contentType:'text/html'}));
 await p.goto('http://local.test/');await p.waitForTimeout(800);
 const vis=()=>p.evaluate(()=>!document.getElementById('deskMenu').hidden);
 if(!touch){await p.hover('#deskBtn');await p.waitForTimeout(200);out.push('hover '+await vis());await p.screenshot({path:'/tmp/nav_open.png'});
  await p.click('#deskMenu a[href="#ctc"].ddh');await p.waitForTimeout(500);out.push('nav->'+await p.evaluate(()=>location.hash)+' closed '+!(await vis())+' current '+await p.getAttribute('#deskBtn','aria-current'));
  await p.mouse.move(5,600);await p.waitForTimeout(300);
  await p.focus('#deskBtn');await p.keyboard.press('Enter');out.push('kbd '+await vis());await p.keyboard.press('Escape');out.push('esc closed '+!(await vis()));}
 else{await p.tap('#deskBtn');await p.waitForTimeout(200);out.push('tap '+await vis());await p.screenshot({path:'/tmp/nav_m.png'});await p.tap('#deskMenu a[href="#mo-trend"]');await p.waitForTimeout(500);out.push('m nav->'+await p.evaluate(()=>location.hash)+' closed '+!(await vis()));}
 await p.close()}
console.log(out.join(' | '),errs.length?errs:'no errors');await b.close()})();
