import json,math,pickle
from shapely.geometry import LineString,MultiLineString,Point
from shapely.ops import linemerge,unary_union
LON0,LAT1,K=-10.9,44.6,100;C=math.cos(math.radians(40))
H=1120;IX,IY=14,H-14-200;CL0,CA1=-18.4,29.5;CC=math.cos(math.radians(28.5))
def P(lon,lat):return [round(IX+(lon-CL0)*K*CC,1),round(IY+(CA1-lat)*K,1)] if lon<-12.5 else [round((lon-LON0)*K*C,1),round((LAT1-lat)*K,1)]
S=json.load(open('/mnt/user-data/uploads/sel.json'))['elements']
N={e['id']:e for e in S}
OSM='OpenStreetMap'
def node(i):e=N[i];return (e['lon'],e['lat'])
def way(*ids):
  ls=[LineString([(g['lon'],g['lat']) for g in N[i]['geometry']]) for i in dict.fromkeys(ids)]
  m=linemerge(ls) if len(ls)>1 else ls[0]
  return m
def lines_of(g):return [[P(*c) for c in l.coords] for l in (g.geoms if g.geom_type=='MultiLineString' else [g])]
def mid(g):
  l=max(g.geoms,key=lambda x:x.length) if g.geom_type=='MultiLineString' else g
  p=l.interpolate(.5,normalized=True);return (p.x,p.y)
out=[];src={}
def add(id,name,short,cat,kind,ru,s,pts=None,g=None,big=False,r=None):
  o=dict(id=id,name=name,short=short,cat=cat,kind=kind,ru=ru)
  if kind=='ridge':o['lines']=lines_of(g);o['xy']=[P(*mid(g))]
  else:o['xy']=[P(*p) for p in pts]
  if big:o['big']=1
  if r:o['r']=r
  out.append(o);src[id]=s
WIKI='Wikipedia (координаты статьи)'
# --- rivers / OSM objects
riv=pickle.load(open('osm_pick2.pkl','rb'))
G={k:way(*v) for k,v in {
 'sc':[1557800256],'guad':[1117490328],'gata':[1378106694],'gudar':[1486840524],'javal':[1486844137],'alb':[1557318519],'univ':[1516388602],'cuen':[1565449106],
 'arac':[894154176,907304994],'madr':[624197209],'lit':[1117929203],'prelit':[1117929201],'mserr':[492819272],'msant':[1560199072],'graz':[907149472],'ronda':[907064241],
 'nev':[893886386],'fil':[893886377,894158365],'mag':[894585726],'caz':[895480904],'seg':[895480903,908978643],'sag':[895480902],'tram':[219374698]}.items()}
# Meseta
duero=riv['Duero'];tajo=riv['Tajo'];gua=riv['Guadiana']
def at_lon(g,lon):
  from shapely.geometry import LineString as LS
  cut=g.intersection(LS([(lon,35),(lon,44)]))
  pts=[cut] if cut.geom_type=='Point' else list(getattr(cut,'geoms',[]))
  return pts
