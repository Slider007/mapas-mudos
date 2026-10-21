import json,math,pickle
from shapely.geometry import shape,Point,LineString,MultiLineString,box
from shapely.ops import split,nearest_points,substring
G=pickle.load(open('rivers_ne.pkl','rb'))
# fix NE mislabel: "Jiloca" line continues to the Ebro; below the confluence it is the Jalón
jal=G['jalon'];jil=G['jiloca']
e=[Point(jal.coords[0]),Point(jal.coords[-1])];jend=min(e,key=lambda p:p.distance(jil))
print('Jalón fragment end to Jiloca line, km:',round(jend.distance(jil)*111*0.76,2))
d=jil.project(jend)
up,down=substring(jil,0,d),substring(jil,d,jil.length)
# which part touches the Ebro?
eb=G['ebro']
if up.distance(eb)<down.distance(eb):up,down=down,up
G['jiloca']=up
from shapely.ops import linemerge
G['jalon']=linemerge([jal,down]) if linemerge([jal,down]).geom_type=='LineString' else MultiLineString([jal,down])
print('Jalón now to Ebro km:',round(G['jalon'].distance(eb)*111*.76,2),' Jiloca to Jalón km:',round(G['jiloca'].distance(G['jalon'])*111*.76,2))
LON0,LAT1,K=-10.9,44.6,100;C=math.cos(math.radians(40))
def pm(lon,lat):return[round((lon-LON0)*K*C,1),round((LAT1-lat)*K,1)]
H=1120;IX,IY=14,H-14-200;CL0,CA1=-18.4,29.5;CC=math.cos(math.radians(28.5))
def pc(lon,lat):return[round(IX+(lon-CL0)*K*CC,1),round(IY+(CA1-lat)*K,1)]
P=lambda lon,lat:pc(lon,lat) if lon<-12.5 else pm(lon,lat)
NE='Natural Earth 1:10M (GitHub nvkelso/natural-earth-vector)'
RV=[ # id, Spanish name, short, cat(basin), ru, parent, side
 ('mino','Río Miño','Miño','r_gal','Миньо',None,None),('sil','Río Sil','Sil','r_gal','Силь (приток Миньо)','mino',None),
 ('narcea','Río Narcea','Narcea','r_can','Нарсеа',None,None),
 ('duero','Río Duero','Duero','r_duero','Дуэро',None,None),('pisuerga','Río Pisuerga','Pisuerga','r_duero','Писуэрга','duero','D'),
 ('esla','Río Esla','Esla','r_duero','Эсла','duero','D'),('adaja','Río Adaja','Adaja','r_duero','Адаха','duero','I'),('tormes','Río Tormes','Tormes','r_duero','Тормес','duero','I'),
 ('tajo','Río Tajo','Tajo','r_tajo','Тахо',None,None),('henares','Río Henares','Henares','r_tajo','Энарес','tajo','D'),('alberche','Río Alberche','Alberche','r_tajo','Альберче','tajo','D'),
 ('tietar','Río Tiétar','Tiétar','r_tajo','Тьетар','tajo','D'),('alagon','Río Alagón','Alagón','r_tajo','Алагон','tajo','D'),
 ('guadiana','Río Guadiana','Guadiana','r_guadiana','Гвадиана',None,None),('zancara','Río Záncara','Záncara','r_guadiana','Санкара','guadiana','D'),('zujar','Río Zújar','Zújar','r_guadiana','Сухар','guadiana','I'),
 ('guadalquivir','Río Guadalquivir','Guadalquivir','r_gq','Гвадалквивир',None,None),('guadalimar','Río Guadalimar','Guadalimar','r_gq','Гвадалимар','guadalquivir','D'),
 ('guadianamenor','Río Guadiana Menor','Guadiana Menor','r_gq','Гвадиана-Менор','guadalquivir','I'),('genil','Río Genil','Genil','r_gq','Хениль','guadalquivir','I'),
 ('ebro','Río Ebro','Ebro','r_ebro','Эбро',None,None),('jalon','Río Jalón','Jalón','r_ebro','Халон','ebro','D'),('jiloca','Río Jiloca','Jiloca','r_ebro','Хилока','ebro','D'),
 ('aragon','Río Aragón','Aragón','r_ebro','Арагон','ebro','I'),('cinca','Río Cinca','Cinca','r_ebro','Синка','ebro','I'),('segre','Río Segre','Segre','r_ebro','Сегре','ebro','I'),
 ('mijares','Río Mijares','Mijares','r_med','Михарес',None,None),('turia','Río Turia','Turia','r_med','Турия',None,None),('jucar','Río Júcar','Júcar','r_med','Хукар',None,None),
 ('cabriel','Río Cabriel','Cabriel','r_med','Кабриэль (приток Хукара)','jucar',None),('segura','Río Segura','Segura','r_med','Сегура',None,None)]
