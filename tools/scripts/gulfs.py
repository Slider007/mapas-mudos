import json,math,pickle
from shapely.geometry import shape,Point,Polygon,LineString,box
from shapely.ops import unary_union,substring,nearest_points
es=pickle.load(open('es_hr.pkl','rb'))
C10={f['properties']['ADM0_A3']:shape(f['geometry']) for f in json.load(open('c10.geojson'))['features'] if f['properties']['ADM0_A3'] in ('PRT','FRA','MAR','GIB','AND')}
land=unary_union([es,*C10.values()])
iber=unary_union([es,C10['PRT'],C10['FRA'],C10['AND'],C10['GIB']]).buffer(0)
main=max(iber.geoms,key=lambda g:g.area) if iber.geom_type=='MultiPolygon' else iber
ring=LineString(main.exterior.coords)
MAR={}
for f in json.load(open('ne_10m_geography_marine_polys.geojson'))['features']:
  n=f['properties'].get('name_es')
  if n:MAR.setdefault(n,[]).append(shape(f['geometry']))
L=lambda lat,lon:(lon,lat)
H=dict(SV=(-8.969,37.038),TRAF=L(36.18289,-6.03510),SAB=L(36.68685,-2.70129),GATA=L(36.72165,-2.19288),TIN=L(37.53543,-1.10810),COPE=(-1.492981731,37.427978027),
 SPOLA=L(38.20951,-0.51367),HUER=L(38.35299,-0.4049),NAO=L(38.73284,0.230005),TORT=L(40.7155,0.92847),SALOU=L(41.05573,1.17204),NORF=(3.2648470,42.2423940))
def arcpoly(a,b):
  pa=ring.project(Point(a));pb=ring.project(Point(b))
  s1=substring(ring,min(pa,pb),max(pa,pb))
  # choose the shorter arc
  if s1.length>ring.length/2:
    s1=LineString(list(substring(ring,max(pa,pb),ring.length).coords)+list(substring(ring,0,min(pa,pb)).coords))
  pts=list(s1.coords)
  poly=Polygon(pts+[pts[0]]).buffer(0)
  sea=poly.difference(land).buffer(-0.002).buffer(0.002)
  if sea.geom_type=='MultiPolygon':sea=max(sea.geoms,key=lambda g:g.area)
  return sea,s1.length
# Roses south limit: coast point 16 km south of Norfeu (Wikipedia: bay 16 km wide)
cand=[ring.interpolate(t) for t in [i*0.0005*ring.length for i in range(2000)]]
nor=Point(H['NORF'])
south=[p for p in cand if p.y<nor.y-0.05 and p.x>2.9 and p.x<3.4 and p.y>41.9]
def km(p,q):return math.hypot((p.x-q.x)*111*math.cos(math.radians(42)),(p.y-q.y)*111)
rs=min(south,key=lambda p:abs(km(p,nor)-16))
print('Roses south point',round(rs.x,3),round(rs.y,3),'km',round(km(rs,nor),1))
G={}
for k,(a,b,src) in {'cadiz':('SV','TRAF','границы: м. Сан-Висенти — м. Трафальгар (es.wikipedia, Britannica)'),
 'alme':('SAB','GATA','границы: Пунта-Сабинар — м. Гата (en.wikipedia «Gulf of Almería»)'),
 'mazar':('TIN','COPE','границы: м. Тиньосо — м. Копе (es.wikipedia; координаты Копе — вершина IGN)'),
 'alic':('SPOLA','HUER','границы: м. Санта-Пола — м. Уэрта (es.wikipedia «Bahía de Alicante»)'),
 'valen':('NAO','TORT','границы: м. Нао — м. Тортоса (es.wikipedia «Golfo de Valencia»)'),
 'jorge':('TORT','SALOU','границы: м. Тортоса — м. Салоу (лоция sea-seek)')}.items():
  sea,al=arcpoly(H[a],H[b]);G[k]=(sea,src);print(k,round(sea.area,4),sea.geom_type,'arc°',round(al,2))
sea,al=arcpoly(H['NORF'],(rs.x,rs.y));G['roses']=(sea,'границы: м. Норфеу — берег в 16 км южнее (ширина залива 16 км, en.wikipedia «Gulf of Roses»)');print('roses',round(sea.area,4))
frame=box(-11.5,33,6.2,45.2)
viz=unary_union(MAR['Golfo de Vizcaya']).intersection(frame).intersection(box(-3.0,43,6,46)).difference(land)
G['vizc']=(viz,'восточная часть полигона «Golfo de Vizcaya» Natural Earth (западнее — Mar Cantábrico)')
leo=unary_union(MAR['Golfo de León']).intersection(frame).difference(land);G['leon']=(leo,'полигон «Golfo de León» Natural Earth')
LON0,LAT1,K=-10.9,44.6,100;C=math.cos(math.radians(40))
P=lambda x,y:f'{(x-LON0)*K*C:.1f},{(LAT1-y)*K:.1f}'
out={}
for k,(g,src) in G.items():
  g=g.simplify(0.004);ps=[g] if g.geom_type=='Polygon' else [p for p in g.geoms if p.area>0.0003]
  d=''.join('M'+'L'.join(P(*c) for c in p.exterior.coords)+'Z' for p in ps)
  rp=max(ps,key=lambda p:p.area).representative_point()
  out[k]=dict(d=d,xy=[[round((rp.x-LON0)*K*C,1),round((LAT1-rp.y)*K,1)]],src=src)
json.dump(out,open('gulfs.json','w'),ensure_ascii=False);print({k:len(v['d']) for k,v in out.items()})
