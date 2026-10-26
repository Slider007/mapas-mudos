# Geometría de Europa física a partir de Natural Earth 1:10m. Uso: python3 build_geo.py <carpeta con los geojson de NE>  →  geo.json
import json, sys, os, math
from shapely.geometry import shape, box, Polygon, MultiPolygon, LineString, MultiLineString, Point
from shapely.ops import unary_union, linemerge, polylabel
from shapely import transform as shp_transform
import numpy as np
import proj
from datos import O
SRC = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
def rd(fn): return json.load(open(os.path.join(SRC, fn + '.geojson')))['features']
ROI = box(-60, 26, 100, 86)
def P(g):  # lon/lat → mapa
    def f(a):
        out = np.empty_like(a)
        for i, (x, y) in enumerate(a): out[i] = proj.prj(x, y)
        return out
    return shp_transform(g, f)
FRAME = box(-3, -3, proj.W + 3, proj.H + 3)
def polys(g): return [p for p in (g.geoms if hasattr(g, 'geoms') else [g]) if p.geom_type == 'Polygon' and not p.is_empty]
def dpath(g, tol=0.3, mina=0.08):
    g = g.intersection(FRAME).simplify(tol, preserve_topology=True); s = []
    for p in polys(g):
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            if len(c) < 4 or Polygon(c).area < mina: continue
            s.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in c[:-1]) + 'Z')
    return ''.join(s)
print('cargando…', flush=True)
land_ll = [shape(f['geometry']).buffer(0) for f in rd('ne_10m_land')]
land_ll = [g.intersection(ROI) for g in land_ll if g.intersects(ROI)]
minor = [shape(f['geometry']).buffer(0) for f in rd('ne_10m_minor_islands')]
minor = [g for g in minor if g.intersects(ROI)]
LANDP = [p for g in land_ll + minor for p in polys(g)]
LAND = unary_union(LANDP)
marine = {}
for f in rd('ne_10m_geography_marine_polys'):
    n = f['properties'].get('name') or f['properties'].get('NAME')
    if n: marine.setdefault(n, []).append(shape(f['geometry']).buffer(0))
regions = {}
for f in rd('ne_10m_geography_regions_polys'):
    n = f['properties'].get('name') or f['properties'].get('NAME') or f['properties'].get('name_en')
    if n: regions.setdefault(n, []).append(shape(f['geometry']).buffer(0))
lakes = {}
lake_all = []
for fn in ['ne_10m_lakes', 'ne_10m_lakes_europe']:
    for f in rd(fn):
        g = shape(f['geometry']).buffer(0)
        if not g.intersects(ROI): continue
        lake_all.append(g); n = f['properties'].get('name')
        if n: lakes.setdefault(n, []).append(g)
rivers = {}
for fn in ['ne_10m_rivers_lake_centerlines', 'ne_10m_rivers_europe']:
    for f in rd(fn):
        n = f['properties'].get('name')
        if n and f['geometry']: rivers.setdefault(n, []).append(shape(f['geometry']))
def names(x): return x if isinstance(x, list) else [x]
def gmarine(n): return unary_union([g for k in names(n) for g in marine[k]])
def gregion(n): return unary_union([g for k in names(n) for g in regions[k]])
out = {'W': proj.W, 'H': proj.H, 'O': {}}
LANDM = P(LAND.intersection(ROI)).buffer(0); SEAM = FRAME.difference(LANDM)
DEM = json.load(open(os.path.join(HERE, 'osm', 'dem_regions.json')))
def osm(oid):
    d = json.load(open(os.path.join(HERE, 'osm', oid + '.json')))['res']
    for want in (('Polygon', 'MultiPolygon'), ('LineString', 'MultiLineString'), ('Point',)):
        for r in d:
            if r['geojson']['type'] in want: return shape(r['geojson']), r
    raise ValueError('sin resultado OSM')
