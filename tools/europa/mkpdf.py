# PDF para imprimir (sin respuestas): python3 mkpdf.py ../../europa-politica/pdf/mapa-mudo-europa-politica.pdf
import json, re, sys, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
base = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, base)
from paises import P
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('DVB', FD + 'DejaVuSans-Bold.ttf'))
G = json.load(open(os.path.join(base, 'geo.json')))
INK = HexColor('#1f2f45'); SEA = HexColor('#e6f0f4'); GR = HexColor('#888888'); OTH = HexColor('#eeeeea')
W, H = landscape(A4)
def header(c, title, sub):
    c.setFillColor(INK); c.setFont('DVB', 15); c.drawString(28, H - 34, title)
    c.setFont('DV', 8.5); c.setFillColor(GR)
    words, line, y = sub.split(), '', H - 47
    for w_ in words:
        if c.stringWidth(line + ' ' + w_, 'DV', 8.5) > W - 320: c.drawString(28, y, line.strip()); line, y = '', y - 10
        line += ' ' + w_
    c.drawString(28, y, line.strip())
    c.setFont('DV', 9); c.setFillColor(INK)
    for i, l in enumerate(['Nombre:', 'Curso:', 'Fecha:']):
        y = H - 22 - i * 13; c.drawString(W - 250, y, l); c.setStrokeColor(GR); c.setLineWidth(.4); c.line(W - 205, y - 2, W - 28, y - 2)
    c.setFont('DV', 6); c.setFillColor(GR); c.drawRightString(W - 28, 14, 'Mapas mudos · slider007.github.io/mapas-mudos/europa-politica · mapa: Natural Earth')
def path(c, d, tr):
    p = c.beginPath()
    for sub in re.findall(r'M[^M]*', d):
        pts = [tuple(map(float, xy.split(','))) for xy in re.findall(r'-?[\d.]+,-?[\d.]+', sub)]
        if not pts: continue
        p.moveTo(*tr(*pts[0]))
        for q in pts[1:]: p.lineTo(*tr(*q))
        if sub.endswith('Z'): p.close()
    return p
def mapbox(c, x0, y0, w, h):
    s = min(w / G['W'], h / G['H']); mw, mh = G['W'] * s, G['H'] * s; ox = x0 + (w - mw) / 2; oy = y0 + (h - mh) / 2
    tr = lambda x, y: (ox + x * s, oy + mh - y * s)
    c.saveState(); cl = c.beginPath(); cl.rect(ox, oy, mw, mh); c.clipPath(cl, stroke=0, fill=0)
    c.setFillColor(SEA); c.rect(ox, oy, mw, mh, fill=1, stroke=0)
    c.setFillColor(OTH); c.setStrokeColor(HexColor('#bbbbbb')); c.setLineWidth(.3); c.drawPath(path(c, G['other'], tr), fill=1, stroke=1)
    c.setFillColor(white); c.setStrokeColor(INK); c.setLineWidth(.45)
    for k, v in G['countries'].items(): c.drawPath(path(c, v['d'], tr), fill=1, stroke=1)
    c.setFillColor(SEA); c.setLineWidth(.25); c.drawPath(path(c, G['lakes'], tr), fill=1, stroke=1)
    c.restoreState(); c.setStrokeColor(INK); c.setLineWidth(.8); c.rect(ox, oy, mw, mh, fill=0, stroke=1)
    return tr, s
def order():  # numeración geográfica (de noroeste a sureste), no alfabética
    ks = list(G['countries']); return sorted(ks, key=lambda k: (round(G['countries'][k]['lab'][1] / 60), G['countries'][k]['lab'][0]))
def build(out):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('Mapa mudo político de Europa'); c.setAuthor('Mapas mudos')
    # 1. mapa mudo en blanco
    header(c, 'Mapa mudo político de Europa', 'Escribe el nombre de cada país y marca su capital con un punto. Colorea los países con colores distintos.')
    mapbox(c, 28, 26, W - 56, H - 90); c.showPage()
    # 2. países numerados y capitales
    header(c, 'Mapa político de Europa · países numerados', 'Escribe en la tabla de la hoja siguiente el nombre de cada país numerado y su capital (punto negro).')
    tr, s = mapbox(c, 28, 26, W - 56, H - 90)
    for k in G['countries']:
        if P[k][6] != 'otros':
            x, y = tr(*G['countries'][k]['cap']); c.setFillColor(INK); c.circle(x, y, 1.3, fill=1, stroke=0)
    for n, k in enumerate(order(), 1):
        v = G['countries'][k]; x, y = tr(*(v['c'] if v['area'] < 14 else v['lab']))
        r = 5.2 if n < 10 else 6
        c.setFillColor(white); c.setStrokeColor(INK); c.setLineWidth(.6); c.circle(x, y, r, fill=1, stroke=1)
        c.setFillColor(INK); c.setFont('DVB', 5.6); c.drawCentredString(x, y - 2, str(n))
    c.showPage()
    # 3. tabla para completar
    header(c, 'Países y capitales de Europa', 'Completa con los números del mapa de la hoja anterior. Donde no hay línea de capital, escribe solo el país (no tiene capital en la lista del profesor).')
    ks = order(); per = 26; colw = (W - 56) / 2
    for col in range(2):
        x = 28 + col * colw; y = H - 80
        c.setFont('DVB', 9); c.setFillColor(INK); c.drawString(x, y, 'Nº'); c.drawString(x + 24, y, 'País'); c.drawString(x + 24 + colw * .48, y, 'Capital')
        for i in range(per):
            n = col * per + i + 1
            if n > len(ks): break
            yy = y - 18 - i * 17.6; c.setFont('DV', 9); c.drawString(x, yy, f'{n}.')
            c.setStrokeColor(GR); c.setLineWidth(.4); c.line(x + 22, yy - 2, x + colw * .46, yy - 2)
            if P[ks[n - 1]][6] != 'otros': c.line(x + 24 + colw * .48, yy - 2, x + colw - 14, yy - 2)
    c.showPage(); c.save()
build(sys.argv[1]); print('ok', sys.argv[1])
