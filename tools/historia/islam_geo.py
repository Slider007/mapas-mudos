# Границы для тренажёра «El islam» (тема 2) из Cliopatria (Seshat Global History Databank, CC BY 4.0).
# Запуск: python3 islam_geo.py cliopatria_polities_only_v021.geojson ne_10m_land.geojson → islam_geo.json рядом со скриптом
import json, sys, os
from shapely.geometry import shape, box
from shapely.ops import unary_union
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from andalus_geo_util import smooth, rings
src = json.load(open(sys.argv[1]))['features']
FR = box(-13, 5, 81, 51)
LAND = unary_union([shape(f['geometry']).intersection(FR) for f in json.load(open(sys.argv[2]))['features']]).buffer(0.08)
def pol(y, name):
    g = [shape(f['geometry']).buffer(0) for f in src if f['properties']['Name'] == name and f['properties']['FromYear'] <= y <= f['properties']['ToYear']]
    if not g: raise SystemExit(f'no {name} in {y}')
    return unary_union(g).intersection(FR).intersection(LAND)
res = {}
# Arabia y sus vecinos hacia el 600–630
s = smooth({'byz': pol(630, 'Eastern Roman Empire'), 'per': pol(630, 'Sasanian Empire'), 'gha': pol(630, 'Ghassanids'), 'lak': pol(630, 'Lakhmid Kingdom')}, tol=0.15)
res['byz600'] = rings(s['byz'], 0.02, 0.05); res['per600'] = rings(s['per'], 0.02, 0.05)
from shapely.geometry import Polygon
ARABIA = Polygon([(34.2, 29.6), (35.0, 28.0), (39.0, 22.0), (42.8, 12.6), (44.0, 12.4), (52.0, 15.0), (60.5, 22.5), (56.5, 26.6), (51.0, 24.0), (48.0, 29.5), (47.6, 30.6), (44.0, 32.0), (39.0, 32.2), (35.2, 31.6)])
arab = ARABIA.intersection(LAND).difference(unary_union([s['byz'], s['per']]))
res['arab'] = rings(arab, 0.02, 0.05)
# Expansión: 632 (Rashidun 633), 661 (Rashidun 656–660), 750 (omeyas 718–723: máxima extensión)
e632 = pol(633, 'Rashidun Caliphate'); e661 = unary_union([pol(658, 'Rashidun Caliphate'), pol(658, 'Umayyad Caliphate')]); e750 = pol(720, 'Umayyad Caliphate').difference(box(26, 37.6, 41.6, 43))  # sin la franja de Anatolia (incursiones, no dominio)
s = smooth({'a': e632, 'b': e661.difference(e632), 'c': e750.difference(e661).difference(e632)}, tol=0.15)
res['e632'] = rings(s['a'], 0.02, 0.05); res['e661'] = rings(s['b'], 0.02, 0.05); res['e750'] = rings(s['c'], 0.02, 0.05)
res['all750'] = rings(unary_union(list(s.values())), 0.02, 0.05)
s = smooth({'byz': pol(720, 'Byzantine Empire'), 'fra': unary_union([pol(720, 'Kingdom of the Franks'), pol(720, 'Aquitaine')])}, tol=0.15)
res['byz720'] = rings(s['byz'], 0.02, 0.05); res['fra720'] = rings(s['fra'], 0.02, 0.05)
# Abasíes hacia el 800 y territorios ya independientes
ab = pol(800, 'Abbasid Caliphate')
ind = unary_union([pol(800, n) for n in ['Emirate of Córdoba', 'Idrisids', 'Rustamid dynasty']])
s = smooth({'ab': ab, 'ind': ind.difference(ab)}, tol=0.15)
res['abb800'] = rings(s['ab'], 0.02, 0.05); res['ind800'] = rings(s['ind'], 0.02, 0.05)
res['byz800'] = rings(pol(800, 'Byzantine Empire'), 0.03, 0.05)
for k, v in res.items(): print(k, len(v), sum(map(len, v)))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'islam_geo.json'), 'w'), separators=(',', ':'))
