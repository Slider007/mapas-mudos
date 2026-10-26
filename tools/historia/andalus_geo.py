# Границы для тренажёра «Al-Ándalus» (тема 2) из данных Cliopatria (Seshat Global History Databank, CC BY 4.0).
# Запуск: python3 andalus_geo.py cliopatria_polities_only_v021.geojson ne_10m_admin_0_countries.geojson → andalus_geo.json рядом со скриптом
# Полуостров = Испания + Португалия + Андорра + Гибралтар (Natural Earth 1:10m). Внутри него каждая точка отдаётся ближайшему
# государству Cliopatria, чтобы не оставалось щелей из-за несовпадения береговых линий.
import json, sys, os
from shapely.geometry import shape, box, Point
from shapely.ops import unary_union
from shapely.prepared import prep

src = json.load(open(sys.argv[1]))['features']
ne = json.load(open(sys.argv[2]))['features']
ISO = lambda f: f['properties'].get('ADM0_A3') or f['properties'].get('ISO_A3')
ib = unary_union([shape(f['geometry']) for f in ne if ISO(f) in ('ESP', 'PRT', 'AND', 'GIB')]).intersection(box(-10, 35.5, 4.5, 44.5))
fra = unary_union([shape(f['geometry']) for f in ne if ISO(f) == 'FRA']).buffer(0)
MASK = ib.buffer(0.15).difference(fra).intersection(box(-10.5, 35.6, 4.6, 44.2))
AFR = unary_union([shape(f['geometry']) for f in ne if ISO(f) in ('MAR', 'DZA', 'ESH', 'TUN')]).intersection(box(-11, 33.4, 6, 37.5))

def pol(y, name):
    g = [shape(f['geometry']).buffer(0) for f in src if f['properties']['Name'] == name and f['properties']['FromYear'] <= y <= f['properties']['ToYear']]
    if not g: raise SystemExit(f'no {name} in {y}')
    return unary_union(g)

def split(y, groups, step=0.04):
    """groups: {key: [polity names]} → {key: geometry ∩ MASK}, MASK cubierto sin huecos (cada celda al grupo más cercano)"""
    raw = {k: unary_union([pol(y, n) for n in v]).intersection(MASK) for k, v in groups.items()}
    cov = unary_union(list(raw.values()))
    gap = MASK.difference(cov)
    if gap.area > 0:
        x0, y0, x1, y1 = gap.bounds; pg = prep(gap); cells = {k: [] for k in raw}
        xs = x0
        while xs < x1:
            ys = y0
            while ys < y1:
                c = box(xs, ys, xs + step, ys + step)
                if pg.intersects(c):
                    p = Point(xs + step / 2, ys + step / 2)
                    k = min(raw, key=lambda k: raw[k].distance(p) if not raw[k].is_empty else 1e9)
                    cells[k].append(c)
                ys += step
            xs += step
        raw = {k: unary_union([raw[k]] + [c.intersection(gap) for c in cells[k]]) for k in raw}
    # quitar solapes: el orden de groups manda
    out, used = {}, None
    for k in groups:
        g = raw[k] if used is None else raw[k].difference(used)
        out[k] = g; used = g if used is None else used.union(g)
    return out

def chaikin(coords, n=3):
    pts = list(coords)[:-1]
    for _ in range(n):
        q = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        pts = q
    return pts + [pts[0]]
def smooth(groups, tol=0.07):
    """fronteras suaves y comunes: coverage_simplify (bordes compartidos iguales) + Chaikin; quita los escalones de los datos"""
    from shapely import coverage_simplify
    from shapely.geometry import Polygon, MultiPolygon
    keys = [k for k in groups if not groups[k].is_empty]
    simp = coverage_simplify([groups[k].buffer(0) for k in keys], tol)
    out = dict(groups)
    for k, g in zip(keys, simp):
        ps = [Polygon(chaikin(p.exterior.coords), [chaikin(r.coords) for r in p.interiors]) for p in polys(g) if len(p.exterior.coords) > 3]
        out[k] = unary_union([p.buffer(0) for p in ps if p.area > 0]) if ps else g
    return out
def polys(g): return [p for p in (list(g.geoms) if hasattr(g, 'geoms') else [g]) if p.geom_type == 'Polygon']
def rings(g, tol=0.006, mina=0.004):
    g = g.buffer(0).simplify(tol, preserve_topology=True); out = []
    for p in polys(g):
        if p.area < mina: continue
        r = [[round(x, 2), round(y, 2)] for x, y in p.exterior.coords]
        out.append([r[0]] + [q for i, q in enumerate(r[1:], 1) if q != r[i - 1]])
    return out

res = {}
# 1. Conquista (Cliopatria 718–723): todo es musulmán salvo la franja cantábrica (Pelayo) y el oeste de los Pirineos (vascones)
s = smooth(split(720, {'cri': ['Visigothic Kingdom', 'Aquitaine'], 'and': ['Umayyad Caliphate']}))
res['c_and'] = rings(s['and']); res['c_cri'] = rings(s['cri'])
res['c_afr'] = rings(pol(720, 'Umayyad Caliphate').intersection(AFR))
res['c_fra'] = rings(unary_union([pol(720, 'Aquitaine'), pol(720, 'Carolingian Empire')]).intersection(box(-2, 42.4, 7, 48)).difference(MASK))
res['c_sep'] = rings(pol(720, 'Visigothic Kingdom').intersection(box(1.5, 42.3, 5, 44.5)).difference(MASK))  # Septimania (Narbona)
# 2. Califato (990–1009)
CRI1000 = ['Kingdom of León', 'Kingdom of Castile', 'County of Ribagorza', 'County of Pallars', 'County of Barcelona', 'County of Urgell',
           'County of Berga', 'County of Osona', 'County of Rosellón', 'Duchy of Gascony']
