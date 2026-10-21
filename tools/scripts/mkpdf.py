import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]          # корень репозитория
DATA=ROOT/'tools'/'data'
TEMPLATE=ROOT/'tools'/'src'/'espana-fisica.template.html'
OUT=ROOT/'espana-fisica'/'pdf'/'mapa-mudo-espana-fisica.pdf'
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color,HexColor
from reportlab.platypus import Paragraph,Frame
from reportlab.lib.styles import ParagraphStyle
G=json.load(open(DATA/'geo2.json'))
html=open(TEMPLATE,encoding='utf-8').read();j=html.index('const O2=');O2=json.loads(html[j+9:html.index(';\nO.push',j)])
RIV=[o for o in O2 if o['kind']=='line']
W,H=G['W'],G['H'];IX,IY,IW,IH=G['inset']
PW,PH=landscape(A4);M=22
MH0=PH-2*M-26;K_=.93;MH=MH0*K_;S=MH/H;MW=W*S;X0,Y0=M,M+MH0-MH     # map box (чуть меньше, чтобы справа поместились нумерованные списки)
def tr(x,y):return X0+x*S,Y0+(H-y)*S
def svgpath(c,d):
  p=c.beginPath()
  for cmd in re.findall(r'M[^MZ]*Z?',d):
    pts=[tuple(map(float,q.split(','))) for q in re.findall(r'-?[\d.]+,-?[\d.]+',cmd)]
    if not pts:continue
    p.moveTo(*tr(*pts[0]))
    for q in pts[1:]:p.lineTo(*tr(*q))
    if cmd.endswith('Z'):p.close()
  return p
SEA=HexColor('#e6f0f4');LINE=HexColor('#1f3a4d');OTH=HexColor('#ececea');RIVC=HexColor('#4f7f9c')
# нумерованные списки строятся из тех же данных, что и страница (шаблон), чтобы PDF и приложение не расходились
def _cats():
  b=html[html.index('const CATS=['):];b=b[:b.index('];')]
  return re.findall(r"\{id:'(\w+)'(?:,sec:'\w+')?(?:,g:'\w+')?,ru:'[^']*',es:'([^']*)'\}",b)
CATS=_cats()
COSTA=re.findall(r"^ \['(\w+)','([^']+)','([^']+)','(\w+)'",html,re.M)
RIVORD=['r_gal','r_can','r_duero','r_tajo','r_guadiana','r_gq','r_and','r_ebro','r_med']
SHORT={o['id']:o['short'] for o in O2}
ORDER_REL=[('MESETA',['Meseta','Submeseta Norte','Submeseta Sur']),
('CORD. INTERIORES',['Sistema Central','Somosierra','Guadarrama','Gredos','Almanzor','Gata','Estrella','Montes de Toledo','Guadalupe','Montánchez','San Pedro']),
('CORD. PERIFÉRICAS',['Montes de León','Teleno','Cantábrica','Peña Ubiña','Picos de Europa','Torre Cerredo','Peña Prieta','Sistema Ibérico','Demanda','Urbión','Moncayo','Gúdar','Javalambre','Maestrazgo','Albarracín','Montes Universales','Serranía de Cuenca','Sierra Morena','Aracena','Madrona','Alcaraz','Almenaras']),
('CORD. EXTERIORES',['Macizo Galaico','Manzaneda','Montes Vascos','Gorbea','Pirineos','Aneto','Monte Perdido','Costero-Catalanas',"Turó de l'Home",'Montserrat','Montsant','Penibética','Grazalema','Serranía de Ronda','Torrecilla','Sierra Nevada','Mulhacén','Veleta','Filabres','Calar Alto','Subbética','Mágina','Cazorla','Segura','La Sagra','Tramuntana','Puig Major','Levante','Teide'])]
SUB={'Almanzor','Teleno','Peña Ubiña','Torre Cerredo','Peña Prieta','Urbión','Moncayo','Almenaras','Manzaneda','Gorbea','Aneto','Monte Perdido',"Turó de l'Home",'Torrecilla','Mulhacén','Veleta','Calar Alto','Puig Major','Teide','Guadalupe','Montánchez'}
def build_lists():
  # элемент списка: ('h',заголовок) или ('i',текст,вложенность,вершина?)
  L={}
  lv=re.search(r'O\.push\((\{"id":"levante".*?\})\);',html);O=O2+([json.loads(lv.group(1))] if lv else [])
  rel={o['short']:o for o in O if o['cat'].startswith('rel_')}
  cs=[];cur=None
  for oid,nm,sh,cat in COSTA:
    if cat!=cur:cur=cat;cs.append(('h',dict(CATS)[cat].upper()))
    cs.append(('i',sh,0,False,''))
  L['costa']=('Costas e islas',cs)
  rv=[]
  for cat in RIVORD:
    rv.append(('h',dict(CATS)[cat].upper().replace('CUENCA DEL ','')))
    for o in RIV:
      if o['cat']!=cat:continue
      tag='';ind=0
      if o.get('bank'):tag=o['bank'];ind=1
      elif o.get('parent'):tag='afl. '+SHORT[o['parent']];ind=1
      rv.append(('i',o['short'],ind,False,tag))
  L['rios']=('Ríos',rv)
  rl=[];used=set()
  for h_,names in ORDER_REL:
    rl.append(('h',h_))
    for n_ in names:
      assert n_ in rel,n_;used.add(n_)
      rl.append(('i',n_,1 if n_ in SUB else 0,n_ in SUB and rel[n_]['kind']=='peak',''))
  assert used==set(rel),set(rel)^used
  L['rel']=('Relieve',rl)
  return L
