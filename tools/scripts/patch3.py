import json,re
s=open('tpl2.html').read()
objs=json.load(open('objs3.json'))
remap={'p_int':'rel_int','p_per':'rel_per','p_ext':'rel_ext','z_per':'rel_per','z_ext':'rel_ext'}
for o in objs:o['cat']=remap.get(o['cat'],o['cat'])
src={o['id']:o.pop('src') for o in objs}
def R(a,b,cnt=1):
  global s
  assert s.count(a)>=1,('missing',a[:60])
  s=s.replace(a,b,cnt)
# --- CATS with sections
R("""const CATS=[""","""const SECS=['costa','rios','rel'];
const CATS=[""")
R(""" {id:'can',ru:'Канарские о-ва',es:'Canarias'}];""",""" {id:'can',ru:'Канарские о-ва',es:'Canarias'},
 {id:'r_gal',sec:'rios',ru:'Галисийские',es:'Gallegos'},{id:'r_can',sec:'rios',ru:'Кантабрийские',es:'Cantábricos'},
 {id:'r_duero',sec:'rios',ru:'Бассейн Дуэро',es:'Cuenca del Duero'},{id:'r_tajo',sec:'rios',ru:'Бассейн Тахо',es:'Cuenca del Tajo'},
 {id:'r_guadiana',sec:'rios',ru:'Бассейн Гвадианы',es:'Cuenca del Guadiana'},{id:'r_gq',sec:'rios',ru:'Бассейн Гвадалквивира',es:'Cuenca del Guadalquivir'},
 {id:'r_ebro',sec:'rios',ru:'Бассейн Эбро',es:'Cuenca del Ebro'},{id:'r_med',sec:'rios',ru:'Средиземноморские',es:'Mediterráneos'},
 {id:'rel_int',sec:'rel',ru:'Внутренние кордильеры',es:'Cordilleras interiores'},{id:'rel_per',sec:'rel',ru:'Периферийные',es:'Cordilleras periféricas'},
 {id:'rel_ext',sec:'rel',ru:'Внешние',es:'Cordilleras exteriores'}];
CATS.forEach(c=>c.sec=c.sec||'costa');
const CSEC=Object.fromEntries(CATS.map(c=>[c.id,c.sec]));""")
# --- extra objects
R("""const SIDE={""","""const O2="""+json.dumps(objs,ensure_ascii=False,separators=(',',':'))+""";
O.push(...O2);
Object.assign(SRC,"""+json.dumps(src,ensure_ascii=False)+""");
const SIDE={""")
R("""O.forEach(o=>o.side=SIDE[o.id]||(o.kind==='pt'||o.kind==='isl'?'r':'c'));""","""O.forEach(o=>o.side=SIDE[o.id]||(o.kind==='pt'||o.kind==='isl'||o.kind==='peak'?'r':'c'));""")
# --- texts
R("""modes:['Изучать','Найти','Что это?','Экзамен','Успехи'],""","""modes:['Изучать','Найти','Что это?','Экзамен','Успехи','Притоки'],secs:['Побережье','Реки','Рельеф'],der:'правый берег',izq:'левый берег',tribq:'Чей это приток и с какого берега?',tribof:'Приток:',notrib:'В выбранных группах нет притоков с указанным берегом',""")
R("""modes:['Estudiar','Localizar','¿Qué es?','Examen','Progreso'],""","""modes:['Estudiar','Localizar','¿Qué es?','Examen','Progreso','Afluentes'],secs:['Costas','Ríos','Relieve'],der:'margen derecha',izq:'margen izquierda',tribq:'¿De qué río es afluente y por qué margen?',tribof:'Afluente de:',notrib:'No hay afluentes con margen en estos grupos',""")
# --- state
R("""let S={lang:LS.get('lang','ru'),mode:'study',""","""let S={sec:LS.get('sec','costa'),lang:LS.get('lang','ru'),mode:'study',""")
R("""cats:LS.get('cats',CATS.map(c=>c.id))""","""cats:(()=>{const c=LS.get('cats2',null);return c||CATS.map(c=>c.id)})()""")
s=s.replace("LS.set('cats',S.cats)","LS.set('cats2',S.cats)")
# hidden zone paths for hit tests
R("""const ISL={};""","""const ZP={};const zh=el('g',{visibility:'hidden'},base);
for(const o of O.filter(o=>o.kind==='zone'))ZP[o.id]=el('path',{d:o.d},zh);
const ISL={};""")
# --- active & draw
R("""function active(){return O.filter(o=>S.cats.includes(o.cat))}""","""function inSec(o){return CSEC[o.cat]===S.sec}
function active(){return O.filter(o=>inSec(o)&&S.cats.includes(o.cat))}
const lineD=o=>o.lines.map(l=>'M'+l.map(p=>p.join(',')).join('L')).join('');""")
R("""function drawMarks(){marks.innerHTML='';labels.innerHTML='';if(S.mode==='exam')return;
 for(const o of O){if(!S.cats.includes(o.cat))continue;""","""function drawMarks(){marks.innerHTML='';labels.innerHTML='';
 if(S.mode==='exam'&&S.sec!=='rios')return;
 if(S.sec==='rios')for(const o of O)if(o.kind==='line'&&inSec(o))el('path',{d:lineD(o),class:'riv'+(o.parent?'':' main')+(S.cats.includes(o.cat)?'':' dim')},marks);
 if(S.mode==='exam')return;
 for(const o of O){if(!inSec(o)||!S.cats.includes(o.cat))continue;
  if(o.kind==='zone')el('path',{d:o.d,class:'zone'},marks);
  if(o.kind==='peak'){const[x,y]=o.xy[0];el('path',{class:'peak','data-x':x,'data-y':y},marks)}""")
