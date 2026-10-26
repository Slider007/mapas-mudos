# Colores pastel de los países, tomados del «Mapa político de Europa» del IGN (2025) ya reproyectado (europa-politica/img/ign.jpg):
# para cada país, color más frecuente de su interior (sin textos, ríos ni fronteras) y aclarado hacia el blanco.
# Uso: python3 colores.py → colores.json (lo lee build.py)
import json, os, re, numpy as np
from PIL import Image, ImageDraw
base = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(base, 'geo.json')))
im = np.asarray(Image.open(os.path.join(base, '..', '..', 'europa-politica', 'img', 'ign.jpg')).convert('RGB')).astype(int)
k = im.shape[1] / G['W']
PASTEL = 0.35          # cuánto se aclara (0 = color del IGN, 1 = blanco)
out = {}
for cid, c in G['countries'].items():
    mk = Image.new('L', (im.shape[1], im.shape[0]), 0); dr = ImageDraw.Draw(mk)
    for part in re.findall(r'M[^M]+', c['d']):
        pts = [(float(x) * k, float(y) * k) for x, y in re.findall(r'(-?[\d.]+),(-?[\d.]+)', part)]
        if len(pts) > 2: dr.polygon(pts, fill=255)
    m = np.asarray(mk) > 0
    px = im[m]
    if len(px) < 20: continue
    q = np.minimum((px // 12) * 12 + 6, 255)                                  # cuantizar y quedarse con el color más frecuente
    sat = px.max(1) - px.min(1); bright = px.sum(1)
    keep = (bright > 360) & ~((px[:, 2] > px[:, 0] + 30) & (px[:, 2] > px[:, 1]))   # fuera texto oscuro y agua (ríos, lagos)
    q = q[keep] if keep.sum() > 10 else q
    vals, cnt = np.unique(q, axis=0, return_counts=True); col = vals[cnt.argmax()]
    if col.min() > 235: col = np.array([243, 222, 190])      # microestados: el color del IGN no se distingue a esta escala
    col = col + (255 - col) * PASTEL
    out[cid] = '#%02x%02x%02x' % tuple(int(round(v)) for v in col)
out['kosovo'] = '#d2f1c3'   # el IGN no lo separa de Serbia; aquí va con un color distinto de sus vecinos
json.dump(out, open(os.path.join(base, 'colores.json'), 'w'), indent=0, ensure_ascii=False)
print(len(out), out)
