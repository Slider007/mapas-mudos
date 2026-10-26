# Regiones de relieve sin contorno en Natural Earth ni en OpenStreetMap, calculadas a partir de las altitudes (reglas fijas, reproducibles).
# Uso: python3 regions_dem.py <elev.npy de relief.py> <ne_10m_land.geojson> <ne_10m_rivers_lake_centerlines.geojson>  →  osm/dem_regions.json (lon/lat)
import sys, os, json, math, numpy as np
from scipy import ndimage as nd
from shapely.geometry import shape, Polygon, MultiPolygon, LineString, Point, box, mapping
from shapely.ops import unary_union
from PIL import Image, ImageDraw
import proj
E = np.load(sys.argv[1]); h, w = E.shape; SC = w / proj.W
HERE = os.path.dirname(os.path.abspath(__file__))
# tierra
mask = Image.new('L', (w, h), 0); dr = ImageDraw.Draw(mask)
for f in json.load(open(sys.argv[2]))['features']:
    g = shape(f['geometry'])
    if not g.intersects(box(-30, 30, 75, 82)): continue
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        dr.polygon([tuple(v * SC for v in proj.prj(a, b)) for a, b in p.exterior.coords], fill=1)
LAND = np.asarray(mask).astype(bool)
# lon/lat de cada píxel
yy, xx = np.mgrid[0:h, 0:w]; X = (xx + .5) / SC / proj.S + proj.X0; Y = proj.Y1 - (yy + .5) / SC / proj.S
p0, l0 = math.radians(proj.LAT0), math.radians(proj.LON0); r = np.hypot(X, Y); r[r == 0] = 1e-12; c = 2 * np.arcsin(np.minimum(1, r / 2))
LAT = np.degrees(np.arcsin(np.cos(c) * math.sin(p0) + Y * np.sin(c) * math.cos(p0) / r))
LON = np.degrees(l0 + np.arctan2(X * np.sin(c), r * math.cos(p0) * np.cos(c) - Y * math.sin(p0) * np.sin(c)))
Es = nd.gaussian_filter(np.where(LAND, E, 0), 2.0)   # suavizado ≈ 5 km
def poly_mask(g):
    im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        d.polygon([tuple(v * SC for v in proj.prj(a, b)) for a, b in p.exterior.coords], fill=1)
    return np.asarray(im).astype(bool)
REG = {}
for f in json.load(open(os.path.join(sys.argv[2].rsplit('/', 1)[0], 'ne_10m_geography_regions_polys.geojson')))['features']:
    n = f['properties'].get('NAME') or f['properties'].get('name')
    if n in ('URAL MOUNTAINS', 'CAUCASUS MTS.'): REG[n] = shape(f['geometry']).buffer(0)
COUNTRIES = [(f['properties']['ADM0_A3'], shape(f['geometry']).buffer(0)) for f in json.load(open(os.path.join(sys.argv[2].rsplit('/', 1)[0], 'ne_10m_admin_0_countries_esp.geojson')))['features'] if f['properties']['ADM0_A3'] in ('ESP',)]
def px(lon, lat): x, y = proj.prj(lon, lat); return int(y * SC), int(x * SC)
def component(m, lon, lat, close=6, open_=3):
    m = nd.binary_opening(m, iterations=open_); lab, n = nd.label(m); i = lab[px(lon, lat)]
    assert i, ('el punto semilla no está en la región', lon, lat)
    m = lab == i; m = nd.binary_closing(m, iterations=close); m = nd.binary_fill_holes(m); return m & LAND
def to_poly(m, tol_px=3, min_px=400):
    from skimage import measure
    out = []
    for cont in measure.find_contours(np.pad(m, 1).astype(float), .5):
        cont = cont - 1
        if len(cont) < 20: continue
        pts = [proj.unprj((x + .5) / SC, (y + .5) / SC) for y, x in cont]
        pg = Polygon(pts).buffer(0)
        if pg.area > 0: out.append(pg)
    g = unary_union(out)
    tol = tol_px / SC / proj.S * 57.3  # ≈ grados
    return g.simplify(tol * .6, preserve_topology=True)
R = {}
# 1. Meseta Castellana: altiplano de 450–1100 m del centro peninsular (las sierras interiores >1100 m quedan fuera); semilla: Madrid
ES = poly_mask([g for g in COUNTRIES if g[0] == 'ESP'][0][1])
from basins import flow, upstream
def basin_of(mouths, win, near_km=12, any_cell=False):
    (lo0, la1), (lo1, la0) = win; cs = [px(lo0, la1), px(lo1, la0), px(lo0, la0), px(lo1, la1)]
    y0, y1 = max(0, min(c[0] for c in cs) - 10), min(h, max(c[0] for c in cs) + 10); x0, x1 = max(0, min(c[1] for c in cs) - 10), min(w, max(c[1] for c in cs) + 10)
    rec, (hh, ww) = flow(E, LAND, y0, y1, x0, x1)
    seeds = []
    for lo, la in mouths:   # las celdas de tierra cercanas a la desembocadura
        cy, cx = px(lo, la); r = int(near_km / ((proj.X1 - proj.X0) * 6371 / w))
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if y0 <= y < y1 and x0 <= x < x1 and LAND[y, x] and (any_cell or rec[y - y0, x - x0] < 0): seeds.append((y - y0) * ww + (x - x0))  # celdas por donde el agua sale al mar
    up = upstream(rec, (hh, ww), seeds); out = np.zeros_like(LAND); out[y0:y1, x0:x1] = up; return out