R("""const lb=el('text',{x,y,class:'lbl'+(big?' big':''),""","""const lb=el('text',{x,y,class:'lbl'+(big||o.kind==='zone'?' big':'')+(o.kind==='line'?' rlbl':''),""")
R("""lb.textContent=o.kind==='isl'||big?o.name:o.short}}""","""lb.textContent=o.kind==='isl'||big||o.kind==='zone'?o.name:o.short}}""")
R("""function scaleUI(){const k=u(1);""","""function scaleUI(){const k=u(1);
 marks.querySelectorAll('.peak').forEach(p=>{const x=+p.dataset.x,y=+p.dataset.y,r=6*Math.max(k,.35);p.setAttribute('d',`M${x},${y-r}L${x+r*.9},${y+r*.6}L${x-r*.9},${y+r*.6}Z`)});""")
# --- geometry
R("""function dist(o,x,y){if(o.kind==='isl'&&inIsland(o.id,x,y))return 0;""","""function inPath(p,x,y){try{return p.isPointInFill(new DOMPoint(x,y))}catch(e){try{const q=svg.createSVGPoint();q.x=x;q.y=y;return p.isPointInFill(q)}catch(e2){return false}}}
function segNear(x,y,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],L=dx*dx+dy*dy;let t=L?((x-a[0])*dx+(y-a[1])*dy)/L:0;t=Math.max(0,Math.min(1,t));return[a[0]+t*dx,a[1]+t*dy]}
function nearPt(o,x,y){let best=o.xy[0],bd=1e9;
 if(o.kind==='line'){for(const l of o.lines)for(let i=1;i<l.length;i++){const p=segNear(x,y,l[i-1],l[i]),d=Math.hypot(p[0]-x,p[1]-y);if(d<bd){bd=d;best=p}}return best}
 for(const p of o.xy){const d=Math.hypot(p[0]-x,p[1]-y);if(d<bd){bd=d;best=p}}return best}
function dist(o,x,y){if(o.kind==='isl'&&inIsland(o.id,x,y))return 0;
 if(o.kind==='zone')return inPath(ZP[o.id],x,y)?0:Math.max(0,Math.hypot(o.xy[0][0]-x,o.xy[0][1]-y)-40);
 if(o.kind==='line'){const p=nearPt(o,x,y);return Math.hypot(p[0]-x,p[1]-y)}""")
