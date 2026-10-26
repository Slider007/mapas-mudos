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
out.update({'andorra': '#d9c8ec', 'monaco': '#f5c6dd', 'sanmarino': '#c4e8ee', 'vaticano': '#ffe3a6', 'liechtenstein': '#fff1a0', 'malta': '#f8c4ae'})  # microestados (con su llamada)
out['kosovo'] = '#d2f1c3'   # el IGN no lo separa de Serbia; aquí va con un color distinto de sus vecinos
# cada país con un color propio: de mayor a menor, cada uno toma la variante de su color del IGN más cercana
# (tono ±, luminosidad ±) que quede a una distancia ≥ MIND de los colores ya asignados
import colorsys
MIND = 18
hx = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
def variant(c, dh, dl):
    r, g_, b_ = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)); h, l, sa = colorsys.rgb_to_hls(r, g_, b_)
    rr, gg, bb = colorsys.hls_to_rgb((h + dh / 360) % 1, min(.92, max(.68, l + dl)), sa)
    return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in (rr, gg, bb))
CAND = sorted([(dh, dl) for dh in range(-36, 37, 6) for dl in (-.08, -.06, -.04, -.02, 0, .02, .04)], key=lambda t: abs(t[0]) / 6 + abs(t[1]) / .02)
ign, out, used = dict(out), {}, []
for cid in sorted(ign, key=lambda c: -float(G['countries'][c]['area'])):
    best, bd = None, -1
    for dh, dl in CAND:
        v = variant(ign[cid], dh, dl); d = min([np.linalg.norm(hx(v) - u) for u in used] or [999])
        if d >= MIND: best = v; break
        if d > bd: best, bd = v, d
    out[cid] = best; used.append(hx(best))
assert len(set(out.values())) == len(out), 'colores repetidos'
json.dump(out, open(os.path.join(base, 'colores.json'), 'w'), indent=0, ensure_ascii=False)
print(len(out), out)
