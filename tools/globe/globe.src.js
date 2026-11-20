import {geoOrthographic,geoPath,geoGraticule10} from 'd3-geo';
import {feature} from 'topojson-client';
import topo from 'world-atlas/land-110m.json';
(function(){
  var c=document.getElementById('globe'); if(!c||!c.getContext)return;
  var land=feature(topo,topo.objects.land), grat=geoGraticule10();
  var S=c.width, x=c.getContext('2d'), r=S/2-1.5;
  var proj=geoOrthographic().scale(r).translate([S/2,S/2]).clipAngle(90).precision(0.6);
  var path=geoPath(proj,x);
  var still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function col(n,f){var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||f}
  var lam=100,last=0;
  function draw(){
    var ink=col('--ink','#141414'),paper=col('--paper','#ecebe5');
    proj.rotate([lam,-18]);
    x.clearRect(0,0,S,S);
    x.beginPath();path({type:'Sphere'});x.fillStyle=paper;x.fill();
    x.beginPath();path(grat);x.strokeStyle=ink;x.globalAlpha=.28;x.lineWidth=.8;x.stroke();x.globalAlpha=1;
    x.beginPath();path(land);x.fillStyle=ink;x.fill();
    x.beginPath();path({type:'Sphere'});x.strokeStyle=ink;x.lineWidth=2.4;x.stroke();
  }
  function tick(t){ if(t-last>40){lam+=0.45;last=t;draw()} requestAnimationFrame(tick) }
  draw(); if(!still) requestAnimationFrame(tick);
  new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
})();