out=[]
for rid,name,short,cat,ru,par,side in RV:
  g=G[rid].simplify(0.004)
  ls=list(g.geoms) if g.geom_type=='MultiLineString' else [g]
  lines=[[P(*c) for c in l.coords] for l in ls]
  main=max(ls,key=lambda l:l.length);lp=main.interpolate(0.5,normalized=True)
  src=NE
  if par: src+=f'; впадение в {dict((r[0],r[2]) for r in RV)[par]} проверено по геометрии'+(f', берег совпал с геометрией' if side else '')
  out.append(dict(id=rid,name=name,short=short,cat=cat,kind='line',ru=ru,xy=[P(lp.x,lp.y)],lines=lines,parent=par,side=side,src=src))
# peaks (NE elevation points; Veleta & Monte Perdido from GeoNames)
PK=[('teleno','El Teleno','Teleno','p_per',(-6.390019,42.349986),'Телено (Montes de León)',NE),
 ('cerredo','Torre Cerredo','Torre Cerredo','p_per',(-4.845041,43.194695),'Торре-Серредо (Picos de Europa)',NE),
 ('almanzor','Pico Almanzor','Almanzor','p_int',(-5.300012,40.260086),'Альмансор (Гредос, Система Сентраль)',NE),
 ('moncayo','Moncayo','Moncayo','p_per',(-1.839988,41.77998),'Монкайо (Иберийская система)',NE),
 ('aneto','Aneto','Aneto','p_ext',(0.663078,42.632202),'Ането (Пиренеи)',NE),
 ('perdido','Monte Perdido','Monte Perdido','p_ext',(0.034,42.675),'Монте-Пердидо (Пиренеи)','GeoNames, «Spain — Highest Mountains»'),
 ('mulhacen','Mulhacén','Mulhacén','p_ext',(-3.311373,37.051379),'Мулацен (Сьерра-Невада)',NE),
 ('veleta','Veleta','Veleta','p_ext',(-3.366,37.056),'Велета (Сьерра-Невада)','GeoNames, «Spain — Highest Mountains»'),
 ('puigmajor','Puig Major','Puig Major','p_ext',(2.795995,39.808467),'Пуч-Майор (Сьерра-де-Трамунтана, Мальорка)',NE),
 ('teide','Teide','Teide','p_ext',(-16.639099,28.270815),'Тейде (Тенерифе)',NE)]
for pid,name,short,cat,(lon,lat),ru,src in PK:
  out.append(dict(id=pid,name=name,short=short,cat=cat,kind='peak',ru=ru,xy=[P(lon,lat)],src=src))
# ranges: Natural Earth region polygons
RP={f['properties']['NAME_ES']:shape(f['geometry']) for f in json.load(open('ne_10m_geography_regions_polys.geojson'))['features'] if f['properties'].get('NAME_ES') in ('Cordillera Cantábrica','Sierra Morena','Pirineos')}
ZN=[('cantabrica','Cordillera Cantábrica','Cantábrica','z_per','Кантабрийские горы'),('morena','Sierra Morena','Sierra Morena','z_per','Сьерра-Морена'),('pirineos','Pirineos','Pirineos','z_ext','Пиренеи')]
for zid,name,short,cat,ru in ZN:
  g=RP[name].simplify(0.01);ps=[g] if g.geom_type=='Polygon' else list(g.geoms)
  d=''.join('M'+'L'.join(f'{a},{b}' for a,b in (P(*c) for c in p.exterior.coords))+'Z' for p in ps)
  rp=g.representative_point()
  out.append(dict(id=zid,name=name,short=short,cat=cat,kind='zone',ru=ru,xy=[P(rp.x,rp.y)],d=d,src='полигон «'+name+'», '+NE))
json.dump(out,open('objs3.json','w'),ensure_ascii=False)
print(len(out),'objects',len(json.dumps(out,ensure_ascii=False))//1024,'KB')
