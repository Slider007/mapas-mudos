import json,math,pickle,re
from shapely.geometry import shape,box,Point,MultiPolygon,LineString
from shapely.ops import unary_union,nearest_points
es=pickle.load(open('es_hr.pkl','rb'))            # IGN-derived (AlexGPlay/SpainLayers)
C10={f['properties']['ADM0_A3']:shape(f['geometry']) for f in json.load(open('c10.geojson'))['features'] if f['properties']['ADM0_A3'] in ('PRT','FRA','AND','MAR','GIB','DZA')}
_M={}
for f in json.load(open('ne_10m_geography_marine_polys.geojson'))['features']:
  n=f['properties'].get('name_es')
  if n:_M.setdefault(n,[]).append(shape(f['geometry']))
MAR={n:unary_union(v) for n,v in _M.items()}
LON0,LON1,LAT0,LAT1=-10.9,5.6,33.4,44.6;K=100;C=math.cos(math.radians(40))
def pm(lon,lat):return((lon-LON0)*K*C,(LAT1-lat)*K)
W,H=pm(LON1,LAT0)
CL0,CL1,CA0,CA1=-18.4,-13.2,27.5,29.5;CC=math.cos(math.radians(28.5))
IX,IY=14,H-14-(CA1-CA0)*K
def pc(lon,lat):return(IX+(lon-CL0)*K*CC,IY+(CA1-lat)*K)
def path(g,f,tol):
  g=g.simplify(tol,preserve_topology=True);ps=[g] if g.geom_type=='Polygon' else list(g.geoms);o=[]
  for p in ps:
    if p.is_empty or p.geom_type!='Polygon':continue
    for r in [p.exterior]+list(p.interiors):o.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in (f(*c) for c in r.coords))+'Z')
  return ''.join(o)
frame=box(LON0-.5,LAT0-.5,LON1+.5,LAT1+.5)
res={'W':round(W),'H':round(H),'inset':[IX,IY,round((CL1-CL0)*K*CC,1),(CA1-CA0)*K],'land':{}}
for k,g in C10.items():
  gg=g.intersection(frame)
  if not gg.is_empty:res['land'][k]=path(gg,pm,0.004)
# ---- sources ----
LH='Wikipedia «List of lighthouses in Spain» (Rowlett, Lighthouse Directory)'
SRC={}
def L(lat,lon):return(lon,lat)
light={ # lighthouse coords from the Wikipedia list
 'machi':L(43.45419,-2.75270),'ajo':L(43.51155,-3.59529),'penas':L(43.65559,-5.84856),'orte':L(43.77107,-7.87018),
 'prior':L(43.56761,-8.31453),'touri':L(43.05336,-9.29814),'finis':L(42.88236,-9.27196),'gata':L(36.72165,-2.19288),
 'palos':L(37.63468,-0.69026),'nao':L(38.73284,0.230005),'creus':L(42.31891,3.31592),'bares':L(43.78623,-7.68430),'tarifa':L(36.00118,-5.60962)}
isl_light={'mallorca':L(39.96145,3.21271),'menorca':L(40.08909,4.09227),'ibiza':L(38.90416,1.45388),'formentera':L(38.66337,1.58430),
 'cabrera':L(39.12919,2.92145),'gran_canaria':L(28.17408,-15.41897),'fuerteventura':L(28.04613,-14.333),'lanzarote':L(28.85575,-13.87259),
 'tenerife':L(28.58132,-16.14003),'la_gomera':L(28.09609,-17.10007),'la_palma':L(28.45528,-17.84308),'el_hierro':L(27.70666,-18.14758)}
