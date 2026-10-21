import json
from shapely.geometry import Polygon,MultiPolygon
from shapely.ops import unary_union
def load(fn,obj):
  t=json.load(open(fn));sx,sy=t['transform']['scale'];tx,ty=t['transform']['translate']
  arcs=[]
  for a in t['arcs']:
    x=y=0;pts=[]
    for dx,dy in a: x+=dx;y+=dy;pts.append((x*sx+tx,y*sy+ty))
    arcs.append(pts)
  def arc(i): return arcs[i] if i>=0 else arcs[~i][::-1]
  def ring(r):
    pts=[]
    for i in r: a=arc(i); pts.extend(a if not pts else a[1:])
    return pts
  out=[]
  for g in t['objects'][obj]['geometries']:
    polys=[g['arcs']] if g['type']=='Polygon' else g['arcs']
    ps=[Polygon(ring(p[0]),[r for r in (ring(h) for h in p[1:]) if len(r)>=4]) for p in polys if len(ring(p[0]))>=4]
    out.append((g.get('id'),g.get('properties',{}),MultiPolygon([p.buffer(0) if not p.is_valid else p for p in ps]) if len(ps)>1 else ps[0].buffer(0)))
  return out
