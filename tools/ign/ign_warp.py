# Подложки из листов IGN/CNIG «Mapa físico de Europa» и «Mapa político de Europa» (Atlas Nacional de España, ed. 2025,
# 1:13 725 000, cónica conforme de Lambert) → картинка в проекции урока (как relief-*.jpg).
# Оба листа свёрстаны одинаково (та же рамка и сетка), поэтому привязка общая:
#   коническая Ламберта, параметры подобраны методом наименьших квадратов по 32 столицам — красным значкам на политическом листе,
#   найденным автоматически; средняя ошибка 6 px при 300 dpi (≈ 0,1 % ширины листа). Проверено наложением береговой линии Natural Earth
#   на физический лист (Исландия, Иберия, Чёрное море, Кольский п-ов).
# Uso:
#   python3 ign_warp.py fisico   <Mapa-fisico-de-Europa…2025….pdf>   ../../europa-fisica/img/ign.jpg   <ne_10m_land.geojson>
#   python3 ign_warp.py politico <Mapa-politico-de-Europa…2025….pdf> ../../europa-politica/img/ign.jpg <ne_10m_land.geojson>
#   (PDF del centro de descargas del CNIG; se rasteriza con pdftoppm a 300 dpi)
import sys, os, math, json, subprocess, tempfile, numpy as np, cv2
from PIL import Image, ImageDraw
from shapely.geometry import shape, box
Image.MAX_IMAGE_PIXELS = None
KIND, PDF, OUT, LAND = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
# lat1, lat2 (paralelos estándar), lon0, lat0, escala (px a 300 dpi), desplazamiento x, y (px), giro (rad)
P = (37.7592, 67.0565, 17.0359, 50.0, 5612.8813, 3470.7694, 2516.4189, 0.0614)
FRAME = (334, 436, 6062, 4228)                      # interior del marco (px a 300 dpi)
LEGEND = {'fisico': (400, 657, 1187, 1332), 'politico': (680, 793, 1404, 1256)}[KIND]   # cuadro de signos convencionales
def lcc(lon, lat):
    l1, l2, lon0, lat0, s, tx, ty, rot = P
    f1, f2, f0 = map(math.radians, (l1, l2, lat0))
    n = math.log(math.cos(f1) / math.cos(f2)) / math.log(math.tan(math.pi / 4 + f2 / 2) / math.tan(math.pi / 4 + f1 / 2))
    F = math.cos(f1) * math.tan(math.pi / 4 + f1 / 2) ** n / n
    rho = F / np.tan(math.pi / 4 + np.radians(lat) / 2) ** n; rho0 = F / math.tan(math.pi / 4 + f0 / 2) ** n
    th = n * np.radians(lon - lon0); x = rho * np.sin(th); y = rho0 - rho * np.cos(th)
    c, si = math.cos(rot), math.sin(rot)
    return tx + s * (c * x - si * y), ty - s * (si * x + c * y)
# proyección de cada lección (acimutal equivalente de Lambert, como sus geo.json)
def lesson_proj(kind):
    if kind == 'fisico':
        sys.path.insert(0, os.path.join(HERE, '..', 'europa_fisica')); import proj
        return proj.LON0, proj.LAT0, proj.X0, proj.Y1, proj.S, proj.W, proj.H
    LON0, LAT0 = 15.0, 52.0   # = tools/europa/build_geo.py
    def laea(lon, lat):
        l, p, l0, p0 = map(math.radians, (lon, lat, LON0, LAT0))
        k = math.sqrt(2 / (1 + math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)))
        return k * math.cos(p) * math.sin(l - l0), k * (math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0))
    fp = [(-25, 63.2), (-24.5, 66.6), (-10.5, 35.8), (36.5, 33.6), (51.5, 38.5), (60, 56), (31, 71.3), (-10, 64)]
    xs, ys = zip(*[laea(*p) for p in fp]); x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    mx, my = (x1 - x0) * .02, (y1 - y0) * .02; x0 -= mx; x1 += mx; y0 -= my; y1 += my
    S = 1000.0 / (x1 - x0); return LON0, LAT0, x0, y1, S, 1000.0, round((y1 - y0) * S, 1)
LON0, LAT0, X0, Y1, S, W, H = lesson_proj(KIND)
SC = 4.0                                            # px de la imagen por unidad del mapa (4000 px de ancho)
w, h = int(W * SC), int(H * SC)
# 1) lámina a 300 dpi, sin el cuadro de leyenda (relleno con inpainting)
with tempfile.TemporaryDirectory() as td:
    subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', PDF, os.path.join(td, 'p')], check=True)
    src = cv2.imread(os.path.join(td, 'p.png'))
m = np.zeros(src.shape[:2], np.uint8); x0_, y0_, x1_, y1_ = LEGEND; m[y0_:y1_, x0_:x1_] = 255
src = cv2.inpaint(src, m, 9, cv2.INPAINT_TELEA)
src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
# 2) lon/lat de cada píxel de salida → px de la lámina
px, py = np.meshgrid((np.arange(w) + .5) / SC, (np.arange(h) + .5) / SC)
X = px / S + X0; Y = Y1 - py / S
p0, l0 = math.radians(LAT0), math.radians(LON0); r = np.hypot(X, Y); r[r == 0] = 1e-12; c = 2 * np.arcsin(np.minimum(1, r / 2))
lat = np.degrees(np.arcsin(np.cos(c) * math.sin(p0) + Y * np.sin(c) * math.cos(p0) / r))
lon = np.degrees(l0 + np.arctan2(X * np.sin(c), r * math.cos(p0) * np.cos(c) - Y * math.sin(p0) * np.sin(c)))
gx, gy = lcc(lon, lat)
img = cv2.remap(src, gx.astype(np.float32), gy.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
# 3) fuera de la lámina: mar del color del mar de la lámina, tierra gris claro (Svalbard, Nueva Zembla…); transición suave
sea = np.median(src[FRAME[1] + 40:FRAME[1] + 400, FRAME[0] + 40:FRAME[0] + 300].reshape(-1, 3), 0)
mk = Image.new('L', (w, h), 0); dr = ImageDraw.Draw(mk)
def P2(lon_, lat_):
    l, p, l0_, p0_ = map(math.radians, (lon_, lat_, LON0, LAT0))
    k = math.sqrt(2 / (1 + math.sin(p0_) * math.sin(p) + math.cos(p0_) * math.cos(p) * math.cos(l - l0_)))
    x, y = k * math.cos(p) * math.sin(l - l0_), k * (math.cos(p0_) * math.sin(p) - math.sin(p0_) * math.cos(p) * math.cos(l - l0_))
    return ((x - X0) * S * SC, (Y1 - y) * S * SC)
for f in json.load(open(LAND))['features']:
    g = shape(f['geometry']).intersection(box(-45, 22, 95, 86))
    for pg in (g.geoms if hasattr(g, 'geoms') else [g]):
        if pg.geom_type == 'Polygon' and not pg.is_empty: dr.polygon([P2(x, y) for x, y in pg.exterior.coords], fill=255)
fb = np.where((np.asarray(mk) > 127)[..., None], np.array([228, 226, 214], np.float32), sea.astype(np.float32))
d = np.minimum.reduce([gx - FRAME[0], FRAME[2] - gx, gy - FRAME[1], FRAME[3] - gy])
a = np.clip(d / 25.0, 0, 1)[..., None]
out = img * a + fb * (1 - a)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(OUT, quality=80, optimize=True, progressive=True)
print(OUT, w, h, f'{(d > 0).mean():.0%} dentro de la lámina', os.path.getsize(OUT) // 1024, 'KB')
