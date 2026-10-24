# Границы для тренажёра «Carolingios» из данных Cliopatria (Seshat Global History Databank, CC BY 4.0).
import json
from shapely.geometry import shape, box, Polygon
from shapely.ops import unary_union
import sys
# Вход: GeoJSON Cliopatria (github.com/Seshat-Global-History-Databank/cliopatria, CC BY 4.0), распакованный cliopatria.geojson.zip
# Запуск: python3 carolingios_geo.py путь/к/cliopatria_polities_only_v021.geojson  → carolingios_geo.json рядом со скриптом
src=json.load(open(sys.argv[1]))
_fr=box(-14,33,34,60)
R={}
for y in (768,814,850):
    R[str(y)]={}
    for f in src['features']:
        p=f['properties']
        if p['FromYear']<=y<=p['ToYear'] and not p['Name'].startswith('('):
            g=shape(f['geometry']).buffer(0).intersection(_fr)
            if not g.is_empty: R[str(y)][p['Name']]=g.__geo_interface__
frame=box(-14,33,34,60)
def polys(g): return [p for p in (list(g.geoms) if hasattr(g,'geoms') else [g]) if p.geom_type=='Polygon']
def G(y,n): return shape(R[str(y)][n]).buffer(0)
def grow(y,names,d=0.15):
    """polity + nearby land not claimed by any other polity that year (fills coastline mismatch)"""
    g=unary_union([G(y,n) for n in names])
    others=unary_union([shape(v).buffer(0) for k,v in R[str(y)].items() if k not in names])
    return unary_union([g,g.buffer(d).difference(others)]).intersection(frame)
def rings(g,tol=0.02,mina=0.01):
    g=g.simplify(tol,preserve_topology=True); out=[]
    for p in polys(g):
        if p.area<mina: continue
        r=[[round(x,2),round(y,2)] for x,y in p.exterior.coords]
        out.append([r[0]]+[q for i,q in enumerate(r[1:],1) if q!=r[i-1]])
    return out
res={}
f768=grow(768,['Kingdom of the Franks']); f814=grow(814,['Kingdom of the Franks'])
pap=grow(814,['Papal States'])
res['f768']=rings(f768.difference(pap))
res['conq']=rings(f814.difference(f768).difference(pap))
res['pap']=rings(pap)
res['byz']=rings(grow(814,['Byzantine Empire']))
res['and']=rings(grow(814,['Emirate of Córdoba']))
res['ast']=rings(grow(814,['Kingdom of Asturias']))
res['isl']=rings(grow(814,['Aghlabid Dynasty','Idrisids','Rustamid dynasty','Emirate of Nekor']))
res['emp814']=rings(f814)
# Verdun (Cliopatria 850-859 snapshot)
W=unary_union([grow(850,['West Franks']),grow(850,['Viking settlements']).intersection(box(-5,42.5,8,51.5))])  # Burdeos: en 850 asentamiento vikingo, en 843 de Carlos el Calvo
M=grow(850,['Middle Franks']); E=grow(850,['East Franks']); P=grow(850,['Papal States'])
res['carlos']=rings(W); res['lotario']=rings(M.difference(P)); res['luis']=rings(E); res['pap850']=rings(P)
for k,v in res.items(): print(k,len(v),sum(map(len,v)))

# --- following the textbook (map 12): Aquitania/Gascuña inside the Frankish kingdom; marches as their own layer
f768b=unary_union([f768,grow(768,['Duchy of Gascony'])]).difference(pap)
conqb=f814.difference(f768b).difference(pap)
res['f768']=rings(f768b); res['conq']=rings(conqb)
B=lambda pts: Polygon(pts)
def band(win,d):
    """марка = полоса вдоль внешней границы империи 814 г. внутри окна win"""
    return f814.intersection(f814.boundary.buffer(d)).intersection(win)
marcas={
 'm_hisp': f814.intersection(box(-2.5,40.5,3.6,42.72)),
 'm_bret': band(box(-2.4,47.0,-0.6,48.9),0.55).intersection(f768b),
 'm_dan':  band(box(8.0,53.55,11.6,55.4),0.55),
 'm_sor':  band(box(10.9,50.2,13.6,53.2),0.75),
 'm_este': band(box(13.9,47.45,17.6,49.3),0.85),
 'm_pan':  band(box(15.2,45.2,19.6,47.45),0.95),
 'm_fri':  band(box(12.7,44.8,15.6,46.75),0.7),
}
for k,g in marcas.items(): res[k]=rings(g,mina=0.001)
res['mar']=rings(unary_union(list(marcas.values())),mina=0.001)
res['sajonia']=rings(conqb.intersection(box(6.5,51.0,12.5,55.5)))
res['lombardia']=rings(conqb.intersection(box(6.5,43.6,13.9,46.8)))
res['baviera']=rings(conqb.intersection(box(10.0,47.2,14.0,49.6)))
for k in ['f768','conq','mar','sajonia','lombardia','baviera']: print(k,len(res[k]),sum(map(len,res[k])))
json.dump(res,open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'carolingios_geo.json'),'w'),separators=(',',':'))
