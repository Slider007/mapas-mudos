import json,re
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color,HexColor
from reportlab.platypus import Paragraph,Frame
from reportlab.lib.styles import ParagraphStyle
G=json.load(open('geo2.json'))
html=open('tpl11.html').read();j=html.index('const O2=');O2=json.loads(html[j+9:html.index(';\nO.push',j)])
RIV=[o for o in O2 if o['kind']=='line']
W,H=G['W'],G['H'];IX,IY,IW,IH=G['inset']
PW,PH=landscape(A4);M=22
MH=PH-2*M-26;S=MH/H;MW=W*S;X0,Y0=M,M     # map box
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
LISTS={
'costa':('Costas e islas',[('OCÉANOS','Atlántico'),('MARES','Cantábrico, Mediterráneo'),('GOLFOS','Vizcaya, Cádiz, Almería, Mazarrón, Alicante, Valencia, San Jorge, Roses, León'),('CABOS','Machichaco, Ajo, Peñas, Ortegal, Prior, Touriñán, Finisterre, Gata, Palos, Nao, Creus'),('ESTRECHOS Y PUNTAS','Estrecho de Gibraltar, Punta de Estaca de Bares, Punta de Tarifa'),('ISLAS','Baleares (Mallorca, Menorca, Ibiza, Formentera, Cabrera) y Canarias (Gran Canaria, Fuerteventura, Lanzarote, Tenerife, La Gomera, La Palma, El Hierro)')]),
'rios':('Ríos',[('GALLEGOS','Miño, Sil, Ulla, Tambre, Eo'),('CÁNTABROS','Navia, Nalón, Narcea, Besaya, Nervión, Bidasoa'),('DUERO','Derecha: Pisuerga, Arlanzón, Carrión, Esla, Bernesga. Izquierda: Eresma, Adaja, Tormes'),('TAJO','Derecha: Jarama, Henares, Alberche, Tiétar, Alagón. Izquierda: Almonte, Salor'),('GUADIANA','Derecha: Záncara, Cigüela. Izquierda: Jabalón, Zújar, Matachel'),('GUADALQUIVIR','Derecha: Guadalimar, Jándula, Guadalmellato, Guadiato, Bembézar, Viar. Izquierda: Guadiana Menor, Guadalbullón, Genil'),('ATLÁNTICOS ANDALUCES','Odiel, Tinto, Guadalete, Barbate'),('MEDITERRÁNEO','Ter, Llobregat'),('EBRO','Derecha: Jalón, Jiloca, Huerva, Guadalope. Izquierda: Arga, Aragón, Gállego, Cinca, Noguera Pallaresa, Noguera Ribagorzana, Segre'),('MEDITERRÁNEOS','Mijares, Turia, Júcar, Cabriel, Segura, Almanzora, Andarax, Adra, Guadalfeo, Guadalhorce, Guadiaro')]),
'rel':('Relieve',[('MESETA','Castellana (Submeseta Norte o del Duero y Submeseta Sur o del Tajo)'),('CORDILLERAS INTERIORES','Sistema Central (Somosierra, Guadarrama, Gredos – Almanzor, Gata, Estrella). Montes de Toledo (Guadalupe – Villuercas – Montánchez, San Pedro)'),('CORDILLERAS PERIFÉRICAS','Montes de León (Teleno), Cordillera Cantábrica (Peña Ubiña, Picos de Europa – Torre Cerredo – Peña Prieta), Sistema Ibérico (Sierra de la Demanda, Picos de Urbión, Moncayo, Gúdar, Javalambre, Maestrazgo, Albarracín, Montes Universales, Serranía de Cuenca), Sierra Morena (Aracena, Madrona, Alcaraz – Almenaras)'),('CORDILLERAS EXTERIORES',"Macizo Galaico (Cabeza de Manzaneda), Montes Vascos (Gorbea), Pirineos (Aneto, Monte Perdido), Cordilleras Costero-Catalanas (Montseny – Turó de l'Home, Montserrat, Montsant), Cordillera Penibética (Grazalema, Serranía de Ronda – Torrecilla, Sierra Nevada – Mulhacén, Veleta, Filabres – Calar Alto), Cordillera Subbética (Mágina, Cazorla, Segura, La Sagra), Cordilleras insulares (Sierra de Tramuntana – Puig Major, Sierra de Levante; Teide)")])}
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
    c.clipPath(pp,stroke=0,fill=0);c.drawImage('grayp_main.png',*tr(0,H),W*S,H*S);c.restoreState()
    for k,d in G['isl'].items():
      if k not in CAN:c.saveState();c.clipPath(svgpath(c,d),stroke=0,fill=0);c.drawImage('grayp_main.png',*tr(0,H),W*S,H*S);c.restoreState()
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
      sp=svgpath(c,G['isl'][k]);c.saveState();c.clipPath(sp,stroke=0,fill=0);c.drawImage('grayp_can.png',*tr(IX,IY+IH),IW*S,IH*S);c.restoreState()
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
  st=ParagraphStyle('n',fontName='Helvetica',fontSize=8.2 if key!='rel' else 7.6,leading=10.2 if key!='rel' else 9.4,textColor=HexColor('#1f2a33'))
  html_=''.join(f'<b>{a}:</b> {b}<br/><br/>' for a,b in items)
  fr=Frame(RX-4,Y0+64,RW+8,yy-Y0-70,showBoundary=0,leftPadding=4,rightPadding=4,topPadding=2,bottomPadding=2)
  fr.addFromList([Paragraph(html_,st)],c)
  c.setStrokeColor(LINE);c.setLineWidth(.6);c.rect(RX,Y0,RW,56,fill=0,stroke=1)
  c.setFont('Helvetica-Bold',8);c.setFillColor(LINE);c.drawString(RX+5,Y0+46,'LEYENDA')
  c.setFont('Helvetica',6);c.setFillColor(HexColor('#6c7e88'))
  c.drawString(M,M-12,'Contorno: IGN (Líneas Límite); ríos: OpenStreetMap; relieve: Natural Earth. Proyección equirrectangular; Canarias en recuadro.')
  c.showPage()
c=canvas.Canvas('/mnt/user-data/outputs/mapa-mudo-espana-fisica.pdf',pagesize=landscape(A4))
c.setTitle('Mapa mudo de España — España física')
page(c,'costa',False,False)
page(c,'rios',False,True)
page(c,'rel',True,True)
page(c,'costa',False,False) if False else None
c.save()
