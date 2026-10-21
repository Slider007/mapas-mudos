import base64,json
s=open('tpl9.html').read()
def R(a,b,n=1):
  global s;assert s.count(a)==n,(s.count(a),a[:70]);s=s.replace(a,b)
R("modes:['Изучать','Найти','Что это?','Экзамен','Успехи','Притоки'],","modes:['Изучать','Найти','Что это?','Экзамен','Успехи','Притоки','Карточки','Цепочка'],cardq:'Вспомни название и переверни карточку',knew:'Знал',didnt:'Не знал',flip:'Показать ответ',chainq:'Найди по порядку',restart:'Сначала',chaindone:'Цепочка пройдена!',hint:'Подсказка',weakbtn:'Тренировать ошибки',noweak:'Ошибок нет: повторять нечего',")
R("modes:['Estudiar','Localizar','¿Qué es?','Examen','Progreso','Afluentes'],","modes:['Estudiar','Localizar','¿Qué es?','Examen','Progreso','Afluentes','Tarjetas','Cadena'],cardq:'Recuerda el nombre y gira la tarjeta',knew:'Lo sabía',didnt:'No lo sabía',flip:'Ver respuesta',chainq:'Localiza en orden',restart:'Desde el principio',chaindone:'¡Cadena completada!',hint:'Pista',weakbtn:'Repasar errores',noweak:'No hay errores que repasar',")
R("const modes=['study','find','what','exam','prog'];if(S.sec==='rios')modes.splice(3,0,'trib');","const modes=['study','cards','find','what','chain','exam','prog'];if(S.sec==='rios')modes.splice(5,0,'trib');")
R("t('modes')[['study','find','what','exam','prog','trib'].indexOf(m)]","t('modes')[['study','find','what','exam','prog','trib','cards','chain'].indexOf(m)]")
R("({study,find,what,exam:examIntro,prog,trib})[m]()}","({study,find,what,exam:examIntro,prog,trib,cards,chain,weak:()=>{if(!curPool().length){h(`<p class=\"sub\">${t('noweak')}</p>`);return}find()}})[m]()}")
R("function find(){clearFx();cur=pick(active(),cur&&cur.id);let done=false;","function curPool(){return S.mode==='weak'?active().filter(o=>box[o.id]!==undefined&&(box[o.id]||0)<2):active()}\nfunction find(){clearFx();const pool=curPool();if(!pool.length){h(`<p class=\"sub\">${t('noweak')}</p>`);return}cur=pick(pool,cur&&cur.id);let done=false;")
R("""  $('#fb').innerHTML=ok?`<p class="fb ok">${t('ok')}</p>`:`<p class="fb bad">${o&&dist(o,x,y)<u(30)&&o!==cur?t('bad')+o.name:t('far')}</p><div class="row"><button class="btn" id="nx">${t('next')}</button></div>`;""",
"""  $('#fb').innerHTML=ok?`<p class="fb ok">${t('ok')}</p>`:`<p class="fb bad">${o&&dist(o,x,y)<u(30)&&o!==cur?t('bad')+o.name:t('far')}</p>${hintHtml(cur)}<div class="row"><button class="btn" id="nx">${t('next')}</button></div>`;""")
R("if(ok)setTimeout(()=>S.mode==='find'&&find(),1100);else $('#nx').onclick=find}}","if(ok)setTimeout(()=>(S.mode==='find'||S.mode==='weak')&&find(),1100);else $('#nx').onclick=find}}")
# study card hint
R("""<p class="src">${t('srcl')}: ${SRC[o.id]||''}</p>
  <div class="row"><button class="btn ghost" id="say">""","""${hintHtml(o)}<p class="src">${t('srcl')}: ${SRC[o.id]||''}</p>
  <div class="row"><button class="btn ghost" id="say">""")
# prog weak button
R("""<div class="row"><button class="btn ghost" id="rs">${t('reset')}</button></div>`);
 $('#rs').onclick=""","""<div class="row">${weak.length?`<button class="btn" id="wk">${t('weakbtn')} (${weak.length})</button>`:''}<button class="btn ghost" id="rs">${t('reset')}</button></div>`);
 if($('#wk'))$('#wk').onclick=()=>go('weak');
 $('#rs').onclick=""")
