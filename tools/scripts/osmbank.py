import pickle,math
from shapely.geometry import Point,MultiPoint
from shapely.ops import unary_union,nearest_points
exec(open('osmriv2.py').read().split('OUT={}')[0])
P=pickle.load(open('osm_pick2.pkl','rb'))
P['Noguera Ribagorzana']=unary_union([g for c in comps['Noguera Ribagorzana'] for g in c.geoms])
pickle.dump(P,open('osm_pick2.pkl','wb'))
MOUTH={'Duero':(-8.67,41.14),'Tajo':(-9.3,38.7),'Guadiana':(-7.4,37.18),'Guadalquivir':(-6.4,36.8),'Ebro':(0.86,40.72),'Miño':(-8.87,41.87),'Nalón':(-6.08,43.56),'Júcar':(-0.25,39.17)}
DOC={'Pisuerga':'D','Arlanzón':'D','Carrión':'D','Esla':'D','Bernesga':'D','Eresma':'I','Adaja':'I','Tormes':'I',
 'Jarama':'D','Henares':'D','Alberche':'D','Tiétar':'D','Alagón':'D','Almonte':'I','Salor':'I',
 'Záncara':'D','Cigüela':'D','Jabalón':'I','Zújar':'I','Matachel':'I',
 'Guadalimar':'D','Jándula':'D','Guadalmellato':'D','Guadiato':'D','Bembézar':'D','Viar':'D','Guadiana Menor':'I','Guadalbullón':'I','Genil':'I',
 'Jalón':'D','Jiloca':'D','Huerva':'D','Guadalope':'D','Arga':'I','Aragón':'I','Gállego':'I','Cinca':'I','Noguera Pallaresa':'I','Noguera Ribagorzana':'I','Segre':'I'}
def verts(g):
  ls=list(g.geoms) if hasattr(g,'geoms') else [g]
  return [p for l in ls for p in l.coords]
def first_order(n):
  chain=[n]
  while REC.get(chain[-1]) and REC[chain[-1]] not in MOUTH: chain.append(REC[chain[-1]])
  return chain[-1],REC.get(chain[-1]),chain
res={}
for n,doc in DOC.items():
  f,main,chain=first_order(n)
  M=P[main];T=P[f]
  j=nearest_points(M,T)[0]
  cl=math.cos(math.radians(j.y));D=lambda a,b:math.hypot((a[0]-b[0])*cl,a[1]-b[1])*111
  mv=[v for v in verts(M) if 2<D(v,(j.x,j.y))<7]
  if len(mv)<2: mv=[v for v in verts(M) if 1<D(v,(j.x,j.y))<15]
  # split into two directions by sign of projection on principal axis
  import statistics
  ax=max(mv,key=lambda v:D(v,(j.x,j.y)));A=[v for v in mv if D(v,ax)<D(v,(j.x,j.y))];B=[v for v in mv if v not in A]
  cA=(sum(v[0] for v in A)/len(A),sum(v[1] for v in A)/len(A));cB=(sum(v[0] for v in B)/len(B),sum(v[1] for v in B)/len(B)) if B else (j.x,j.y)
  mo=MOUTH[main];down,upp=(cA,cB) if D(cA,mo)<D(cB,mo) else (cB,cA)
  dx,dy=(down[0]-upp[0])*cl,down[1]-upp[1]
  tv=[v for v in verts(T) if 3<D(v,(j.x,j.y))<20] or verts(T)
  c=(sum(v[0] for v in tv)/len(tv),sum(v[1] for v in tv)/len(tv));vx,vy=(c[0]-j.x)*cl,c[1]-j.y
  geo='I' if dx*vy-dy*vx>0 else 'D'
  res[n]=(main,geo,chain)
  print(f"{n:20s} → {main:12s} через {'→'.join(chain)}  док:{doc} геом:{geo} {'OK' if doc==geo else '!!'}")
pickle.dump(res,open('osm_bank.pkl','wb'))
