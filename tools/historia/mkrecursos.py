# PDF для печати (без ответов): контурные карты, линия времени, шаблоны тетради и работы.
# Запуск: python3 mkrecursos.py <папка вывода>
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import bizancio, visigodos

FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', FD + 'DejaVuSans-Bold.ttf'))
INK = HexColor('#1f2f45'); GR = HexColor('#8a8a8a'); LG = HexColor('#cfcfcf'); SEA = HexColor('#eef5f8'); BIZ = HexColor('#5e35b1')
BASE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(BASE, 'geo.json')))
prj = lambda lo, la: ((lo - G['LON0']) * G['C'] * G['K'], (G['LAT1'] - la) * G['K'])
AUTHOR = 'Mapas mudos · slider007.github.io/mapas-mudos'

def header(c, W, H, title, sub=''):
    c.setFillColor(INK); c.setFont('DVB', 15); c.drawString(28, H - 34, title)
    if sub: c.setFont('DV', 9.5); c.setFillColor(GR); c.drawString(28, H - 48, sub)
    c.setFillColor(INK); c.setFont('DV', 9)
    x = W - 300
    for i, lab in enumerate(['Nombre:', 'Curso:', 'Fecha:']):
        y = H - 26 - i * 14; c.drawString(x, y, lab); c.setStrokeColor(GR); c.setLineWidth(.4); c.line(x + 44, y - 2, W - 28, y - 2)
    c.setFont('DV', 6.5); c.setFillColor(GR); c.drawRightString(W - 28, 14, AUTHOR)

def svgpath(c, d, tr):
    p = c.beginPath()
    for cmd in re.findall(r'M[^MZ]*Z?', d):
        pts = [tuple(map(float, q.split(','))) for q in re.findall(r'-?[\d.]+,-?[\d.]+', cmd)]
        if not pts: continue
        p.moveTo(*tr(*pts[0]))
        for q in pts[1:]: p.lineTo(*tr(*q))
        if cmd.endswith('Z'): p.close()
    return p

