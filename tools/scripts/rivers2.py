import json,math,pickle
from shapely.geometry import shape,Point,box,LineString,MultiLineString
from shapely.ops import linemerge,unary_union,nearest_points
es=pickle.load(open('es_hr.pkl','rb'))
seg=[]
for f in ['ne_10m_rivers_lake_centerlines','ne_10m_rivers_europe']:
  for x in json.load(open(f+'.geojson'))['features']:
    g=shape(x['geometry'])
    if g.intersects(box(-10,35.8,4.5,43.9)):seg.append((x['properties'].get('name'),g))
def get(names,flt=None):
  gs=[g for n,g in seg if n in names]
  parts=[]
  for g in gs:
    for l in (g.geoms if g.geom_type=='MultiLineString' else [g]):
      if flt is None or flt(l):parts.append(l)
  u=unary_union(parts)
  m=u if u.geom_type=="LineString" else linemerge(u)
  return m
R={ # id: (NE names, filter)
 'mino':(['Minho','Mio'],None),'sil':(['Sil'],None),'narcea':(['Narcea'],None),
 'duero':(['Duero'],None),'pisuerga':(['Pisuerga'],None),'esla':(['Esla'],None),'adaja':(['Adaja'],None),'tormes':(['Tormes'],None),
 'tajo':(['Tajo','Tejo'],None),'henares':(['Henares'],None),'alberche':(['Alberche'],None),'tietar':(['Tiétar'],None),
 'alagon':(['Alagón'],lambda l:l.centroid.x<-4),'guadiana':(['Guadiana'],None),'zancara':(['Zncara'],None),'zujar':(['Zújar'],None),
 'guadalquivir':(['Guadalquivir'],None),'guadalimar':(['Guadalimar'],None),'guadianamenor':(['Guadiana Menor'],None),'genil':(['Genil'],None),
 'ebro':(['Ebro'],None),'jalon':(['Jalón'],None),'jiloca':(['Jiloca'],None),'aragon':(['Alagón'],lambda l:l.centroid.x>-4),
 'cinca':(['Cinca'],None),'segre':(['Segre'],None),'mijares':(['Mijares'],None),'turia':(['Turia'],None),'jucar':(['Júcar'],None),
 'cabriel':(['Cabriel'],None),'segura':(['Segura'],None)}
G={k:get(*v) for k,v in R.items()}
for k,g in G.items(): print(k,g.geom_type,len(getattr(g,'geoms',[g])),round(g.length,2))
pickle.dump(G,open('rivers_ne.pkl','wb'))
