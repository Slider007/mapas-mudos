# Подложка «Mapa físico-político de Europa» (IGN/CNIG, Atlas Nacional de España, ed. 2016, 1:13 725 000, cónica de Lambert)
# → img/ign.jpg в проекции урока (как relief-*.jpg).
# Привязка: коническая Ламберта, параметры подобраны методом наименьших квадратов по 22 столицам (красные значки на карте),
# найденным автоматически; средняя ошибка ≈ 3 px исходного изображения (≈ 0,1 % ширины). Проверка — наложением береговой линии Natural Earth.
# Uso: python3 ign_warp.py ign/IGN_mapa_fisico_politico_Europa_2016.jpg img/relief-color.jpg img/ign.jpg ne_10m_land.geojson
import sys, math, numpy as np
from PIL import Image
import proj
SRC, FALLBACK, OUT, LAND = sys.argv[1:5]
# lat1, lat2 (paralelos estándar), lon0, lat0, escala (px), desplazamiento x, y (px), giro (rad)
P = (35.528, 66.312, 17.372, 50.0, 1848.739, 1100.27, 778.594, 0.065)
FRAME = (70, 101, 1936, 1339)            # interior del marco de la lámina (px)
LEGEND = (92, 175, 349, 482)             # cuadro de signos convencionales (se tapa con el color del mar)

def lcc(lon, lat):
    l1, l2, lon0, lat0, s, tx, ty, rot = P
    f1, f2, f0 = map(math.radians, (l1, l2, lat0))
    n = math.log(math.cos(f1) / math.cos(f2)) / math.log(math.tan(math.pi / 4 + f2 / 2) / math.tan(math.pi / 4 + f1 / 2))
    F = math.cos(f1) * math.tan(math.pi / 4 + f1 / 2) ** n / n
    rho = F / np.tan(math.pi / 4 + np.radians(lat) / 2) ** n; rho0 = F / math.tan(math.pi / 4 + f0 / 2) ** n
    th = n * np.radians(lon - lon0); x = rho * np.sin(th); y = rho0 - rho * np.cos(th)
    c, si = math.cos(rot), math.sin(rot)
    return tx + s * (c * x - si * y), ty - s * (si * x + c * y)
src = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float32)
fb = np.asarray(Image.open(FALLBACK).convert('RGB')).astype(np.float32)
h, w = fb.shape[:2]; SC = w / proj.W
px, py = np.meshgrid((np.arange(w) + .5) / SC, (np.arange(h) + .5) / SC)
X = px / proj.S + proj.X0; Y = proj.Y1 - py / proj.S
p0, l0 = math.radians(proj.LAT0), math.radians(proj.LON0); r = np.hypot(X, Y); r[r == 0] = 1e-12; c = 2 * np.arcsin(np.minimum(1, r / 2))
lat = np.degrees(np.arcsin(np.cos(c) * math.sin(p0) + Y * np.sin(c) * math.cos(p0) / r))
lon = np.degrees(l0 + np.arctan2(X * np.sin(c), r * math.cos(p0) * np.cos(c) - Y * math.sin(p0) * np.sin(c)))
gx, gy = lcc(lon, lat)
leg = (gx >= LEGEND[0]) & (gx < LEGEND[2]) & (gy >= LEGEND[1]) & (gy < LEGEND[3])
x0 = np.clip(np.floor(gx).astype(int), 0, src.shape[1] - 2); y0 = np.clip(np.floor(gy).astype(int), 0, src.shape[0] - 2)
fx = np.clip(gx - x0, 0, 1)[..., None]; fy = np.clip(gy - y0, 0, 1)[..., None]
img = src[y0, x0] * (1 - fx) * (1 - fy) + src[y0, x0 + 1] * fx * (1 - fy) + src[y0 + 1, x0] * (1 - fx) * fy + src[y0 + 1, x0 + 1] * fx * fy
img[leg] = (163, 255, 254)   # cuadro de signos convencionales → color del mar de la lámina
# transición suave (≈12 px) entre la lámina y el relieve en color de fuera
d = np.minimum.reduce([gx - FRAME[0], FRAME[2] - gx, gy - FRAME[1], FRAME[3] - gy])  # px de la lámina hasta el marco
a = np.clip(d / 10.0, 0, 1)[..., None]
# fuera de la lámina: el mar con el color del mar de la lámina; la tierra (Svalbard, Nueva Zembla…) con el relieve en color
import json
from PIL import ImageDraw
from shapely.geometry import shape, box
mk = Image.new('L', (w, h), 0); dr = ImageDraw.Draw(mk)
for f in json.load(open(LAND))['features']:
    g = shape(f['geometry']).intersection(box(-40, 25, 90, 85))
    for pg in (g.geoms if hasattr(g, 'geoms') else [g]):
        if pg.geom_type != 'Polygon' or pg.is_empty: continue
        dr.polygon([tuple(v * SC for v in proj.prj(x, y)) for x, y in pg.exterior.coords], fill=255)
land = (np.asarray(mk) > 127)[..., None]
fb = np.where(land, fb, np.array([163, 255, 254], np.float32))
out = img * a + fb * (1 - a)   # fuera de la lámina (Svalbard, Nueva Zembla…): relieve en color
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(OUT, quality=82, optimize=True, progressive=True)
print(OUT, w, h, f'{(d > 0).mean():.0%} cubierto por la lámina')