# 1. Meseta Castellana = cuencas del Duero (submeseta norte), del Tajo y del Guadiana (submeseta sur) dentro de España, por encima de 300 m
B = basin_of([(-8.66, 41.14), (-9.0, 38.9), (-7.40, 37.18)], ((-10.2, 44.2), (3.6, 35.8)), near_km=30)
mm = B & ES & (Es > 150)
R['m_meseta'] = (component(nd.binary_fill_holes(mm), -3.7, 40.4, close=3, open_=3) & ES, 'Cuencas del Duero (submeseta norte), del Tajo y del Guadiana (submeseta sur) dentro de España, por encima de 150 m. Sus divisorias son las cordilleras que rodean la Meseta (Cantábrica, Montes de León, Sistema Ibérico, Sierra Morena).')

# 2. Cordilleras Béticas: más de 600 m al sur y al este del valle del Guadalquivir
gq = [shape(f['geometry']) for f in json.load(open(sys.argv[3]))['features'] if f['properties'].get('name') == 'Guadalquivir']
gql = unary_union(gq); coords = sorted([c for l in (gql.geoms if hasattr(gql, 'geoms') else [gql]) for c in l.coords])
# límite norte: el río Guadalquivir y su prolongación hasta la costa de Alicante
line = [(-6.4, 36.8)] + [c for c in coords if c[0] > -6.4] + [(-2.3, 38.1), (-0.5, 38.9), (0.3, 38.95)]
north = Polygon(line + [(0.5, 35.5), (-6.5, 35.5)]).buffer(0)
south = np.zeros_like(LAND); sp = Image.new('L', (w, h), 0); ImageDraw.Draw(sp).polygon([tuple(v * SC for v in proj.prj(a, b)) for a, b in north.exterior.coords], fill=1)
south = np.asarray(sp).astype(bool)
m = (Es > 500) & south & (LON > -6.6) & (LON < 0.6) & (LAT < 39.0)
lab, n = nd.label(nd.binary_closing(m, iterations=4)); sizes = nd.sum(m, lab, range(1, n + 1)); keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 300])
R['m_beticas'] = (nd.binary_fill_holes(nd.binary_closing(keep, iterations=8)) & LAND, 'Tierras de más de 500 m al sur y al este del valle del Guadalquivir (de Cádiz a Alicante).')
# 3. Macizo de Bohemia = cuenca del Elba (Labe) y del Moldava (Vltava) aguas arriba del desfiladero de Děčín: la cubeta cerrada por las sierras bohemias
B = basin_of([(14.21, 50.78)], ((11.6, 51.4), (17.2, 48.3)), near_km=4, any_cell=True)  # todo lo que drena hacia Děčín
R['m_bohemia'] = (component(nd.binary_fill_holes(B), 14.42, 50.08, close=3, open_=2), 'Cuenca del Elba (Labe) y del Moldava (Vltava) aguas arriba del desfiladero de Děčín: la cubeta cerrada por las sierras de Bohemia (Šumava, Montes Metálicos, Sudetes, Altiplano de Bohemia-Moravia).')
# 4. Gran Llanura Europea: tierras bajas de menos de 300 m desde los Países Bajos hasta los Urales (sin Escandinavia, Finlandia ni la llanura de Hungría)
URAL = poly_mask(REG['URAL MOUNTAINS'].buffer(0.15)); CAUC = poly_mask(REG['CAUCASUS MTS.'].buffer(0.3))
m = (Es < 300) & (Es > -60) & LAND & (LON > -5) & (LON < 66) & (LAT > 43.0) & (LAT < 68.5) & ~URAL & ~CAUC
m &= ~poly_mask(Polygon([(58.0, 30), (58.0, 51.3), (60.5, 52.5), (90, 52.5), (90, 30)]))   # al sur de los Urales empieza Asia (tierras bajas de Turán)
m &= ~poly_mask(Polygon([(59.0, 52.0), (60.0, 56), (61.0, 60), (63.0, 66), (66.5, 69), (90, 69), (90, 52)]))  # al este de los Urales: llanura de Siberia Occidental
m &= ~poly_mask(Polygon([(5, 72), (5, 54.5), (14, 54.5), (28.5, 60.2), (31.5, 61.0), (35.0, 62.6), (36.5, 64.6), (41.5, 67.2), (41.5, 72)]))  # escudo escandinavo: Fenoscandia y Carelia (límite Ladoga – Onega – mar Blanco)
m &= ~((LON > 15.5) & (LON < 23.5) & (LAT < 48.8))                # cuenca de los Cárpatos (llanura de Hungría)
m &= ~((LAT < 46.2) & (LON < 15))                                 # Aquitania y valle del Po
m &= ~((LAT < 46.2) & (LON < 28.6))                               # llanura del bajo Danubio (Valaquia)
R['ll_europea'] = (component(m, 30.0, 55.0, close=6, open_=4), 'Tierras de menos de 300 m desde la costa atlántica de Francia hasta los Urales y el Caspio, sin el escudo escandinavo (Escandinavia, Finlandia, Carelia) ni la llanura de Hungría.')
out = {}
for k, (mk, rule) in R.items():
    g = to_poly(mk); out[k] = {'rule': rule, 'geometry': mapping(g)}; print(k, g.geom_type, round(g.area, 2), 'grados²')
json.dump(out, open(os.path.join(HERE, 'osm', 'dem_regions.json'), 'w'), ensure_ascii=False)