s = split(1000, {'cri': CRI1000, 'and': ['Caliphate of Córdoba']})
leon = s['cri'].intersection(pol(1000, 'Kingdom of León').buffer(0.1))
cas = s['cri'].intersection(pol(1000, 'Kingdom of Castile').buffer(0.1)).difference(leon)
cat = s['cri'].intersection(box(0.6, 40.5, 4.6, 43)).difference(leon).difference(cas)
k = smooth({'and': s['and'], 'leon': leon, 'cas': cas, 'cat': cat, 'resto': s['cri'].difference(unary_union([leon, cas, cat]))})
s['cri'] = unary_union([k['leon'], k['cas'], k['cat'], k['resto']]); s['and'] = k['and']
res['k_and'] = rings(s['and']); res['k_cri'] = rings(s['cri'])
res['k_afr'] = rings(pol(1000, 'Caliphate of Córdoba').intersection(AFR))
res['k_leon'] = rings(k['leon']); res['k_cas'] = rings(k['cas']); res['k_cat'] = rings(k['cat'])
# 3. Taifas (1046–1055)
T = {'toledo': 'Taifa of Toledo', 'zaragoza': 'Taifa of Zaragoza', 'badajoz': 'Taifa of Badajoz', 'sevilla': 'Taifa of Seville',
     'granada': 'Taifa of Granada', 'valencia': 'Taifa of Valencia', 'denia': 'Taifa of Dénia', 'almeria': 'Taifa of Almería', 'cordoba': 'Caliphate of Córdoba'}
CRI1050 = ['Kingdom of Castile', 'Kingdom of Aragon', 'County of Ribagorza', 'County of Pallars Jussà', 'County of Pallars Sobirà', 'County of Urgell',
           'County of Barcelona', 'County of Berga', 'County of Osona', 'County of Rosellón', 'County of Ampuria', 'Duchy of Gascony']
s = split(1050, {'cri': CRI1050, 'and': ['(Taifas of Iberia)']})
res['t_and'] = rings(s['and']); res['t_cri'] = rings(s['cri'])
tg, used = {}, None
for k, n in T.items():
    g = pol(1050, n).buffer(0.03).intersection(s['and'])
    if used is not None: g = g.difference(used)
    tg[k] = g; used = g if used is None else used.union(g)
tg['otras'] = s['and'].difference(used)  # taifas pequeñas
cas = s['cri'].intersection(pol(1050, 'Kingdom of Castile').buffer(0.1))
tg['cas'] = cas; tg['cri_resto'] = s['cri'].difference(cas)
tg = smooth(tg)
for k, g in tg.items():
    if k != 'cri_resto': res['t_' + k] = rings(g)
res['t_cri'] = rings(unary_union([tg['cas'], tg['cri_resto']]))
res['t_and'] = rings(unary_union([g for k, g in tg.items() if k not in ('cas', 'cri_resto')]))
# Almorávides (1099–1110), para la minimapa
s = split(1100, {'cri': ['Kingdom of Castile', 'Kingdom of Aragon', 'County of Barcelona', 'County of Urgell', 'County of Pallars Jussà', 'County of Pallars Sobirà',
                         'County of Osona', 'County of Berga', 'County of Ampuria'],
                 'tai': ['Taifa of Zaragoza', 'Taifa of Albarracín', 'Taifa of Alpuente', 'Taifa of Tortosa'],
                 'and': ['Almoravid Dynasty', 'Taifa of Dénia']})
s = smooth(s)
res['m_and'] = rings(s['and']); res['m_cri'] = rings(s['cri']); res['m_tai'] = rings(s['tai']); res['m_afr'] = rings(pol(1100, 'Almoravid Dynasty').intersection(AFR))
# 4. Almohades (1188–1201)
s = split(1200, {'cas': ['Kingdom of Castile'], 'leo': ['Kingdom of León'], 'por': ['Kingdom of Portugal'], 'nav': ['Kingdom of Navarre'],
                 'ara': ['Crown of Aragon', 'County of Urgell', 'County of Pallars Sobirà', 'County of Ampuria', 'County of Berga'],
                 'and': ['Almohad Caliphate', 'Almoravid Dynasty']})
s = smooth(s)
for k, g in s.items(): res['a_' + k] = rings(g)
res['a_afr'] = rings(pol(1200, 'Almohad Caliphate').intersection(AFR))
# 5. Reino nazarí (1375–1401)
s = smooth(split(1400, {'gra': ['Emirate of Granada'], 'cas': ['Crown of Castile'], 'por': ['Kingdom of Portugal'], 'nav': ['Kingdom of Navarre'], 'ara': ['Crown of Aragon']}))
for k, g in s.items(): res['n_' + k] = rings(g)
res['n_afr'] = rings(AFR)
for k, v in res.items(): print(k, len(v), sum(map(len, v)))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'andalus_geo.json'), 'w'), separators=(',', ':'))