def map_page(c, W, H, m, title, sub, legend, numbered_regions=None, draw_lines=None, show_regions=True, tasks=None, legend_title='Leyenda (colorea y completa)'):
    header(c, W, H, title, sub)
    x0, y0, w, h = m['vb']
    top = H - 62; RWmin = 232
    MW = W - 56 - RWmin; MH = MW * h / w
    stacked = MH < (top - 28) * 0.72          # широкая карта: сверху во всю ширину, легенда снизу
    if stacked:
        MH = min((W - 56) * h / w, top - 28 - 150); MW = MH * w / h
    elif MH > top - 28:
        MH = top - 28; MW = MH * w / h
    s = MW / w; MX = 28 if not stacked else (W - MW) / 2; MY = top - MH
    tr = lambda x, y: (MX + (x - x0) * s, MY + MH - (y - y0) * s)
    c.saveState(); p = c.beginPath(); p.rect(MX, MY, MW, MH); c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(SEA); c.rect(MX, MY, MW, MH, fill=1, stroke=0)
    land = svgpath(c, G['land'], tr); c.setFillColor(white); c.setStrokeColor(HexColor('#555')); c.setLineWidth(.5); c.drawPath(land, fill=1, stroke=1)
    c.setStrokeColor(HexColor('#9cc3da')); c.setLineWidth(.5); c.drawPath(svgpath(c, G['rivers'], tr), fill=0, stroke=1)
    if show_regions:  # границы областей — только по суше
        c.saveState(); c.clipPath(svgpath(c, G['land'], tr), stroke=0, fill=0)
        c.setStrokeColor(HexColor('#333')); c.setLineWidth(.9); c.setDash(3, 2)
        for l in m['layers']:
            if len(l) > 3 and l[3] == 'route': continue
            for pl in m['regions'][l[0]]:
                pp = c.beginPath(); q = [tr(*prj(*a)) for a in pl]; pp.moveTo(*q[0])
                for a in q[1:]: pp.lineTo(*a)
                pp.close(); c.drawPath(pp, fill=0, stroke=1)
        c.restoreState(); c.setDash()
    for ln in draw_lines or []:
        c.setStrokeColor(HexColor('#6a1b9a')); c.setLineWidth(1.2); c.setDash(5, 3)
        q = [tr(*prj(*a)) for a in ln]; pp = c.beginPath(); pp.moveTo(*q[0])
        for a in q[1:]: pp.lineTo(*a)
        c.drawPath(pp, fill=0, stroke=1); c.setDash()
    for k, (lo, la) in enumerate(numbered_regions or [], 1):  # номера областей
        x, y = tr(*prj(lo, la)); c.setFillColor(white); c.setStrokeColor(INK); c.setLineWidth(.8); c.circle(x, y, 7, fill=1, stroke=1)
        c.setFillColor(INK); c.setFont('DVB', 8); c.drawCentredString(x, y - 3, str(k))
    cities = list(m['cities'].items())
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for k, (n, (lo, la, _)) in enumerate(cities):  # города — точки с буквами
        x, y = tr(*prj(lo, la)); c.setFillColor(HexColor('#7a2e2e')); c.circle(x, y, 2.2, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('DVB', 7.5); c.drawString(x + 3.5, y + 2.5, letters[k])
    c.restoreState()
    c.setStrokeColor(INK); c.setLineWidth(.8); c.rect(MX, MY, MW, MH, fill=0, stroke=1)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if stacked:
        cw = (W - 56) / 3; cols = [(28 + i * cw, MY - 16, cw - 14) for i in range(3)]
    else:
        RX = MX + MW + 16; cols = [(RX, top - 18, W - RX - 28)] * 3
    ci = 0; RX, y, RW = cols[0]
    def nextcol(need):
        nonlocal ci, RX, y, RW
        if stacked and ci < 2 and y - need < 30: ci += 1; RX, y, RW = cols[ci]
    c.setFillColor(INK); c.setFont('DVB', 10); c.drawString(RX, y, legend_title); y -= 16; c.setFont('DV', 8.6)
    for item in legend:
        ls = split(c, item, RW - 24, 'DV', 8.6); nextcol(10.5 * len(ls) + 5)
        c.setStrokeColor(INK); c.setLineWidth(.6); c.rect(RX, y - 2, 16, 10, fill=0, stroke=1); c.setFillColor(INK); c.setFont('DV', 8.6)
        for i, line in enumerate(ls): c.drawString(RX + 22, y - i * 10.5, line)
        y -= 10.5 * len(ls) + 5
    if numbered_regions:
        if stacked: ci += 1; RX, y, RW = cols[min(ci, 2)]
        else: y -= 6
        c.setFont('DVB', 10); c.drawString(RX, y, 'Escribe el nombre de cada zona'); y -= 15; c.setFont('DV', 8.6)
        for k in range(1, len(numbered_regions) + 1):
            c.drawString(RX, y, f'{k}.'); c.setStrokeColor(GR); c.setLineWidth(.4); c.line(RX + 16, y - 2, RX + RW, y - 2); y -= 15
    if stacked and ci < 1: ci = 1; RX, y, RW = cols[1]
    else: y -= 6
    c.setFillColor(INK); c.setFont('DVB', 10); c.drawString(RX, y, 'Ciudades'); y -= 15; c.setFont('DV', 8.6)
    half = (len(cities) + 1) // 2
    for k in range(len(cities)):
        col = k // half; row = k % half; xx = RX + col * (RW / 2); yy = y - row * 15
        c.drawString(xx, yy, letters[k] + '.'); c.setStrokeColor(GR); c.setLineWidth(.4); c.line(xx + 12, yy - 2, xx + RW / 2 - 8, yy - 2)
    y -= half * 15 + 8
    if stacked: ci = 2; RX, y, RW = cols[2]
    for t in tasks or []:
        for line in split(c, t, RW, 'DV', 8.2):
            if y < 30: break
            c.setFont('DV', 8.2); c.setFillColor(INK); c.drawString(RX, y, line); y -= 10.5
        y -= 4
    c.showPage()

def split(c, text, width, font, size):
    words = text.split(); lines = []; cur = ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if c.stringWidth(t, font, size) <= width: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def maps_pdf(out):
    W, H = landscape(A4); c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle('Mapas mudos · Tema 1 (Historia)'); c.setAuthor('Mapas mudos')
    mb = bizancio.MAPS[0]
    map_page(c, W, H, mb, 'Mapa mudo · El Imperio bizantino', 'Tema 1 · como el mapa 18 del libro (p. 23)',
             ['Imperio romano de Oriente a la llegada de Justiniano (527)', 'Conquistas de Justiniano', 'Imperio bizantino en 1025 (rayado)', 'Imperio bizantino en 1204 (rayado vertical)', 'Imperio bizantino en 1453'],
             show_regions=False, tasks=['Colorea con los colores de tu leyenda. Marca también los territorios actuales de España que fueron bizantinos.'])
    ma, mr, mt = visigodos.MAPS
    map_page(c, W, H, ma, 'Mapa mudo · Rutas de las invasiones germanas', 'Tema 1 · como el mapa 1 del libro (p. 14)',
             ['Imperio romano de Occidente', 'Imperio romano de Oriente'], show_regions=False, draw_lines=[[[19.2, 47.5], [19.2, 30.6]]],
             tasks=['La línea discontinua es el límite de Teodosio (395).', 'Dibuja con flechas de colores la ruta de: visigodos, vándalos, suevos, alanos, ostrogodos, francos, anglos y sajones, y hunos. Añade cada color a la leyenda.', 'Marca con una X la batalla de los Campos Cataláunicos (451).'])
    nums = [(-4.3, 38.9), (-8.0, 42.4), (2.2, 49.3), (5.6, 46.4), (9.0, 48.4), (11.3, 51.0), (9.4, 53.4), (-0.7, 52.4), (12.6, 43.3), (8.5, 34.9), (32, 39.2)]
    map_page(c, W, H, mr, 'Mapa mudo · Los reinos germanos a finales del siglo V', 'Tema 1 · como el mapa 5 del libro (p. 16)',
             ['Reino de los visigodos', 'Reino de los suevos', 'Reino de los francos', 'Reino de los burgundios', 'Alamanes', 'Turingios', 'Sajones', 'Anglos', 'Reino de los ostrogodos', 'Reino de los vándalos', 'Imperio romano de Oriente'],
             numbered_regions=nums)
    map_page(c, W, H, mt, 'Mapa mudo · El reino visigodo en el siglo VI', 'Tema 1 · como el mapa 6 del libro (p. 17)',
             ['Reino de los visigodos de Toledo', 'Conquistas de Leovigildo (568–586)', 'Posesiones bizantinas', 'Pueblos no sometidos (astures, cántabros, vascones)'],
             numbered_regions=[(-3.5, 40.6), (-8.1, 42.3), (-4.9, 37.75), (-3.6, 36.95), (-4.5, 43.25)],
             tasks=['Dibuja con una flecha el itinerario de los visigodos desde la Galia hasta Toledo.'])
    c.save()

def timeline_pdf(out):
    W, H = landscape(A4); c = canvas.Canvas(out, pagesize=(W, H)); c.setTitle('Línea del tiempo · Tema 1'); c.setAuthor('Mapas mudos')
    header(c, W, H, 'Línea del tiempo · Tema 1', 'Fin de la Edad Antigua e inicio de la Edad Media · escribe qué pasó en cada fecha')
    X0, X1, Y = 40, W - 40, H / 2 - 10; y0, y1 = 300, 1500
    X = lambda yr: X0 + (yr - y0) / (y1 - y0) * (X1 - X0)
    eras = [(300, 476, '#d7ccc8', 'Edad Antigua'), (476, 1000, '#bbdefb', 'Alta Edad Media'), (1000, 1300, '#c8e6c9', 'Plena Edad Media'), (1300, 1453, '#ffcdd2', 'Baja Edad Media'), (1453, 1500, '#eeeeee', 'Edad Moderna')]
    for a, b_, col, t in eras:
        c.setFillColor(HexColor(col)); c.rect(X(a), Y - 9, X(b_) - X(a), 18, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont('DVB', 7.5)
        if X(b_) - X(a) > 60: c.drawCentredString((X(a) + X(b_)) / 2, Y - 3, t)
    c.setStrokeColor(INK); c.setLineWidth(1); c.line(X0, Y - 9, X1, Y - 9); c.line(X0, Y + 9, X1, Y + 9)
    c.setFont('DV', 7)
    for yr in range(300, 1501, 100):
        c.line(X(yr), Y - 13, X(yr), Y - 9); c.drawCentredString(X(yr), Y - 22, str(yr))
    dates = [395, 409, 415, 451, 476, 507, 527, 565, 589, 654, 711, 726, 732, 800, 843, 1054, 1453]
    BW = 74; rows = [(+1, k) for k in range(4)] + [(-1, k) for k in range(4)]; end = {r: -1e9 for r in rows}
    order = [r for k in range(4) for r in ((+1, k), (-1, k))]  # сначала ближние ряды сверху и снизу
    for yr in dates:
        x = X(yr); r = next((r for r in order if end[r] < x - BW / 2 - 4), order[-1]); end[r] = x + BW / 2
        side, k = r; yy = Y + 34 + k * 46 if side > 0 else Y - 60 - k * 46
        c.setStrokeColor(GR); c.setLineWidth(.5); c.line(x, Y + 9 * side, x, yy if side > 0 else yy + 26)
        c.setStrokeColor(INK); c.setFillColor(white); c.rect(x - BW / 2, yy, BW, 26, fill=1, stroke=1)
        c.setFillColor(BIZ); c.setFont('DVB', 8.5); c.drawCentredString(x, yy + 29 if side > 0 else yy - 9, str(yr))
    c.setFont('DV', 8); c.setFillColor(INK)
    c.drawString(40, 40, 'Pista: germanos y visigodos (395–711), Imperio bizantino (395–1453) y carolingios (732–843). Cuenta los años: ¿cuánto duró el Imperio bizantino?')
    c.showPage(); c.save()

def checkbox_list(c, x, y, items, width, size=9):
    c.setFont('DV', size)
    for it in items:
        lines = split(c, it, width - 18, 'DV', size)
        c.setStrokeColor(INK); c.setLineWidth(.6); c.rect(x, y - 1.5, 9, 9, fill=0, stroke=1)
        for i, ln in enumerate(lines): c.setFillColor(INK); c.drawString(x + 16, y - i * (size + 2.5), ln)
        y -= (size + 2.5) * len(lines) + 6
    return y

def frame_page(c, W, H, top, title, sub):
    c.setStrokeColor(BIZ); c.setLineWidth(3); c.roundRect(30, 30, W - 60, H - 60, 14, fill=0, stroke=1)
    c.setLineWidth(.8); c.roundRect(38, 38, W - 76, H - 76, 10, fill=0, stroke=1)
    c.setFillColor(BIZ); c.setFont('DVB', 30); c.drawCentredString(W / 2, H - 150, top)
    c.setFillColor(INK); y = H - 200
    for ln in split(c, title, W - 140, 'DVB', 20): c.setFont('DVB', 20); c.drawCentredString(W / 2, y, ln); y -= 26
    c.setFont('DV', 11); c.setFillColor(GR); c.drawCentredString(W / 2, y - 6, sub)
    c.setStrokeColor(LG); c.setDash(4, 3); c.rect(90, 250, W - 180, H - 560, fill=0, stroke=1); c.setDash()
    c.setFont('DV', 9); c.setFillColor(GR); c.drawCentredString(W / 2, 250 + (H - 560) / 2, 'dibujo o imagen del tema · drawing')

def cuaderno_pdf(out):
    W, H = A4; c = canvas.Canvas(out, pagesize=A4); c.setTitle('Plantilla del cuaderno · Tema 1'); c.setAuthor('Mapas mudos')
    def foot(n): c.setFont('DV', 9); c.setFillColor(INK); c.drawCentredString(W / 2, 46, str(n)); c.setFont('DV', 6.5); c.setFillColor(GR); c.drawRightString(W - 44, 46, AUTHOR)
    def namelines(labels):
        y = 200
        for lab in labels:
            c.setFont('DV', 12); c.setFillColor(INK); c.drawString(100, y, lab); c.setStrokeColor(GR); c.setLineWidth(.5); c.line(100 + c.stringWidth(lab, 'DV', 12) + 8, y - 3, W - 100, y - 3); y -= 30
    frame_page(c, W, H, 'TEMA 1', 'Fin de la Edad Antigua e inicio de la Edad Media', 'Geografía e Historia'); namelines(['Nombre:', 'Curso:']); c.showPage()
    frame_page(c, W, H, 'UNIT 1', 'The end of Antiquity and the beginning of the Middle Ages', 'Geography and History'); namelines(['Name:', 'Class:']); c.showPage()
    # чек-лист + оглавление
    c.setFillColor(INK); c.setFont('DVB', 15); c.drawString(50, H - 60, 'Antes de entregar: lista de cotejo del cuaderno')
    y = checkbox_list(c, 50, H - 90, [
        'Primera página del tema: nombre, curso y portada con el número y el título del tema (con colores, letra más grande…).',
        'Todas las páginas están numeradas.', 'Hay márgenes arriba, abajo, a la izquierda y a la derecha (uno o dos dedos).',
        'Limpieza, buena ortografía y letra legible.', 'Cada tarea tiene enunciado, número y, si es del libro, la página.',
        'He tomado apuntes (se valora en niveles superiores).',
        'Inglés: portada en inglés, enunciados en inglés y, al final del tema, vocabulario (glosario) o esquema hecho en clase.',
        'Todo escaneado en un solo PDF con el nombre del tema (por ejemplo, «T.1 Fin de la Edad Antigua e inicio de la Edad Media») y subido a Classroom.',
        'Entregado en la fecha indicada.'], W - 100, 9.5)
    y -= 14; c.setFont('DVB', 13); c.setFillColor(INK); c.drawString(50, y, 'Índice de tareas'); y -= 10
    cols = [50, 80, 400, 470, W - 50]; heads = ['Nº', 'Enunciado / actividad', 'Página', 'Hecho']
    c.setFillColor(HexColor('#efeaf7')); c.rect(cols[0], y - 16, cols[-1] - cols[0], 16, fill=1, stroke=0); c.setFillColor(INK); c.setFont('DVB', 9)
    for i, hd in enumerate(heads): c.drawString(cols[i] + 4, y - 12, hd)
    y -= 16; c.setStrokeColor(LG); c.setLineWidth(.5)
    while y > 90:
        c.line(cols[0], y - 18, cols[-1], y - 18)
        for xx in cols: c.line(xx, y, xx, y - 18)
        y -= 18
    foot(3); c.showPage()
    # глоссарий
    c.setFillColor(INK); c.setFont('DVB', 15); c.drawString(50, H - 60, 'Unit 1 · Glossary (vocabulary)')
    c.setFont('DV', 9); c.setFillColor(GR); c.drawString(50, H - 76, 'Write the words you did not know and their meaning · palabras que no conocías y su significado')
    y = H - 96; cols = [50, 190, 330, W - 50]; heads = ['English', 'Español', 'Meaning / significado']
    c.setFillColor(HexColor('#efeaf7')); c.rect(cols[0], y - 16, cols[-1] - cols[0], 16, fill=1, stroke=0); c.setFillColor(INK); c.setFont('DVB', 9)
    for i, hd in enumerate(heads): c.drawString(cols[i] + 4, y - 12, hd)
    y -= 16; c.setStrokeColor(LG)
    while y > 90:
        c.line(cols[0], y - 21, cols[-1], y - 21)
        for xx in cols: c.line(xx, y, xx, y - 21)
        y -= 21
    foot(4); c.showPage(); c.save()

def trabajo_pdf(out):
    W, H = A4; c = canvas.Canvas(out, pagesize=A4); c.setTitle('Plantilla para un trabajo'); c.setAuthor('Mapas mudos')
    def foot(n): c.setFont('DV', 6.5); c.setFillColor(GR); c.drawRightString(W - 44, 30, AUTHOR)
    c.setFillColor(INK); c.setFont('DVB', 16); c.drawString(50, H - 60, 'Cómo organizar un trabajo')
    c.setFont('DV', 9.5); c.setFillColor(GR); c.drawString(50, H - 76, 'Para trabajos escritos (a mano o con ordenador). En presentaciones no se numeran las diapositivas.')
    steps = ['1. Portada con el título del trabajo.', '2. Hoja en blanco con tu nombre y curso.', '3. Índice: cada apartado con su página.',
             '4. Desarrollo: un párrafo distinto para cada apartado; imágenes con pie de foto (también gráficos o mapas).',
             '5. Opinión personal y conclusión.', '6. Bibliografía o webgrafía (libros y páginas web usadas).', '7. Hoja en blanco al final.']
    y = H - 104; c.setFont('DV', 10.5); c.setFillColor(INK)
    for st_ in steps:
        for i, ln in enumerate(split(c, st_, W - 110, 'DV', 10.5)): c.drawString(56, y - i * 13, ln)
        y -= 13 * len(split(c, st_, W - 110, 'DV', 10.5)) + 6
    y -= 10; c.setFont('DVB', 13); c.drawString(50, y, 'Lista de cotejo antes de entregar'); y -= 22
    checkbox_list(c, 50, y, ['Nombre y curso.', 'Páginas numeradas (trabajo escrito).', 'Márgenes arriba, abajo, izquierda y derecha.', 'Limpieza y letra legible; si es en ordenador, tipos y tamaños de letra adecuados.',
                              'A mano: folios blancos, escribir por una cara, folio blanco después de la portada y al final.', 'Índice con las páginas de cada apartado.', 'Párrafos distintos para cada apartado.',
                              'Imágenes con pie de foto.', 'Contiene toda la información pedida y respeta la extensión.', 'Opinión personal o conclusión al final.', 'Bibliografía o webgrafía.',
                              'Buena ortografía y redacción fluida. Originalidad.', 'Archivo en PDF con nombre correcto (número y nombre del tema) subido a Classroom.', 'Prepárate: el profesor o los compañeros te harán preguntas sobre tu trabajo.'], W - 100, 9.5)
    foot(1); c.showPage()
    # портада-шаблон
    c.setStrokeColor(LG); c.setLineWidth(1); c.rect(60, 60, W - 120, H - 120, fill=0, stroke=1)
    c.setFont('DV', 10); c.setFillColor(GR); c.drawCentredString(W / 2, H - 140, 'TÍTULO DEL TRABAJO')
    c.setStrokeColor(GR); c.line(110, H - 180, W - 110, H - 180); c.line(110, H - 215, W - 110, H - 215)
    c.setDash(4, 3); c.rect(130, H - 560, W - 260, 300, fill=0, stroke=1); c.setDash(); c.drawCentredString(W / 2, H - 410, 'imagen de portada')
    c.drawCentredString(W / 2, H - 580, 'pie de foto: una frase corta que explica la imagen')
    y = 170
    for lab in ['Nombre:', 'Curso:', 'Asignatura:', 'Fecha:']:
        c.setFont('DV', 11); c.setFillColor(INK); c.drawString(140, y, lab); c.setStrokeColor(GR); c.line(225, y - 3, W - 140, y - 3); y -= 26
    foot(2); c.showPage()
    # оглавление + мнение + источники
    c.setFillColor(INK); c.setFont('DVB', 16); c.drawString(50, H - 60, 'Índice')
    y = H - 96
    for i in range(1, 11):
        c.setFont('DV', 11); c.drawString(60, y, f'{i}.'); c.setStrokeColor(LG); c.setDash(1, 3); c.line(80, y - 2, W - 110, y - 2); c.setDash(); c.drawString(W - 100, y, 'pág. ____'); y -= 24
    y -= 16; c.setFont('DVB', 14); c.drawString(50, y, 'Opinión personal y conclusión: ideas para empezar'); y -= 20; c.setFont('DV', 10)
    for t in ['• Lo que más me ha llamado la atención es… porque…', '• Comparado con la actualidad, ahora… mientras que antes…', '• En mi opinión… porque…', '• Como conclusión, he aprendido que…']:
        c.drawString(60, y, t); y -= 16
    y -= 14; c.setFont('DVB', 14); c.drawString(50, y, 'Bibliografía y webgrafía: cómo escribirla'); y -= 20; c.setFont('DV', 10)
    for t in ['Libro: Autor (año). Título. Editorial. Ejemplo: VV. AA. (2023). Geografía e Historia 2º ESO. Editorial.', 'Web: Título de la página. Dirección web (fecha en que la consultaste).',
              'Ejemplo: «Imperio bizantino». es.wikipedia.org/wiki/Imperio_bizantino (consultado el 25-10-2026).']:
        for i, ln in enumerate(split(c, t, W - 120, 'DV', 10)): c.drawString(60, y - i * 13, ln)
        y -= 13 * len(split(c, t, W - 120, 'DV', 10)) + 6
    foot(3); c.showPage(); c.save()

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    maps_pdf(os.path.join(out, 'mapas-mudos-tema1.pdf'))
    timeline_pdf(os.path.join(out, 'linea-del-tiempo-tema1.pdf'))
    cuaderno_pdf(os.path.join(out, 'plantilla-cuaderno-tema1.pdf'))
    trabajo_pdf(os.path.join(out, 'plantilla-trabajo.pdf'))
    print('ok', sorted(os.listdir(out)))