LISTS=build_lists()
NOTE={'costa':'','rios':'(D) / (I) = margen derecha / izquierda · afl. = afluente de','rel':'= cumbre'}
IND=4
def tri(c,x,y,r):
  c.setFillColor(LINE);p=c.beginPath();p.moveTo(x-r*.6,y-.3);p.lineTo(x+r*.6,y-.3);p.lineTo(x,y+r);p.close();c.drawPath(p,fill=1,stroke=0)
def draw_list(c,items,x,ybot,w,h,key_=''):
  # подбираем число столбцов и размер шрифта так, чтобы всё поместилось
  done=False
  for fs in (9,8.5,8,7.5,7,6.6,6.2):
    for ncol in (1,2,3):
      cw=(w-(ncol-1)*8)/ncol
      lead=fs*1.22;gap=fs*.5;nw=c.stringWidth('88.','Helvetica',fs)+3
      def need(it):return lead+(gap if it[0]=='h' else 0)
      ok=all(c.stringWidth(it[1],('Helvetica-Bold' if it[0]=='h' else 'Helvetica'),fs*(.88 if it[0]=='h' else 1))+((nw+it[2]*IND+(fs*.85 if it[3] else 0)+(c.stringWidth('(D)' if len(it[4])==1 else it[4],'Helvetica',fs*.85)+4 if it[4] else 0)) if it[0]=='i' else 0)<=cw for it in items)
      if not ok:continue
      cols=[[]];hh=0
      for k,it in enumerate(items):
        nxt=items[k+1] if k+1<len(items) else None
        extra=need(it)+(need(nxt) if it[0]=='h' and nxt else 0)
        if hh+extra>h and cols[-1]:cols.append([]);hh=0
        cols[-1].append(it);hh+=need(it)
      if len(cols)<=ncol:done=True;break
    if done:break
  n=0
  for ci,col in enumerate(cols):
    cx=x+ci*(cw+8);y=ybot+h-fs
    for it in col:
      if it[0]=='h':
        y-=gap;c.setFont('Helvetica-Bold',fs*.88);c.setFillColor(LINE);c.drawString(cx,y,it[1]);y-=lead
      else:
        n+=1;c.setFillColor(HexColor('#1f2a33'));c.setFont('Helvetica-Bold',fs)
        c.drawRightString(cx+nw-3+it[2]*IND,y,'%d.'%n)
        tx=cx+nw+it[2]*IND
        if it[3]:tri(c,tx+fs*.3,y,fs*.62);tx+=fs*.85
        c.setFont('Helvetica',fs);c.drawString(tx,y,it[1])
        if it[4]:c.setFont('Helvetica',fs*.85);c.setFillColor(HexColor('#6c7e88'));c.drawString(tx+c.stringWidth(it[1],'Helvetica',fs)+3,y,('(%s)'%it[4]) if len(it[4])==1 else it[4])
        y-=lead
  return n
