# PDF para imprimir (sin respuestas): python3 mkpdf.py ../../europa-fisica/pdf/mapa-mudo-europa-fisica.pdf
import json, re, sys, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageEnhance
base = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, base)
from datos import O, CATS
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('DVB', FD + 'DejaVuSans-Bold.ttf'))
G = json.load(open(os.path.join(base, 'geo.json')))
IMG = os.path.join(base, '..', '..', 'europa-fisica', 'img', 'relief-gray.jpg')
INK = HexColor('#1f2f45'); GR = HexColor('#888888'); BLUE = HexColor('#3d86b8')
W, H = landscape(A4)
def header(c, title, sub):
    c.setFillColor(INK); c.setFont('DVB', 15); c.drawString(28, H - 34, title)
    c.setFont('DV', 8.5); c.setFillColor(GR); c.drawString(28, H - 47, sub)
    c.setFont('DV', 9); c.setFillColor(INK)
    for i, l in enumerate(['Nombre:', 'Curso:', 'Fecha:']):
        y = H - 22 - i * 13; c.drawString(W - 250, y, l); c.setStrokeColor(GR); c.setLineWidth(.4); c.line(W - 205, y - 2, W - 28, y - 2)
    c.setFont('DV', 6); c.setFillColor(GR); c.drawRightString(W - 28, 14, 'Mapas mudos · slider007.github.io/mapas-mudos/europa-fisica · Natural Earth · relieve: Mapzen/AWS Terrain Tiles')
def path(c, d, tr, close=True):
    p = c.beginPath()
    for sub in re.findall(r'M[^M]*', d):
        pts = [tuple(map(float, xy.split(','))) for xy in re.findall(r'-?[\d.]+,-?[\d.]+', sub)]
        if not pts: continue
        p.moveTo(*tr(*pts[0]))
        for q in pts[1:]: p.lineTo(*tr(*q))
        if close and sub.endswith('Z'): p.close()
    return p
_img = None
def relief(strength):
    im = Image.open(IMG).convert('RGB'); im = ImageEnhance.Contrast(im).enhance(strength); im = ImageEnhance.Brightness(im).enhance(1.04)
    im.thumbnail((1600, 1600)); fn = os.path.join(__import__('tempfile').gettempdir(), f'eufis_{strength}.jpg'); im.save(fn, quality=80); return fn
def mapbox(c, x0, y0, w, h, strength):
    s = min(w / G['W'], h / G['H']); mw, mh = G['W'] * s, G['H'] * s; ox = x0; oy = y0 + (h - mh) / 2
    tr = lambda x, y: (ox + x * s, oy + mh - y * s)
    c.drawImage(relief(strength), ox, oy, mw, mh)
    c.saveState(); cl = c.beginPath(); cl.rect(ox, oy, mw, mh); c.clipPath(cl, stroke=0, fill=0)
    c.setStrokeColor(INK); c.setLineWidth(.35); c.drawPath(path(c, G['land'], tr), fill=0, stroke=1)
    c.restoreState(); c.setStrokeColor(INK); c.setLineWidth(.8); c.rect(ox, oy, mw, mh, fill=0, stroke=1)
    return tr, ox + mw
def legend(c, x, cats, top):
    y = top; colw = W - 28 - x
    for cid in cats:
        name = [cc[2] for cc in CATS if cc[0] == cid][0]; items = [o[1] for o in O if o[3] == cid]
        c.setFont('DVB', 8.4); c.setFillColor(INK); c.drawString(x, y, name.upper()); y -= 10.5
        c.setFont('DV', 7.6); line = ''
        for it in items:
            t = (line + ', ' + it) if line else it
            if c.stringWidth(t, 'DV', 7.6) > colw: c.drawString(x, y, line + ','); y -= 9.4; line = it
            else: line = t
        c.drawString(x, y, line + '.'); y -= 13
    return y
def build(out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('Mapa mudo físico de Europa'); c.setAuthor('Mapas mudos')
    mh = H - 84; mw = mh * G['W'] / G['H']
    # 1. costas
    header(c, 'Europa física · costas', 'Escribe en el mapa los océanos, mares, penínsulas, golfos, cabos (puntos), estrechos, canales e islas de la lista.')
    tr, xr = mapbox(c, 28, 26, mw, mh, 1.25)
    for o in O:
        g = G['O'].get(o[0])
        if g and g['k'] == 'pt': x, y = tr(*g['xy']); c.setFillColor(INK); c.circle(x, y, 1.6, fill=1, stroke=0)
    legend(c, xr + 14, ['oc', 'mar', 'pen', 'golfo', 'cabo', 'est', 'isla'], H - 70); c.showPage()
    # 2. ríos y lagos
    header(c, 'Europa física · ríos y lagos', 'Escribe el nombre de cada río y lago. Colorea de un color distinto los ríos de cada vertiente.')
    tr, xr = mapbox(c, 28, 26, mw, mh, 1.25)
    c.setStrokeColor(BLUE); c.setLineWidth(.8)
    for o in O:
        g = G['O'].get(o[0])
        if not g: continue
        if g['k'] == 'line':
            for l in g['lines']:
                p = c.beginPath(); p.moveTo(*tr(*l[0]))
                for q in l[1:]: p.lineTo(*tr(*q))
                c.drawPath(p, fill=0, stroke=1)
        if g['k'] == 'lake': c.setFillColor(HexColor('#bcd8e6')); c.setLineWidth(.3); c.drawPath(path(c, g['d'], tr), fill=1, stroke=1); c.setLineWidth(.8)
    legend(c, xr + 14, ['v_med', 'v_neg', 'v_cas', 'v_atl', 'v_nor', 'v_bal', 'v_art', 'lago_n', 'lago_a'], H - 70); c.showPage()
    # 3. relieve
    header(c, 'Europa física · relieve', 'Sitúa las montañas, mesetas, macizos y llanuras. Colorea de marrón las montañas jóvenes, de naranja las viejas y de verde las llanuras.')
    tr, xr = mapbox(c, 28, 26, mw, mh, 1.6)
    legend(c, xr + 14, ['m_vie', 'm_jov', 'm_mes', 'llan'], H - 70); c.showPage()
    c.save()
build(sys.argv[1]); print('ok', sys.argv[1])
