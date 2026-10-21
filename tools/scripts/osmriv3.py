import pickle,math,json
from shapely.geometry import MultiLineString,LineString,Point,box
from shapely.ops import unary_union,linemerge
exec(open('osmriv2.py').read().split('OUT={}')[0])
P=pickle.load(open('osm_pick.pkl','rb'))
# grow picks with nearby clusters of the same name (reservoir gaps)
for n in list(P):
  if P[n] is None or n not in comps:continue
  cs=clusters([g for c in comps[n] for g in c.geoms]);cur=P[n]
  changed=True
  while changed:
    changed=False
    for c in cs:
      if c.length>0 and not c.within(cur.buffer(1e-6)) and KM(c,cur)<15 and c.distance(cur)>0:
        cur=unary_union([cur,c]);changed=True
  if cur.length>P[n].length+1e-6:print('дополнено',n,round(P[n].length,2),'→',round(cur.length,2))
  P[n]=cur
P['Segre']=unary_union([P['Segre'],NE['segre']]) ;print('Segre: OSM нижнее течение + Natural Earth')
for n,k in [('Duero','duero'),('Tajo','tajo'),('Miño','mino'),('Guadiana','guadiana')]:
  print(n,'запад до',round(P[n].bounds[0],2))
  if P[n].bounds[0]>-8.6:
    ext=NE[k].difference(es.buffer(0.01))
    P[n]=unary_union([P[n],ext]);print('  + португальская часть из Natural Earth, теперь до',round(P[n].bounds[0],2))
pickle.dump(P,open('osm_pick2.pkl','wb'))
for n in ['Cinca','Noguera Pallaresa','Noguera Ribagorzana','Segura','Llobregat']:
  print(n,'длина',round(P[n].length,2),'до приёмника',(round(KM(P[n],P[REC[n]]),1) if n in REC else '-'))