KM = proj.S * 1 / 6371  # unidades de mapa por km (aprox. en el centro)
for oid, es, short, cat, geo, ru in O:
    kind = geo[0]; o = {}
    try:
        if kind == 'osm':
            g, r = osm(geo[1])
            if cat == 'cabo' and g.geom_type != 'Point':   # cabo dado como zona (Cap Corse): su extremo norte
                pts = [c for p in polys(g) for c in p.exterior.coords]; g = Point(max(pts, key=lambda c: c[1]))
            if g.geom_type == 'Point':
                x, y = proj.prj(g.x, g.y); o = {'k': 'pt', 'xy': [round(x, 2), round(y, 2)], 'lab': [round(x, 2), round(y, 2)]}
            else:
                gp = P(g).buffer(0) if g.geom_type in ('Polygon', 'MultiPolygon') else P(g).buffer((geo[2] if len(geo) > 2 else 6) * KM).intersection(SEAM)
                if cat not in ('pen', 'cabo'): gp = gp.intersection(SEAM.buffer(0.3))
                gp = gp.intersection(FRAME); o = {'k': 'zone', 'd': dpath(gp, 0.15, 0.003)}
                big = max(polys(gp), key=lambda p: p.area); lp = polylabel(big, 0.2) if big.area > 2 else big.centroid; o['lab'] = [round(lp.x, 1), round(lp.y, 1)]
            o['src'] = f"OpenStreetMap {r['osm_type']} {r['osm_id']}"
        elif kind == 'dem':
            gp = P(shape(DEM[geo[1]]['geometry'])).buffer(0).intersection(LANDM).intersection(FRAME)
            o = {'k': 'zone', 'd': dpath(gp, 0.3)}; big = max(polys(gp), key=lambda p: p.area); lp = polylabel(big, 0.5); o['lab'] = [round(lp.x, 1), round(lp.y, 1)]
            o['src'] = 'altitudes: ' + DEM[geo[1]]['rule']
        elif kind == 'closing':
            (a, b), inland = geo[1], geo[2]
            g = Polygon([tuple(a), tuple(b)] + [tuple(x) for x in inland]).buffer(0)
            gp = P(g).buffer(0).intersection(SEAM); o = {'k': 'zone', 'd': dpath(gp, 0.15, 0.003)}
            big = max(polys(gp), key=lambda p: p.area); lp = polylabel(big, 0.2); o['lab'] = [round(lp.x, 1), round(lp.y, 1)]
            o['src'] = 'mar entre la costa y la línea que une los cabos que cierran el golfo'
        elif kind == 'biscay_strip':
            g = gmarine('Bay of Biscay').intersection(box(geo[1], 42, geo[2], geo[3]))
            gp = P(g).buffer(0).intersection(FRAME); o = {'k': 'zone', 'd': dpath(gp, 0.3)}; big = max(polys(gp), key=lambda p: p.area); lp = polylabel(big, 0.3); o['lab'] = [round(lp.x, 1), round(lp.y, 1)]
            o['src'] = 'parte sur del golfo de Vizcaya (Natural Earth) junto a la costa española, de Estaca de Bares a la desembocadura del Adour'
        elif kind in ('marine', 'region', 'poly'):
            if kind == 'marine': g = gmarine(geo[1])
            elif kind == 'region': g = gregion(geo[1])
            else:
                g = Polygon(geo[1]).buffer(0)
                g = g.intersection(LAND) if geo[2] == 'land' else g.difference(LAND)
            gp = P(g.intersection(ROI)).buffer(0).intersection(FRAME)
            o = {'k': 'zone', 'd': dpath(gp, 0.4)}
            big = max(polys(gp), key=lambda p: p.area)
            lp = polylabel(big, 0.5); o['lab'] = [round(lp.x, 1), round(lp.y, 1)]
        elif kind == 'lake':
            if isinstance(geo[1], list) and isinstance(geo[1][0], (int, float)):
                pt = Point(geo[1]); g = [x for x in lake_all if x.contains(pt)][0]
            else: g = unary_union([x for k in names(geo[1]) for x in lakes[k]])
            gp = P(g).intersection(FRAME); o = {'k': 'lake', 'd': dpath(gp, 0.15, 0.01)}
            big = max(polys(gp), key=lambda p: p.area); c = big.representative_point(); o['lab'] = [round(c.x, 1), round(c.y, 1)]
        elif kind == 'area':
            x, y = proj.prj(*geo[1]); o = {'k': 'area', 'xy': [round(x, 1), round(y, 1)], 'r': round(geo[2] * KM, 1), 'lab': [round(x, 1), round(y, 1)]}
        elif kind == 'pt':
            x, y = proj.prj(*geo[1]); o = {'k': 'pt', 'xy': [round(x, 2), round(y, 2)], 'lab': [round(x, 2), round(y, 2)]}
        elif kind == 'isl':
            spec = geo[1]
            if spec and spec[0] == 'in_marine':
                sea = gmarine(spec[1]); sel = [p for p in LANDP if sea.contains(p.representative_point()) and p.area < 1.5]
            elif spec and spec[0] == 'in_box':
                b = box(*spec[1]); mina = spec[2] if len(spec) > 2 else 0.0005
                sel = [p for p in LANDP if b.contains(p.representative_point()) and p.area >= mina]
            else: sel = [p for p in LANDP for s in spec if p.contains(Point(s))]
            g = unary_union(sel); gp = P(g).intersection(FRAME)
            o = {'k': 'isl', 'd': dpath(gp, 0.12, 0.004)}
            big = max(polys(gp), key=lambda p: p.area); c = polylabel(big, 0.3) if big.area > 4 else big.centroid
            o['lab'] = [round(c.x, 1), round(c.y, 1)]; o['n'] = len(sel)
        elif kind == 'river':
            ls = [l for k in names(geo[1]) for l in rivers.get(k, [])]
            u = unary_union(ls); ml = linemerge(u) if u.geom_type == 'MultiLineString' else u; gp = P(ml).intersection(FRAME).simplify(0.35)
            lines = [list(l.coords) for l in (gp.geoms if hasattr(gp, 'geoms') else [gp]) if l.geom_type == 'LineString' and l.length > 1]
            o = {'k': 'line', 'lines': [[[round(x, 1), round(y, 1)] for x, y in l] for l in lines]}
            L = max((LineString(l) for l in lines), key=lambda l: l.length); c = L.interpolate(.5, normalized=True); o['lab'] = [round(c.x, 1), round(c.y, 1)]
            o['len'] = round(sum(LineString(l).length for l in lines), 1)
    except Exception as e:
        print('ERROR', oid, e); continue
    if 'src' not in o: o['src'] = {'marine': 'Natural Earth (geography_marine_polys)', 'region': 'Natural Earth (geography_regions_polys)', 'lake': 'Natural Earth (lakes)',
                                   'isl': 'Natural Earth (land, minor_islands)', 'river': 'Natural Earth (rivers)'}.get(kind, '')
    out['O'][oid] = o
# base: costa, fronteras, lagos de fondo
out['land'] = dpath(LANDM.intersection(FRAME), 0.3, 0.05)
cs = [shape(f['geometry']).buffer(0) for f in rd('ne_10m_admin_0_countries_esp')]
bl = unary_union([P(g.intersection(ROI)).boundary for g in cs if g.intersects(ROI)]).intersection(LANDM.buffer(-0.6)).intersection(FRAME).simplify(0.4)
out['borders'] = ''.join('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in l.coords) for l in (bl.geoms if hasattr(bl, 'geoms') else [bl]) if l.geom_type == 'LineString' and l.length > .5)
out['lakes'] = dpath(P(unary_union([g for g in lake_all if g.area > 0.05])).intersection(FRAME), 0.2, 0.05)
json.dump(out, open(os.path.join(HERE, 'geo.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
for k, v in out['O'].items():
    if v['k'] == 'line': print(k, 'lines', len(v['lines']), 'len', v['len'])
    if v['k'] == 'isl': print(k, 'islas', v['n'])
print('size', os.path.getsize(os.path.join(HERE, 'geo.json')), 'objs', len(out['O']), 'of', len(O))
