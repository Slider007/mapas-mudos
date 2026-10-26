# Geometría del mapa político de Europa a partir de Natural Earth 1:10m.
# Entrada (se descargan aparte, ver README de tools): ne_10m_admin_0_countries_esp.geojson (punto de vista de España: Crimea en Ucrania),
# ne_10m_admin_0_countries.geojson (de aquí solo Kosovo, que la hoja del profesor incluye), ne_10m_lakes.geojson.
# Uso: python3 build_geo.py <carpeta con los geojson>  →  geo.json
import json, math, sys, os
from shapely.geometry import shape, box, Polygon, MultiPolygon, mapping
from shapely.ops import unary_union, transform
from shapely.ops import polylabel
from paises import P, SEAS
SRC = sys.argv[1]
LON0, LAT0 = 15.0, 52.0
def laea(lon, lat):
    l, p, l0, p0 = map(math.radians, (lon, lat, LON0, LAT0))
    k = math.sqrt(2 / (1 + math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)))
    return k * math.cos(p) * math.sin(l - l0), k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
# encuadre: de Islandia al Caspio y los Urales, del Sáhara al cabo Norte
frame_pts = [(-25, 63.2), (-24.5, 66.6), (-10.5, 35.8), (36.5, 33.6), (51.5, 38.5), (60, 56), (31, 71.3), (-10, 64)]
xs, ys = zip(*[laea(*p) for p in frame_pts])
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
mx, my = (x1 - x0) * .02, (y1 - y0) * .02; x0 -= mx; x1 += mx; y0 -= my; y1 += my
W = 1000.0; S = W / (x1 - x0); H = round((y1 - y0) * S, 1)
def prj(lon, lat):
    x, y = laea(lon, lat); return ((x - x0) * S, (y1 - y) * S)
def tr(g): return transform(lambda X, Y, Z=None: tuple(zip(*[prj(a, b) for a, b in zip(X, Y)])) if hasattr(X, '__len__') else prj(X, Y), g)
CLIP = box(-2, -2, W + 2, H + 2)
ROI = box(-40, 24, 75, 79)
def load(fn):
    out = []
    for f in json.load(open(os.path.join(SRC, fn)))['features']:
        g = shape(f['geometry']).buffer(0)
        if not g.intersects(ROI): continue
        out.append((f['properties']['ADM0_A3'], f['properties']['ADMIN'], g.intersection(ROI)))
    return out
esp = load('ne_10m_admin_0_countries_esp.geojson')
kos = [g for a, n, g in load('ne_10m_admin_0_countries.geojson') if a == 'KOS'][0]
code2id = {c: k for k, v in P.items() for c in v[7]}
geo = {}; other = []
for a3, name, g in esp:
    pid = code2id.get(a3)
    if a3 == 'SRB': g = g.difference(kos)
    if pid: geo.setdefault(pid, []).append(g)
    else: other.append(g)
geo['kosovo'] = [kos]
def d_of(g, tol):
    g = tr(g).intersection(CLIP).simplify(tol, preserve_topology=True)
    polys = [p for p in (g.geoms if hasattr(g, 'geoms') else [g]) if p.geom_type == 'Polygon' and not p.is_empty]
    s = []
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            if len(c) < 4 or Polygon(c).area < 0.15: continue
            s.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in c[:-1]) + 'Z')
    return ''.join(s), g
MICRO = {k for k, v in P.items() if v[6] == 'micro' and k not in ('luxemburgo',)}
out = {'W': W, 'H': H, 'countries': {}, 'src': 'Natural Earth 1:10m (admin_0_countries, punto de vista de España; Kosovo de la versión general), proyección acimutal equivalente de Lambert centrada en 15°E 52°N'}
for pid, gs in geo.items():
    g = unary_union(gs)
    d, gp = d_of(g, 0.05 if pid in MICRO or pid in ('malta', 'luxemburgo') else 0.32)
    big = max((p for p in (gp.geoms if hasattr(gp, 'geoms') else [gp]) if p.geom_type == 'Polygon'), key=lambda p: p.area, default=None)
    lp = polylabel(big, 0.5) if big is not None and big.area > 30 else (big.centroid if big is not None else None)
    v = P[pid]; cx, cy = prj(v[4], v[5])
    out['countries'][pid] = {'d': d, 'lab': [round(lp.x, 1), round(lp.y, 1)] if lp else [round(cx, 1), round(cy, 1)],
                             'cap': [round(cx, 1), round(cy, 1)], 'area': round(gp.area, 1),
                             'c': [round(big.centroid.x, 1), round(big.centroid.y, 1)] if big is not None else [round(cx, 1), round(cy, 1)]}
od, _ = d_of(unary_union(other), 0.32)
out['other'] = od
lakes = [shape(f['geometry']) for f in json.load(open(os.path.join(SRC, 'ne_10m_lakes.geojson')))['features']
         if f['properties'].get('scalerank', 9) <= 3 and shape(f['geometry']).intersects(ROI)]
ld, _ = d_of(unary_union(lakes).intersection(ROI), 0.32)
out['lakes'] = ld
out['seas'] = [[es, ru, *[round(v, 1) for v in prj(lo, la)]] for es, ru, lo, la in SEAS]
# retícula cada 10°
grat = []
for lon in range(-30, 71, 10):
    pts = [prj(lon, la) for la in range(30, 76, 1)]; grat.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts))
for lat in range(30, 76, 10):
    pts = [prj(lo, lat) for lo in range(-35, 76, 1)]; grat.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts))
out['grat'] = ''.join(grat)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geo.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('W,H', W, H, 'countries', len(out['countries']), 'size', os.path.getsize('geo.json'))
