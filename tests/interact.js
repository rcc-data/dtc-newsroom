// Interaction test under hostile frame conditions.
// usage: node tests/interact.js <mode>  mode: normal | dead (rAF never fires) | slow (rAF every 1s) | once (first few frames then dead)
const {chromium}=require('playwright');const fs=require('fs');
const RAF={
 normal:'',
 dead:'window.requestAnimationFrame=()=>0;',
 slow:'(function(){var n=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=function(cb){return setTimeout(function(){cb(performance.now())},1000)}})();',
 once:'(function(){var n=window.requestAnimationFrame.bind(window),k=0;window.requestAnimationFrame=function(cb){return ++k<5?n(cb):0}})();',
};
(async()=>{
 const mode=process.argv[2]||'dead';
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:900},colorScheme:'dark'});
 await p.route('**/chart.umd.js',r=>r.fulfill({body:fs.readFileSync('/tmp/cj/package/dist/chart.umd.js','utf8'),contentType:'application/javascript'}));
 await p.route('**/fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
 const html=fs.readFileSync(__dirname+'/../index.html','utf8').replace('<head>','<head><script>'+RAF[mode]+'</script>');
 await p.route('http://local.test/',r=>r.fulfill({body:html,contentType:'text/html'}));
 const errs=[];p.on('pageerror',e=>errs.push(e.message+' @ '+(e.stack||'').split('\n').slice(0,6).join(' | ')));
 const ink=id=>p.evaluate(id=>{const c=document.getElementById(id);if(!c)return 'missing';const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let k=0;for(let i=3;i<d.length;i+=4*97)if(d[i])k++;return k},id);
 const wait=ms=>p.waitForTimeout(ms);
 const log=[];
 await p.goto('http://local.test/#nb-share');await wait(2500);log.push('share load '+await ink('cShare'));
 const bx=await p.locator('#cShare').boundingBox();
 await p.mouse.move(bx.x+bx.width*.5,bx.y+bx.height*.5);await wait(1500);log.push('share hover '+await ink('cShare'));
 await p.mouse.click(bx.x+bx.width*.5,bx.y+bx.height*.5);await wait(1500);log.push('share click '+await ink('cShare'));
 await p.click('#shScale button[data-s="linear"]');await wait(1500);log.push('share linear '+await ink('cShare'));
 await p.click('#shChart button[data-c="stack"]');await wait(1500);log.push('share stack '+await ink('cShare'));
 await p.click('#shBasis button[data-b="pub"]');await wait(1500);log.push('share pub '+await ink('cShare'));
 // legend click (hide a dataset)
 const b2=await p.locator('#cShare').boundingBox();await p.mouse.click(b2.x+b2.width*.3,b2.y+b2.height-12);await wait(1500);log.push('share legend '+await ink('cShare'));
 await p.goto('http://local.test/#nb-channels');await wait(2500);log.push('cmp load '+await ink('cCmp'));
 await p.selectOption('#cmpMetric','roas');await wait(1500);log.push('cmp metric '+await ink('cCmp'));
 await p.click('#cmpMode button[data-m="wow"]');await wait(1500);log.push('cmp wow '+await ink('cCmp'));
 const b3=await p.locator('#cCmp').boundingBox();await p.mouse.move(b3.x+b3.width*.7,b3.y+b3.height*.4);await wait(1500);log.push('cmp hover '+await ink('cCmp'));
 await p.selectOption('#trMetric','cac');await wait(1500);log.push('mini metric '+await ink('mini0'));
 await p.goto('http://local.test/#nb-bench');await wait(2500);log.push('lens load '+await ink('cLens'));
 await p.selectOption('#lensDim','vert');await wait(1500);log.push('lens vert '+await ink('cLens'));
 await p.setViewportSize({width:900,height:900});await wait(1500);log.push('lens resized '+await ink('cLens'));
 await p.screenshot({path:`/tmp/interact_${mode}.png`});
 console.log(mode,errs.length?errs:'no errors','\n '+log.join('\n '));await b.close()})();
