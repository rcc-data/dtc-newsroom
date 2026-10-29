// Full interaction sweep: every view, every toggle button / select / checkbox, hover + click on every chart.
// Fails if any page error fires or any visible chart canvas ends up blank.
// usage: node tests/sweep.js [normal|dead]
const {chromium}=require('playwright');const fs=require('fs');
const VIEWS=['front','trends','ctc','foxwell','bfcm','nb-channels','nb-share','nb-bench','nb-creative','nb-q4','nb-meta','nb-library','mkt','mo-bench','mo-trend','mo-research','haus','triplewhale','wire'];
(async()=>{
 const mode=process.argv[2]||'normal';
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900},colorScheme:'dark'});
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 const pre=mode==='dead'?'<script>window.requestAnimationFrame=()=>0;</script>':'';
 const html=fs.readFileSync(__dirname+'/../index.html','utf8').replace('<head>','<head>'+pre);
 await p.route('http://local.test/',r=>r.fulfill({body:html,contentType:'text/html'}));
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 const blanks=async tag=>p.evaluate(tag=>[...document.querySelectorAll('section.view:not([hidden]) canvas')].filter(c=>c.offsetParent).map(c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let k=0;for(let i=3;i<d.length;i+=4*61)if(d[i])k++;return k<3?tag+':'+c.id:null}).filter(Boolean),tag);
 await p.goto('http://local.test/');await p.waitForTimeout(1500);
 const bad=[];let actions=0;
 for(const v of VIEWS){
  await p.evaluate(v=>location.hash=v,v);await p.waitForTimeout(1200);
  bad.push(...await blanks(v+' load'));
  // toggle every segmented button
  const btns=await p.$$(`#v-${v} .seg button, #v-${v} .pseg button`);
  for(const bt of btns){if(!await bt.isVisible())continue;await bt.click();actions++;await p.waitForTimeout(250)}
  // every select: pick each option
  for(const sel of await p.$$(`#v-${v} select`)){if(!await sel.isVisible()||!await sel.isEnabled())continue;const vals=await sel.$$eval('option',o=>o.map(x=>x.value));for(const val of vals.slice(0,6)){await sel.selectOption(val);actions++;await p.waitForTimeout(200)}}
  for(const cb of await p.$$(`#v-${v} input[type=checkbox]`)){if(!await cb.isVisible()||!await cb.isEnabled())continue;await cb.click();await p.waitForTimeout(200);await cb.click();actions+=2;await p.waitForTimeout(200)}
  // hover and click every chart
  for(const c of await p.$$(`#v-${v} canvas`)){if(!await c.isVisible())continue;const bx=await c.boundingBox();if(!bx||bx.width<20)continue;await c.scrollIntoViewIfNeeded();const bb=await c.boundingBox();for(const fx of [.3,.6,.9]){await p.mouse.move(bb.x+bb.width*fx,bb.y+bb.height*.5);await p.waitForTimeout(120)}await p.mouse.click(bb.x+bb.width*.5,bb.y+bb.height*.5);actions++;await p.waitForTimeout(150)}
  await p.mouse.move(2,2);await p.waitForTimeout(900);
  bad.push(...await blanks(v+' after'));
 }
 console.log(mode,'actions',actions,'errors',errs.length?[...new Set(errs)]:'none','blank',bad.length?bad:'none');
 await b.close();process.exit(errs.length||bad.length?1:0)})();
