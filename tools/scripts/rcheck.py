import pickle,math
from shapely.geometry import Point,LineString
from shapely.ops import nearest_points,linemerge
G=pickle.load(open('rivers_ne.pkl','rb'));es=pickle.load(open('es_hr.pkl','rb'))
def lines(g):return list(g.geoms) if g.geom_type=='MultiLineString' else [g]
def ends(g):
  e=[]
  for l in lines(g):e+=[Point(l.coords[0]),Point(l.coords[-1])]
  return e
km=lambda d,lat=40:d*111*math.cos(math.radians(lat))**.5
DOC={'pisuerga':('duero','D'),'esla':('duero','D'),'adaja':('duero','I'),'tormes':('duero','I'),
 'henares':('tajo','D'),'alberche':('tajo','D'),'tietar':('tajo','D'),'alagon':('tajo','D'),
 'zancara':('guadiana','D'),'zujar':('guadiana','I'),
 'guadalimar':('guadalquivir','D'),'guadianamenor':('guadalquivir','I'),'genil':('guadalquivir','I'),
 'jalon':('ebro','D'),'jiloca':('ebro','D'),'aragon':('ebro','I'),'cinca':('ebro','I'),'segre':('ebro','I'),
 'sil':('mino',None),'cabriel':('jucar',None)}
# mouth of main rivers: endpoint closest to sea
coast=es.boundary
def flowdir(main,pt):
  # direction downstream near pt: find nearest line, orient so last coord is the end nearer coast/ further downstream
  best=min(lines(main),key=lambda l:l.distance(pt))
  a,b=Point(best.coords[0]),Point(best.coords[-1])
  # downstream end: whichever closer to the main river's global mouth
  allends=ends(main);mouth=min(allends,key=lambda p:p.distance(coast) if es.contains(p) else 0)
  d=best.project(pt); s=max(0,d-0.05); t=min(best.length,d+0.05)
  p1,p2=best.interpolate(s),best.interpolate(t)
  if a.distance(mouth)<b.distance(mouth): p1,p2=p2,p1
  return (p2.x-p1.x)*math.cos(math.radians(pt.y)),p2.y-p1.y
for t,(par,side) in DOC.items():
  trib=G[t];main=G[par]
  e=ends(trib);j=min(e,key=lambda p:p.distance(main));dist=km(j.distance(main))
  far=max(e,key=lambda p:p.distance(j))  # upstream point
  dx,dy=flowdir(main,j)
  # vector from junction to tributary point ~0.2 deg upstream along trib
  tl=min(lines(trib),key=lambda l:l.distance(j));pj=tl.project(j);q=tl.interpolate(pj+0.15 if pj<0.01 else pj-0.15)
  vx,vy=(q.x-j.x)*math.cos(math.radians(j.y)),q.y-j.y
  cr=dx*vy-dy*vx; geo='I' if cr>0 else 'D'
  print(f"{t:14s} → {par:12s} стык {dist:5.1f} км  док:{side}  геом:{geo}  {'OK' if side in (None,geo) else '!!'}")
