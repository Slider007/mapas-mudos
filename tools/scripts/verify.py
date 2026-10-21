import json,re,math
from shapely.geometry import shape,Point
from shapely.ops import unary_union
d=json.load(open('c10.geojson'))
land=unary_union([shape(f['geometry']) for f in d['features'] if f['properties']['ADM0_A3'] in ('ESP','PRT','FRA','AND','MAR','GIB')])
esp=[shape(f['geometry']) for f in d['features'] if f['properties']['ADM0_A3']=='ESP'][0]
s=open('tpl.html').read()
block=s[s.index('const O=['):s.index('].map(([id')]
rows=re.findall(r"\['(\w+)','([^']+)','[^']+','(\w+)',(\[\[.*?\]\]),'(\w+)'",block)
km=lambda deg_lat,deg_lon,lat:math.hypot(deg_lat*111,deg_lon*111*math.cos(math.radians(lat)))
out=[]
for id,name,cat,pts,kind in rows:
  pts=json.loads(pts)
  for lon,lat in pts:
    p=Point(lon,lat)
    onland=land.contains(p)
    dc=land.boundary.distance(p)  # deg, rough
    dkm=dc*111*math.cos(math.radians(lat))**0.5
    out.append((id,name,kind,lon,lat,onland,round(dkm,1)))
for r in out:
  id,name,kind,lon,lat,onland,dk=r
  flag=''
  if kind=='pt' and dk>1.5: flag='!! мыс далеко от берега'
  if kind=='area' and onland: flag='!! точка акватории на суше'
  if kind=='isl' and not esp.contains(Point(lon,lat)): flag='!! вне острова'
  print(f"{name:28s} {kind:4s} {lat:7.3f} {lon:8.3f} land={onland!s:5} coast={dk:5.1f}km {flag}")
