import json,math,pickle
from shapely.geometry import shape,Point,box,MultiLineString,LineString
from shapely.ops import linemerge,unary_union
es=pickle.load(open('es_hr.pkl','rb'))
feats=[]
for f in ['ne_10m_rivers_lake_centerlines','ne_10m_rivers_europe']:
  for x in json.load(open(f+'.geojson'))['features']:
    g=shape(x['geometry'])
    if g.intersects(box(-10,35.8,4.5,43.9)):
      p=x['properties'];feats.append((p.get('name'),p.get('name_es'),p.get('featurecla'),g,f))
by={}
for n,ne,c,g,f in feats:
  key=n or ne
  by.setdefault(key,[]).append((ne,g,f))
for k,v in sorted(by.items(),key=lambda a:str(a[0])):
  g=unary_union([x[1] for x in v])
  print(f"{str(k):18s} es={v[0][0]!s:14s} n={len(v)} len={g.length:.2f} bounds={[round(b,2) for b in g.bounds]}")