# --- effects
R("""function clearFx(){fx.innerHTML='';""","""function clearFx(){fx.innerHTML='';fxl.innerHTML='';""")
R("""const marks=$('#marks'),labels=$('#labels'),fx=$('#fx');""","""const marks=$('#marks'),labels=$('#labels'),fx=$('#fx'),fxl=$('#fxl');""")
R("""<g id="marks"></g>""","""<g id="fxl"></g><g id="marks"></g>""")
R("""function highlight(o,cls='pulse'){if(o.kind==='isl'){ISL[o.id].classList.add(cls==='ok'?'ok':'hi')}""","""function highlight(o,cls='pulse'){if(o.kind==='isl'){ISL[o.id].classList.add(cls==='ok'?'ok':'hi')}
 if(o.kind==='line'){el('path',{d:lineD(o),class:'rivhi '+cls},fxl);return}
 if(o.kind==='zone'){el('path',{d:o.d,class:'zonehi '+cls},fxl);return}""")
R("""function markTap(x,y,o){const[ax,ay]=o.xy.reduce((b,p)=>Math.hypot(p[0]-x,p[1]-y)<Math.hypot(b[0]-x,b[1]-y)?p:b);""","""function markTap(x,y,o){const[ax,ay]=nearPt(o,x,y);""")
# --- chrome
R(""" $('#ttl').innerHTML=`${t('ttl')}<small>${t('sub')}</small>`;""",""" $('#ttl').innerHTML=`${t('ttl')}<small>${t('secs')[SECS.indexOf(S.sec)]}</small>`;
 $('#secs').innerHTML=SECS.map((x,i)=>`<button data-s="${x}" aria-pressed="${S.sec===x}">${t('secs')[i]}</button>`).join('');""")
R(""" const modes=['study','find','what','exam','prog'];""",""" const modes=['study','find','what','exam','prog'];if(S.sec==='rios')modes.splice(3,0,'trib');
 $('#modes').style.gridTemplateColumns=`repeat(${modes.length},1fr)`;""")
