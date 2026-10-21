import json,re,math,pickle,collections
from shapely.geometry import LineString,MultiLineString,Point
from shapely.ops import linemerge,unary_union
d=json.load(open('osm/rivers.json'))
BAD=re.compile(r'cauce antiguo|viejo|ramal|subord|empord|madre del',re.I)
ALIAS={'millars':'Mijares','nerbioi ibaia':'Nervión','nerbioi':'Nervión','gigüela':'Cigüela','xúquer':'Júcar','túria':'Turia','minho':'Miño'}
def norm(n):
  if not n or BAD.search(n):return None
  n=n.split(';')[0].split(' - ')[0].strip()
  n=re.sub(r'^(r[ií]o|riu)\s+','',n,flags=re.I).strip()
  n=ALIAS.get(n.lower(),n)
  return n[0].upper()+n[1:]
groups=collections.defaultdict(list)
for e in d['elements']:
  if e['type']!='way' or 'geometry' not in e:continue
  t=e.get('tags',{});n=norm(t.get('name:es')) or norm(t.get('name'))
  if not n:continue
  groups[n].append(LineString([(p['lon'],p['lat']) for p in e['geometry']]))
comps={}
for n,ls in groups.items():
  u=unary_union(ls)
  m=u if u.geom_type=="LineString" else linemerge(u)
  parts=list(m.geoms) if m.geom_type=='MultiLineString' else [m]
  # cluster parts that touch within ~300 m
  cl=[]
  for p in sorted(parts,key=lambda g:-g.length):
    for c in cl:
      if any(p.distance(q)<0.003 for q in c):c.append(p);break
    else:cl.append([p])
  comps[n]=[MultiLineString(c) for c in cl]
pickle.dump(comps,open('osm_comps.pkl','wb'))
for n in sorted(comps):print(f"{n:22s} comps={len(comps[n]):3d} top={[round(c.length,2) for c in sorted(comps[n],key=lambda g:-g.length)[:4]]}")
