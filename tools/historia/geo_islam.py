# Base cartográfica amplia para el tema «El islam» (de la península ibérica a la India): costas y ríos de Natural Earth 1:10m.
# Запуск: python3 geo_islam.py ne_10m_land.geojson ne_10m_rivers_lake_centerlines.geojson → geo_islam.json рядом со скриптом
# Проекция та же по форме, что geo.json (x=(lon-LON0)*C*K, y=(LAT1-lat)*K), но с другими параметрами.
import json, sys, os, math
from shapely.geometry import shape, box
from shapely.ops import unary_union
LON0, LON1, LAT0, LAT1, K = -12, 82, 6, 50, 10
C = math.cos(math.radians(30))
P = lambda x, y: f"{(x - LON0) * C * K:.1f},{(LAT1 - y) * K:.1f}"
fr = box(LON0 - 2, LAT0 - 2, LON1 + 2, LAT1 + 2)
land = unary_union([shape(f['geometry']).intersection(fr) for f in json.load(open(sys.argv[1]))['features']]).simplify(0.035, preserve_topology=True)
def polys(g): return list(g.geoms) if hasattr(g, 'geoms') else [g]
d = []
for p in polys(land):
    if p.geom_type != 'Polygon' or p.area < 0.02: continue
    for r in [p.exterior] + list(p.interiors):
        if r.length < 0.3: continue
        d.append('M' + 'L'.join(P(x, y) for x, y in r.coords[:-1]) + 'Z')
RIV = {'Nile', 'Tigris', 'Euphrates', 'Indus', 'Danube', 'Amu Darya', 'Syr Darya', 'Guadalquivir', 'Ebro', 'Tagus', 'Duero', 'Douro', 'Rhône', 'Loire', 'Rhine', 'Volga', 'Don', 'Dnieper', 'Ganges', 'Niger', 'Garonne', 'Seine', 'Guadiana', 'Po'}
rv = []
for f in json.load(open(sys.argv[2]))['features']:
    n = (f['properties'].get('name_en') or f['properties'].get('name') or '')
    if not any(n.startswith(r) for r in RIV): continue
    g = shape(f['geometry']).intersection(fr).simplify(0.03)
    for l in (list(g.geoms) if hasattr(g, 'geoms') else [g]):
        if l.geom_type == 'LineString' and l.length > 0.2: rv.append('M' + 'L'.join(P(x, y) for x, y in l.coords))
out = {'W': round((LON1 - LON0) * C * K), 'H': (LAT1 - LAT0) * K, 'LON0': LON0, 'LAT1': LAT1, 'K': K, 'C': C, 'land': ''.join(d), 'rivers': ''.join(rv), 'src': 'Natural Earth 1:10m'}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geo_islam.json'), 'w'), separators=(',', ':'))
print(out['W'], out['H'], len(out['land']), len(out['rivers']))
