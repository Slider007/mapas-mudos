# Relieve: teselas «terrarium» (Mapzen/AWS, datos SRTM, GMTED, ETOPO…) → img/relief-gray.jpg, img/relief-color.jpg en la proyección del mapa.
# Uso: python3 relief.py <carpeta con t6_x_y.png> <ne_10m_land.geojson> <salida img/> [elev.npy]
import sys, os, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from shapely.geometry import shape, box
import proj
TD, LAND, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
Z = 6; N = 256 * 2 ** Z; SC = 2.0
w, h = int(proj.W * SC), int(proj.H * SC)
# mosaico
tiles = [f for f in os.listdir(TD) if f.startswith('t6_')]
xs = sorted({int(f.split('_')[1]) for f in tiles}); ys = sorted({int(f.split('_')[2][:-4]) for f in tiles})
mos = np.zeros(((ys[-1] - ys[0] + 1) * 256, (xs[-1] - xs[0] + 1) * 256), np.float32)
for f in tiles:
    x, y = int(f.split('_')[1]), int(f.split('_')[2][:-4]); a = np.asarray(Image.open(os.path.join(TD, f)).convert('RGB')).astype(np.float32)
    mos[(y - ys[0]) * 256:(y - ys[0] + 1) * 256, (x - xs[0]) * 256:(x - xs[0] + 1) * 256] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
# lon/lat de cada píxel (vectorizado)
px, py = np.meshgrid((np.arange(w) + .5) / SC, (np.arange(h) + .5) / SC)
X = px / proj.S + proj.X0; Y = proj.Y1 - py / proj.S
p0, l0 = math.radians(proj.LAT0), math.radians(proj.LON0); r = np.hypot(X, Y); r[r == 0] = 1e-12; c = 2 * np.arcsin(np.minimum(1, r / 2))
lat = np.arcsin(np.cos(c) * math.sin(p0) + Y * np.sin(c) * math.cos(p0) / r)
lon = l0 + np.arctan2(X * np.sin(c), r * math.cos(p0) * np.cos(c) - Y * math.sin(p0) * np.sin(c))
gx = (np.degrees(lon) + 180) / 360 * N - xs[0] * 256
gy = (1 - np.log(np.tan(lat) + 1 / np.cos(lat)) / math.pi) / 2 * N - ys[0] * 256
# interpolación bilineal
x0 = np.clip(np.floor(gx).astype(int), 0, mos.shape[1] - 2); y0 = np.clip(np.floor(gy).astype(int), 0, mos.shape[0] - 2); fx = np.clip(gx - x0, 0, 1); fy = np.clip(gy - y0, 0, 1)
E = (mos[y0, x0] * (1 - fx) * (1 - fy) + mos[y0, x0 + 1] * fx * (1 - fy) + mos[y0 + 1, x0] * (1 - fx) * fy + mos[y0 + 1, x0 + 1] * fx * fy)
if len(sys.argv) > 4: np.save(sys.argv[4], E.astype(np.float32))  # rejilla de altitudes (para regions_dem.py)
# máscara de tierra con la costa de Natural Earth
mask = Image.new('L', (w, h), 0); dr = ImageDraw.Draw(mask)
roi = box(-45, 25, 90, 86)
for f in json.load(open(LAND))['features']:
    g = shape(f['geometry'])
    if not g.intersects(roi): continue
    for poly in (g.geoms if hasattr(g, 'geoms') else [g]):
        pts = [tuple(v * SC for v in proj.prj(a, b)) for a, b in poly.exterior.coords]
        if len(pts) > 2: dr.polygon(pts, fill=255)
        for ring in poly.interiors: dr.polygon([tuple(v * SC for v in proj.prj(a, b)) for a, b in ring.coords], fill=0)
M = np.asarray(mask).astype(np.float32) / 255
# sombreado (iluminación desde el noroeste), exagerado como en los atlas escolares
cell = (proj.X1 - proj.X0) * 6371000 / w
El = np.where(M > .5, np.maximum(E, 0), 0)
from scipy.ndimage import gaussian_filter
Es = gaussian_filter(El.astype(np.float32), .8)
dzdx = np.gradient(Es, axis=1) / cell * 6; dzdy = np.gradient(Es, axis=0) / cell * 6
slope = np.arctan(np.hypot(dzdx, dzdy)); aspect = np.arctan2(-dzdx, dzdy)
az, alt = math.radians(315), math.radians(42)
hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect); hs = np.clip(hs, 0, 1)
sea = np.array([0xcf, 0xe1, 0xe8], np.float32)
# gris
g = (0.93 + 0.34 * (hs - np.sin(alt))) * 255; g = np.clip(g, 150, 255)
land_gray = np.stack([g * .995, g * .99, g * .975], -1)
gray = land_gray * M[..., None] + sea * (1 - M[..., None])
Image.fromarray(np.clip(gray, 0, 255).astype(np.uint8)).save(os.path.join(OUT, 'relief-gray.jpg'), quality=82, optimize=True, progressive=True)
# color hipsométrico (tintas de los atlas escolares) y batimetría
ST = [(0, (152, 196, 132)), (200, (189, 214, 150)), (500, (236, 228, 160)), (1000, (226, 190, 120)), (1500, (205, 150, 90)), (2000, (176, 115, 70)), (3000, (140, 90, 70)), (4000, (238, 234, 230))]
def ramp(v, stops):
    out = np.zeros(v.shape + (3,), np.float32)
    for i in range(len(stops) - 1):
        a, ca = stops[i]; b, cb = stops[i + 1]; t = np.clip((v - a) / (b - a), 0, 1)[..., None]; m = ((v >= a) & (v < b))[..., None] if i < len(stops) - 2 else (v >= a)[..., None]
        out = np.where(m, np.array(ca) * (1 - t) + np.array(cb) * t, out)
    out = np.where((v < stops[0][0])[..., None], np.array(stops[0][1], np.float32), out); return out
hyp = ramp(El, ST)
shade = (0.72 + 0.5 * (hs - np.sin(alt)))[..., None]
landc = np.clip(hyp * shade, 0, 255)
BT = [(-6000, (120, 165, 200)), (-3000, (150, 190, 215)), (-1000, (178, 208, 226)), (-200, (200, 224, 236)), (0, (214, 234, 242))]
dep = np.where(M < .5, np.minimum(E, 0), 0)
seac = ramp(dep, BT)
color = landc * M[..., None] + seac * (1 - M[..., None])
Image.fromarray(color.astype(np.uint8)).save(os.path.join(OUT, 'relief-color.jpg'), quality=82, optimize=True, progressive=True)
print('ok', w, h, 'elev range', float(E.min()), float(E.max()))
