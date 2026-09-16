(() => {
'use strict';
const canvas=document.querySelector('canvas'), ctx=canvas.getContext('2d',{alpha:false});
const TAU=Math.PI*2, duration=30;
const opening=new Image(); opening.src='assets/hero/city-opening.webp';
let floorOffset=0;
let w=0,h=0,dpr=1,time=0,playing=true,visible=true,last=performance.now();
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const clamp=x=>Math.max(0,Math.min(1,x)), smooth=x=>{x=clamp(x);return x*x*(3-2*x)}, mix=(a,b,t)=>a+(b-a)*t;
const range=(t,a,b)=>smooth((t-a)/(b-a));
const rgb=(a,b,t)=>a.map((v,i)=>Math.round(mix(v,b[i],t)));
const color=(v,a=1)=>`rgba(${v[0]},${v[1]},${v[2]},${a})`;
const navy=[12,28,43],cyan=[98,224,235],coral=[255,117,93],warm=[251,190,121];
let cam={x:30,y:27,z:36,tx:0,ty:6,tz:0,f:1}, forward,right,up;
const sub=(a,b)=>a.map((v,i)=>v-b[i]);
const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
const norm=a=>{const n=Math.hypot(...a);return a.map(v=>v/n)};
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
function camera(c){cam=c;forward=norm([c.tx-c.x,c.ty-c.y,c.tz-c.z]);right=norm(cross(forward,[0,1,0]));up=cross(right,forward)}
function project(p){const v=sub([p[0],p[1]+floorOffset,p[2]],[cam.x,cam.y,cam.z]),z=dot(v,forward);const f=Math.min(w/1.7,h)*cam.f;return [w*.5+dot(v,right)*f/z,h*.52-dot(v,up)*f/z,z]}
let faces=[];
function face(points,fill,stroke,alpha=1){const ps=points.map(project);if(ps.some(p=>p[2]<.1))return;faces.push({ps,fill,stroke,alpha,z:ps.reduce((a,p)=>a+p[2],0)/ps.length})}
function box(x,y,z,sx,sy,sz,base,alpha=1,edge='rgba(144,198,209,.16)'){
const a=[x,y,z],b=[x+sx,y,z],c=[x+sx,y,z+sz],d=[x,y,z+sz],e=[x,y+sy,z],f=[x+sx,y+sy,z],g=[x+sx,y+sy,z+sz],i=[x,y+sy,z+sz];
face([a,b,f,e],color(base.map(v=>v*.58)),edge,alpha);face([b,c,g,f],color(base.map(v=>v*.73)),edge,alpha);face([c,d,i,g],color(base.map(v=>v*.86)),edge,alpha);face([d,a,e,i],color(base.map(v=>v*.66)),edge,alpha);face([e,f,g,i],color(base),edge,alpha);
}
function flush(){faces.sort((a,b)=>b.z-a.z);for(const f of faces){ctx.globalAlpha=f.alpha;ctx.beginPath();f.ps.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fillStyle=f.fill;ctx.fill();if(f.stroke){ctx.strokeStyle=f.stroke;ctx.lineWidth=.7;ctx.stroke()}}ctx.globalAlpha=1;faces=[]}
function line(points,c,width=1,alpha=1){const ps=points.map(project);if(ps.some(p=>p[2]<.1))return;ctx.globalAlpha=alpha;ctx.strokeStyle=c;ctx.lineWidth=width;ctx.beginPath();ps.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();ctx.globalAlpha=1}
function glow(p,size,c,alpha=1){const q=project(p);if(q[2]<.1)return;const r=Math.min(w/1.7,h)*size*cam.f/q[2];if(r<.2)return;const g=ctx.createRadialGradient(q[0],q[1],0,q[0],q[1],r);g.addColorStop(0,color(c,alpha));g.addColorStop(.22,color(c,alpha*.45));g.addColorStop(1,color(c,0));ctx.fillStyle=g;ctx.fillRect(q[0]-r,q[1]-r,r*2,r*2)}
function backdrop(t){const g=ctx.createLinearGradient(0,0,w,h);g.addColorStop(0,'#173344');g.addColorStop(.55,'#091823');g.addColorStop(1,'#040c15');ctx.fillStyle=g;ctx.fillRect(0,0,w,h);const a=ctx.createRadialGradient(w*.7,h*.2,0,w*.7,h*.2,w*.65);a.addColorStop(0,'rgba(79,138,147,.13)');a.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=a;ctx.fillRect(0,0,w,h)}
// Deterministic blocks: no network, random frame jitter or external assets.
const blocks=[];for(let x=-4;x<=4;x++)for(let z=-4;z<=4;z++){if(Math.abs(x)<2&&Math.abs(z)<2)continue;let n=Math.abs(Math.sin(x*71.13+z*19.73));blocks.push({x:x*8,z:z*8,s:3.1+n*1.6,height:2+n*16})}
function city(t,fade){
box(-50,-.4,-50,100,.3,100,[20,38,48],fade);
for(let k=-5;k<=5;k++){face([[-50,0,k*8-1], [50,0,k*8-1],[50,0,k*8+1],[-50,0,k*8+1]],'#101d27',null,fade);face([[k*8-1,0,-50],[k*8+1,0,-50],[k*8+1,0,50],[k*8-1,0,50]],'#101d27',null,fade)}
for(const b of blocks){box(b.x,0,b.z,b.s,b.height,b.s,[47,71,84],fade);for(let y=1;y<b.height;y+=1.4){face([[b.x,y,b.z+b.s+.01],[b.x+b.s,y,b.z+b.s+.01],[b.x+b.s,y+.38,b.z+b.s+.01],[b.x,y+.38,b.z+b.s+.01]],'rgba(165,197,204,.22)',null,fade)}}
}
function tower(t,open,digital){const outside=1-open, base=rgb([91,123,136],[44,125,143],digital);
if(outside>.01){box(-6,0,-4,12,20,8,base,outside*.88);for(let y=1;y<20;y+=1.1){face([[-6,y,4.03],[6,y,4.03],[6,y+.12,4.03],[-6,y+.12,4.03]],'#bdd5d5',null,outside*.45);face([[6.03,y,-4],[6.03,y,4],[6.03,y+.12,4],[6.03,y+.12,-4]],'#bdd5d5',null,outside*.35)}for(let x=-5;x<6;x+=1.2)face([[x,0,4.04],[x+.04,0,4.04],[x+.04,20,4.04],[x,20,4.04]],'#b8d3d5',null,outside*.6);box(-5.8,20,-3.8,11.6,.3,7.6,[143,170,176],outside)}
}
const desks=[];for(let z=-2.6;z<3;z+=2.7)for(let x=-4.8;x<5;x+=2.7)desks.push({x,z});
function person(x,z,thermal,absorb,t,index){const b=rgb([126,157,174],[249,154,95],thermal),shift=Math.sin(t*1.2+index)*.028;
box(x-.14,10.12,z-.2,.28,.46,.28,[33,50,64]);box(x-.2,10.57,z-.18,.4,.48,.28,b);box(x-.125,11.07+shift,z-.15,.25,.27,.25,rgb([207,184,157],[255,210,120],thermal));
box(x-.3,10.69,z-.5,.13,.12,.4,b);box(x+.18,10.69,z-.5,.13,.12,.4,b);
}
function floor(t,open,thermal,absorb,digital){
const floorcolor=rgb(rgb([149,161,165],[79,65,127],thermal),[35,79,94],digital);
box(-6,9.9,-4,12,.2,8,floorcolor);
// Back walls, glazed meeting rooms, and translucent room partitions.
box(-6,10,-4,.12,2.8,8,rgb([122,147,159],[52,94,125],thermal),.65);
box(-6,10,-4,12,2.8,.12,rgb([128,153,163],[67,81,131],thermal),.75);
for(const x of [-.7,2]){box(x,10,-3.9,.055,2.4,3.9,[112,182,194],.17);box(x,12.35,-3.9,.055,.055,3.9,[130,191,201],.65)}
box(-5.9,10,-.05,11.8,2.35,.045,[115,175,188],.12);
for(let i=0;i<desks.length;i++){const {x,z}=desks[i],heat=thermal*(1-absorb*.75);const deskColor=rgb(rgb([179,164,140],[218,112,126],heat),[70,118,132],digital);
box(x,10.75,z,1.8,.09,.85,deskColor);box(x+.1,10,z+.12,.06,.75,.06,[83,111,125]);box(x+1.62,10,z+.65,.06,.75,.06,[83,111,125]);box(x+.56,10.84,z+.55,.64,.45,.055,rgb([46,77,93],[255,127,87],heat));box(x+.65,10.85,z+.22,.46,.025,.19,[139,166,172]);person(x+.87,z-.35,thermal,absorb,t,i);
}
// Integrated overhead thermal panels become visible after the thermal scan.
const panels=range(t,10,12)*(1-range(t,25,28));
if(panels>.001)for(const {x,z} of desks){box(x-.1,12.85,z-.4,2.05,.13,1.55,rgb([126,145,158],[235,136,98],absorb),panels*.82,color(cyan,.5));box(x+.06,12.82,z-.22,1.73,.025,1.2,[43,82,102],panels*.8)}
}
function effects(t,thermal,absorb,digital){
for(const {x,z} of desks){if(thermal>0){glow([x+.85,10.95,z],1.05,coral,thermal*(1-absorb*.75)*.38);glow([x+.7,12.88,z+.2],.9,warm,absorb*.28)}
if(t>11&&t<17.5){const a=range(t,11,12)*(1-range(t,16,17.5));beam([[x+.75,10.85,z+.22],[x+.9,11.6,z+.3],[x+.9,12.35,z+.3],[x+.7,12.87,z+.2]],t+x*.1,warm,a*.75,1.15)}
if(digital>0){const route=[[x+.75,12.94,z+.2],[x+.75,13.2,3.6],[5.6,13.2,3.6],[5.6,9,3.6]];line(route,color(cyan,.3*digital),1);for(let i=0;i<2;i++){const f=(t*.4+i*.5+(x+5)*.1)%1,seg=Math.min(2,Math.floor(f*3)),u=f*3-seg;glow(route[seg].map((v,j)=>mix(v,route[seg+1][j],u)),.14,cyan,digital)}}
}

}
function beam(points,t,c,alpha=1,width=2){
ctx.save();ctx.globalCompositeOperation='screen';
line(points,color(c,.08*alpha),width*10);line(points,color(c,.2*alpha),width*4);line(points,color(c,.85*alpha),width);line(points,'rgba(232,255,255,'+alpha*.85+')',Math.max(.5,width*.32));
const lengths=points.slice(1).map((p,i)=>Math.hypot(...sub(p,points[i]))),total=lengths.reduce((a,b)=>a+b,0);
for(let j=0;j<3;j++){let distance=((t*.23+j/3)%1)*total;for(let k=0;k<lengths.length;k++){if(distance<=lengths[k]){glow(points[k].map((v,i)=>mix(v,points[k+1][i],distance/lengths[k])),.3,c,alpha);break}distance-=lengths[k]}}
ctx.restore();
}
function powerGrid(t,alpha){if(alpha<=0)return;
for(let x=-22;x<=22;x+=4)line([[x,25,-22],[x,25,22]],color(cyan,.22*alpha),.8);
for(let z=-22;z<=22;z+=4)line([[-22,25,z],[22,25,z]],color(cyan,.22*alpha),.8);
for(let x=-22;x<=22;x+=4)for(let z=-22;z<=22;z+=4){glow([x,25,z],.14,cyan,alpha*.7);line([[x-.12,25,z],[x+.12,25,z]],color(cyan,alpha*.8),1)}
beam([[-22,25,-6],[-2,25,-6],[-2,25,2],[6.6,25,2],[6.6,1,2]],t,cyan,alpha,1.7);
}
function drawScene(t){
const close=range(t,8,10)*(1-range(t,16.5,19)),thermal=range(t,9,11)*(1-range(t,16,19)),absorb=range(t,11.5,16)*(1-range(t,25,28)),digital=range(t,16,19)*(1-range(t,26,29));
camera({x:mix(31,14,close),y:mix(27,19,close),z:mix(38,18,close),tx:0,ty:mix(11,11.3,close),tz:0,f:mix(1.32,1.42,close)});
city(t,.09);for(let i=0;i<6;i++){floorOffset=(i-3)*3.2;const start=faces.length;floor(t,1,thermal,absorb,digital);if(i!==3)for(let j=start;j<faces.length;j++)faces[j].alpha*=1-close}floorOffset=0;flush();
for(let i=0;i<6;i++){floorOffset=(i-3)*3.2;if(i===3||close<.3)effects(t,thermal,absorb,digital)}floorOffset=0;
const network=range(t,16,19)*(1-range(t,25,27));
for(let i=0;i<6;i++){const y=3.25+i*3.2;
beam([[-5.5,y,3.8],[0,y,3.8],[6.6,y,3.8],[6.6,21.5,3.8],[6.6,25,2]],t+i*.17,cyan,network*.8,1.4)}
powerGrid(t,(1-close*.88)*range(t,5,7)*(1-range(t,25,27)));
}
function photoScene(t){
if(!opening.complete||!opening.naturalWidth)return;
const end=range(t,25,29),intro=1-range(t,5.3,7),opacity=Math.max(intro,end);if(opacity<=0)return;
const zoom=range(t,1.8,6)*(1-end),scale=mix(1,3.9,zoom);
// Right-side blue glass tower, tracked in source-image coordinates.
const base=Math.min(w/opening.naturalWidth,h/opening.naturalHeight),iw=opening.naturalWidth*base*scale,ih=opening.naturalHeight*base*scale;
const ox=mix((w-iw)/2,w*.5-iw*.811,zoom),oy=mix((h-ih)/2,h*.53-ih*.60,zoom);
ctx.save();ctx.globalAlpha=opacity;ctx.fillStyle='#07131e';ctx.fillRect(0,0,w,h);ctx.drawImage(opening,ox,oy,iw,ih);
const blue=range(t,1.4,5)*(1-end);ctx.fillStyle='rgba(3,20,47,'+blue*.38+')';ctx.fillRect(0,0,w,h);
const select=range(t,2,3.3)*(1-range(t,6,7))*(1-end);
// Trace the photographed tower facade and each visible floor before cutaway.
ctx.strokeStyle=color(cyan,select*.7);ctx.shadowColor='#64e7ff';ctx.shadowBlur=6;ctx.lineWidth=1;
for(let i=0;i<29;i++){const v=i/29;ctx.beginPath();ctx.moveTo(ox+iw*.764,oy+ih*(.37+v*.59));ctx.lineTo(ox+iw*.855,oy+ih*(.335+v*.63));ctx.stroke()}
ctx.shadowBlur=0;
const gridAlpha=range(t,1,3)*(1-range(t,5,7))*(1-end);
ctx.save();ctx.globalCompositeOperation='screen';
function skyPoint(x,z){const dep=(z+1)/9;return [w*.5+x*w*(.11+dep*.055),h*(.015+Math.pow(dep,1.6)*.33)]}
ctx.strokeStyle=color(cyan,gridAlpha*.42);ctx.lineWidth=.7;
for(let i=-8;i<=8;i++){ctx.beginPath();for(let j=0;j<9;j++){const p=skyPoint(i,j);j?ctx.lineTo(...p):ctx.moveTo(...p)}ctx.stroke()}
for(let j=0;j<9;j++){ctx.beginPath();ctx.moveTo(...skyPoint(-8,j));ctx.lineTo(...skyPoint(8,j));ctx.stroke();for(let i=-8;i<=8;i++){const [x,y]=skyPoint(i,j);ctx.fillStyle=color([180,252,255],gridAlpha*.9);ctx.shadowBlur=8;ctx.shadowColor='#8af2ff';ctx.fillRect(x-1.1,y-1.1,2.2,2.2)}}ctx.shadowBlur=0;
// Luminous electricity ribbons across the city; thermal battery remains orange indoors.
for(let k=0;k<3;k++){ctx.beginPath();ctx.moveTo(-w*.1,h*(.83+k*.014));ctx.bezierCurveTo(w*.22,h*.48,w*.56,h*1.14,w*.86,h*.49);ctx.strokeStyle=color(cyan,gridAlpha*.15);ctx.lineWidth=12;ctx.stroke();ctx.strokeStyle=color([123,224,255],gridAlpha*.72);ctx.lineWidth=2.2;ctx.stroke();ctx.strokeStyle=color([239,253,255],gridAlpha*.8);ctx.lineWidth=.65;ctx.stroke()}
ctx.restore();ctx.restore();
}
function rounded(x,y,ww,hh,r,fill,stroke){ctx.beginPath();ctx.roundRect(x,y,ww,hh,r);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1;ctx.stroke()}}
function dashboard(t){const alpha=range(t,19,21)*(1-range(t,24,26));if(alpha<=0)return;ctx.save();ctx.globalAlpha=alpha;
// Architectural control-room alcove surrounding a panoramic, entirely unlabelled screen.
ctx.fillStyle='rgba(3,11,20,.91)';ctx.fillRect(0,0,w,h);
const ww=Math.min(w*.84,h*1.7),hh=ww*.49,x=(w-ww)/2,y=h*.46-hh/2;
ctx.strokeStyle='rgba(113,163,185,.18)';for(let k=0;k<8;k++){ctx.beginPath();ctx.moveTo(w/2,h*.5);ctx.lineTo(w*(k/7),h);ctx.stroke()}
rounded(x-ww*.025,y-hh*.06,ww*1.05,hh*1.13,10,'#122430','rgba(166,215,224,.25)');rounded(x,y,ww,hh,6,'#071622','rgba(113,226,237,.24)');
const sx=x+ww*.08,sy=y+hh*.2;
// Digital building model drawn as a perspective wireframe, not a text icon.
ctx.strokeStyle='rgba(108,222,231,.7)';ctx.lineWidth=1;
for(let j=0;j<9;j++){const yy=sy+j*hh*.065;ctx.beginPath();ctx.moveTo(sx,yy);ctx.lineTo(sx+ww*.13,yy+hh*.04);ctx.lineTo(sx+ww*.21,yy);ctx.lineTo(sx+ww*.08,yy-hh*.04);ctx.closePath();ctx.stroke()}
for(const [xx,yy] of [[sx,sy],[sx+ww*.13,sy+hh*.04],[sx+ww*.21,sy],[sx+ww*.08,sy-hh*.04]]){ctx.beginPath();ctx.moveTo(xx,yy);ctx.lineTo(xx,yy+hh*.52);ctx.stroke()}
// A familiar fan silhouette gives the adjacent curve an HVAC context without labels.
const fx=x+ww*.4,fy=y+hh*.26;ctx.strokeStyle='rgba(126,174,191,.65)';ctx.beginPath();ctx.arc(fx,fy,hh*.065,0,TAU);ctx.stroke();for(let i=0;i<3;i++){const a=t*.6+i*TAU/3;ctx.beginPath();ctx.ellipse(fx+Math.cos(a)*hh*.025,fy+Math.sin(a)*hh*.025,hh*.028,hh*.009,a,0,TAU);ctx.fillStyle='#69b4c3';ctx.fill()}
const gx=x+ww*.39,gy=y+hh*.81,gw=ww*.53,gh=hh*.4;
for(let k=0;k<4;k++){ctx.strokeStyle='rgba(119,162,184,.12)';ctx.beginPath();ctx.moveTo(gx,gy-k*gh/3);ctx.lineTo(gx+gw,gy-k*gh/3);ctx.stroke()}
for(let mode=0;mode<2;mode++){ctx.beginPath();for(let i=0;i<=100;i++){let u=i/100;const peak=Math.exp(-Math.pow((u-.57)/.16,2));const v=.15+Math.sin(u*9)*.045+peak*(mode?mix(.85,.37,range(t,20.7,23)):.85);const xx=gx+u*gw,yy=gy-v*gh;i?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy)}ctx.strokeStyle=mode?'#78e4e7':'rgba(237,149,137,.42)';ctx.lineWidth=mode?2.5:1.5;ctx.stroke()}
// Quiet status rings use geometry alone.
for(let j=0;j<3;j++){const xx=x+ww*(.57+j*.14),yy=y+hh*.23,r=hh*.055;ctx.strokeStyle='#203a49';ctx.lineWidth=3;ctx.beginPath();ctx.arc(xx,yy,r,0,TAU);ctx.stroke();ctx.strokeStyle='#7adbd9';ctx.beginPath();ctx.arc(xx,yy,r,-Math.PI/2,Math.PI*(.7+j*.25));ctx.stroke()}
// Console and operator establish a physical central control room.
ctx.fillStyle='#1c3441';ctx.beginPath();ctx.moveTo(x+ww*.12,y+hh*1.18);ctx.lineTo(x+ww*.85,y+hh*1.18);ctx.lineTo(x+ww*.96,h);ctx.lineTo(x+ww*.02,h);ctx.fill();
ctx.fillStyle='#08111c';ctx.beginPath();ctx.ellipse(w*.51,h*.92,ww*.044,hh*.11,0,0,TAU);ctx.fill();ctx.beginPath();ctx.arc(w*.51,h*.83,hh*.045,0,TAU);ctx.fill();ctx.restore()}
function render(t){backdrop(t);drawScene(t);dashboard(t);photoScene(t);const vignette=ctx.createRadialGradient(w*.5,h*.46,h*.2,w*.5,h*.5,Math.max(w,h)*.72);vignette.addColorStop(0,'rgba(1,8,17,0)');vignette.addColorStop(1,'rgba(1,8,17,'+(.65*range(t,4,7)*(1-range(t,25,29)))+')');ctx.fillStyle=vignette;ctx.fillRect(0,0,w,h)}
function resize(){w=canvas.clientWidth;h=canvas.clientHeight;dpr=Math.min(devicePixelRatio||1,1.6);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);render(time)}
const params=new URLSearchParams(location.search);if(params.has('t')){time=Number(params.get('t'))||0;playing=false}if(reduced.matches){time=7.5;playing=false}
function tick(now){const dt=Math.min((now-last)/1000,.08);last=now;if(playing&&visible){time=(time+dt)%duration;render(time)}requestAnimationFrame(tick)}
window.heroAnimation={seek(t){time=((t%duration)+duration)%duration;render(time)},play(){playing=true},pause(){playing=false},get time(){return time},duration};
window.addEventListener('resize',resize);document.addEventListener('visibilitychange',()=>{visible=!document.hidden;last=performance.now()});
window.addEventListener('message',e=>{if(e.origin!==location.origin)return;if(e.data?.type==='hero-visible')visible=e.data.visible});
reduced.addEventListener('change',()=>{playing=!reduced.matches;if(!playing){time=7.5;render(time)}});
opening.onload=()=>render(time);resize();requestAnimationFrame(tick);
})();