def page(c,key,relief,rivers):
  title,items=LISTS[key]
  # frame + sea
  c.setFillColor(SEA);c.setStrokeColor(LINE);c.setLineWidth(.8);c.rect(X0,Y0,MW,MH,fill=1,stroke=1)
  c.saveState();p=c.beginPath();p.rect(X0,Y0,MW,MH);c.clipPath(p,stroke=0,fill=0)
  # neighbours
  c.setFillColor(OTH);c.setStrokeColor(HexColor('#b9c6cc'));c.setLineWidth(.3)
  for d in G['land'].values():c.drawPath(svgpath(c,d),fill=1,stroke=1)
  # spain fill white
  c.setFillColor(HexColor('#ffffff'));c.drawPath(svgpath(c,G['spain']),fill=1,stroke=0)
  CAN=['gran_canaria','fuerteventura','lanzarote','tenerife','la_gomera','la_palma','el_hierro']
  for k,d in G['isl'].items():
    if k not in CAN:c.drawPath(svgpath(c,d),fill=1,stroke=0)
  if relief:
    c.saveState();pp=svgpath(c,G['spain'])
    c.clipPath(pp,stroke=0,fill=0);c.drawImage(str(DATA/'grayp_main.png'),*tr(0,H),W*S,H*S);c.restoreState()
    for k,d in G['isl'].items():
      if k not in CAN:c.saveState();c.clipPath(svgpath(c,d),stroke=0,fill=0);c.drawImage(str(DATA/'grayp_main.png'),*tr(0,H),W*S,H*S);c.restoreState()
  # graticule
  c.setStrokeColor(HexColor('#9fb0b8'));c.setLineWidth(.25);c.setFont('Helvetica',6);c.setFillColor(HexColor('#6c7e88'))
  import math
  K=100;C=math.cos(math.radians(40));L0=-10.9;L1=44.6
  ix2=IX+IW
  for lon in range(-10,5,2):
    x=(lon-L0)*K*C;yb=IY if x<ix2 else H;c.line(*tr(x,0),*tr(x,yb));c.drawString(tr(x,0)[0]+2,tr(x,0)[1]-8,f"{abs(lon)}°{'W' if lon<0 else 'E' if lon>0 else ''}")
  for lat in range(34,45,2):
    y=(L1-lat)*K;xa=ix2 if y>IY else 0;c.line(*tr(xa,y),*tr(W,y));c.drawString(tr(xa,y)[0]+2,tr(xa,y)[1]+2,f"{lat}°N")
  # rivers
  if rivers:
    c.setStrokeColor(RIVC);c.setLineCap(1);c.setLineJoin(1)
    for o in RIV:
      c.setLineWidth(.75 if not o.get('parent') else .45)
      for l in o['lines']:
        p=c.beginPath();p.moveTo(*tr(*l[0]))
        for q in l[1:]:p.lineTo(*tr(*q))
        c.drawPath(p,stroke=1,fill=0)
  # coastline
  c.setStrokeColor(LINE);c.setLineWidth(.6)
  c.drawPath(svgpath(c,G['spain']),fill=0,stroke=1)
  for k,d in G['isl'].items():
    if k not in CAN:c.drawPath(svgpath(c,d),fill=0,stroke=1)
  # canary inset
  c.setFillColor(SEA);c.setStrokeColor(LINE);c.setLineWidth(.6);c.rect(*tr(IX,IY+IH),IW*S,IH*S,fill=1,stroke=1)
  c.setFillColor(HexColor('#ffffff'))
  for k in CAN:c.drawPath(svgpath(c,G['isl'][k]),fill=1,stroke=0)
  if G.get('canx'):c.drawPath(svgpath(c,G['canx']),fill=1,stroke=0)
  if relief:
    c.saveState();pp=c.beginPath()
    for k in CAN:
      sp=svgpath(c,G['isl'][k]);c.saveState();c.clipPath(sp,stroke=0,fill=0);c.drawImage(str(DATA/'grayp_can.png'),*tr(IX,IY+IH),IW*S,IH*S);c.restoreState()
    c.restoreState()
  c.setStrokeColor(LINE)
  for k in CAN:c.drawPath(svgpath(c,G['isl'][k]),fill=0,stroke=1)
  c.restoreState()
  c.setStrokeColor(LINE);c.setLineWidth(.8);c.rect(X0,Y0,MW,MH,fill=0,stroke=1)
  # header
  c.setFillColor(LINE);c.setFont('Helvetica-Bold',15);c.drawString(M,PH-M-12,'MAPA MUDO DE ESPAÑA')
  tw=c.stringWidth('MAPA MUDO DE ESPAÑA','Helvetica-Bold',15);c.setFont('Helvetica',10.5);c.drawString(M+tw+10,PH-M-12,'España física: '+title)
  # right column
  RX=X0+MW+14;RW=PW-RX-M
  c.setFont('Helvetica',9);c.setFillColor(HexColor('#333333'))
  yy=PH-M-14
  for lab in ('Nombre:','Curso:','Fecha:'):
    c.drawString(RX,yy,lab);c.setStrokeColor(HexColor('#999999'));c.setLineWidth(.4);c.line(RX+40,yy-2,RX+RW,yy-2);yy-=17
  c.setFont('Helvetica-Oblique',7);c.setFillColor(HexColor('#555555'))
  c.drawString(RX,yy-4,'Escribe en el mapa el número de cada nombre.')
  nt=NOTE[key]
  if nt:
    c.drawString(RX+(9 if key=='rel' else 0),yy-13,nt)
    if key=='rel':tri(c,RX+3.5,yy-13,6)
  draw_list(c,items,RX,M+44,RW,yy-(22 if nt else 13)-(M+44),key)
  c.setStrokeColor(LINE);c.setLineWidth(.6);c.rect(RX,M,RW,36,fill=0,stroke=1)
  c.setFont('Helvetica-Bold',8);c.setFillColor(LINE);c.drawString(RX+5,M+26,'LEYENDA')
  c.setFont('Helvetica',6);c.setFillColor(HexColor('#6c7e88'))
  c.drawString(M,M-12,'Contorno: IGN (Líneas Límite); ríos: OpenStreetMap; relieve: Copernicus DEM (ESA); países vecinos y mares: Natural Earth. Proyección equirrectangular; Canarias en recuadro.')
  c.showPage()
c=canvas.Canvas(str(OUT),pagesize=landscape(A4))
c.setTitle('Mapa mudo de España — España física');c.setAuthor('Slider007');c.setSubject('Mapas mudos — https://slider007.github.io/mapas-mudos/')
page(c,'costa',False,False)
page(c,'rios',False,True)
page(c,'rel',True,False)
page(c,'costa',False,False) if False else None
c.save()
