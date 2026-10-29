// Render the page inside an iframe under hostile conditions the artifact viewer may impose.
// usage: node tests/frame.js <view> <mode>   mode: normal | noraf | hidden
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const view=process.argv[2]||'nb-share',mode=process.argv[3]||'normal';
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:900},colorScheme:'dark'});
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 let inject=`<script>location.hash=${JSON.stringify(view)};</script>`;
 if(mode==='noraf')inject+='<script>window.requestAnimationFrame=()=>0;</script>';
 const html=fs.readFileSync(__dirname+'/../index.html','utf8').replace('<head>','<head>'+inject);
 await p.route('http://local.test/inner',r=>r.fulfill({body:html,contentType:'text/html'}));
 const style=mode==='hidden'?'display:none;':'';
 await p.route('http://local.test/',r=>r.fulfill({body:`<!doctype html><body style="margin:0"><iframe id=f src="/inner" style="${style}width:1080px;height:880px;border:0"></iframe><script>setTimeout(()=>f.style.display="block",2500)</script>`,contentType:'text/html'}));
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://local.test/');await p.waitForTimeout(6000);
 const fr=p.frames().find(f=>f.url().includes('/inner'));
 const info=await fr.evaluate(()=>[...document.querySelectorAll('section.view:not([hidden]) canvas')].map(c=>{const ch=window.Chart&&Chart.getChart(c);
   // count non-transparent pixels in the canvas
   let ink=0;try{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;for(let i=3;i<d.length;i+=4*97)if(d[i])ink++}catch(e){ink=-1}
   return c.id+':'+c.width+'x'+c.height+':ink'+ink+(ch?'':':NOCHART')}).join(' '));
 await p.screenshot({path:`/tmp/frame_${view}_${mode}.png`});
 console.log(view,mode,errs.length?errs:'',info);await b.close()})();
