/** Original seamless profile animation. Source artwork: built-in image_gen.
 * Usage: node tools/build_orbit_gif.cjs --sharp <installed sharp module path>
 * No network requests; fonts use the local Segoe UI / Arial installation.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const sharpPath = process.argv[process.argv.indexOf('--sharp') + 1];
if (!sharpPath || sharpPath === process.argv[0]) throw new Error('Supply --sharp module path');
const sharp = require(sharpPath);
const out = path.resolve(__dirname, '../assets/career-v5');
const W = 900, H = 353, N = 96, DELAY = 100;
const tau = Math.PI * 2;

function text(x,y,value,size=18,fill='#d6dde6',extra='') {
  return `<text x="${x}" y="${y}" font-family="Segoe UI,Arial,sans-serif" font-size="${size}" fill="${fill}" ${extra}>${value}</text>`;
}
function starField(phase) {
  let s='';
  for (let i=0;i<84;i++) {
    const x=(i*193+419)%1180+10, y=(i*79+11)%440+12;
    const fade=x<560 ? .23 : .7;
    const alpha=fade*(.45+.25*Math.sin(phase+(i*2.39996)));
    s+=`<circle cx="${x}" cy="${y}" r="${i%9===0?1.5:.65}" opacity="${alpha.toFixed(3)}" fill="#dce9f5"/>`;
  }
  return s;
}
function orbitPoint(phase) {
  const a=phase-.35, x=870+269*Math.cos(a),y=275+100*Math.sin(a);
  const angle=-21*Math.PI/180,dx=x-870,dy=y-275;
  return {x:870+dx*Math.cos(angle)-dy*Math.sin(angle),y:275+dx*Math.sin(angle)+dy*Math.cos(angle)};
}
function frame(phase,astronaut) {
  let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 1200 470"><defs>
    <radialGradient id="space"><stop stop-color="#19232d"/><stop offset=".6" stop-color="#0d131b"/><stop offset="1" stop-color="#070b10"/></radialGradient>
    <radialGradient id="planet" cx=".27" cy=".1" r=".83"><stop stop-color="#596573"/><stop offset=".12" stop-color="#222d39"/><stop offset=".5" stop-color="#101821"/><stop offset="1" stop-color="#05090e"/></radialGradient>
    <linearGradient id="rim"><stop stop-color="#dbe8f2" stop-opacity=".7"/><stop offset=".5" stop-color="#8ba0b2" stop-opacity=".2"/><stop offset="1" stop-color="#627a92" stop-opacity="0"/></linearGradient>
    <linearGradient id="metal"><stop stop-color="#f2f5f7"/><stop offset=".55" stop-color="#b9c4ce"/><stop offset="1" stop-color="#f8f9fa"/></linearGradient>
    <linearGradient id="fade"><stop stop-color="#070b10"/><stop offset=".55" stop-color="#070b10" stop-opacity=".4"/><stop offset="1" stop-color="#070b10" stop-opacity="0"/></linearGradient>
    <radialGradient id="halo"><stop stop-color="#cadceb" stop-opacity=".18"/><stop offset="1" stop-color="#cadceb" stop-opacity="0"/></radialGradient>
    <clipPath id="clip"><rect width="1200" height="470" rx="18"/></clipPath>
  </defs><g clip-path="url(#clip)"><rect width="1200" height="470" fill="#070b10"/>
  <ellipse cx="885" cy="230" rx="520" ry="410" fill="url(#space)"/>${starField(phase)}
  <circle cx="1112" cy="607" r="292" fill="url(#planet)"/>
  <path d="M822 576A292 292 0 0 1 1189 326" fill="none" stroke="url(#rim)" stroke-width="2.2"/>
  <path d="M836 579A279 279 0 0 1 1185 340" fill="none" stroke="#758a9c" stroke-opacity=".11"/>
  <g transform="rotate(-21 870 275)"><ellipse cx="870" cy="275" rx="269" ry="100" fill="none" stroke="#a2b1bf" stroke-opacity=".3"/><ellipse cx="870" cy="275" rx="281" ry="108" fill="none" stroke="#9aaab9" stroke-opacity=".09"/></g>`;
  const p=orbitPoint(phase);
  s+=`<circle cx="${p.x}" cy="${p.y}" r="19" fill="url(#halo)"/><circle cx="${p.x}" cy="${p.y}" r="2.4" fill="#eef4f9"/>`;
  const dx=10*Math.sin(phase),dy=20*Math.cos(phase),rot=4.8*Math.sin(phase);
  s+=`<g transform="translate(${dx.toFixed(2)} ${dy.toFixed(2)}) rotate(${rot.toFixed(2)} 899 224)"><image href="data:image/png;base64,${astronaut}" x="621" y="56" width="555" height="370"/></g>`;
  s+=`<rect x="0" width="620" height="470" fill="url(#fade)"/>
  ${text(57,90,'DENIS / GALAXY',15,'#8e9caa','letter-spacing="4"')}
  ${text(53,206,'DENIS BM',72,'url(#metal)','font-weight="300" letter-spacing="7"')}
  ${text(58,254,'PYTHON AUTOMATION',23,'#e0e6eb','font-weight="400" letter-spacing="4.5"')}
  ${text(58,293,'API INTEGRATIONS · AI TOOLS',15,'#aab7c4','letter-spacing="1.6"')}
  <path d="M58 332H128" stroke="#bac6d0" stroke-opacity=".65"/>
  ${text(58,374,'REMOTE · UP TO 25 HOURS A WEEK',13,'#8493a3','letter-spacing="2.1"')}
  <rect x=".7" y=".7" width="1198.6" height="468.6" rx="18" fill="none" stroke="#697b8c" stroke-opacity=".22"/>
  </g></svg>`;
  return Buffer.from(s);
}
async function main() {
  const astronaut=await fs.readFile(path.join(out,'astronaut-source.png'));
  const embedded=(await sharp(astronaut).resize({width:920}).png().toBuffer()).toString('base64');
  const frames=[];
  for(let i=0;i<N;i++) {
    const svg=frame(tau*i/N,embedded);
    if(i===0) await sharp(svg).png().toFile(path.join(out,'hero-poster.png'));
    frames.push(await sharp(svg).removeAlpha().raw().toBuffer());
    if((i+1)%24===0) console.log(`Rendered ${i+1}/${N} frames`);
  }
  const raw=Buffer.concat(frames);
  await sharp(raw,{raw:{width:W,height:H*N,channels:3,pageHeight:H}})
    .gif({loop:0,delay:Array(N).fill(DELAY),colours:128,effort:8,dither:.05,interFrameMaxError:4,interPaletteMaxError:8})
    .toFile(path.join(out,'galaxy-orbit.gif'));
  const meta=await sharp(path.join(out,'galaxy-orbit.gif'),{animated:true}).metadata();
  if(meta.pages!==N || meta.loop!==0) throw new Error('Animation export incomplete');
  const size=(await fs.stat(path.join(out,'galaxy-orbit.gif'))).size;
  console.log(JSON.stringify({width:meta.width,pageHeight:meta.pageHeight,frames:meta.pages,durationMs:meta.delay.reduce((a,b)=>a+b,0),bytes:size}));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