R("""modes.map((m,i)=>`<button data-m="${m}" aria-pressed="${S.mode===m}">${t('modes')[i]}</button>`)""","""modes.map(m=>`<button data-m="${m}" aria-pressed="${S.mode===m}">${t('modes')[['study','find','what','exam','prog','trib'].indexOf(m)]}</button>`)""")
R("""$('#cats').innerHTML=CATS.map(""","""$('#cats').innerHTML=CATS.filter(c=>c.sec===S.sec).map(""")
R("""$('#modes').onclick=e=>{const m=e.target.dataset.m;if(m)go(m)};""","""$('#modes').onclick=e=>{const m=e.target.dataset.m;if(m)go(m)};
$('#secs').onclick=e=>{const x=e.target.dataset.s;if(!x||x===S.sec)return;S.sec=x;LS.set('sec',x);cur=null;if(S.mode==='trib'&&x!=='rios')S.mode='study';go(S.mode)};""")
R("""<div class="controls"><div class="modes" id="modes"></div>""","""<div class="controls"><div class="secs" id="secs" role="group"></div><div class="modes" id="modes"></div>""")
R(""" ({study,find,what,exam:examIntro,prog})[m]()}""",""" ({study,find,what,exam:examIntro,prog,trib})[m]()}""")
# study card: tributary info
R("""<p class="sub">${o.ru}</p><p class="src">""","""<p class="sub">${o.ru}${o.parent?`<br>${t('tribof')} ${BY[o.parent].name}${o.side?', '+t(o.side==='D'?'der':'izq'):''}`:''}</p><p class="src">""")
# prog only section cats
R("""function prog(){const rows=CATS.map(""","""function prog(){const rows=CATS.filter(c=>c.sec===S.sec).map(""")
R("""const weak=O.filter(o=>box""","""const weak=O.filter(o=>inSec(o)&&box""")
# trib mode
R("""function examIntro(){""","""function trib(){clearFx();const pool=active().filter(o=>o.parent&&o.side);if(!pool.length){h(`<p class="sub">${t('notrib')}</p>`);return}
 cur=pick(pool,cur&&cur.id);highlight(cur);let done=false;
 const lab=(p,sd)=>`${BY[p].short}, ${t(sd==='D'?'der':'izq')}`;
 const parents=[...new Set(O.filter(o=>o.parent&&o.side).map(o=>o.parent))].filter(p=>p!==cur.parent).sort(()=>Math.random()-.5);
 const opts=[[cur.parent,cur.side],[cur.parent,cur.side==='D'?'I':'D'],...parents.slice(0,2).map(p=>[p,Math.random()<.5?'D':'I'])].sort(()=>Math.random()-.5);
 h(`<p class="prompt">${t('tribq')} ${scoreLine()}</p><p class="target">${cur.name}</p><div class="opts">${opts.map(([p,sd])=>`<button data-k="${p}|${sd}">${lab(p,sd)}</button>`).join('')}</div>`);
 panel.querySelector('.opts').onclick=e=>{const k=e.target.dataset.k;if(!k||done)return;done=true;const ok=k===cur.parent+'|'+cur.side;streak.n++;if(ok)streak.ok++;grade(cur,ok);
  panel.querySelectorAll('.opts button').forEach(b=>{if(b.dataset.k===cur.parent+'|'+cur.side)b.classList.add('ok');else if(b.dataset.k===k)b.classList.add('bad')});
  clearFx();highlight(BY[cur.parent],'pulse');highlight(cur,'ok');panel.querySelector('.score').textContent=`${streak.ok} / ${streak.n}`;setTimeout(()=>S.mode==='trib'&&trib(),ok?1100:2400)}}
function examIntro(){""")
# CSS
R(""".modes{display:grid;grid-template-columns:repeat(5,1fr);""",""".secs{display:flex;gap:6px}
.secs button{flex:1;border:1.5px solid var(--ink);background:none;border-radius:12px;padding:7px 4px;font-weight:700;cursor:pointer;font-size:.9rem}
.secs button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
.modes{display:grid;grid-template-columns:repeat(5,1fr);""")
R(""".ring{fill:none;""",""".riv{fill:none;stroke:#3d86b8;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.riv.main{stroke-width:2.6}.riv.dim{stroke-opacity:.35}
.rivhi{fill:none;stroke:var(--hi);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;stroke-opacity:.9}
.rivhi.ok{stroke:var(--ok)}
.zone{fill:#b08a5a;fill-opacity:.18;stroke:#8a6a40;stroke-opacity:.5;stroke-width:1;stroke-dasharray:4 3;vector-effect:non-scaling-stroke}
.zonehi{fill:var(--hi);fill-opacity:.45;stroke:var(--hi);stroke-width:2;vector-effect:non-scaling-stroke}.zonehi.ok{fill:var(--ok);stroke:var(--ok)}
.peak{fill:#7a5530;stroke:var(--land);stroke-width:1;vector-effect:non-scaling-stroke}
.lbl.rlbl{fill:#2a6f9e;font-style:italic}
.ring{fill:none;""")
s=s.replace(".modes button{border:0;background:none;padding:8px 2px;border-radius:10px;font-size:.85rem;",".modes button{border:0;background:none;padding:8px 2px;border-radius:10px;font-size:.82rem;")
open('tpl3.html','w').write(s)
open('/mnt/user-data/outputs/mapa-mudo-espana.html','w').write(s.replace('__GEO__',open('geo2.json').read()))
print('ok',len(s))