# new modes + hints + sequences
SEQ={'costa':'vizc machi ajo cant penas bares orte prior touri finis atl cadiz tarifa gibr med alme gata mazar palos alic nao valen jorge roses creus leon mallorca menorca ibiza formentera cabrera lanzarote fuerteventura gran_canaria tenerife la_gomera la_palma el_hierro',
 'rios':'mino sil ulla tambre eo navia nalon narcea besaya nervion bidasoa duero pisuerga arlanzon carrion esla bernesga eresma adaja tormes tajo jarama henares alberche tietar alagon almonte salor guadiana zancara ciguela jabalon zujar matachel guadalquivir guadalimar jandula guadalmellato guadiato bembezar viar guadianamenor guadalbullon genil odiel tinto guadalete barbate ter llobregat ebro jalon jiloca huerva guadalope arga aragon gallego cinca noguerapallaresa nogueraribagorzana segre mijares turia jucar cabriel segura almanzora andarax adra guadalfeo guadalhorce guadiaro',
 'rel':'meseta subnorte subsur sistemacentral somosierra guadarrama gredos almanzor gata_s estrella montestoledo guadalupe montanchez sanpedro montesleon teleno cantabrica ubina picoseuropa cerredo prieta iberico demanda urbion moncayo gudar javalambre maestrazgo albarracin universales cuenca morena aracena madrona alcaraz almenara galaico manzaneda vascos gorbea pirineos aneto perdido costerocat montseny montserrat montsant penibetica grazalema ronda torrecilla nevada mulhacen veleta filabres calaralto subbetica magina cazorla segura_s sagra tramuntana puigmajor levante teide'}
SEQ={k:v.split() for k,v in SEQ.items()}
HINT={'bares':'самая северная точка Испании','touri':'самая западная точка материковой Испании','tarifa':'самая южная точка материковой Испании',
 'gata':'юго-восточный «угол» полуострова; рядом Golfo de Almería','creus':'самая восточная точка; разделяет Golfo de Roses и Golfo de León',
 'finis':'чуть южнее Туриньяна; «край земли» паломников','orte':'западнее Estaca de Bares, почти рядом',
 'mulhacen':'высшая точка Пиренейского полуострова (Сьерра-Невада)','teide':'высшая точка Испании (Тенерифе)','aneto':'высшая точка Пиренеев',
 'cerredo':'высшая точка Кантабрийских гор (Пикос-де-Эуропа)','almanzor':'высшая точка Системы Сентраль (Гредос)','moncayo':'высшая точка Иберийской системы',
 'sil':'Сил течёт к Миньо','narcea':'Нарсеа — приток Налона','arlanzon':'Арлансон → Арланса → Писуэрга → Дуэро','bernesga':'Бернесга → Эсла → Дуэро',
 'eresma':'Эресма → Адаха → Дуэро','henares':'Энарес → Харама → Тахо','zancara':'Санкара → Сигуэла → Гвадиана','jiloca':'Хилока → Халон → Эбро',
 'arga':'Арга → Арагон → Эбро','cinca':'Синка → Сегре → Эбро','noguerapallaresa':'обе Ногеры → Сегре → Эбро','nogueraribagorzana':'обе Ногеры → Сегре → Эбро','cabriel':'Кабриэль → Хукар',
 'meseta':'Система Сентраль делит её на Северную и Южную субмесеты','subnorte':'долина Дуэро','subsur':'долины Тахо и Гвадианы',
 'montestoledo':'делят Южную субмесету: Тахо к северу, Гвадиана к югу'}
FROM={'duero':{'D':'с севера, с Кантабрийских и Леонских гор','I':'с юга, с Системы Сентраль'},'tajo':{'D':'с севера, с Системы Сентраль','I':'с юга, с Монтес-де-Толедо'},
 'guadiana':{'D':'с севера','I':'с юга, со стороны Сьерра-Морены'},'guadalquivir':{'D':'с севера, со Сьерра-Морены','I':'с юга, с Бетических кордильер'},'ebro':{'D':'с юга, с Иберийской системы','I':'с севера, с Пиренеев'}}