islname={'mallorca':'Formentor','menorca':'Cavalleria','ibiza':'Botafoc','formentera':'La Mola','cabrera':"N'Ensiola",'gran_canaria':'La Isleta','fuerteventura':'Morro Jable','lanzarote':'Punta Pechiguera','tenerife':'Punta de Anaga','la_gomera':'San Cristóbal','la_palma':'Fuencaliente','el_hierro':'Punta Orchilla'}
mid=lambda a,b,t=.5:(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
SV=(-8.969,37.038);TRAF=L(36.18289,-6.03510);SAB=L(36.68685,-2.70129);SPOLA=L(38.20951,-0.51367);HUER=L(38.35299,-0.4049)
TORT=L(40.7155,0.92847);SALOU=L(41.05573,1.17204);NAO=light['nao'];VALP=L(39.44910,-0.30223);TIN=L(37.53543,-1.10810);MAZL=L(37.56045,-1.25444)
gulf={
 'cadiz':(mid(SV,TRAF),'середина линии м. Сан-Висенти — м. Трафальгар (границы залива: es.wikipedia, Britannica)'),
 'alme':(mid(SAB,light['gata']),'середина линии Пунта-Сабинар — м. Гата (en.wikipedia «Gulf of Almería»)'),
 'alic':(mid(SPOLA,HUER),'середина линии м. Санта-Пола — м. Уэрта (es.wikipedia «Bahía de Alicante»)'),
 'valen':(mid(VALP,mid(NAO,TORT)),'между портом Валенсии и серединой линии м. Нао — м. Тортоса (es.wikipedia «Golfo de Valencia»)'),
 'jorge':(mid(TORT,SALOU),'середина линии м. Тортоса — м. Салоу (лоция sea-seek)'),
 'mazar':(mid(MAZL,TIN,0.35),'у маяка Масаррона, внутри залива м. Тиньосо — м. Копе (es.wikipedia «Puerto de Mazarrón»)'),
 'roses':(L(42.183,3.183),'координаты залива из en.wikipedia «Gulf of Roses»'),
}
def inmar(name,lon,lat):return MAR[name].contains(Point(lon,lat))
marine={
 'atl':([(-8.4,36.45),(-10.2,40.3),(-10.3,42.5)],'océano Atlántico'),
 'med':([(1.4,37.5),(4.2,41.1),(-1.2,36.6)],None),
 'vizc':([(-2.2,44.2)],'Golfo de Vizcaya'),
 'leon':([(4.1,42.95)],'Golfo de León'),
 'gibr':([(-5.652,35.974)],'Estrecho de Gibraltar'),
 'cant':([(-5.4,44.05),(-7.0,44.05)],'Golfo de Vizcaya'),
}
out={}
for k,(lon,lat) in light.items():
  q=nearest_points(es.boundary,Point(lon,lat))[0]
  d=Point(lon,lat).distance(q)*111*math.cos(math.radians(lat))
  out[k]={'pts':[[round(q.x,4),round(q.y,4)]],'src':f'маяк, {lat:.4f}, {lon:.4f} — {LH}','snap_km':round(d,2)}
for k,(pt,s) in gulf.items():
  p=Point(*pt);ok=not es.contains(p) and not any(g.contains(p) for g in C10.values())
  out[k]={'pts':[[round(pt[0],3),round(pt[1],3)]],'src':s,'sea':ok}
for k,(pts,poly) in marine.items():
  chk=[]
  for lon,lat in pts:
    if poly: chk.append(inmar(poly,lon,lat))
    else: chk.append(any(inmar(n,lon,lat) for n in ('Mediterráneo','mar Balear','mar de Alborán')))
  src={'atl':'внутри полигона «océano Atlántico» Natural Earth','med':'внутри полигонов Средиземного / Балеарского / Альборанского морей Natural Earth',
   'vizc':'внутри полигона «Golfo de Vizcaya» Natural Earth','leon':'внутри полигона «Golfo de León» Natural Earth',
   'gibr':'центр полигона «Estrecho de Gibraltar» Natural Earth','cant':'южная, испанская часть полигона «Golfo de Vizcaya» Natural Earth'}[k]
  out[k]={'pts':pts,'src':src,'inside':chk}
# islands from IGN polygons, identified by the island's lighthouse
polys=list(es.geoms)
used=set();islpaths={}
for k,(lon,lat) in isl_light.items():
  p=Point(lon,lat);cand=[g for g in polys if g.distance(p)<0.03];best=max(cand,key=lambda g:g.area)
  f=pc if lon<-12.5 else pm
  islpaths[k]=path(best,f,0.0015);used.add(id(best))
  c=best.representative_point()
  out[k]={'pts':[[round(c.x,3),round(c.y,3)]],'src':f'полигон острова IGN, опознан по маяку {islname[k]} ({lat:.4f}, {lon:.4f})','dist_km':round(best.distance(p)*111,2),'area':round(best.area,4)}
rest=[g for g in polys if id(g) not in used]
main=MultiPolygon([g for g in rest if g.centroid.x>-12.5]);can=[g for g in rest if g.centroid.x<=-12.5]
res['spain']=path(main.intersection(frame),pm,0.0015)
res['canx']=path(MultiPolygon(can),pc,0.0015) if can else ''
res['isl']=islpaths
json.dump(res,open('geo2.json','w'));json.dump(out,open('objs.json','w'),ensure_ascii=False,indent=0)
print('geo size',len(json.dumps(res)))
for k,v in out.items():print(k,{a:b for a,b in v.items() if a!='src'})
