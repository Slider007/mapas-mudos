import pickle,math,json
from shapely.geometry import MultiLineString,LineString,Point
from shapely.ops import unary_union
comps=pickle.load(open('osm_comps.pkl','rb'));es=pickle.load(open('es_hr.pkl','rb'));NE=pickle.load(open('rivers_ne.pkl','rb'))
coast=es.boundary
KM=lambda g1,g2:g1.distance(g2)*111*0.77
REC={'Sil':'Miño','Narcea':'Nalón','Arlanzón':'Pisuerga','Carrión':'Pisuerga','Pisuerga':'Duero','Bernesga':'Esla','Esla':'Duero','Eresma':'Adaja','Adaja':'Duero','Tormes':'Duero',
 'Henares':'Jarama','Jarama':'Tajo','Alberche':'Tajo','Tiétar':'Tajo','Alagón':'Tajo','Almonte':'Tajo','Salor':'Tajo',
 'Záncara':'Cigüela','Cigüela':'Guadiana','Jabalón':'Guadiana','Zújar':'Guadiana','Matachel':'Guadiana',
 'Guadalimar':'Guadalquivir','Jándula':'Guadalquivir','Guadalmellato':'Guadalquivir','Guadiato':'Guadalquivir','Bembézar':'Guadalquivir','Viar':'Guadalquivir',
 'Guadiana Menor':'Guadalquivir','Guadalbullón':'Guadalquivir','Genil':'Guadalquivir',
 'Jalón':'Ebro','Jiloca':'Jalón','Huerva':'Ebro','Guadalope':'Ebro','Arga':'Aragón','Aragón':'Ebro','Gállego':'Ebro','Cinca':'Segre','Noguera Pallaresa':'Segre','Noguera Ribagorzana':'Segre','Segre':'Ebro','Cabriel':'Júcar'}
SEA=['Miño','Ulla','Tambre','Eo','Navia','Nalón','Besaya','Nervión','Bidasoa','Duero','Tajo','Guadiana','Guadalquivir','Odiel','Tinto','Guadalete','Barbate','Ter','Llobregat','Ebro','Mijares','Turia','Júcar','Segura','Almanzora','Andarax','Adra','Guadalfeo','Guadalhorce','Guadiaro']
def clusters(parts,th=0.06):
  cl=[]
  for p in sorted(parts,key=lambda g:-g.length):
    hit=[c for c in cl if any(p.distance(q)<th for q in c)]
    if hit:
      base=hit[0]
      for h in hit[1:]:base.extend(h);cl.remove(h)
      base.append(p)
    else:cl.append([p])
  return [unary_union(c) for c in cl]
OUT={}
order=SEA+[r for r in REC if r not in SEA]
# process mains first, then tributaries in dependency order
done=set()
def proc(n):
  if n in done:return
  if n in REC and REC[n] not in done:proc(REC[n])
  done.add(n)
  if n not in comps:OUT[n]=None;print(f'{n:20s} НЕТ В OSM');return
  cs=clusters([g for c in comps[n] for g in c.geoms])
  if n in REC and OUT.get(REC[n]) is not None:
    tgt=OUT[REC[n]];ok=[c for c in cs if KM(c,tgt)<3]
    pick=max(ok or cs,key=lambda g:g.length);info=f'впадение в {REC[n]}: {KM(pick,tgt):.1f} км'+('' if ok else ' !! НЕ КАСАЕТСЯ')
  else:
    ok=[c for c in cs if KM(c,coast)<4]
    pick=max(ok or cs,key=lambda g:g.length);info=f'до моря/границы {KM(pick,coast):.1f} км'
  OUT[n]=pick
  print(f'{n:20s} кластеров={len(cs):2d} длина={pick.length:5.2f}° (всего {sum(c.length for c in cs):5.2f}) {info}')
for n in order:proc(n)
pickle.dump(OUT,open('osm_pick.pkl','wb'))