js="""
const SEQ="""+json.dumps(SEQ)+""";const HINT="""+json.dumps(HINT,ensure_ascii=False)+""";const FROM="""+json.dumps(FROM,ensure_ascii=False)+""";
function hintText(o){const a=[];if(HINT[o.id])a.push(HINT[o.id]);if(o.bank&&FROM[o.parent])a.push((o.bank==='D'?'правый':'левый')+' приток: течёт '+FROM[o.parent][o.bank]);return a.join('. ')}
function hintHtml(o){const h=hintText(o);return h&&S.lang==='ru'?`<p class="hint">💡 ${h}</p>`:''}
function cards(){clearFx();const pool=active();if(!pool.length)return;cur=pick(pool,cur&&cur.id);highlight(cur);let shown=false;
 h(`<p class="prompt">${t('cardq')} ${scoreLine()}</p><button class="card" id="cd"><span class="cq">?</span><span class="sub">${t('flip')}</span></button><div class="row" id="cr"></div>`);
 $('#cd').onclick=()=>{if(shown)return;shown=true;$('#cd').innerHTML=`<span class="target">${cur.name}</span><span class="sub">${cur.ru}</span>${hintHtml(cur)}`;speak(cur.name);
  $('#cr').innerHTML=`<button class="btn" id="kn">✓ ${t('knew')}</button><button class="btn ghost" id="nk">✗ ${t('didnt')}</button>`;
  $('#kn').onclick=()=>{streak.n++;streak.ok++;grade(cur,true);cards()};$('#nk').onclick=()=>{streak.n++;grade(cur,false);cards()}};
 tapHandler=null}
let chainI={};
function chain(){clearFx();const act=new Set(active().map(o=>o.id));const seq=(SEQ[S.sec]||[]).filter(id=>BY[id]&&act.has(id));if(!seq.length){h(`<p class="sub">${t('none')}</p>`);return}
 const key=S.sec+'|'+seq.join(',');let i=chainI[key]||0;
 if(i>=seq.length){h(`<p class="target">${t('chaindone')}</p><div class="row"><button class="btn" id="rst">${t('restart')}</button></div>`);for(const id of seq)highlight(BY[id],'ok');$('#rst').onclick=()=>{chainI[key]=0;chain()};return}
 for(let k=0;k<i;k++)highlight(BY[seq[k]],'ok');
 const q=BY[seq[i]];let done=false;
 h(`<p class="prompt">${t('chainq')}: ${i+1} / ${seq.length} <span class="score">${streak.ok} / ${streak.n}</span></p><p class="target">${q.name}</p><div id="fb"></div><div class="row"><button class="btn ghost" id="rst">${t('restart')}</button></div>`);
 $('#rst').onclick=()=>{chainI[key]=0;chain()};
 tapHandler=(x,y)=>{if(done)return;done=true;const[o]=nearest(x,y,O.filter(inSec));const dt=dist(q,x,y);const ok=(o===q&&dt<u(140))||dt<6||own(q,x,y);
  if(o&&dist(o,x,y)<u(40))flash(o,ok?'ok':'bad');streak.n++;if(ok)streak.ok++;grade(q,ok);
  if(ok){chainI[key]=i+1;setTimeout(()=>S.mode==='chain'&&chain(),700)}
  else{highlight(q,'pulse');tagName(q);markTap(x,y,q);$('#fb').innerHTML=`<p class="fb bad">${t('far')}</p>${hintHtml(q)}<div class="row"><button class="btn" id="nx">${t('next')}</button></div>`;
   $('#nx').onclick=()=>{chainI[key]=i+1;chain()}}}}
"""
R("function examIntro(){",js+"function examIntro(){")
R(""".cgrp{""",""".card{width:100%;min-height:96px;margin-top:8px;border:1.5px solid var(--sea2);border-radius:16px;background:var(--panel);color:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;padding:12px}
.cq{font-size:2.4rem;font-weight:800;color:var(--ink2);line-height:1}
.hint{font-size:.88rem;margin:6px 0 0;padding:6px 10px;border-radius:10px;background:color-mix(in srgb,var(--hi) 18%,var(--panel));color:var(--ink)}
.cgrp{""")
open('tpl10.html','w').write(s)
e=lambda f:base64.b64encode(open(f,'rb').read()).decode()
open('/mnt/user-data/outputs/mapa-mudo-espana.html','w').write(s.replace('__GEO__',open('geo2.json').read()).replace('__HYPM__',e('hyp_main_e.jpg')).replace('__HYPC__',e('hyp_can_e.jpg')).replace('__GRYM__',e('gray_main.jpg')).replace('__GRYC__',e('gray_can.jpg')))
print('ok')