dn=at_lon(duero,-4.75)[0];tj=sorted(at_lon(tajo,-3.6),key=lambda p:p.y)[-1];gd=sorted(at_lon(gua,-3.6),key=lambda p:-p.y)[0]
sn=(dn.x,dn.y);ss=(-3.6,(tj.y+gd.y)/2)
print('Duero@-4.75',sn,'Tajo@-3.6',tj.y,'Guadiana@-3.6',gd.y)
add('meseta','Meseta Castellana','Meseta','rel_mes','area','Кастильская Месета (Центральная)','две субмесеты: точки на долине Дуэро и между Тахо и Гвадианой (Wikipedia: Meseta Central)',pts=[sn,ss],big=True,r=60)
add('subnorte','Submeseta Norte','Submeseta Norte','rel_mes','area','Северная субмесета (долина Дуэро)','на линии Дуэро (OSM): «submeseta norte, ocupada por el valle del Duero»',pts=[(sn[0]+0.6,sn[1]+0.25)],big=True,r=55)
add('subsur','Submeseta Sur','Submeseta Sur','rel_mes','area','Южная субмесета (долины Тахо и Гвадианы)','между Тахо и Гвадианой (OSM) по долготе 3,6° з. д.',pts=[ss],big=True,r=55)
# Interiores
add('sistemacentral','Sistema Central','Sistema Central','rel_int','ridge','Центральная система',OSM+' (mountain_range)',g=G['sc'],big=True)
add('somosierra','Sierra de Somosierra','Somosierra','rel_int','area','Сомосьерра',OSM+' (вершина Somosierra, 1468 м)',pts=[node(6005369182)],r=14)
add('guadarrama','Sierra de Guadarrama','Guadarrama','rel_int','ridge','Сьерра-де-Гвадаррама',OSM,g=G['guad'])
add('gredos','Sierra de Gredos','Gredos','rel_int','area','Сьерра-де-Гредос','центр листа IGN «Región Central de Gredos» (5°27′–4°59′ з. д., 40°07′–40°22′ с. ш.)',pts=[(-5.05,40.245)],r=22)
add('gata_s','Sierra de Gata','Gata','rel_int','ridge','Сьерра-де-Гата',OSM+' (ridge)',g=G['gata'])
add('estrella','Sierra de la Estrella','Estrella','rel_int','area','Серра-да-Эштрела (Португалия)',OSM+' (Serra da Estrela)',pts=[node(5172661705)],r=18)
add('montestoledo','Montes de Toledo','Montes de Toledo','rel_int','area','Толедские горы','координаты хребта, Wikipedia «Montes de Toledo»',pts=[(-4.49167,39.38333)],big=True,r=30)
add('guadalupe','Sierra de Guadalupe – Las Villuercas','Guadalupe','rel_int','peak','Сьерра-де-Гуадалупе, вершина Вильуэркас (1595 м)',OSM+'; Вильуэркас — центральный массив Сьерра-де-Гуадалупе (EcuRed)',pts=[node(26865092)])
add('montanchez','Sierra de Montánchez','Montánchez','rel_int','peak','Монтанчес (994 м)',OSM,pts=[node(12631253109)])
add('sanpedro','Sierra de San Pedro','San Pedro','rel_int','area','Сьерра-де-Сан-Педро','координаты хребта, Wikipedia «Sierra de San Pedro»',pts=[(-6.583,39.3)],r=20)
# Periféricas
add('montesleon','Montes de León','Montes de León','rel_per','area','Леонские горы','координаты хребта, Wikipedia «Montes de León»',pts=[(-6.3,42.5)],big=True,r=25)
add('ubina','Peña Ubiña','Peña Ubiña','rel_per','peak','Пенья-Убинья (2417 м)',OSM,pts=[node(1157264807)])
add('picoseuropa','Picos de Europa','Picos de Europa','rel_per','area','Пикос-де-Эуропа',OSM+' (mountain_range)',pts=[node(2146258561)],r=20)
add('prieta','Peña Prieta','Peña Prieta','rel_per','peak','Пенья-Приета (2539 м)',OSM,pts=[node(948475375)])
mem=[mid(G[k]) for k in ('alb','univ','gudar','javal','cuen')]
add('iberico','Sistema Ibérico','Sistema Ibérico','rel_per','area','Иберийская система',OSM+' (Sistema Ibérico) и центры его сьерр',pts=[node(4872294121)]+mem,big=True,r=30)
add('demanda','Sierra de la Demanda','Demanda','rel_per','area','Сьерра-де-ла-Деманда','вершина San Lorenzo (2271 м), Natural Earth',pts=[(-2.937791,42.246301)],r=18)
add('urbion','Picos de Urbión','Urbión','rel_per','peak','Пикос-де-Урбьон (2228 м)',OSM,pts=[node(9924870737)])
add('gudar','Sierra de Gúdar','Gúdar','rel_per','ridge','Сьерра-де-Гудар',OSM+' (ridge)',g=G['gudar'])
add('javalambre','Sierra de Javalambre','Javalambre','rel_per','ridge','Сьерра-де-Хаваламбре',OSM+' (ridge)',g=G['javal'])
add('maestrazgo','Maestrazgo','Maestrazgo','rel_per','area','Маэстрасго','Sierra Carrascosa в Маэстрасго, Wikipedia',pts=[(-0.35333,40.70417)],r=22)
add('albarracin','Sierra de Albarracín','Albarracín','rel_per','ridge','Сьерра-де-Альбаррасин',OSM,g=G['alb'])
add('universales','Montes Universales','Montes Universales','rel_per','ridge','Монтес-Универсалес',OSM+' (ridge)',g=G['univ'])
add('cuenca','Serranía de Cuenca','Serranía de Cuenca','rel_per','ridge','Серрания-де-Куэнка',OSM,g=G['cuen'])
add('aracena','Sierra de Aracena','Aracena','rel_per','ridge','Сьерра-де-Арасена',OSM,g=G['arac'])
add('madrona','Sierra Madrona','Madrona','rel_per','ridge','Сьерра-Мадрона',OSM,g=G['madr'])
add('alcaraz','Sierra de Alcaraz','Alcaraz','rel_per','area','Сьерра-де-Алькарас','координаты хребта, Wikipedia «Sierra de Alcaraz»',pts=[(-2.367,38.617)],r=16)
add('almenara','Pico Almenara','Almenaras','rel_per','peak','Альменара (1798 м), высшая точка Сьерра-де-Алькарас',OSM,pts=[node(26862479)])
# Exteriores
add('galaico','Macizo Galaico','Macizo Galaico','rel_ext','area','Галисийский массив','координаты хребта, Wikipedia «Galician Massif»',pts=[(-8.1,42.5)],big=True,r=30)
add('manzaneda','Cabeza de Manzaneda','Manzaneda','rel_ext','peak','Кабеса-де-Мансанеда (1781 м)',OSM,pts=[node(883517436)])
add('vascos','Montes Vascos','Montes Vascos','rel_ext','area','Баскские горы','координаты хребта, Wikipedia «Basque Mountains»',pts=[(-2.317,42.95)],big=True,r=25)
add('gorbea','Gorbea','Gorbea','rel_ext','peak','Горбея (1482 м)',OSM+' (Gorbeiako gurutzea)',pts=[node(511135960)])
cc=unary_union([G['lit'],G['prelit']])
add('costerocat','Cordilleras Costero-Catalanas','Costero-Catalanas','rel_ext','ridge','Каталонские прибрежные хребты',OSM+' (Serralada Litoral и Prelitoral)',g=cc,big=True)
add('montseny','Montseny – Turó de l\'Home',"Turó de l'Home",'rel_ext','peak',"Монсень, вершина Туро-де-л'Ом (1706 м)",OSM,pts=[node(5126232285)])
add('montserrat','Montserrat','Montserrat','rel_ext','ridge','Монсеррат',OSM,g=G['mserr'])
add('montsant','Montsant','Montsant','rel_ext','ridge','Монсант',OSM,g=G['msant'])
add('penibetica','Cordillera Penibética','Penibética','rel_ext','area','Пенибетская кордильера','центры её сьерр (OSM): Grazalema, Ronda, Nevada, Filabres',pts=[mid(G[k]) for k in ('graz','ronda','nev','fil')],big=True,r=30)
add('grazalema','Sierra de Grazalema','Grazalema','rel_ext','ridge','Сьерра-де-Грасалема',OSM,g=G['graz'])
add('ronda','Serranía de Ronda','Serranía de Ronda','rel_ext','ridge','Серрания-де-Ронда',OSM,g=G['ronda'])
add('torrecilla','Torrecilla','Torrecilla','rel_ext','peak','Торресилья (1919 м)',OSM,pts=[node(26864940)])
add('nevada','Sierra Nevada','Sierra Nevada','rel_ext','ridge','Сьерра-Невада',OSM,g=G['nev'])
add('filabres','Sierra de los Filabres','Filabres','rel_ext','ridge','Сьерра-де-лос-Филабрес',OSM,g=G['fil'])
add('calaralto','Calar Alto','Calar Alto','rel_ext','peak','Калар-Альто (2168 м)',OSM,pts=[node(317532199)])
add('subbetica','Cordillera Subbética','Subbética','rel_ext','area','Суббетская кордильера','центры её сьерр (OSM): Mágina, Cazorla, Segura, La Sagra',pts=[mid(G[k]) for k in ('mag','caz','seg','sag')],big=True,r=30)
add('magina','Sierra Mágina','Mágina','rel_ext','ridge','Сьерра-Махина',OSM,g=G['mag'])
add('cazorla','Sierra de Cazorla','Cazorla','rel_ext','ridge','Сьерра-де-Касорла',OSM,g=G['caz'])
add('segura_s','Sierra de Segura','Segura','rel_ext','ridge','Сьерра-де-Сегура',OSM,g=G['seg'])
add('sagra','Sierra de la Sagra','La Sagra','rel_ext','ridge','Сьерра-де-ла-Сагра',OSM,g=G['sag'])
add('tramuntana','Sierra de Tramuntana','Tramuntana','rel_ext','ridge','Сьерра-де-Трамонтана (Мальорка)',OSM+' (ridge)',g=G['tram'])
# Llobregat
L=json.load(open('/mnt/user-data/uploads/llob.json'))['elements']
ls=[LineString([(g['lon'],g['lat']) for g in e['geometry']]) for e in L if "Empord" not in e['tags'].get('name','')]
lg=linemerge(unary_union(ls))
es=pickle.load(open('es_hr.pkl','rb'))
print('Llobregat len',round(lg.length,2),'to coast km',round(lg.distance(es.boundary)*85,1))
g=lg.simplify(0.003);parts=list(g.geoms) if g.geom_type=='MultiLineString' else [g]
lp=max(parts,key=lambda l:l.length).interpolate(.5,normalized=True)
out.append(dict(id='llobregat',name='Río Llobregat',short='Llobregat',cat='r_med',kind='line',ru='Льобрегат',xy=[P(lp.x,lp.y)],lines=[[P(*c) for c in l.coords] for l in parts]))
src['llobregat']='OpenStreetMap (Overpass, «Riu Llobregat»); устье у моря проверено'
json.dump({'objs':out,'src':src},open('rel_osm.json','w'),ensure_ascii=False)
print(len(out))
